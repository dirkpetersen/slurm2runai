# API Reference

## Client Library API

### Python API

#### `convert_slurm_to_runai()`

Convert a SLURM script to Run.ai configuration.

```python
from s2r import convert_slurm_to_runai, ConversionError

def convert_slurm_to_runai(
    slurm_script: str,
    api_endpoint: Optional[str] = None,
    timeout: int = 60
) -> str
```

**Parameters**:
- `slurm_script` (str): SLURM batch script content
- `api_endpoint` (str, optional): Lambda Function URL. Defaults to `S2R_API_ENDPOINT` env var
- `timeout` (int, optional): Request timeout in seconds. Default: 60

**Returns**:
- `str`: Run.ai configuration (YAML or CLI commands)

**Raises**:
- `ConversionError`: If conversion fails (invalid signature, rate limit, timeout, etc.)

**Example**:
```python
from s2r import convert_slurm_to_runai, ConversionError

slurm_script = """#!/bin/bash
#SBATCH --job-name=my-job
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
python train.py
"""

try:
    runai_config = convert_slurm_to_runai(slurm_script)
    print(runai_config)
except ConversionError as e:
    print(f"Conversion failed: {e}")
```

#### `ConversionError`

Exception raised when conversion fails.

```python
class ConversionError(Exception):
    """Raised when conversion fails."""
    pass
```

**Common error messages**:
- `"SLURM script cannot be empty"`
- `"Request timed out"`
- `"Request failed: 403 Forbidden"`
- `"API error: Rate limit exceeded: 100 requests per day"`
- `"Invalid JSON response"`

### Authentication API

#### `create_signed_headers()`

Generate headers with HMAC signature for API requests.

```python
from s2r.auth import create_signed_headers

def create_signed_headers(payload: str) -> Dict[str, str]
```

**Parameters**:
- `payload` (str): Request body to sign

**Returns**:
- `dict`: Headers dictionary with signature, timestamp, and content-type

**Example**:
```python
from s2r.auth import create_signed_headers

payload = "test payload"
headers = create_signed_headers(payload)

print(headers)
# {
#     "X-S2R-Timestamp": "1234567890.123",
#     "X-S2R-Signature": "abc123...",
#     "Content-Type": "text/plain"
# }
```

#### `generate_signature()`

Generate HMAC-SHA256 signature for a payload.

```python
from s2r.auth import generate_signature

def generate_signature(
    payload: str,
    timestamp: str,
    secret: str = SHARED_SECRET
) -> str
```

**Parameters**:
- `payload` (str): Request body
- `timestamp` (str): Unix timestamp as string
- `secret` (str): Shared secret key. Default: from `SHARED_SECRET` constant

**Returns**:
- `str`: Hex-encoded HMAC-SHA256 signature (64 characters)

**Example**:
```python
from s2r.auth import generate_signature
import time

payload = "test"
timestamp = str(time.time())
signature = generate_signature(payload, timestamp)

print(signature)  # "a1b2c3d4..."
```

#### `verify_signature()`

Verify HMAC signature and timestamp (Lambda side).

```python
from s2r.auth import verify_signature

def verify_signature(
    payload: str,
    timestamp: str,
    signature: str,
    secret: str = SHARED_SECRET,
    max_age_seconds: int = 300
) -> bool
```

**Parameters**:
- `payload` (str): Request body
- `timestamp` (str): Unix timestamp as string
- `signature` (str): Hex-encoded signature to verify
- `secret` (str): Shared secret key
- `max_age_seconds` (int): Maximum age of timestamp. Default: 300 (5 minutes)

**Returns**:
- `bool`: True if signature valid and timestamp fresh, False otherwise

## Command-Line Interface

### `s2r` Command

Convert SLURM scripts from stdin/file to stdout/file.

```bash
s2r [input_file] [output_file]
```

**Usage Patterns**:

```bash
# Read from stdin, write to stdout
s2r < slurm_script.sh
cat slurm_script.sh | s2r

# Read from file, write to stdout
s2r slurm_script.sh

# Read from file, write to file
s2r slurm_script.sh output.yaml
```

**Environment Variables**:
- `S2R_API_ENDPOINT`: Lambda Function URL (required)

