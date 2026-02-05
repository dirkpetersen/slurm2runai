# Architecture Documentation

## System Overview

The s2r (SLURM to Run.ai) converter is a distributed system that uses AI to translate HPC batch scripts to Kubernetes-based orchestration configurations.

## High-Level Architecture

```
┌─────────────┐
│   User      │
│  CLI/Script │
└──────┬──────┘
       │
       │ SLURM Script
       ▼
┌──────────────────────────────────────┐
│   s2r Python Package (Client)       │
│                                      │
│  ┌───────────────────────────────┐  │
│  │  1. Read Input                │  │
│  │     - stdin/file             │  │
│  │                               │  │
│  │  2. Sign Request              │  │
│  │     - HMAC-SHA256            │  │
│  │     - Timestamp              │  │
│  │                               │  │
│  │  3. HTTP POST                 │  │
│  │     - Headers: signature     │  │
│  │     - Body: SLURM script     │  │
│  └───────────────────────────────┘  │
└──────────────┬───────────────────────┘
               │
               │ HTTPS (TLS)
               ▼
┌──────────────────────────────────────┐
│   AWS Lambda Function URL            │
│   (Public, CORS-enabled)             │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│   Lambda Function (s2r-converter)    │
│                                      │
│  ┌───────────────────────────────┐  │
│  │  1. Verify Signature          │  │
│  │     - Check HMAC              │  │
│  │     - Validate timestamp      │  │
│  │                               │  │
│  │  2. Rate Limiting             │  │
│  │     - Query DynamoDB          │  │
│  │     - Increment counter       │  │
│  │                               │  │
│  │  3. Call Bedrock              │  │
│  │     - Send prompt + script    │  │
│  │     - Get Run.ai config       │  │
│  │                               │  │
│  │  4. Return Response           │  │
│  │     - JSON with config        │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────┬────────────┘
       │                  │
       │                  │
       ▼                  ▼
┌──────────────┐   ┌─────────────────┐
│  DynamoDB    │   │  AWS Bedrock    │
│  Rate Limits │   │  Claude 4.5     │
└──────────────┘   └─────────────────┘
```

## Component Details

### 1. Client Library (s2r Package)

**Location**: `s2r/`

**Files**:
- `__init__.py`: Package exports
- `converter.py`: Core conversion function, HTTP client
- `auth.py`: HMAC signature generation
- `cli.py`: Command-line interface

**Responsibilities**:
- Accept SLURM scripts from various sources (stdin, file, string)
- Generate HMAC-SHA256 signatures with timestamp
- Send signed HTTP POST requests to Lambda
- Parse and return Run.ai configurations
- Handle errors and retries

**Dependencies**:
- `requests`: HTTP client
- Standard library: `hmac`, `hashlib`, `time`, `os`

### 2. Lambda Function

**Location**: `lambda/lambda_function.py`

**Configuration**:
- Runtime: Python 3.11
- Memory: 512 MB
- Timeout: 60 seconds
- Region: us-west-2

**Responsibilities**:
1. **Request Validation**:
   - Extract headers and body from Lambda event
   - Verify HMAC signature matches
   - Check timestamp is within 5-minute window
   - Reject invalid/expired requests with 401

2. **Rate Limiting**:
   - Extract source IP from request context
   - Query DynamoDB for today's request count
   - Increment counter atomically
   - Reject if limit exceeded with 429

3. **AI Conversion**:
   - Construct prompt for Claude
   - Call AWS Bedrock InvokeModel API
   - Parse response to extract Run.ai config
   - Handle Bedrock errors gracefully

4. **Response**:
   - Return JSON with `runai_config` field
   - Include error messages for debugging
   - Set appropriate HTTP status codes

**Dependencies** (provided by Lambda runtime):
- `boto3`: AWS SDK for DynamoDB and Bedrock
- Standard library: `json`, `os`, `time`, `hmac`, `hashlib`

### 3. DynamoDB Rate Limiting

**Table**: `s2r-rate-limits`

**Schema**:
- **Primary Key**: `ip_date` (String) - format: `{ip}#{YYYY-MM-DD}`
- **Attributes**:
  - `request_count` (Number): Number of requests today
  - `timestamp` (Number): Last request timestamp
  - `ttl` (Number, optional): Time-to-live for auto-cleanup

**Access Pattern**:
- **Write**: Update item with atomic increment
  ```python
  table.update_item(
      Key={"ip_date": f"{ip}#{today}"},
      UpdateExpression="ADD request_count :inc",
      ConditionExpression="request_count < :limit"
  )
  ```
- **Read**: Implicit during update (conditional check)

**Billing**: PAY_PER_REQUEST (on-demand)

### 4. AWS Bedrock Integration

**Model**: `anthropic.claude-sonnet-4-5-20250929-v1:0`

**API Call**:
```python
bedrock.invoke_model(
    modelId="anthropic.claude-sonnet-4-5-20250929-v1:0",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    })
)
```

**Prompt Structure**:
- System context: Expert in HPC and Kubernetes
- Task: Convert SLURM script to Run.ai config
- SLURM script provided in code block
- Instructions for mapping resources
- Request for YAML or CLI commands only

**Response Parsing**:
- Extract `content[0].text` from response
- Return as `runai_config` in JSON

## Security Architecture

### HMAC Request Signing

**Algorithm**: HMAC-SHA256

**Message Format**:
```
{timestamp}:{payload}
```

**Signature Generation** (Client):
```python
timestamp = str(time.time())
message = f"{timestamp}:{payload}"
signature = hmac.new(
    SHARED_SECRET.encode("utf-8"),
    message.encode("utf-8"),
    hashlib.sha256
).hexdigest()
```

