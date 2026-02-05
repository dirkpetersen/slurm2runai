# Troubleshooting Guide

## Current Known Issues

### Issue 1: Lambda Function URL Returns 403 Forbidden

**Symptoms**:
- All requests to Lambda Function URL return 403 Forbidden
- Error message: "Forbidden. For troubleshooting Function URL authorization issues..."
- Occurs even with `AUTH_TYPE=NONE` configured

**Root Cause**:
The IAM execution role (`DeleteUnusedVolumesRole`) may lack necessary permissions for:
1. AWS Bedrock InvokeModel action
2. DynamoDB read/write operations
3. CloudWatch Logs creation

**Current Status**:
- Function deployed: ✓
- Function URL created: ✓
- Public access permission added: ✓
- Bedrock permissions: ✗ (likely missing)

**Solutions**:

#### Option 1: Update IAM Role Permissions (Recommended)

Add these policies to the Lambda execution role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-west-2:405644541454:table/s2r-rate-limits"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-west-2:405644541454:log-group:/aws/lambda/s2r-converter:*"
    }
  ]
}
```

**AWS CLI Command**:
```bash
# Create policy document
cat > /tmp/bedrock-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0"
    }
  ]
}
EOF

# Attach inline policy
aws iam put-role-policy \
  --role-name DeleteUnusedVolumesRole \
  --policy-name BedrockAccess \
  --policy-document file:///tmp/bedrock-policy.json
```

#### Option 2: Create New IAM Role

If you can't modify the existing role, create a new one with proper permissions:

```bash
# Use CloudFormation template
cd lambda
aws cloudformation deploy \
  --template-file cloudformation-template.yaml \
  --stack-name s2r-converter \
  --capabilities CAPABILITY_NAMED_IAM
