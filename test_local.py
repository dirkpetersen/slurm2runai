#!/usr/bin/env python3
"""Test script for s2r library (requires deployed Lambda)."""

import os
import sys

# Add s2r to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from s2r import convert_slurm_to_runai, ConversionError


# Example SLURM script
slurm_script = """#!/bin/bash
#SBATCH --job-name=pytorch-training
#SBATCH --output=output_%j.log
#SBATCH --error=error_%j.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:2
#SBATCH --time=24:00:00
#SBATCH --partition=gpu

# Load modules
module load python/3.9
module load cuda/11.8

# Activate virtual environment
source /home/user/venv/bin/activate

# Set environment variables
export NCCL_DEBUG=INFO
export PYTHONUNBUFFERED=1

# Run training
cd /home/user/project
python train.py \\
    --batch-size 32 \\
    --epochs 100 \\
    --learning-rate 0.001 \\
    --data-dir /data/imagenet
"""


def main():
    """Run test conversion."""
    print("Testing s2r conversion...")
    print("-" * 80)

    # Check if API endpoint is set
    api_endpoint = os.environ.get("S2R_API_ENDPOINT")
    if not api_endpoint:
        print("WARNING: S2R_API_ENDPOINT not set!")
        print("Please set it to your Lambda Function URL:")
        print("  export S2R_API_ENDPOINT=https://your-lambda-url.lambda-url.us-east-1.on.aws/")
        print()
        sys.exit(1)

    print(f"API Endpoint: {api_endpoint}")
    print()
    print("Input SLURM script:")
    print("-" * 80)
    print(slurm_script)
    print("-" * 80)
    print()

    try:
        print("Converting...")
        runai_config = convert_slurm_to_runai(slurm_script)

        print("Run.ai Configuration:")
        print("-" * 80)
        print(runai_config)
        print("-" * 80)
        print()
        print("✓ Conversion successful!")

    except ConversionError as e:
        print(f"✗ Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
