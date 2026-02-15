# Deployment Guide

This guide covers deploying the s2r Lambda function to AWS.

## Prerequisites

- AWS CLI configured with credentials
- Python 3.11+
- Access to AWS Bedrock with Claude models
- Permissions to create Lambda functions, DynamoDB tables, and Function URLs

## Current Deployment Status

**Deployed Resources:**
- **Lambda Function**: `s2r-converter` (us-west-2)
- **DynamoDB Table**: `s2r-rate-limits` (us-west-2)
- **IAM Role**: `DeleteUnusedVolumesRole` (reused existing role)
- **Bedrock Model**: `anthropic.claude-sonnet-4-5-20250929-v1:0`

**Environment Variables:**
- `SHARED_SECRET`: `s2r-shared-secret-change-this-in-production`
- `BEDROCK_MODEL_ID`: `anthropic.claude-sonnet-4-5-20250929-v1:0`
- `MAX_REQUESTS_PER_IP_PER_DAY`: `100`
- `RATE_LIMIT_TABLE`: `s2r-rate-limits`

## Deployment Methods

### Method 1: Manual Deployment (Used for Current Deployment)

This method was used because of IAM permission constraints.

#### Step 1: Create DynamoDB Table

```bash
aws dynamodb create-table \
  --table-name s2r-rate-limits \
  --attribute-definitions AttributeName=ip_date,AttributeType=S \
  --key-schema AttributeName=ip_date,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

#### Step 2: Create Lambda Deployment Package

```bash
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
```

#### Step 3: Create Lambda Function

```bash
aws lambda create-function \
  --function-name s2r-converter \
  --runtime python3.11 \
  --role arn:aws:iam::405644541454:role/DeleteUnusedVolumesRole \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment "Variables={SHARED_SECRET=s2r-shared-secret-change-this-in-production,BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0,MAX_REQUESTS_PER_IP_PER_DAY=100,RATE_LIMIT_TABLE=s2r-rate-limits}"
```

#### Step 4: Create Function URL

```bash
aws lambda create-function-url-config \
  --function-name s2r-converter \
  --auth-type NONE \
  --cors 'AllowOrigins=["*"],AllowMethods=["POST"],AllowHeaders=["*"]'
```

#### Step 5: Add Public Access Permission

```bash
aws lambda add-permission \
  --function-name s2r-converter \
  --statement-id FunctionURLAllowPublicAccess \
  --action lambda:InvokeFunctionUrl \
  --principal "*" \
  --function-url-auth-type NONE
```

### Method 2: CloudFormation Deployment (Requires Full IAM Permissions)

If you have full IAM permissions, use the CloudFormation template:

```bash
cd lambda
aws cloudformation deploy \
  --template-file cloudformation-template.yaml \
  --stack-name s2r-converter \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    SharedSecret=your-secret-here \
    BedrockModelId=anthropic.claude-sonnet-4-5-20250929-v1:0 \
    MaxRequestsPerIpPerDay=100
```

### Method 3: AWS SAM Deployment (Ideal)

If SAM CLI is installed:

```bash
cd lambda
sam build
sam deploy --guided
```

## Updating the Lambda Function

To update just the code:

```bash
cd lambda
python3 -m zipfile -c lambda.zip lambda_function.py
aws lambda update-function-code \
  --function-name s2r-converter \
  --zip-file fileb://lambda.zip
```

To update environment variables:

```bash
aws lambda update-function-configuration \
  --function-name s2r-converter \
  --environment "Variables={SHARED_SECRET=new-secret,BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0,MAX_REQUESTS_PER_IP_PER_DAY=100,RATE_LIMIT_TABLE=s2r-rate-limits}"
```

## Checking Bedrock Model Availability

To list available Claude models in your region:

```bash
aws bedrock list-foundation-models \
  --query 'modelSummaries[?contains(modelId, `claude`) && contains(modelId, `sonnet`)].{ModelId:modelId,Name:modelName}' \
  --output table
```

## Post-Deployment

After deployment:

1. **Note the Function URL** from the output
2. **Update the client configuration**:
   ```bash
   export S2R_API_ENDPOINT=<your-function-url>
   ```
3. **Update the shared secret** in both:
   - `s2r/auth.py` (line 11)
   - Lambda environment variable

## Verifying Deployment

Test the Lambda function:

```bash
# Set the endpoint
export S2R_API_ENDPOINT=https://your-lambda-url.lambda-url.us-west-2.on.aws/

# Run test
cd /home/dp/gh/slurm2runai
python3 test_local.py
```

Or test with curl:

```bash
cd /home/dp/gh/slurm2runai
python3 -c "
from s2r.auth import create_signed_headers
headers = create_signed_headers('test payload')
print(' '.join([f'-H \"{k}: {v}\"' for k, v in headers.items()]))
"

# Use the output to construct a curl command
curl -X POST <headers> -d "test payload" <function-url>
```

## Monitoring

View Lambda logs:

```bash
aws logs tail /aws/lambda/s2r-converter --follow
```

Check DynamoDB rate limit table:

```bash
aws dynamodb scan --table-name s2r-rate-limits
```

## Cost Estimation

Approximate costs per 1000 conversions:
- **Lambda**: ~$0.20 (1M requests, 512MB, 30s avg)
- **Bedrock (Claude Sonnet 4.5)**: ~$3-15 depending on prompt/response size
- **DynamoDB**: ~$0.01 (PAY_PER_REQUEST)
- **Total**: ~$3-15 per 1000 conversions

## Security Considerations

1. **Change the shared secret** from the default
2. **Rotate the secret periodically**
3. **Monitor DynamoDB for abuse** patterns
4. **Set up CloudWatch alarms** for cost thresholds
5. **Review Lambda execution role** permissions

## Known Limitations

- Current IAM role (`DeleteUnusedVolumesRole`) may not have Bedrock permissions
- Function URL returns 403 Forbidden until permissions are resolved
- See `troubleshooting.md` for resolution steps
