# slurm2runai — Setup & Development Journey

This document captures all steps taken to build, deploy, and validate the
`s2r` tool from initial state to a working public service.

---

## 1. Repository State at Start

- Package `s2r` v0.2.2 on PyPI
- Lambda `s2r-converter` deployed in us-west-2 but broken (403 on all requests)
- Default endpoint in `converter.py` pointed at a stale Function URL
- `boto3` was a hard dependency even though most users don't need IAM auth

---

## 2. Diagnosing the 403 on Lambda Function URL

The Lambda had `AuthType=NONE` set but every request returned 403.

**What we checked:**
```bash
# IAM policy simulation — confirmed no SCP blocking it
aws --profile iam-dirk iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::405644541454:user/iam-dirk \
  --action-names lambda:InvokeFunctionUrl \
  --resource-arns arn:aws:lambda:us-west-2:405644541454:function:s2r-converter \
  --context-entries "ContextKeyName=lambda:FunctionUrlAuthType,ContextKeyValues=NONE,ContextKeyType=string"
# Result: EvalDecision=allowed, AllowedByOrganizations=true
# → No SCP. Something else is blocking it.
```

**Root cause (unresolved):** Likely an account-level "Block Public Access for
Lambda Function URLs" setting or a Resource Control Policy (RCP) managed from
the Org root. The AWS CLI does not expose these; they must be checked in the
console or by an org admin. Flipping to `AuthType=AWS_IAM` + SigV4-signed
requests works fine.

**Workaround chosen:** Put AWS API Gateway HTTP API in front of the Lambda.
API Gateway is a separate resource type not subject to the same guardrail.

---

## 3. Upgrade Lambda Model to Claude Sonnet 4.6

```bash
# Check available inference profiles
aws --profile iam-dirk bedrock list-inference-profiles --region us-west-2 \
  --query "inferenceProfileSummaries[?contains(inferenceProfileId,'sonnet-4')].[inferenceProfileId,inferenceProfileName]"
# Selected: us.anthropic.claude-sonnet-4-6 (US cross-region profile)

# Update Lambda env var
aws --profile iam-dirk lambda update-function-configuration \
  --function-name s2r-converter --region us-west-2 \
  --environment "Variables={
    SHARED_SECRET=s2r-shared-secret-change-this-in-production,
    BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6,
    MAX_REQUESTS_PER_IP_PER_DAY=100,
    RATE_LIMIT_TABLE=s2r-rate-limits}"
```

Also updated the default in `lambda/lambda_function.py`:
```python
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-6")
```

---

## 4. Create API Gateway HTTP API (v0.3.0)

```bash
# Create HTTP API — --target creates integration + $default route + auto-deploy stage
aws --profile iam-dirk apigatewayv2 create-api \
  --region us-west-2 \
  --name s2r-api \
  --protocol-type HTTP \
  --target "arn:aws:lambda:us-west-2:405644541454:function:s2r-converter"
# → ApiId: zzk4zf48pi
# → Public URL: https://zzk4zf48pi.execute-api.us-west-2.amazonaws.com/

# Grant API Gateway permission to invoke the Lambda
aws --profile iam-dirk lambda add-permission \
  --function-name s2r-converter --region us-west-2 \
  --statement-id ApiGatewayInvoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-west-2:405644541454:zzk4zf48pi/*"
```

**Important:** The source ARN must use the simple wildcard `zzk4zf48pi/*` —
the triple-wildcard `zzk4zf48pi/*/*/*` does not match the HTTP API v2 `$default`
route and causes 500 errors (requests never reach Lambda).

**Client changes in `s2r/converter.py`:**
```python
DEFAULT_API_ENDPOINT = "https://zzk4zf48pi.execute-api.us-west-2.amazonaws.com/"
USE_IAM_AUTH = os.environ.get("S2R_USE_IAM_AUTH", "false").lower() in ("true","1","yes")
```