**Signature Verification** (Lambda):
```python
expected = hmac.new(
    SHARED_SECRET.encode("utf-8"),
    f"{timestamp}:{payload}".encode("utf-8"),
    hashlib.sha256
).hexdigest()
return hmac.compare_digest(signature, expected)
```

**Security Properties**:
- **Authentication**: Only clients with the shared secret can generate valid signatures
- **Integrity**: Any modification to payload or timestamp invalidates signature
- **Replay Protection**: Timestamp must be within 5 minutes (prevents replay attacks)
- **Constant-time Comparison**: `compare_digest` prevents timing attacks

### Threat Model

**Protected Against**:
- Unauthorized API usage (requires shared secret)
- Replay attacks (timestamp expiry)
- Request tampering (HMAC integrity)
- DoS attacks (rate limiting per IP)
- Timing attacks (constant-time comparison)

**Not Protected Against**:
- Shared secret compromise (rotate periodically)
- IP spoofing (Lambda Function URL doesn't validate)
- Distributed attacks from many IPs (consider AWS WAF)
- Cost attacks within rate limits (set CloudWatch alarms)

## Data Flow

### Successful Request

1. User runs `s2r < script.sh`
2. CLI reads script from stdin
3. `auth.create_signed_headers()` generates signature with current timestamp
4. `converter.convert_slurm_to_runai()` POSTs to Lambda URL with headers
5. Lambda validates signature and timestamp → ✓
6. Lambda checks rate limit in DynamoDB → ✓ (count: 45/100)
7. Lambda increments counter → count: 46/100
8. Lambda calls Bedrock with prompt + script
9. Bedrock returns Run.ai YAML configuration
10. Lambda returns JSON: `{"runai_config": "..."}`
11. Client prints YAML to stdout
12. User saves or pipes to kubectl

### Failed Request (Rate Limited)

1. User runs `s2r < script.sh`
2. Signature generated and request sent
3. Lambda validates signature → ✓
4. Lambda checks rate limit → ✗ (count: 100/100)
5. Lambda returns 429 with error message
6. Client raises `ConversionError` with rate limit message
7. User sees error on stderr, script exits with code 1

### Failed Request (Invalid Signature)

1. Attacker sends request without proper signature
2. Lambda validates signature → ✗
3. Lambda returns 401 Unauthorized
4. Request rejected, no Bedrock call made

## Scalability

### Current Limits

- **Lambda Concurrency**: Default account limit (1000)
- **Lambda Timeout**: 60 seconds per request
- **DynamoDB**: On-demand (auto-scales)
- **Bedrock**: Per-region quotas (varies by model)
- **Rate Limit**: 100 requests/IP/day

### Scaling Considerations

**To Handle More Traffic**:
- Increase Lambda concurrency if needed
- Add CloudFront for caching (if deterministic conversions)
- Use API Gateway for advanced rate limiting
- Add multiple Function URLs in different regions

**To Reduce Costs**:
- Cache common conversions (Redis/DynamoDB)
- Use Lambda provisioned concurrency for consistent latency
- Switch to cheaper Bedrock model for simple scripts
- Add request size limits (currently 50KB)

## Monitoring and Observability

### Key Metrics

**Lambda**:
- Invocations per minute
- Duration (should be < 30s avg)
- Errors (4xx, 5xx)
- Throttles (if concurrency exceeded)

**DynamoDB**:
- Read/Write capacity units
- Throttled requests
- Items with high request counts

**Bedrock**:
- InvokeModel API calls
- Latency
- Errors (throttling, model not found)
- Input/Output token counts (for cost)

### Logging

**Lambda Logs** (CloudWatch):
- All requests logged with IP, signature status
- Rate limit checks logged
- Bedrock calls and responses logged
- Errors include stack traces

**Access Pattern**:
```bash
aws logs tail /aws/lambda/s2r-converter --follow
```

### Alarms

**Recommended CloudWatch Alarms**:
1. Lambda errors > 10 in 5 minutes
2. Lambda duration > 45 seconds (approaching timeout)
3. Estimated charges > $50/day
4. DynamoDB throttling > 0

## Deployment Architecture

### Infrastructure as Code

**Options**:
1. **SAM Template** (`template.yaml`): Full serverless deployment
2. **CloudFormation** (`cloudformation-template.yaml`): More control
3. **Manual AWS CLI**: For constrained environments

**Resources Created**:
- Lambda Function
- Lambda Function URL
- DynamoDB Table
- IAM Role (if permissions allow)
- CloudWatch Log Group (automatic)

### Current Deployment

- **Method**: Manual AWS CLI (due to IAM constraints)
- **Region**: us-west-2
- **Account**: 405644541454
- **Role**: Reused existing `DeleteUnusedVolumesRole`

## Future Enhancements

### Potential Improvements

1. **Authentication**: User-specific API keys instead of shared secret
2. **Caching**: Cache identical SLURM scripts (hash-based lookup)
3. **Async Processing**: Queue long conversions, poll for results
4. **Multi-Model**: Allow users to select model (Sonnet vs Haiku)
5. **Validation**: Validate generated Run.ai configs before returning
6. **Feedback Loop**: Let users report bad conversions, improve prompts
7. **Web UI**: Simple web interface for non-CLI users
8. **Batch API**: Convert multiple scripts in one request

### Architectural Changes

1. **API Gateway**: Add before Lambda for advanced features
2. **SQS Queue**: Decouple Lambda from Bedrock for retry logic
3. **Step Functions**: Orchestrate complex multi-step conversions
4. **ECS/Fargate**: For long-running or resource-intensive conversions
5. **CDN**: CloudFront for global distribution and caching
