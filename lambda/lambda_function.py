"""AWS Lambda function for SLURM to Run.ai conversion.

This function:
1. Validates signed requests from the s2r library
2. Implements rate limiting per IP
3. Calls AWS Bedrock to perform the conversion
4. Returns the Run.ai configuration

Environment variables required:
- SHARED_SECRET: Secret key for HMAC signature verification
- BEDROCK_MODEL_ID: Bedrock model ID (e.g., us.anthropic.claude-sonnet-4-6)
- MAX_REQUESTS_PER_IP_PER_DAY: Daily rate limit per IP (default: 100)
"""

import hashlib
import hmac
import json
import os
import time
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


# Configuration
SHARED_SECRET = os.environ.get("SHARED_SECRET", "s2r-shared-secret-change-this-in-production")
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-6")
MAX_REQUESTS_PER_IP_PER_DAY = int(os.environ.get("MAX_REQUESTS_PER_IP_PER_DAY", "100"))
MAX_PAYLOAD_SIZE = 50 * 1024  # 50KB max

# AWS clients
bedrock = boto3.client("bedrock-runtime")
dynamodb = boto3.resource("dynamodb")
rate_limit_table = dynamodb.Table(os.environ.get("RATE_LIMIT_TABLE", "s2r-rate-limits"))


