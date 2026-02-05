# s2r Documentation

Comprehensive documentation for the slurm2runai (s2r) project.

## Quick Links

- **New Users**: Start with [API Reference](api.md) for usage examples
- **Deploying**: See [Deployment Guide](deployment.md) for AWS setup
- **Troubleshooting**: Check [Troubleshooting Guide](troubleshooting.md) for common issues
- **Understanding the System**: Read [Architecture](architecture.md) for design details

## Documentation Structure

### [API Reference](api.md)
Complete API documentation for developers using s2r as a library or CLI tool.

**Contents**:
- Python API (`convert_slurm_to_runai()`, authentication functions)
- Command-line interface (`s2r` command)
- REST API (Lambda Function URL)
- Configuration options
- Error handling
- Usage examples

**Target Audience**: Developers integrating s2r into their workflows.

### [Architecture](architecture.md)
System design, component details, and technical architecture.

**Contents**:
- High-level system architecture
- Component descriptions (client, Lambda, DynamoDB, Bedrock)
- Security architecture (HMAC signing, threat model)
- Data flow diagrams
- Scalability considerations
- Monitoring and observability

**Target Audience**: Developers understanding or modifying the system, DevOps engineers.

### [Deployment Guide](deployment.md)
Step-by-step instructions for deploying the Lambda function to AWS.

**Contents**:
- Prerequisites and current deployment status
- Three deployment methods (manual, CloudFormation, SAM)
- Updating existing deployments
- Post-deployment configuration
- Verification and testing
- Cost estimation
- Security considerations

**Target Audience**: DevOps engineers, system administrators deploying s2r.

### [Troubleshooting Guide](troubleshooting.md)
Solutions for common issues and debugging tips.

**Contents**:
- Known issues (403 Forbidden, rate limits, timeouts, etc.)
- Step-by-step resolution procedures
- Debugging commands and techniques
- Error message reference table
- AWS CLI commands for diagnostics

**Target Audience**: Anyone encountering issues with s2r.

## Project Overview

**What is s2r?**

s2r (slurm2runai) converts SLURM batch scripts to Run.ai configurations using AI. It consists of:

1. **Python Package**: Client library with CLI tool
2. **AWS Lambda**: Backend API with rate limiting
3. **AWS Bedrock**: Claude Sonnet 4.5 for conversion
4. **DynamoDB**: Rate limit tracking

**Key Features**:
- HMAC-SHA256 signed requests for security
- 100 requests/IP/day rate limiting
- 5-minute timestamp window (prevents replay attacks)
- 50KB max payload size
- 60-second timeout

## Current Status

**Deployed Resources** (us-west-2):
- Lambda Function: `s2r-converter`
- Function URL: `https://uqbglp42fwfy3yo77jcphk2bhu0wydft.lambda-url.us-west-2.on.aws/`
- DynamoDB Table: `s2r-rate-limits`
- Bedrock Model: `anthropic.claude-sonnet-4-5-20250929-v1:0`

**Known Limitations**:
- Lambda Function URL returns 403 Forbidden (IAM permission issue)
- Existing IAM role lacks Bedrock InvokeModel permission
- Resolution requires updating IAM role or creating new role with proper permissions

## Getting Started

### For End Users

1. **Install the package**:
   ```bash
   pip install s2r
   ```

2. **Set API endpoint**:
   ```bash
   export S2R_API_ENDPOINT=https://uqbglp42fwfy3yo77jcphk2bhu0wydft.lambda-url.us-west-2.on.aws/
   ```

3. **Convert a script**:
   ```bash
   s2r my_slurm_job.sh
   ```

See [API Reference](api.md) for detailed usage.

### For Developers

1. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/slurm2runai.git
   cd slurm2runai
   ```

2. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

See [CLAUDE.md](../CLAUDE.md) for development commands.

### For DevOps/Deployers

1. **Review architecture**:
   Read [Architecture](architecture.md) to understand the system

2. **Prepare AWS account**:
   - Enable AWS Bedrock
   - Request access to Claude models
   - Ensure IAM permissions for Lambda, DynamoDB, Bedrock

3. **Deploy**:
   Follow [Deployment Guide](deployment.md) for step-by-step instructions

4. **Verify**:
   Test deployment and monitor logs

## Common Tasks

### Converting a SLURM Script

**CLI**:
```bash
s2r job.sh output.yaml
```

**Python**:
```python
from s2r import convert_slurm_to_runai