Released as **v0.3.0**.

---

## 5. Make boto3 Optional (v0.3.1)

`boto3` was a hard dependency (~50 MB installed) used only in the SigV4 signing
path that runs when `S2R_USE_IAM_AUTH=true`. Since v0.3.0 defaults to the public
API Gateway endpoint, it was dead weight for most users.

**`pyproject.toml` change:**
```toml
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
iam-auth = ["boto3>=1.28.0"]
dev      = ["pytest>=7.0.0", "ruff>=0.1.0", "mypy>=1.0.0", "boto3>=1.28.0"]
```

**Error message in `converter.py` updated:**
```python
raise ConversionError(
    "boto3 is required for IAM authentication. "
    "Install with: pip install 's2r[iam-auth]'"
)
```

**Install options:**
```bash
pip install s2r              # no AWS dependencies (default, public endpoint)
pip install 's2r[iam-auth]'  # adds boto3 for self-hosted IAM-auth deployments
pip install 's2r[dev]'       # adds pytest, ruff, mypy, boto3
```

Released as **v0.3.1**.

---

## 6. Current Deployment Architecture

```
User (pip install s2r)
    └─ s2r CLI / convert_slurm_to_runai()
           │  HMAC-SHA256 signed request (X-S2R-Timestamp, X-S2R-Signature)
           │  No AWS credentials required
           ▼
  API Gateway HTTP API
  zzk4zf48pi.execute-api.us-west-2.amazonaws.com
  AuthType: NONE  (public)
           │
           ▼
  Lambda: s2r-converter (us-west-2, python3.11, 512 MB)
           │  1. Verify HMAC signature (5-min replay window)
           │  2. Rate limit: 1000 req/IP/day (DynamoDB s2r-rate-limits)
           │  3. Call Bedrock — model from X-S2R-Model header (alias sonnet|opus)
           │     defaulting to us.anthropic.claude-sonnet-4-6
           │
           ▼
  Response: {"runai_config": "```yaml\n...\n```\n```bash\n...\n```"}
```

**AWS resources:**
| Resource | ID / Name | Region |
|---|---|---|
| API Gateway HTTP API | `zzk4zf48pi` | us-west-2 |
| Lambda function | `s2r-converter` | us-west-2 |
| DynamoDB table | `s2r-rate-limits` | us-west-2 |
| Bedrock model | `us.anthropic.claude-sonnet-4-6` (default) / `claude-opus-4-7` (opt-in) | us-west-2 |
| Lambda IAM role | `DeleteUnusedVolumesRole` | us-west-2 |

**Lambda environment variables:**
```
SHARED_SECRET=s2r-shared-secret-change-this-in-production
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6   # default; client can override per request via X-S2R-Model
MAX_REQUESTS_PER_IP_PER_DAY=1000
RATE_LIMIT_TABLE=s2r-rate-limits
```

---

## 7. Rewrite Lambda Prompt (v0.3.2)

The original prompt was vague and produced wrong output — incorrect
`apiVersion`, invented field names, wrong CLI flags. The new prompt is
grounded in the actual `TrainingWorkload` CRD spec and `runai training
standard submit --help` output observed on a live cluster.

**Key prompt rules added:**
- Always produce two fenced blocks: ` ```yaml ` (CRD) + ` ```bash ` (CLI v2)
- Exact SLURM → Run:ai field mapping (see table below)
- `module load` and venv activation omitted with explanatory comments
- `--partition` omitted with note to use `--node-pools` if applicable
- CPU-only jobs omit GPU fields entirely

**SLURM → Run:ai mapping:**

