# s2r - SLURM to Run:ai Converter

Convert SLURM batch scripts to Run:ai configurations using AI.

## Installation

```bash
pip install s2r
```

No AWS account or credentials required — a public hosted endpoint handles
conversion (rate-limited to 100 requests per IP per day).

```bash
pip install 's2r[iam-auth]'   # only needed if you self-host behind IAM auth
```

## Quick Start

### First run — setup wizard

On the first run with no arguments `s2r` detects your Run:ai environment and
saves the configuration to `~/.runai/runai.env`:

```
$ s2r
s2r — SLURM to Run:ai converter

runai CLI detected in PATH.
Auto-detect project, cluster, and datasources from 'runai' CLI? [Y/n]:
Detected:
  project = osu-default
  datasources:
    cache  (HostPath)
    my-bucket  (S3)

Configure environment variables now? [Y/n]:
RUNAI_PROJECT [osu-default]:
RUNAI_BUCKET  (optional, S3 datasource name or s3://uri) [my-bucket]:
RUNAI_CACHE  (datasource name for cache) [cache]:

Saved to /home/user/.runai/runai.env:
  RUNAI_PROJECT=osu-default
  RUNAI_BUCKET=my-bucket
  RUNAI_CACHE=cache

These will be loaded automatically next time you run s2r.
```

Run `s2r --config` at any time to update the configuration.

### Converting scripts

```bash
# Convert file — saves job.yaml, prints runai CLI command to stdout
s2r job.slurm

# Convert file — saves output.yaml only
s2r job.slurm output.yaml

# Convert from stdin — prints runai CLI command to stdout
s2r < my_slurm_script.sh
cat job.slurm | s2r
```

### Library usage

```python
from s2r import convert_slurm_to_runai

result = convert_slurm_to_runai("""
#!/bin/bash
#SBATCH --job-name=my-job
#SBATCH --gres=gpu:2
#SBATCH --mem=32G

python train.py
""")
print(result)
```

## How It Works

1. `s2r` loads `~/.runai/runai.env` and injects your project/bucket/cache as
   context into the SLURM script
2. Signs the request with HMAC-SHA256 (no AWS credentials needed on the client)
3. POSTs to an AWS API Gateway HTTP endpoint
4. A Lambda behind the API calls Bedrock (Claude Sonnet 4.6) to convert the script
5. Returns two fenced blocks: a `TrainingWorkload` YAML manifest + a `runai` shell script

## Configuration

### `~/.runai/runai.env` (auto-loaded on every run)

Created by `s2r --config` or on first run. Supports standard `.env` format.
Shell environment variables always take precedence.

| Variable | Effect |
|---|---|
| `RUNAI_PROJECT` | Fills `--project` and `namespace: runai-<PROJECT>` in output |
| `RUNAI_BUCKET` | S3 datasource name or `s3://uri` — mounted at `/mnt/<name>` |
| `RUNAI_CACHE` | HostPath datasource name for cache (e.g. `cache`) |

### Other environment variables

```bash
export S2R_API_ENDPOINT=https://...   # custom endpoint (self-hosted)
export S2R_AWS_REGION=us-west-2       # region for SigV4 (self-hosted IAM auth)
export S2R_USE_IAM_AUTH=true          # enable IAM auth (requires s2r[iam-auth])
export S2R_VERBOSE=1                  # show detection/API warnings
```

## Example output

Given this SLURM script:

```bash
#!/bin/bash
#SBATCH --job-name=train
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:2

python train.py --epochs 100
```

`s2r` produces a `train.yaml` (TrainingWorkload CRD) and prints the equivalent
`runai training standard submit` command to stdout, with `RUNAI_PROJECT`,
`--s3`, and `--datasource` filled in from your saved configuration.

## S3 datasource auto-provisioning

If you enter a bucket name that is not yet registered in Run:ai, the setup
wizard offers to create it automatically using your AWS credentials from
`~/.aws/credentials` (or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`):

```
  'my-new-bucket' is not yet registered as a Run:ai datasource.
  Using AWS default profile (key: AKIAV44S...)
  Create S3 datasource 'my-new-bucket' in Run:ai now? [Y/n]:
  S3 endpoint URL [https://s3.amazonaws.com]:
  Datasource 'my-new-bucket' created successfully.
```

## Current deployment

| Resource | Value |
|---|---|
| Endpoint | AWS API Gateway HTTP API (`zzk4zf48pi`, us-west-2) |
| Model | Claude Sonnet 4.6 (`us.anthropic.claude-sonnet-4-6`) |
| Rate limit | 100 requests / IP / day |
| Auth | HMAC-SHA256 (no AWS credentials required) |

## Self-hosting

```bash
git clone https://github.com/dirkpetersen/slurm2runai.git
cd slurm2runai/lambda
sam deploy --guided   # creates API Gateway + Lambda + DynamoDB
# then set S2R_API_ENDPOINT to the output URL
```

See [CLAUDE.md](https://github.com/dirkpetersen/slurm2runai/blob/main/CLAUDE.md)
and [SETUP_JOURNEY.md](https://github.com/dirkpetersen/slurm2runai/blob/main/SETUP_JOURNEY.md)
for full deployment and architecture details.

## Examples

See [examples/](https://github.com/dirkpetersen/slurm2runai/tree/main/examples)
for reproduction-ready Run:ai job examples (GPU detection, R statistics, PyTorch training).

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## License

MIT — see [LICENSE](https://github.com/dirkpetersen/slurm2runai/blob/main/LICENSE)
