# s2r - SLURM to Run.ai Converter

Convert SLURM batch scripts to Run.ai configurations using AI.

## Installation

```bash
pip install s2r
```

## Quick Start

### CLI Usage

```bash
# Convert file: saves job.yaml, prints runai CLI command to stdout
s2r job.slurm

# Convert file: saves output.yaml only (no CLI output)
s2r job.slurm output.yaml

# Convert from stdin: prints runai CLI command to stdout (no file)
s2r < my_slurm_script.sh
```

### Library Usage

```python
from s2r import convert_slurm_to_runai

slurm_script = """
#!/bin/bash
#SBATCH --job-name=my-job
#SBATCH --gres=gpu:2
#SBATCH --mem=32G

python train.py
"""

runai_config = convert_slurm_to_runai(slurm_script)
print(runai_config)
```

## How It Works

1. **Client**: The `s2r` library signs your SLURM script with HMAC-SHA256
2. **API**: Sends the signed request to an AWS Lambda endpoint
3. **AI**: Lambda calls AWS Bedrock (Claude) to perform the conversion
4. **Response**: Returns the Run.ai YAML configuration or CLI commands

## Features

- **Free to use**: The service is provided at no cost (rate-limited)
- **Secure**: Signed requests prevent unauthorized API usage
- **Rate-limited**: 100 requests per IP per day
- **Simple**: Works with stdin, files, or as a library

## Configuration

By default, the tool uses a public API endpoint. If you're deploying your own:

```bash
export S2R_API_ENDPOINT=https://your-lambda-url.lambda-url.us-east-1.on.aws/
```

## Example

Given this SLURM script:

```bash
#!/bin/bash
#SBATCH --job-name=pytorch-training
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:2
#SBATCH --time=24:00:00

python train.py --epochs 100
```

The tool will generate an equivalent Run.ai configuration with:
- GPU resource requests (2 GPUs)
- CPU and memory allocations
- Job name and command
- Appropriate container/image specifications

## Documentation

- **[API Reference](https://github.com/dirkpetersen/slurm2runai/blob/main/docs/api.md)**: Complete API documentation for library and CLI
- **[Architecture](https://github.com/dirkpetersen/slurm2runai/blob/main/docs/architecture.md)**: System design and component details
- **[Deployment Guide](https://github.com/dirkpetersen/slurm2runai/blob/main/docs/deployment.md)**: AWS Lambda deployment instructions
- **[Troubleshooting](https://github.com/dirkpetersen/slurm2runai/blob/main/docs/troubleshooting.md)**: Common issues and solutions
- **[CLAUDE.md](https://github.com/dirkpetersen/slurm2runai/blob/main/CLAUDE.md)**: Quick reference for Claude Code

## Current Deployment Status

**Deployed Lambda Function** (us-west-2):
- Function URL: `https://uqbglp42fwfy3yo77jcphk2bhu0wydft.lambda-url.us-west-2.on.aws/`
- Model: Claude Sonnet 4.5 (20250929)
- Rate Limit: 100 requests/IP/day

**Known Issues**:
- Function URL may return 403 Forbidden due to IAM permission constraints
- See [troubleshooting guide](https://github.com/dirkpetersen/slurm2runai/blob/main/docs/troubleshooting.md#issue-1-lambda-function-url-returns-403-forbidden) for resolution

## Development

See [CLAUDE.md](https://github.com/dirkpetersen/slurm2runai/blob/main/CLAUDE.md) for development commands and quick reference.

For detailed architecture and deployment information, see the [docs/](https://github.com/dirkpetersen/slurm2runai/tree/main/docs) directory.

## Self-Hosting

To deploy your own instance:

```bash
# Clone repository
git clone https://github.com/yourusername/slurm2runai.git
cd slurm2runai

# Deploy Lambda function
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
aws lambda create-function --function-name s2r-converter ...

# See https://github.com/dirkpetersen/slurm2runai/blob/main/docs/deployment.md for full instructions
```

## License

MIT License - see [LICENSE](https://github.com/dirkpetersen/slurm2runai/blob/main/LICENSE) file for details.

## Contributing

Contributions welcome! Please:
1. Open an issue to discuss changes
2. Follow the code style (ruff)
3. Add tests for new features
4. Update documentation
