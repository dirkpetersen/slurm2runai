# Lambda Function Deployment

This directory contains the AWS Lambda function that powers the s2r service.

## Architecture

```
s2r client → Lambda Function URL → Bedrock (Claude) → Response
                ↓
            DynamoDB (rate limiting)
```

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. AWS SAM CLI installed: `pip install aws-sam-cli`
3. Access to AWS Bedrock with Claude model

## Deployment

### Option 1: Deploy with SAM (Recommended)

```bash
cd lambda

# Build
sam build

# Deploy (first time - guided)
sam deploy --guided

# Deploy (subsequent times)
sam deploy
```

### Option 2: Manual Deployment

```bash
cd lambda

# Create deployment package
pip install -r requirements.txt -t package/
cp lambda_function.py package/
cd package && zip -r ../lambda.zip . && cd ..

# Create Lambda function (replace with your values)
aws lambda create-function \
  --function-name s2r-converter \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment Variables="{SHARED_SECRET=your-secret,BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0}"

# Create Function URL
aws lambda create-function-url-config \
  --function-name s2r-converter \
  --auth-type NONE
```

## Configuration

After deployment:

1. Note the Function URL from the output
2. Update `s2r/auth.py` with your SHARED_SECRET
3. Set environment variable: `export S2R_API_ENDPOINT=<your-function-url>`
4. Or users can set it: `export S2R_API_ENDPOINT=<your-function-url>`

## Security Notes

- **SHARED_SECRET**: Change this from the default! Use a strong random value.
- The secret is hardcoded in both the library and Lambda for simplicity
- For production, consider using AWS Secrets Manager
- Rate limiting is per-IP per-day (default: 100 requests)
- Requests expire after 5 minutes (prevents replay attacks)
- Max payload size: 50KB

## Monitoring

```bash
# View logs
sam logs -n S2RFunction --tail

# Or with AWS CLI
aws logs tail /aws/lambda/s2r-converter --follow
```

## Cost Estimation

With default settings (100 req/day per IP):
- Lambda: ~$0.20/1M requests
- Bedrock (Claude Sonnet): ~$3/1M input tokens, ~$15/1M output tokens
- DynamoDB: Minimal (PAY_PER_REQUEST)

Typical cost: **$0.01-0.05 per conversion** depending on script size.
