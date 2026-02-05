# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**📚 For detailed documentation, see the [`docs/`](docs/) directory - this file is a quick reference only.**

## Project Overview

**slurm2runai** (package name: `s2r`) is a Python CLI tool and library that uses AI to convert SLURM submit scripts to Run.ai configurations.

## Architecture

```
User/Library → s2r Client → Lambda Function URL → AWS Bedrock (Claude Sonnet 4.5) → Run.ai Config
                                    ↓
                               DynamoDB (rate limiting)
```

**Components:**
1. **s2r Package** (`s2r/`): Client with HMAC-signed requests
2. **Lambda Function** (`lambda/`): Validates signatures, rate limits, calls Bedrock
3. **Security**: HMAC-SHA256 + timestamp (5min window) prevents abuse

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

# CLI Usage
s2r < slurm_script.sh
s2r input.sh output.yaml
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
- URL: `https://uqbglp42fwfy3yo77jcphk2bhu0wydft.lambda-url.us-west-2.on.aws/`
- Model: `anthropic.claude-sonnet-4-5-20250929-v1:0`
- DynamoDB: `s2r-rate-limits` table

**Known Issues:**
- Lambda Function URL may return 403 Forbidden due to IAM permission issues
- The existing role (`DeleteUnusedVolumesRole`) may lack Bedrock permissions
- See `docs/troubleshooting.md` for resolution steps

## Configuration

```bash
# Client
export S2R_API_ENDPOINT=https://uqbglp42fwfy3yo77jcphk2bhu0wydft.lambda-url.us-west-2.on.aws/

# Security
# Update SHARED_SECRET in s2r/auth.py and Lambda environment variable
```

## Key Details

- **Model**: Claude Sonnet 4.5 (20250929)
- **Rate limit**: 100 requests/IP/day
- **Max payload**: 50KB
- **Auth**: HMAC-SHA256 with 5-minute expiry
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