with open('job.sh') as f:
    config = convert_slurm_to_runai(f.read())
```

See: [API Reference](api.md)

### Deploying to AWS

**Quick deploy**:
```bash
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
aws lambda update-function-code --function-name s2r-converter --zip-file fileb://lambda.zip
```

See: [Deployment Guide](deployment.md)

### Fixing 403 Forbidden Error

**Update IAM role**:
```bash
aws iam put-role-policy \
  --role-name DeleteUnusedVolumesRole \
  --policy-name BedrockAccess \
  --policy-document file://bedrock-policy.json
```

See: [Troubleshooting Guide](troubleshooting.md#issue-1-lambda-function-url-returns-403-forbidden)

### Checking Rate Limits

**View DynamoDB entries**:
```bash
aws dynamodb scan --table-name s2r-rate-limits
```

See: [Troubleshooting Guide](troubleshooting.md#debugging-tips)

## Architecture Diagram

```
┌─────────┐
│  User   │
└────┬────┘
     │
     ▼
┌─────────────┐
│ s2r Client  │
│ (HMAC sign) │
└────┬────────┘
     │ HTTPS
     ▼
┌──────────────────────┐
│ Lambda Function URL  │
│ (Verify signature)   │
└────┬─────────────┬───┘
     │             │
     ▼             ▼
┌──────────┐  ┌──────────┐
│ DynamoDB │  │ Bedrock  │
│ (Rate    │  │ (Claude  │
│ limiting)│  │ Sonnet)  │
└──────────┘  └──────────┘
```

See [Architecture](architecture.md) for detailed diagrams.

## Security

### Authentication

All requests are signed with HMAC-SHA256:
- Shared secret between client and Lambda
- Timestamp prevents replay attacks (5-minute window)
- Signature ensures request integrity

### Rate Limiting

- 100 requests per IP per day (default)
- Tracked in DynamoDB per IP/date key
- Atomic increment prevents race conditions

### Best Practices

1. **Change shared secret** from default in production
2. **Rotate secret periodically** (every 90 days)
3. **Monitor CloudWatch** for unusual patterns
4. **Set cost alarms** to prevent surprise bills
5. **Review IAM permissions** regularly

See [Architecture - Security](architecture.md#security-architecture) for details.

## Cost Estimation

Per 1000 conversions:
- **Lambda**: ~$0.20
- **Bedrock (Claude Sonnet 4.5)**: ~$3-15 (varies by script complexity)
- **DynamoDB**: ~$0.01
- **Total**: ~$3-15 per 1000 conversions

At 100 requests/day with rate limiting: ~$0.30-1.50/day

See [Deployment Guide - Cost Estimation](deployment.md#cost-estimation)

## Support

### Issues

- **403 Forbidden**: See [Troubleshooting](troubleshooting.md#issue-1-lambda-function-url-returns-403-forbidden)
- **Rate Limited**: See [Troubleshooting](troubleshooting.md#issue-3-rate-limit-exceeded)
- **Timeout**: See [Troubleshooting](troubleshooting.md#issue-5-lambda-timeout)

### Getting Help

1. Check [Troubleshooting Guide](troubleshooting.md)
2. Review [Architecture](architecture.md) for system understanding
3. Check AWS CloudWatch logs
4. Open GitHub issue with logs and error details

### Contributing

1. Read [Architecture](architecture.md) to understand the system
2. Follow development setup in [CLAUDE.md](../CLAUDE.md)
3. Add tests for new features
4. Update documentation
5. Submit pull request

## Additional Resources

- **Main README**: [../README.md](../README.md)
- **Developer Guide**: [../CLAUDE.md](../CLAUDE.md)
- **Examples**: [../examples/](../examples/)
- **Tests**: [../tests/](../tests/)

## License

MIT License - see [../LICENSE](../LICENSE)
