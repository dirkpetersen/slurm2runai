"""AWS Lambda function for SLURM to Run.ai conversion.

This function:
1. Validates signed requests from the s2r library
2. Implements rate limiting per IP
3. Calls AWS Bedrock to perform the conversion
4. Returns the Run.ai configuration

Environment variables required:
- SHARED_SECRET: Secret key for HMAC signature verification
- BEDROCK_MODEL_ID: Bedrock model ID (e.g., anthropic.claude-sonnet-4-5-20250929-v1:0)
- MAX_REQUESTS_PER_IP_PER_DAY: Daily rate limit per IP (default: 100)
"""

import hashlib
import hmac
import json
import os
import time
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


# Configuration
SHARED_SECRET = os.environ.get("SHARED_SECRET", "s2r-shared-secret-change-this-in-production")
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-sonnet-4-5-20250929-v1:0")
MAX_REQUESTS_PER_IP_PER_DAY = int(os.environ.get("MAX_REQUESTS_PER_IP_PER_DAY", "100"))
MAX_PAYLOAD_SIZE = 50 * 1024  # 50KB max

# AWS clients
bedrock = boto3.client("bedrock-runtime")
dynamodb = boto3.resource("dynamodb")
rate_limit_table = dynamodb.Table(os.environ.get("RATE_LIMIT_TABLE", "s2r-rate-limits"))


def verify_signature(payload: str, timestamp: str, signature: str) -> bool:
    """Verify HMAC signature and timestamp."""
    # Check timestamp is recent (5 minute window)
    try:
        request_time = float(timestamp)
        current_time = time.time()
        if abs(current_time - request_time) > 300:
            return False
    except (ValueError, TypeError):
        return False

    # Verify signature
    message = f"{timestamp}:{payload}"
    expected_signature = hmac.new(
        SHARED_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


def check_rate_limit(ip_address: str) -> bool:
    """Check if IP has exceeded rate limit.

    Returns True if request is allowed, False if rate limit exceeded.
    """
    today = time.strftime("%Y-%m-%d")
    key = f"{ip_address}#{today}"

    try:
        response = rate_limit_table.update_item(
            Key={"ip_date": key},
            UpdateExpression="ADD request_count :inc SET #ts = :ts",
            ExpressionAttributeNames={"#ts": "timestamp"},
            ExpressionAttributeValues={
                ":inc": 1,
                ":ts": int(time.time()),
                ":limit": MAX_REQUESTS_PER_IP_PER_DAY
            },
            ConditionExpression="attribute_not_exists(request_count) OR request_count < :limit",
            ReturnValues="UPDATED_NEW"
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return False
        raise


def call_bedrock(slurm_script: str) -> str:
    """Call AWS Bedrock to convert SLURM script to Run.ai config."""
    prompt = f"""You are an expert in HPC job scheduling and Kubernetes orchestration.
Convert the following SLURM batch script to a Run.ai job configuration.

SLURM Script:
```
{slurm_script}
```

Please provide:
1. A Run.ai YAML configuration file that captures all the resource requirements, or
2. The equivalent Run.ai CLI commands if YAML is not appropriate

Important considerations:
- Map SLURM resource directives (#SBATCH) to Run.ai resource requests
- Convert GPU requests (--gres=gpu:X) to Run.ai GPU specifications
- Map memory and CPU requests appropriately
- Handle job arrays, dependencies, and time limits if present
- Include proper image/container specifications
- Add appropriate environment variables and working directory settings

Provide ONLY the Run.ai configuration/commands, no additional explanation."""

    # Prepare request for Claude on Bedrock
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())
        content = response_body.get("content", [])

        if content and len(content) > 0:
            return content[0].get("text", "")

        return "Error: No content in response"

    except ClientError as e:
        raise Exception(f"Bedrock API error: {e}")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda function handler."""
    try:
        # Extract IP address
        ip_address = event.get("requestContext", {}).get("http", {}).get("sourceIp", "unknown")

        # Get headers (case-insensitive)
        headers = {k.lower(): v for k, v in event.get("headers", {}).items()}

        # Get request body
        body = event.get("body", "")
        if event.get("isBase64Encoded", False):
            import base64
            body = base64.b64decode(body).decode("utf-8")

        # Validate payload size
        if len(body) > MAX_PAYLOAD_SIZE:
            return {
                "statusCode": 413,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Payload too large (max 50KB)"})
            }

        # Verify signature
        timestamp = headers.get("x-s2r-timestamp", "")
        signature = headers.get("x-s2r-signature", "")

        if not verify_signature(body, timestamp, signature):
            return {
                "statusCode": 401,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid signature or expired timestamp"})
            }

        # Check rate limit
        if not check_rate_limit(ip_address):
            return {
                "statusCode": 429,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": f"Rate limit exceeded: {MAX_REQUESTS_PER_IP_PER_DAY} requests per day"
                })
            }

        # Call Bedrock
        runai_config = call_bedrock(body)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"runai_config": runai_config})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