| SLURM directive | YAML field | CLI v2 flag |
|---|---|---|
| `--job-name` | `metadata.name` | positional name arg |
| `--gres=gpu:N` | `spec.compute.gpuDevicesRequest: N` | `--gpu-devices-request N` |
| `--gres=gpu:0.N` | `spec.compute.gpuPortionRequest: 0.N` | `--gpu-portion-request 0.N` |
| `--cpus-per-task=N` | `spec.compute.cpuCoreRequest: N` | `--cpu-core-request N` |
| `--mem=XG` | `spec.compute.cpuMemoryRequest: XG` | `--cpu-memory-request XG` |
| `--time=` | `autoDeleteTimeAfterCompletionSeconds: 86400` | `--auto-deletion-time-after-completion 24h` |
| `export VAR=VAL` | `spec.environment.items.VAR.value` | `--environment-variable VAR=VAL` |
| `cd /path` / `--chdir` | `spec.workingDir.value` | `--working-dir /path` |
| `--partition` | *(omitted — add `--node-pools` manually)* | `--node-pools <pool>` |
| `module load` | *(omitted — bake into container image)* | — |

**Correct YAML structure:**
```yaml
apiVersion: run.ai/v2alpha1
kind: TrainingWorkload
metadata:
  name: <job-name>
  namespace: runai-<PROJECT>
  labels:
    kai.scheduler/preemptibility: preemptible
    priorityClassName: low
spec:
  image:
    value: <IMAGE>
  imagePullPolicy:
    value: IfNotPresent
  command:
    value: <entrypoint>
  args:
    value: [<arg1>, <arg2>, ...]
  workingDir:
    value: /path
  environment:
    items:
      MY_VAR:
        value: "my-value"
  compute:
    gpuDevicesRequest: 1        # whole GPU
    # gpuPortionRequest: 0.5    # fractional GPU (alternative)
    cpuCoreRequest: 8
    cpuMemoryRequest: 32G
  autoScalabilityConfig:
    autoDeleteTimeAfterCompletionSeconds: 86400
```

**Submit via YAML:**
```bash
runai workload submit --file job.yaml --project <project>
```

**Submit via CLI:**
```bash
export RUNAI_PROJECT=your-project
runai training standard submit <job-name> \
  --project "$RUNAI_PROJECT" \
  --image <IMAGE> \
  --gpu-devices-request 1 \
  --cpu-core-request 8 \
  --cpu-memory-request 32G \
  --working-dir /path \
  --environment-variable KEY=VALUE \
  --preemptibility preemptible \
  --priority low \
  --auto-deletion-time-after-completion 24h \
  --command -- python train.py --epochs 100
```

Released as **v0.3.2**.

---

## 8. Live Cluster Details (minipod-dev)

```bash
runai login --help          # see login options for your setup
runai cluster list          # → minipod-dev at https://runai.hpc.oregonstate.edu
runai project list          # → osu-default (8 GPU quota)
runai workload list --project osu-default
```

**Cluster info:**
| Field | Value |
|---|---|
| Cluster name | `minipod-dev` |
| URL | `https://runai.hpc.oregonstate.edu` |
| Run:ai version | `2.25.9` |
| Kubernetes | vanilla v1.34.5 |
| Default project | `osu-default` |
| GPU hardware | NVIDIA H200 (14 GB HBM3e, 700W) |
| Driver | 595.71.05 |
| CUDA | 13.2 |

**Existing workloads observed:**
| Name | Type | Status | GPUs |
|---|---|---|---|
| `dp1` | Training | Running | 0.10 (fractional) |
| `i1133` | Inference | Running | 2.00 |
| `rapidsai-test` | Workspace | Running | 0.50 |

---

## 9. Validated Job Submissions

### Test: nvidia-smi (GPU detection)
```bash
runai training standard submit test-nvidia-smi \
  --project osu-default \
  --image nvcr.io/nvidia/pytorch:25.06-py3 \
  --image-pull-policy IfNotPresent \
  --gpu-portion-request 0.1 \
  --preemptibility preemptible \
  --priority low \
  --auto-deletion-time-after-completion 24h \
  --command -- nvidia-smi
```
**Result:** Completed in 6 seconds. Confirmed NVIDIA H200, Driver 595.71.05, CUDA 13.2.

