# AWS CLI Setup Guide

This guide walks you through setting up AWS CLI and configuring your environment for working with S3.

## Prerequisites

- AWS account with appropriate permissions
- Python 3.x installed (for CLI v2)

## Step 1: Install AWS CLI

### macOS
```bash
# Download and install AWS CLI v2
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Verify installation
aws --version
# Expected: aws-cli/2.x.x ...
```

### Linux
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Windows (PowerShell)
```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

## Step 2: Configure Credentials

```bash
# Interactive configuration
aws configure

# You'll be prompted for:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json, yaml, text, table)

# Verify configuration
aws sts get-caller-identity
# Expected output (example):
# {
#     "UserId": "AIDA...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

## Step 3: Install Additional Tools

### Install PowerShell (for S3 PowerShell scripts)
```bash
# macOS
brew install --cask powershell

# Linux
# Follow instructions at: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell
```

### Install Terraform (for IaC examples)
```bash
# macOS
brew install terraform

# Linux
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### Install Python dependencies
```bash
pip install boto3  # AWS SDK for Python
pip install cryptography  # For client-side encryption examples
```

## Step 4: Test S3 Access

```bash
# Create a test bucket (use a globally unique name)
aws s3api create-bucket --bucket my-test-bucket-$(date +%s) --region us-east-1

# Upload a file
echo "Hello S3" > test.txt
aws s3 cp test.txt s3://my-test-bucket-1650000000/test.txt

# List bucket contents
aws s3 ls s3://my-test-bucket-1650000000/

# Download the file
aws s3 cp s3://my-test-bucket-1650000000/test.txt ./downloaded.txt

# Cleanup
aws s3 rm s3://my-test-bucket-1650000000/test.txt
aws s3 rb s3://my-test-bucket-1650000000
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|---|---|
| `Unable to locate credentials` | Run `aws configure` first |
| `Access Denied` | Check IAM permissions for S3 |
| `BucketAlreadyExists` | Use a unique bucket name |
| `RequestTimeout` | Check network connectivity |
| `InvalidAccessKeyId` | Regenerate access keys in AWS Console |

### Additional Configuration

```bash
# Use a specific profile
aws s3 ls --profile production

# Set environment variables
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1

# Use MFA
aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/user \
  --token-code 123456

# Configure multiple profiles
aws configure --profile dev
aws configure --profile prod

# List all profiles
aws configure list-profiles
```

## Quick Reference

```bash
# Most common S3 commands
aws s3 ls                          # List buckets
aws s3 ls s3://my-bucket/         # List objects
aws s3 cp file.txt s3://bucket/   # Upload
aws s3 cp s3://bucket/file.txt .  # Download
aws s3 sync ./dir s3://bucket/    # Sync directory
aws s3 rm s3://bucket/file.txt    # Delete
aws s3 rb s3://bucket             # Delete bucket

# S3 API commands (more control)
aws s3api create-bucket --bucket my-bucket
aws s3api put-object --bucket my-bucket --key hello.txt --body hello.txt
aws s3api get-object --bucket my-bucket --key hello.txt output.txt
aws s3api list-objects-v2 --bucket my-bucket