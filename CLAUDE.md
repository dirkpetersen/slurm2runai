# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**slurm2runai** (package name: `s2r`) is a Python CLI tool and library that converts SLURM submit scripts to Run.ai configurations using AWS Bedrock (Claude).

## Development Commands

```bash
# Setup
pip install -e ".[dev]"

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a single test
pytest tests/test_auth.py::test_verify_signature_valid

# Lint / format
ruff check .
ruff format .

# Integration test (requires running Lambda endpoint)
S2R_API_ENDPOINT=https://... python test_local.py
```

## Architecture

The client is a thin signing wrapper; all conversion logic lives in the Lambda function.

```
s2r CLI/library
    → signs request (HMAC-SHA256 + timestamp headers)
    → POST to API Gateway HTTP API (public, no AWS auth)
        → invokes Lambda
            → verify HMAC signature (5-min replay window)
            → check rate limit (DynamoDB: ip#date key, atomic increment)
            → call AWS Bedrock (Claude) with SLURM script
            → return {"runai_config": "..."} JSON
```

API Gateway sits in front of Lambda because the AWS account enforces auth on Lambda Function URLs (we couldn't get `AuthType=NONE` to work — see "Known Issues"). API Gateway HTTP APIs are a separate resource type and are not subject to that guardrail. The HMAC signature is the only authentication; AWS-side auth is bypassed.

**s2r package (`s2r/`):**
- `auth.py`: `create_signed_headers(payload)` → adds `X-S2R-Timestamp` + `X-S2R-Signature` headers. The HMAC shared secret is hardcoded as `s2r-shared-secret-change-this-in-production` in both the client and Lambda — in production it should come from `SHARED_SECRET` env var on the Lambda side.
- `converter.py`: `convert_slurm_to_runai()` — signs the request, optionally adds AWS SigV4 (IAM auth, off by default since v0.2.2), POSTs to endpoint, extracts `runai_config` from JSON response.
- `cli.py`: Four I/O modes (stdin→stdout, file→auto-named yaml+stdout, file+output→yaml only, help). The `parse_response()` function extracts fenced code blocks (` ```yaml ` and ` ```bash/shell/sh `) from the AI's markdown response — the raw AI text is never written directly to disk.

**Lambda (`lambda/`):**
- `lambda_function.py`: Handler pipeline — signature verification → rate limit (DynamoDB) → Bedrock call → JSON response.
- `template.yaml`: SAM template that creates the Lambda + DynamoDB table.
- Rate limit key format: `{ip}#{YYYY-MM-DD}`, TTL-enabled for auto-cleanup.

**Tests (`tests/`):**
- All tests are unit tests with no mocking — no integration tests (Lambda not reachable in CI).
- `test_auth.py` covers the full HMAC signing/verification logic.
- `test_converter.py` only tests input validation (empty/whitespace scripts).

## Lambda Deployment

```bash
# Quick update (code only)
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
aws lambda update-function-code --function-name s2r-converter --zip-file fileb://lambda.zip

# Full SAM deploy (first time or infra changes)
cd lambda
sam deploy --guided
```

**Current deployment:**
- API Gateway HTTP API: `zzk4zf48pi` (us-west-2), auth: `NONE` (HMAC signature in app layer)
- Public URL: `https://zzk4zf48pi.execute-api.us-west-2.amazonaws.com/`
- Lambda: `s2r-converter` (still has a Function URL on `AWS_IAM`, but unused)
- Model: `us.anthropic.claude-sonnet-4-6` (US cross-region inference profile)
- DynamoDB: `s2r-rate-limits` table, 100 req/IP/day
- Prompt produces **two fenced blocks** per response: ` ```yaml ` (TrainingWorkload CRD) + ` ```bash ` (CLI v2 shell script); `parse_response()` in `cli.py` splits them automatically

## Configuration

```bash
# Client-side overrides (all optional)
export S2R_API_ENDPOINT=https://your-lambda-url.lambda-url.us-west-2.on.aws/
export S2R_AWS_REGION=us-west-2
export S2R_USE_IAM_AUTH=true   # disabled by default since v0.2.2

# Lambda-side env vars
SHARED_SECRET=...              # must match client's hardcoded secret
BEDROCK_MODEL_ID=...
MAX_REQUESTS_PER_IP_PER_DAY=100
RATE_LIMIT_TABLE=s2r-rate-limits
```

## Known Issues

- Lambda Function URLs return 403 for unauthenticated requests in this account even when configured with `AuthType=NONE` and a `Principal:"*"` resource policy. The `iam simulate-principal-policy` API confirms it is **not** an SCP (`AllowedByOrganizations: true`). Suspected cause: an account-level "Block Public Access for Lambda Function URLs" setting or an RCP managed from the Org root account. **Workaround:** use API Gateway HTTP API in front of the Lambda — that's what the deployment now does. Don't try to "fix" this by switching back to a Function URL without first verifying with the org admin.
- Stale endpoints to ignore: `uqbglp42fwfy3yo77jcphk2bhu0wydft...` and `btohftfievc7zn5ffic7e5jrve0gzafw...` (Lambda Function URLs). The live URL is the API Gateway one in `DEFAULT_API_ENDPOINT`.