```

This will:
- Create a new IAM role with all necessary permissions
- Recreate the Lambda function with the new role
- Preserve all other resources (DynamoDB, Function URL)

#### Option 3: Test Lambda Locally

To verify the function logic works before fixing permissions:

```bash
cd lambda
python3 lambda_function.py
# Manually test the functions
```

### Issue 2: Timestamp Expired Error

**Symptoms**:
- Error: "Invalid signature or expired timestamp"
- Occurs even with valid signature

**Root Cause**:
- Clock skew between client and Lambda
- Request took longer than 5 minutes to reach Lambda

**Solutions**:

1. **Sync system clock**:
   ```bash
   # On Linux
   sudo ntpdate -s time.nist.gov

   # On macOS
   sudo sntp -sS time.apple.com
   ```

2. **Increase timestamp window** (Lambda side):
   Edit `lambda/lambda_function.py`:
   ```python
   max_age_seconds: int = 300  # Change to 600 (10 minutes)
   ```

### Issue 3: Rate Limit Exceeded

**Symptoms**:
- Error: "Rate limit exceeded: 100 requests per day"
- Cannot make any more requests

**Solutions**:

1. **Wait until next day** (UTC timezone)

2. **Clear rate limit entry**:
   ```bash
   # Get current IP
   IP=$(curl -s https://api.ipify.org)
   TODAY=$(date -u +%Y-%m-%d)

   # Delete rate limit entry
   aws dynamodb delete-item \
     --table-name s2r-rate-limits \
     --key "{\"ip_date\": {\"S\": \"${IP}#${TODAY}\"}}"
   ```

3. **Increase rate limit**:
   ```bash
   aws lambda update-function-configuration \
     --function-name s2r-converter \
     --environment "Variables={SHARED_SECRET=s2r-shared-secret-change-this-in-production,BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-20250929-v1:0,MAX_REQUESTS_PER_IP_PER_DAY=1000,RATE_LIMIT_TABLE=s2r-rate-limits}"
   ```

### Issue 4: Bedrock Model Not Found

**Symptoms**:
- Error from Lambda: "Bedrock API error: ... model not found"

**Root Causes**:
- Model not available in your region
- Model ID typo
- Bedrock not enabled in your account

**Solutions**:

1. **Check available models**:
   ```bash
   aws bedrock list-foundation-models \
     --query 'modelSummaries[?contains(modelId, `claude`)].{ModelId:modelId,Name:modelName}' \
     --output table
   ```

2. **Enable Bedrock** (if needed):
   - Go to AWS Console → Bedrock
   - Request access to Claude models
   - Wait for approval (usually instant)

3. **Use different model**:
   ```bash
   # Switch to Claude 3.5 Sonnet v2
   aws lambda update-function-configuration \
     --function-name s2r-converter \
     --environment "Variables={SHARED_SECRET=s2r-shared-secret-change-this-in-production,BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0,MAX_REQUESTS_PER_IP_PER_DAY=100,RATE_LIMIT_TABLE=s2r-rate-limits}"
   ```

### Issue 5: Lambda Timeout

**Symptoms**:
- Request takes > 60 seconds
- Error: "Task timed out after 60.00 seconds"

**Solutions**:

1. **Increase timeout**:
   ```bash
   aws lambda update-function-configuration \
     --function-name s2r-converter \
     --timeout 120
   ```

2. **Optimize Bedrock prompt** (reduce input tokens):
   - Edit `lambda/lambda_function.py`
   - Shorten the system prompt
   - Reduce max_tokens from 4096 to 2048

### Issue 6: Import Error - requests Module

**Symptoms**:
- `ImportError: No module named 'requests'`
- Occurs when running `s2r` CLI

**Solutions**:

1. **Install dependencies**:
   ```bash
   pip install requests
   # Or
   pip install -e .
   ```

2. **Use system Python with proper site-packages**

### Issue 7: DynamoDB ConditionalCheckFailedException

**Symptoms**:
- Rate limit not working correctly
- All requests fail immediately

**Root Cause**:
- DynamoDB item already exists with count >= limit
- Conditional update fails

**Solutions**:

1. **Delete and recreate DynamoDB entries**:
   ```bash
   aws dynamodb scan --table-name s2r-rate-limits \
     --query 'Items[].ip_date.S' \
     --output text | xargs -I {} aws dynamodb delete-item \
       --table-name s2r-rate-limits \
       --key '{"ip_date": {"S": "{}"}}'
   ```

2. **Check rate limit logic**:
   Review `lambda/lambda_function.py` check_rate_limit() function

## Debugging Tips

### Check Lambda Logs

```bash
# Tail logs in real-time
aws logs tail /aws/lambda/s2r-converter --follow

# Get recent errors
aws logs tail /aws/lambda/s2r-converter --since 1h --filter-pattern "ERROR"

# Get specific request
aws logs tail /aws/lambda/s2r-converter --since 1h --filter-pattern "<request-id>"
```

### Test Signature Generation

```bash
cd /home/dp/gh/slurm2runai
python3 -c "
from s2r.auth import create_signed_headers
import time

payload = 'test'
headers = create_signed_headers(payload)

print('Timestamp:', headers['X-S2R-Timestamp'])
print('Signature:', headers['X-S2R-Signature'])
print('Time until expiry:', 300 - (time.time() - float(headers['X-S2R-Timestamp'])), 'seconds')
"
```

### Test Lambda Function Directly

Invoke Lambda without Function URL:

```bash
echo '{"body":"#!/bin/bash\n#SBATCH --gres=gpu:1","headers":{"x-s2r-timestamp":"'$(date +%s)'","x-s2r-signature":"test"}}' > /tmp/event.json

aws lambda invoke \
  --function-name s2r-converter \
  --payload file:///tmp/event.json \
  /tmp/response.json

cat /tmp/response.json
```

### Check DynamoDB Rate Limits

```bash
# Scan all entries
aws dynamodb scan --table-name s2r-rate-limits

# Get specific IP
IP=$(curl -s https://api.ipify.org)
TODAY=$(date -u +%Y-%m-%d)
aws dynamodb get-item \
  --table-name s2r-rate-limits \
  --key "{\"ip_date\": {\"S\": \"${IP}#${TODAY}\"}}"
```

### Verify Function URL Configuration

```bash
# Get Function URL config
aws lambda get-function-url-config --function-name s2r-converter

# Get resource-based policy
aws lambda get-policy --function-name s2r-converter | python3 -m json.tool
```

### Check IAM Role Permissions

```bash
# List role policies
aws iam list-role-policies --role-name DeleteUnusedVolumesRole

# Get inline policy
aws iam get-role-policy \
  --role-name DeleteUnusedVolumesRole \
  --policy-name <policy-name>

# List attached managed policies
aws iam list-attached-role-policies --role-name DeleteUnusedVolumesRole
```

## Getting Help

### Useful AWS CLI Commands

```bash
# Get Lambda function details
aws lambda get-function --function-name s2r-converter

# List recent Lambda invocations
aws lambda list-functions --query 'Functions[?FunctionName==`s2r-converter`]'

# Check Bedrock access
aws bedrock list-foundation-models --region us-west-2

# Test DynamoDB access
aws dynamodb describe-table --table-name s2r-rate-limits
```

### Log Locations

- **Lambda logs**: CloudWatch Logs `/aws/lambda/s2r-converter`
- **Client errors**: stderr when running `s2r` command
- **DynamoDB metrics**: CloudWatch Metrics for `s2r-rate-limits` table

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Invalid signature or expired timestamp" | Signature mismatch or time skew | Check shared secret matches, sync clock |
| "Rate limit exceeded" | Too many requests today | Wait or increase limit |
| "Request failed: 403 Forbidden" | Lambda URL permissions issue | Fix IAM role permissions |
| "Bedrock API error" | Problem calling Bedrock | Check model ID, region, permissions |
| "Request timed out" | Conversion took > 60s | Increase Lambda timeout |
| "Payload too large" | Script > 50KB | Reduce script size or increase limit |

## Next Steps

If issues persist after trying these solutions:

1. Review `docs/architecture.md` for system design
2. Check `docs/deployment.md` for deployment details
3. Review Lambda function code in `lambda/lambda_function.py`
4. Contact AWS support for permission issues
5. Open a GitHub issue with full error logs
