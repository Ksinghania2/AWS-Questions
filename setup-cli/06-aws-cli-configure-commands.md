# AWS CLI Configure Commands

The `aws configure` command is the primary way to set up AWS CLI credentials and settings. This guide covers all configure commands and their variations.

## Basic Configure Commands

### Initial Setup
```bash
# Interactive setup - prompts for all values
aws configure
# AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name [None]: us-east-1
# Default output format [None]: json
```

### Non-Interactive Setup
```bash
# Set credentials inline
aws configure set aws_access_key_id AKIAIOSFODNN7EXAMPLE
aws configure set aws_secret_access_key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
aws configure set region us-east-1
aws configure set output json
```

## Profile-Specific Configure Commands

### Create/Modify Profile
```bash
# Interactive profile creation
aws configure --profile dev

# Set specific values for a profile
aws configure set region us-west-2 --profile dev
aws configure set output table --profile dev
```

## List and View Configuration

```bash
# List all configuration values for current profile
aws configure list

# List values for specific profile
aws configure list --profile dev

# Get a specific value
aws configure get region
aws configure get aws_access_key_id --profile dev

# List all profiles
aws configure list-profiles
```

## Advanced Configure Commands

### Set Nested Config Values
```bash
# Set S3-specific configuration
aws configure set s3.max_concurrent_requests 20
aws configure set s3.max_queue_size 10000
aws configure set s3.multipart_threshold 64MB
aws configure set s3.use_accelerate_endpoint true

# Set CLI-specific settings
aws configure set cli_follow_urlparam false
aws configure set cli_timestamp_format iso8601
aws configure set cli_history enabled

# Set retry behavior
aws configure set max_attempts 5
aws configure set retry_mode adaptive
```

### Configure MFA and Role Assumption
```bash
# Set up a profile that assumes a role with MFA
aws configure set role_arn arn:aws:iam::123456789012:role/Admin --profile admin
aws configure set source_profile default --profile admin
aws configure set mfa_serial arn:aws:iam::987654321098:mfa/admin-user --profile admin
```

## Config File Manipulation

### View Raw Config Files
```bash
# View credentials file
cat ~/.aws/credentials

# View config file
cat ~/.aws/config

# View specific section
grep -A 3 '\[profile dev\]' ~/.aws/config
```

### Direct File Editing
```bash
# Append to credentials file
echo -e "\n[dev]\naws_access_key_id = AKIA...\naws_secret_access_key = secret..." >> ~/.aws/credentials

# Edit config file with sed (macOS/Linux)
sed -i '' 's/region = us-east-1/region = eu-west-1/' ~/.aws/config
```

## Configure Get Command Options

```bash
# Get with default value
aws configure get region || echo "us-east-1"

# Get from specific section
aws configure get default.region

# Get nested config values
aws configure get s3.max_concurrent_requests
```

## Importing Existing Credentials

```bash
# Import from CSV (AWS console download)
# Format: User name,Access key ID,Secret access key
csv_file="credentials.csv"
access_key=$(tail -1 "$csv_file" | cut -d',' -f2)
secret_key=$(tail -1 "$csv_file" | cut -d',' -f3)
aws configure set aws_access_key_id "$access_key"
aws configure set aws_secret_access_key "$secret_key"
```

## Configure Complete Command Reference

| Command | Description |
|---------|-------------|
| `aws configure` | Interactive setup |
| `aws configure list` | Show current configuration |
| `aws configure get` | Get a configuration value |
| `aws configure set` | Set a configuration value |
| `aws configure list-profiles` | List all named profiles |
| `aws configure import` | Import credentials from CSV |
| `aws configure --profile` | Work with named profile |
| `aws configure --json` | Output in JSON format |

## Bash Script for Automated Setup

```bash
#!/bin/bash
# aws-configure-automated.sh
# Automates AWS CLI configuration for multiple environments

configure_profile() {
    local profile=$1
    local region=$2
    local access_key=$3
    local secret_key=$4
    
    echo "Configuring profile: $profile"
    
    aws configure set aws_access_key_id "$access_key" --profile "$profile"
    aws configure set aws_secret_access_key "$secret_key" --profile "$profile"
    aws configure set region "$region" --profile "$profile"
    aws configure set output json --profile "$profile"
    
    echo "Profile $profile configured successfully"
    
    # Verify configuration
    aws sts get-caller-identity --profile "$profile"
}

# Usage
configure_profile "dev" "us-east-1" "AKIA..." "secret..."
configure_profile "prod" "us-west-2" "AKIA..." "secret..."
```

## Exam Tips

- ✅ `aws configure` stores credentials in `~/.aws/credentials` and config in `~/.aws/config`
- ✅ `aws configure set` can modify any config value including nested S3/CLI settings
- ✅ `aws configure get` retrieves values; returns nothing if key doesn't exist
- ✅ `--profile` flag works with all configure subcommands
- ✅ Configuration files are **plain text** - secure them appropriately
- ✅ `aws configure list` does NOT display secret keys for security
- ✅ `max_attempts` and `retry_mode` are important for resilient scripting

## Q&A

**Q1: What files does `aws configure` modify?**
A: `~/.aws/credentials` (access keys) and `~/.aws/config` (region, output, settings).

**Q2: How do you list all configured named profiles?**
A: `aws configure list-profiles`

**Q3: How do you set the region without interactive prompts?**
A: `aws configure set region us-east-1`

**Q4: How do you import credentials from a CSV file?**
A: Parse the CSV and use `aws configure set aws_access_key_id` and `aws configure set aws_secret_access_key`.

**Q5: What command shows current configuration without showing secrets?**
A: `aws configure list`

**Q6: How do you configure S3-specific CLI settings?**
A: `aws configure set s3.max_concurrent_requests 20`

**Q7: How do you set up MFA for a named profile?**
A: Set `mfa_serial`, `role_arn`, and `source_profile` with `aws configure set` commands.

**Q8: Is there a way to test the configuration immediately after setting it?**
A: Yes, run `aws sts get-caller-identity` to verify the credentials work.