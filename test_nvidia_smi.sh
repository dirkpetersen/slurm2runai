#!/usr/bin/env bash
# Run:ai test job — shows NVIDIA devices then exits.
# Usage: bash test_nvidia_smi.sh
set -euo pipefail

runai training standard submit test-nvidia-smi \
  --project osu-default \
  --image nvcr.io/nvidia/pytorch:25.06-py3 \
  --image-pull-policy IfNotPresent \
  --gpu-portion-request 0.1 \
  --preemptibility preemptible \
  --priority low \
  --command -- nvidia-smi