def verify_signature(payload: str, timestamp: str, signature: str) -> bool:
    """Verify HMAC signature and timestamp."""
    # Check timestamp is recent (5 minute window)
    try:
        request_time = float(timestamp)
        current_time = time.time()
        if abs(current_time - request_time) > 300:
            return False
    except (ValueError, TypeError):
        return False

    # Verify signature
    message = f"{timestamp}:{payload}"
    expected_signature = hmac.new(
        SHARED_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


def check_rate_limit(ip_address: str) -> bool:
    """Check if IP has exceeded rate limit.

    Returns True if request is allowed, False if rate limit exceeded.
    """
    today = time.strftime("%Y-%m-%d")
    key = f"{ip_address}#{today}"

    try:
        response = rate_limit_table.update_item(
            Key={"ip_date": key},
            UpdateExpression="ADD request_count :inc SET #ts = :ts",
            ExpressionAttributeNames={"#ts": "timestamp"},
            ExpressionAttributeValues={
                ":inc": 1,
                ":ts": int(time.time()),
                ":limit": MAX_REQUESTS_PER_IP_PER_DAY
            },
            ConditionExpression="attribute_not_exists(request_count) OR request_count < :limit",
            ReturnValues="UPDATED_NEW"
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return False
        raise


def call_bedrock(slurm_script: str) -> str:
    """Call AWS Bedrock to convert SLURM script to Run.ai config."""
    prompt = f"""You are an expert in HPC job scheduling and NVIDIA Run:ai.
Convert the following SLURM batch script to NVIDIA Run:ai format.

SLURM Script:
```
{slurm_script}
```

Produce EXACTLY two fenced code blocks in this order — nothing else, no prose:

## Block 1 — YAML manifest (TrainingWorkload CRD)

```yaml
apiVersion: run.ai/v2alpha1
kind: TrainingWorkload
metadata:
  name: <job-name-from-slurm>          # lowercase, hyphens only, max 63 chars
  namespace: runai-<PROJECT>            # replace <PROJECT> with a placeholder comment
  labels:
    kai.scheduler/preemptibility: preemptible   # preemptible for batch/training
    priorityClassName: low
spec:
  image:
    value: <IMAGE>                      # use a sensible default if not in script
  imagePullPolicy:
    value: IfNotPresent
  command:
    value: <entrypoint>                 # first token of the job command
  args:
    value:
      - <arg1>                          # remaining tokens as list items
  workingDir:
    value: <working-directory>          # from #SBATCH --chdir or script cd
  environment:
    items:
      VAR_NAME:
        value: "value"                  # from export or #SBATCH --export
  compute:
    # Use gpuDevicesRequest (integer) for whole GPUs:
    gpuDevicesRequest: <N>
    # OR use gpuPortionRequest (float 0.0-1.0) for fractional GPU:
    # gpuPortionRequest: 0.5
    cpuCoreRequest: <cores>             # from --cpus-per-task
    cpuMemoryRequest: <NM or NG>        # from --mem, e.g. 32G
  autoScalabilityConfig:
    autoDeleteTimeAfterCompletionSeconds: 86400   # clean up after 24 h
  storage:                             # only if RUNAI_BUCKET is set in s2r context
    s3:
      instances:
        - bucket: <RUNAI_BUCKET_NAME>
          path: <RUNAI_BUCKET_MOUNT>   # /mnt/<bucket-name>
          # accessKeySecret, secretKeyOfAccessKeyId, secretKeyOfSecretKey:
          # leave blank if the cluster uses IAM roles / IRSA for S3 access
```

## Block 2 — Shell script (CLI v2)

```bash
#!/usr/bin/env bash
# Run:ai equivalent of the SLURM script above.
# Pipe-safe: 's2r job.slurm | bash' submits directly. Re-running gets a fresh
# unique workload name via --name-prefix (Run:ai appends an index suffix).
# Set PROJECT before running: export RUNAI_PROJECT=your-project
set -euo pipefail

PROJECT="${{RUNAI_PROJECT:-your-project}}"
JOB_PREFIX=<job-name>

# Use whole GPU (--gpu-devices-request) or fractional (--gpu-portion-request 0.5).
# Repeat --environment-variable for each env var.
# Include --s3 only if RUNAI_BUCKET is in the s2r context.
# Include --datasource only if RUNAI_CACHE is in the s2r context.
# --name-prefix lets Run:ai auto-increment the suffix (job-name-1, job-name-2, ...)
# so re-submitting the same script does NOT collide with an existing workload.
SUBMIT_OUTPUT=$(runai training standard submit \\
  --name-prefix "$JOB_PREFIX" \\
  --project "$PROJECT" \\
  --image <IMAGE> \\
  --image-pull-policy IfNotPresent \\
  --gpu-devices-request <N> \\
  --cpu-core-request <cores> \\
  --cpu-memory-request <NM or NG> \\
  --working-dir <working-directory> \\
  --environment-variable KEY=VALUE \\
  --datasource type=s3,name=<RUNAI_BUCKET_NAME> \\
  --datasource type=hostPath,name=<RUNAI_CACHE> \\
  --preemptibility preemptible \\
  --priority low \\
  --auto-deletion-time-after-completion 24h \\
  --command -- <full command and args> 2>&1)

# Print runai output but suppress its built-in tracking hint (it omits --project).
echo "$SUBMIT_OUTPUT" | grep -v "To track the workload's status"

JOB_NAME=$(echo "$SUBMIT_OUTPUT" | grep -oE "${{JOB_PREFIX}}-[a-f0-9]+" | head -1)
if [[ -n "$JOB_NAME" ]]; then
  echo
  echo "To track the workload's status, run:"
  echo
  echo "runai training standard describe $JOB_NAME -p $PROJECT"
fi
```

CRITICAL: Emit the trailing block EXACTLY as shown above — do NOT add extra commands
(no logs/list/delete hints), do NOT change "To track the workload's status, run:" wording,
and do NOT add a "Monitor your job with:" header. Only the single 'describe' line.

SLURM → Run:ai mapping rules:
- --job-name          → metadata.name (YAML) and --name-prefix (CLI). Use --name-prefix
                        instead of a positional name so Run:ai auto-appends an index suffix
                        and re-submitting the same script never collides.
- --gres=gpu:N        → gpuDevicesRequest: N  (--gpu-devices-request N in CLI)
- --gres=gpu:0.N      → gpuPortionRequest: 0.N (--gpu-portion-request 0.N in CLI)
- --cpus-per-task=N   → cpuCoreRequest: N  (--cpu-core-request N)
- --mem=XG/XM         → cpuMemoryRequest: XG/XM  (--cpu-memory-request XG)
- --time=             → omit (Run:ai uses --auto-deletion-time-after-completion instead)
- --partition=        → omit or use --node-pools if partition maps to a known node pool
- --chdir / cd        → workingDir / --working-dir
- export VAR=VAL      → environment.items / --environment-variable VAR=VAL
- module load         → omit (bake into container image)
- #SBATCH --array     → omit with a comment that job arrays need --runs N in Run:ai
- RUNAI_BUCKET_NAME   → CLI: --datasource type=s3,name=<RUNAI_BUCKET_NAME>   (uses pre-registered credentials)
                        YAML: storage.s3.instances[].bucket
                        DO NOT use the inline --s3 flag — it has no credentials and silently mounts empty.
- RUNAI_BUCKET_MOUNT  → storage.s3.instances[].path  (mount path baked into the datasource definition)
- RUNAI_CACHE         → --datasource type=hostPath,name=<value>  (pre-defined cluster datasource, mount path is baked in)
- If RUNAI_BUCKET is NOT set in the context header, omit the storage.s3 block and --datasource type=s3 flag entirely.
- If RUNAI_CACHE is NOT set in the context header, omit the --datasource type=hostPath flag entirely.

Path remapping rule (CRITICAL):
- When --chdir or any path in the SLURM script is under a user home directory (e.g. /home/<user>/...),
  remap that prefix to RUNAI_BUCKET_MOUNT for ALL occurrences — not just --working-dir.
- This includes:
  - paths inside `--command --` (the actual script path: e.g. /home/pi/peterdir/git/runai-demo/show_devices.py
    becomes /mnt/<bucket-name>/git/runai-demo/show_devices.py)
  - paths inside `singularity exec` arguments
  - paths inside any heredoc, environment variable, or shell substitution
- Strip Singularity wrappers: `singularity exec [--nv] <image>.sif <cmd> <args>` becomes just `<cmd> <args>`,
  with the SIF image replaced by an equivalent OCI image set via --image. Apply path remapping to <cmd> <args>.
- The remapping prefix must be consistent: the SLURM home dir prefix → RUNAI_BUCKET_MOUNT, preserving the
  trailing path. So /home/pi/peterdir/git/X under bucket mount /mnt/runai-peterdir → /mnt/runai-peterdir/git/X.
  The SLURM "user dir" segment is dropped because the bucket itself is the user's data root.

If the script has no explicit container image, use a sensible default based on
the workload (e.g. nvcr.io/nvidia/pytorch:25.06-py3 for PyTorch/CUDA work,
nvcr.io/nvidia/tensorflow:25.03-tf2-py3 for TensorFlow, rocker/r-base:4.6.0 for
R, ubuntu:22.04 otherwise) and add a brief comment telling the user to replace it.

Container/dependency rule (IMPORTANT — avoid bash setup boilerplate when possible):

1. First, decide which container image you would pick (per the rules above).
2. Then check whether all tools the script invokes are ALREADY available in that
   image's standard install. The well-known images cover their core stack:
     - nvcr.io/nvidia/pytorch:*    → python3, pip, torch, torchvision, torchaudio, CUDA, cuDNN
     - nvcr.io/nvidia/tensorflow:* → python3, pip, tensorflow, CUDA
     - rocker/r-base:*             → R, Rscript
     - rocker/tidyverse:*          → R + tidyverse
     - ubuntu:22.04                → bash only — NO python, NO R, NO compilers
   If every tool the script needs is in the chosen image, run the user's command
   DIRECTLY via `--command --` with no venv setup, no pip install, no bash -c
   wrapper. Do NOT add unnecessary pip/apt/venv steps.

3. ONLY when the chosen image is missing a needed package (e.g. ubuntu:22.04 with
   a python script, or rocker/r-base with a niche CRAN package), wrap the command
   in a small `bash -c` block that creates a persistent venv on the S3/cache mount
   so re-runs are fast. Example pattern (replace VENV path, packages, and entrypoint):

     --environment-variable VENV=<RUNAI_BUCKET_MOUNT>/venv/<name> \\
     --command -- bash -c '
       VENV=<RUNAI_BUCKET_MOUNT>/venv/<name>
       if [ ! -d "$VENV" ]; then
         python3 -m venv "$VENV"
       fi
       source "$VENV/bin/activate"
       pip install --quiet <packages>
       <user-entrypoint>
     '

   Use this only when actually needed — never as a default. The reuse path
   (RUNAI_BUCKET_MOUNT/venv/<name>) makes the first run slow but subsequent
   runs near-instant.

Replace all <PLACEHOLDER> values with real values derived from the SLURM script.
Output ONLY the two fenced code blocks."""

    # Prepare request for Claude on Bedrock
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())
        content = response_body.get("content", [])

        if content and len(content) > 0:
            return content[0].get("text", "")

        return "Error: No content in response"

    except ClientError as e:
        raise Exception(f"Bedrock API error: {e}")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda function handler."""
    try:
        # Extract IP address
        ip_address = event.get("requestContext", {}).get("http", {}).get("sourceIp", "unknown")

        # Get headers (case-insensitive)
        headers = {k.lower(): v for k, v in event.get("headers", {}).items()}

        # Get request body
        body = event.get("body", "")
        if event.get("isBase64Encoded", False):
            import base64
            body = base64.b64decode(body).decode("utf-8")

        # Validate payload size
        if len(body) > MAX_PAYLOAD_SIZE:
            return {
                "statusCode": 413,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Payload too large (max 50KB)"})
            }

        # Verify signature
        timestamp = headers.get("x-s2r-timestamp", "")
        signature = headers.get("x-s2r-signature", "")

        if not verify_signature(body, timestamp, signature):
            return {
                "statusCode": 401,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid signature or expired timestamp"})
            }

        # Check rate limit
        if not check_rate_limit(ip_address):
            return {
                "statusCode": 429,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": f"Rate limit exceeded: {MAX_REQUESTS_PER_IP_PER_DAY} requests per day"
                })
            }

        # Call Bedrock
        runai_config = call_bedrock(body)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"runai_config": runai_config})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