### Test: R statistical calculation (CPU-only)
```bash
runai training standard submit r-stats \
  --project osu-default \
  --image rocker/r-base:4.6.0 \
  --image-pull-policy IfNotPresent \
  --cpu-core-request 4 \
  --cpu-memory-request 8G \
  --preemptibility preemptible \
  --priority low \
  --auto-deletion-time-after-completion 24h \
  --command -- Rscript -e '
set.seed(42); n <- 1000000
x <- rnorm(n, mean=50, sd=10); y <- 2.5*x + rnorm(n, mean=0, sd=5)
print(summary(lm(y~x)))'
```
**Result:** Completed in 26 seconds (including image pull).
Slope = 2.4997 (expected 2.5), R² = 0.9616. ✓

---

## 10. Recommended Container Images

| Workload | Image |
|---|---|
| PyTorch / CUDA | `nvcr.io/nvidia/pytorch:25.06-py3` |
| TensorFlow | `nvcr.io/nvidia/tensorflow:25.03-tf2-py3` |
| R (minimal) | `rocker/r-base:4.6.0` |
| R + tidyverse | `rocker/tidyverse:4.6.0` |
| R + ML (torch, xgboost) | `rocker/ml:4.6.0` |
| R + CUDA | `rocker/cuda:4.6.0` |
| Generic Ubuntu | `ubuntu:22.04` |

---

## 11. Quick Reference: Lambda Deployment

```bash
# Code-only update (most common)
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
aws --profile iam-dirk lambda update-function-code \
  --function-name s2r-converter \
  --region us-west-2 \
  --zip-file fileb://lambda.zip
aws --profile iam-dirk lambda wait function-updated \
  --function-name s2r-converter --region us-west-2

# Full infrastructure redeploy (first time or infra changes)
cd lambda
sam deploy --guided
# SAM creates: Lambda + API Gateway + DynamoDB
# Output: ApiEndpoint URL → update DEFAULT_API_ENDPOINT in s2r/converter.py
```

---

## 12. Release History

| Version | Key change |
|---|---|
| 0.2.2 | IAM auth disabled by default |
| 0.3.0 | Switch to API Gateway (no more 403), Claude Sonnet 4.6 |
| 0.3.1 | boto3 made optional (`pip install 's2r[iam-auth]'`) |
| 0.3.2 | Prompt rewritten with exact Run:ai CRD schema and CLI v2 flags |
| 0.4.0 | Setup wizard, persistent runai.env, S3 datasource auto-provisioning |
| 0.4.1 | Pipe-to-bash output, region-aware S3, prompt fixes |
| 0.4.2 | RUNAI_AWS_PROFILE, full-path bucket mirroring, wizard order |
| 0.4.3 | --prompt flag (inspect Bedrock prompt), Claude Opus 4.7, 1000 req/IP/day |
| 0.4.4 | RUNAI_MODEL (sonnet default, opus opt-in) — Lambda revert to Sonnet by default since Opus 4.7 sometimes exceeds API Gateway 30s timeout |

---

## 13. Known Issues

- **Lambda Function URL returns 403 with `AuthType=NONE`** even when configured
  correctly and `iam simulate-principal-policy` shows `AllowedByOrganizations=true`.
  Suspected cause: account-level "Block Public Access for Lambda Function URLs" or
  an RCP at the Org root. **Do not attempt to fix by switching back to a Function URL**
  without first verifying with the org admin. The API Gateway workaround is stable.

- **Stale Function URL endpoints** — `uqbglp42...` and `btohftfievc7...` are Lambda
  Function URLs that no longer work. The live endpoint is always the API Gateway one
  in `DEFAULT_API_ENDPOINT` in `s2r/converter.py`.

- **GitHub Actions Node.js deprecation warning** — the publish workflow uses actions
  pinned to Node 20. These will need updating before September 2026.