**Exit Codes**:
- `0`: Success
- `1`: Conversion error (rate limit, invalid signature, etc.)

**Examples**:

```bash
# Basic usage
export S2R_API_ENDPOINT=https://xxx.lambda-url.us-west-2.on.aws/
s2r examples/example_slurm.sh

# Pipe to kubectl
s2r my_job.sh | kubectl apply -f -

# Save to file with status message
s2r my_job.sh runai_job.yaml
# Output: "Run.ai configuration written to: runai_job.yaml"

# Error handling
s2r invalid_script.sh || echo "Conversion failed"
```

## REST API (Lambda Function URL)

### Endpoint

```
POST https://your-lambda-url.lambda-url.us-west-2.on.aws/
```

### Authentication

HMAC-SHA256 signature in request headers.

**Required Headers**:
- `X-S2R-Timestamp`: Unix timestamp (float as string)
- `X-S2R-Signature`: Hex-encoded HMAC-SHA256 signature
- `Content-Type`: `text/plain`

**Signature Algorithm**:
```
message = "{timestamp}:{payload}"
signature = HMAC-SHA256(SHARED_SECRET, message)
```

### Request

**Method**: `POST`

**Headers**:
```
X-S2R-Timestamp: 1234567890.123
X-S2R-Signature: a1b2c3d4e5f6...
Content-Type: text/plain
```

**Body**: Raw SLURM script (plain text)

```bash
#!/bin/bash
#SBATCH --job-name=my-job
#SBATCH --gres=gpu:2
python train.py
```

**Constraints**:
- Maximum body size: 50 KB
- Timestamp must be within 5 minutes of current time
- Signature must be valid HMAC-SHA256

### Response

**Success (200 OK)**:
```json
{
  "runai_config": "apiVersion: run.ai/v1\nkind: RunaiJob\nmetadata:\n  name: my-job\n..."
}
```

**Rate Limited (429 Too Many Requests)**:
```json
{
  "error": "Rate limit exceeded: 100 requests per day"
}
```

**Unauthorized (401 Unauthorized)**:
```json
{
  "error": "Invalid signature or expired timestamp"
}
```

**Payload Too Large (413 Payload Too Large)**:
```json
{
  "error": "Payload too large (max 50KB)"
}
```

**Internal Error (500 Internal Server Error)**:
```json
{
  "error": "Bedrock API error: ..."
}
```

### Example with curl

```bash
# Generate signature
python3 -c "
from s2r.auth import create_signed_headers
headers = create_signed_headers('test payload')
for k, v in headers.items():
    print(f'-H \"{k}: {v}\"', end=' ')
"

# Make request
curl -X POST \
  -H "X-S2R-Timestamp: 1234567890.123" \
  -H "X-S2R-Signature: abc123..." \
  -H "Content-Type: text/plain" \
  -d "#!/bin/bash
#SBATCH --gres=gpu:1
python train.py" \
  https://your-lambda-url.lambda-url.us-west-2.on.aws/
```

### Rate Limiting

**Limits**:
- 100 requests per IP address per day (UTC)
- Tracked via DynamoDB table

**Rate Limit Headers** (not currently implemented):
- Future: `X-RateLimit-Limit: 100`
- Future: `X-RateLimit-Remaining: 45`
- Future: `X-RateLimit-Reset: 1234567890`

**Bypassing Rate Limits**:
- Change IP address (not recommended)
- Contact admin to increase limit
- Deploy your own Lambda instance

## Lambda Function API

For direct Lambda invocation (e.g., from another AWS service).

### Event Format

```json
{
  "body": "#!/bin/bash\n#SBATCH --gres=gpu:1\npython train.py",
  "headers": {
    "x-s2r-timestamp": "1234567890.123",
    "x-s2r-signature": "abc123...",
    "content-type": "text/plain"
  },
  "requestContext": {
    "http": {
      "sourceIp": "1.2.3.4"
    }
  }
}
```

### Response Format

Same as REST API response (JSON with `runai_config` or `error` field).

## Configuration

### Environment Variables

**Client**:
- `S2R_API_ENDPOINT`: Lambda Function URL (required)

