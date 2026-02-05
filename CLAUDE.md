# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**📚 For detailed documentation, see the [`docs/`](docs/) directory - this file is a quick reference only.**

## Project Overview

**slurm2runai** (package name: `s2r`) is a Python CLI tool and library that uses AI to convert SLURM submit scripts to Run.ai configurations.

## Architecture

```
User/Library → s2r Client (AWS SigV4 + HMAC) → Lambda Function URL (IAM auth) → AWS Bedrock (Claude 3.5 Sonnet v2) → Run.ai Config
                                                           ↓
                                                      DynamoDB (rate limiting)
```

**Components:**
1. **s2r Package** (`s2r/`): Client with AWS SigV4 + HMAC-signed requests
2. **Lambda Function** (`lambda/`): Validates signatures, rate limits, calls Bedrock
3. **Security**: AWS IAM authentication + HMAC-SHA256 + timestamp (5min window)

## Development Commands

```bash
# Setup
pip install -e ".[dev]"

# Testing
pytest
pytest tests/test_converter.py

# Linting
ruff check .
ruff format .

# CLI Usage (requires AWS credentials)
AWS_PROFILE=your-profile s2r < slurm_script.sh
AWS_PROFILE=your-profile s2r input.sh output.yaml
```

## Lambda Deployment

See `docs/deployment.md` for detailed instructions.

**Quick deploy (requires AWS CLI configured):**
```bash
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
aws lambda update-function-code --function-name s2r-converter --zip-file fileb://lambda.zip
```

**Current deployment:**
- Function: `s2r-converter` (us-west-2)
- URL: `https://btohftfievc7zn5ffic7e5jrve0gzafw.lambda-url.us-west-2.on.aws/`
- Auth: AWS_IAM (requires AWS credentials)
- Model: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- DynamoDB: `s2r-rate-limits` table

## Configuration

```bash
# Required: AWS credentials (via AWS_PROFILE, env vars, or IAM role)
export AWS_PROFILE=your-profile

# Optional: Override defaults
export S2R_API_ENDPOINT=https://btohftfievc7zn5ffic7e5jrve0gzafw.lambda-url.us-west-2.on.aws/
export S2R_AWS_REGION=us-west-2
export S2R_USE_IAM_AUTH=true
```

## Key Details

- **Model**: Claude 3.5 Sonnet v2 (20241022)
- **Rate limit**: 100 requests/IP/day
- **Max payload**: 50KB
- **Auth**: AWS IAM (SigV4) + HMAC-SHA256 with 5-minute expiry
- **Region**: us-west-2

## Detailed Documentation

**This CLAUDE.md is a quick reference. For comprehensive documentation:**

Start here: **[`docs/README.md`](docs/README.md)** - Documentation index and overview

Specific guides:
- **[`docs/deployment.md`](docs/deployment.md)** - Complete AWS deployment walkthrough with all commands used
- **[`docs/architecture.md`](docs/architecture.md)** - Detailed system design, data flows, security architecture
- **[`docs/troubleshooting.md`](docs/troubleshooting.md)** - Solutions for 403 errors, rate limits, timeouts, etc.
- **[`docs/api.md`](docs/api.md)** - Full API reference with code examples

The docs/ folder contains 40KB+ of detailed technical documentation.
