#!/usr/bin/env python3
"""
Minimal Run:ai submission test — submits a job that runs nvidia-smi and exits.
Produces two outputs:
  - test_nvidia_smi.yaml   (submit via: runai workload submit --file test_nvidia_smi.yaml -p osu-default)
  - test_nvidia_smi.sh     (submit via: bash test_nvidia_smi.sh)
"""

import subprocess
import sys

PROJECT   = "osu-default"
JOB_NAME  = "test-nvidia-smi"
IMAGE     = "nvcr.io/nvidia/pytorch:25.06-py3"
GPU_FRAC  = 0.1          # fractional GPU — enough to see devices, cheap to schedule


# ── YAML manifest (TrainingWorkload CRD) ─────────────────────────────────────

YAML = f"""\
apiVersion: run.ai/v2alpha1
kind: TrainingWorkload
metadata:
  name: {JOB_NAME}
  namespace: runai-{PROJECT}
  labels:
    kai.scheduler/preemptibility: preemptible
    priorityClassName: low
spec:
  image:
    value: {IMAGE}
  imagePullPolicy:
    value: IfNotPresent
  command:
    value: nvidia-smi
  compute:
    gpuPortionRequest: {GPU_FRAC}
"""

# ── Shell CLI command ─────────────────────────────────────────────────────────

SHELL = f"""\
#!/usr/bin/env bash
# Run:ai test job — shows NVIDIA devices then exits.
# Usage: bash test_nvidia_smi.sh
set -euo pipefail

runai training standard submit {JOB_NAME} \\
  --project {PROJECT} \\
  --image {IMAGE} \\
  --image-pull-policy IfNotPresent \\
  --gpu-portion-request {GPU_FRAC} \\
  --preemptibility preemptible \\
  --priority low \\
  --command -- nvidia-smi
"""

# ── Write files ───────────────────────────────────────────────────────────────

with open("test_nvidia_smi.yaml", "w") as f:
    f.write(YAML)
print("Written: test_nvidia_smi.yaml")

with open("test_nvidia_smi.sh", "w") as f:
    f.write(SHELL)
import os; os.chmod("test_nvidia_smi.sh", 0o755)
print("Written: test_nvidia_smi.sh")

# ── Submit via CLI (shell method) ─────────────────────────────────────────────

print(f"\nSubmitting '{JOB_NAME}' to project '{PROJECT}' via CLI...")
result = subprocess.run(
    [
        "runai", "training", "standard", "submit", JOB_NAME,
        "--project", PROJECT,
        "--image", IMAGE,
        "--image-pull-policy", "IfNotPresent",
        "--gpu-portion-request", str(GPU_FRAC),
        "--preemptibility", "preemptible",
        "--priority", "low",
        "--command", "--", "nvidia-smi",
    ],
    capture_output=True, text=True
)

print(result.stdout)
if result.returncode != 0:
    print(f"stderr: {result.stderr}", file=sys.stderr)
    sys.exit(result.returncode)

print("\nJob submitted. To monitor:")
print(f"  runai workload describe {JOB_NAME} --project {PROJECT}")
print(f"  runai workload logs {JOB_NAME} --project {PROJECT}")