**Lambda**:
- `SHARED_SECRET`: HMAC signing secret (required)
- `BEDROCK_MODEL_ID`: Bedrock model to use (required)
- `MAX_REQUESTS_PER_IP_PER_DAY`: Rate limit (default: 100)
- `RATE_LIMIT_TABLE`: DynamoDB table name (default: s2r-rate-limits)

### Configuration File (Future)

Not currently supported. Configuration via environment variables only.

**Planned**:
```yaml
# ~/.s2r/config.yaml
api_endpoint: https://xxx.lambda-url.us-west-2.on.aws/
timeout: 60
shared_secret: your-secret-here  # For self-hosted
```

## Error Handling

### Client-Side Errors

```python
from s2r import convert_slurm_to_runai, ConversionError

try:
    config = convert_slurm_to_runai(script)
except ConversionError as e:
    if "Rate limit exceeded" in str(e):
        # Handle rate limiting
        print("Too many requests. Try again tomorrow.")
    elif "403 Forbidden" in str(e):
        # Handle auth error
        print("Permission denied. Check Lambda configuration.")
    elif "timed out" in str(e):
        # Handle timeout
        print("Request timed out. Try a smaller script.")
    else:
        # Generic error
        print(f"Conversion failed: {e}")
```

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Use returned config |
| 401 | Invalid signature | Check shared secret, timestamp |
| 413 | Payload too large | Reduce script size |
| 429 | Rate limited | Wait or request increase |
| 500 | Server error | Check logs, retry later |
| 503 | Service unavailable | Bedrock throttling, retry |

## Usage Examples

### Basic Python Usage

```python
import os
from s2r import convert_slurm_to_runai

# Set endpoint
os.environ['S2R_API_ENDPOINT'] = 'https://xxx.lambda-url.us-west-2.on.aws/'

# Read SLURM script
with open('job.sh', 'r') as f:
    slurm_script = f.read()

# Convert
runai_config = convert_slurm_to_runai(slurm_script)

# Save
with open('job.yaml', 'w') as f:
    f.write(runai_config)
```

### Batch Processing

```python
import os
from pathlib import Path
from s2r import convert_slurm_to_runai, ConversionError

os.environ['S2R_API_ENDPOINT'] = 'https://xxx.lambda-url.us-west-2.on.aws/'

# Convert all SLURM scripts in a directory
slurm_dir = Path('slurm_scripts')
runai_dir = Path('runai_configs')
runai_dir.mkdir(exist_ok=True)

for slurm_file in slurm_dir.glob('*.sh'):
    print(f"Converting {slurm_file.name}...")
    try:
        script = slurm_file.read_text()
        config = convert_slurm_to_runai(script)

        output_file = runai_dir / f"{slurm_file.stem}.yaml"
        output_file.write_text(config)
        print(f"  ✓ Saved to {output_file}")
    except ConversionError as e:
        print(f"  ✗ Failed: {e}")
```

### Custom API Endpoint

```python
from s2r import convert_slurm_to_runai

# Use custom endpoint (self-hosted)
config = convert_slurm_to_runai(
    slurm_script,
    api_endpoint='https://my-lambda.example.com/'
)
```

### CLI with Error Handling

```bash
#!/bin/bash
set -e

export S2R_API_ENDPOINT=https://xxx.lambda-url.us-west-2.on.aws/

if s2r job.sh job.yaml 2>/tmp/error.log; then
    echo "✓ Conversion successful"
    kubectl apply -f job.yaml
else
    echo "✗ Conversion failed:"
    cat /tmp/error.log
    exit 1
fi
```

## Best Practices

1. **Set API endpoint once**: Export `S2R_API_ENDPOINT` in shell profile
2. **Handle rate limits**: Implement retry logic with exponential backoff
3. **Cache conversions**: Save converted configs to avoid repeated calls
4. **Validate SLURM scripts**: Check syntax before converting
5. **Use timeouts**: Set reasonable timeout values (30-60s)
6. **Log errors**: Capture and log ConversionError details
7. **Monitor usage**: Track rate limit consumption
8. **Secure secrets**: Don't hardcode SHARED_SECRET in code
