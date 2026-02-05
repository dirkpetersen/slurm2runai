#!/bin/bash
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
python train.py \
    --batch-size 32 \
    --epochs 100 \
    --learning-rate 0.001 \
    --data-dir /data/imagenet
