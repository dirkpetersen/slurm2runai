#!/bin/bash
# Quick deployment script for Lambda function

set -e

echo "Building Lambda function..."
sam build

echo "Deploying Lambda function..."
sam deploy "$@"

echo ""
echo "Deployment complete!"
echo "Don't forget to:"
echo "1. Copy the Function URL from the outputs above"
echo "2. Set S2R_API_ENDPOINT environment variable"
echo "3. Update SHARED_SECRET in both s2r/auth.py and Lambda environment"
