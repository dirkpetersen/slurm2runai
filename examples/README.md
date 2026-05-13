# Run:ai Examples — Reproduction Guide

This guide shows how to reproduce the example workloads on the **minipod-dev** cluster
(`https://runai.hpc.oregonstate.edu`, project `osu-default`).

## Prerequisites

```bash
# Log in to the cluster
runai login

# Confirm your project is visible
runai project list          # → osu-default
```

### Environment variables for smoother conversion

Setting these before running `s2r` causes the AI to fill in real values instead of
`<PROJECT>` / `<CLUSTER>` / `<BUCKET>` placeholders in the generated YAML and shell script:

| Variable | What it controls |
|---|---|
| `RUNAI_PROJECT` | Run:ai project name → used in `--project` and `namespace: runai-<PROJECT>` |
| `RUNAI_BUCKET` | Object-storage bucket for input/output data — mounted at `/mnt/<bucket-name>` |
| `RUNAI_CACHE` | Name of a pre-defined HostPath datasource for cache (default: `cache`) |

```bash
export RUNAI_PROJECT=osu-default
export RUNAI_BUCKET=s3://my-bucket/jobs   # optional
export RUNAI_CACHE=cache                  # optional — name from 'runai datasource list'
```

These only affect the s2r conversion output — `runai` CLI itself reads `RUNAI_PROJECT`
natively so setting it once covers both tools.

The easiest way to set all of these is:
```bash
s2r --config   # interactive wizard: auto-detects from runai CLI and saves to ~/.runai/runai.env
```

---

## Example 1 — GPU Detection (nvidia-smi)

Runs `nvidia-smi` inside the official PyTorch container using a fractional GPU (0.1).
Completes in ~6 seconds (plus image pull on first run).

**Submit via CLI:**
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

**Submit via YAML** (`test_nvidia_smi.yaml` in repo root):
```bash
runai workload submit --file ../test_nvidia_smi.yaml --project osu-default
```

**Monitor and get logs:**
```bash
runai workload describe test-nvidia-smi --project osu-default
runai workload logs test-nvidia-smi --project osu-default
```

**Expected output:**
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.71.05    Driver Version: 595.71.05    CUDA Version: 13.2                |
|-----------------------------------------+------------------------+----------------------|
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
|   0  NVIDIA H200 ...                    | ...                    | ...                  |
+-----------------------------------------------------------------------------------------+
```

**Clean up:**
```bash
runai training standard delete test-nvidia-smi --project osu-default
```

---

## Example 2 — R Statistical Calculation (CPU-only)

Runs a linear regression on 1 million random samples in R.
Completes in ~26 seconds (including image pull on first run).
SLURM source: [`r_calculation.slurm`](r_calculation.slurm)

**Submit via CLI:**
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

**Monitor and get logs:**
```bash
runai workload describe r-stats --project osu-default
runai workload logs r-stats --project osu-default
```

**Expected output:**
```
Coefficients:
             Estimate Std. Error t value Pr(>|t|)
(Intercept) -0.007...   0.049...  -0.14    0.889
x            2.4997...  0.000...  ...    <2e-16 ***

Residual standard error: 4.999 on 999998 degrees of freedom
Multiple R-squared:  0.9616,    Adjusted R-squared:  0.9616
```

Slope ≈ 2.5 (set by `2.5*x`), R² ≈ 0.962. ✓

**Clean up:**
```bash
runai training standard delete r-stats --project osu-default
```

---

## Example 3 — Convert a SLURM Script with s2r, then Submit

`s2r` uses AI (AWS Bedrock / Claude) to translate a SLURM script into a Run:ai
YAML manifest + CLI shell script.

**Install s2r:**
```bash
pip install s2r
```

**Convert the PyTorch training example:**
```bash
s2r examples/example_slurm.sh
# Writes: example_slurm.yaml  (TrainingWorkload CRD)
#         example_slurm.sh    (runai CLI shell script — shown on stdout)
```

**Review and edit the generated files**, then submit:
```bash
# Option A — YAML manifest
runai workload submit --file example_slurm.yaml --project osu-default

# Option B — shell script
bash example_slurm.sh
```

**Convert the R example:**
```bash
s2r examples/r_calculation.slurm
# Writes: r_calculation.yaml
#         r_calculation.sh
```

**Pipe a script directly (no file output):**
```bash
cat examples/example_slurm.sh | s2r
```

---

## Cluster Reference

| Field | Value |
|---|---|
| Cluster | `minipod-dev` |
| URL | `https://runai.hpc.oregonstate.edu` |
| Run:ai version | `2.25.9` |
| Default project | `osu-default` (8 GPU quota) |
| GPU hardware | NVIDIA H200 (140 GB HBM3e) |
| CUDA | 13.2 |

**Useful images:**

| Workload | Image |
|---|---|
| PyTorch / CUDA | `nvcr.io/nvidia/pytorch:25.06-py3` |
| TensorFlow | `nvcr.io/nvidia/tensorflow:25.03-tf2-py3` |
| R (minimal) | `rocker/r-base:4.6.0` |
| R + tidyverse | `rocker/tidyverse:4.6.0` |
| R + ML (torch, xgboost) | `rocker/ml:4.6.0` |
| Generic Ubuntu | `ubuntu:22.04` |

**Common commands:**

```bash
runai workload list --project osu-default          # list all jobs
runai workload describe <name> --project osu-default
runai workload logs <name> --project osu-default
runai training standard delete <name> --project osu-default
```
