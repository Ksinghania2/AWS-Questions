# AWS CLI Configuration Files

The AWS CLI uses configuration files to store credentials and settings.

## File Locations

| File | Path | Purpose |
|---|---|---|
| **Credentials file** | `~/.aws/credentials` | Stores access keys and secret keys |
| **Config file** | `~/.aws/config` | Stores region, output format, and other settings |

## Credentials File (`~/.aws/credentials`)

```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[dev]
aws_access_key_id = AKIAIDEVEXAMPLE
aws_secret_access_key = DevSecretKeyExample123

[prod]
aws_access_key_id = AKIAPRODEXAMPLE
aws_secret_access_key = ProdSecretKeyExample456
```

## Config File (`~/.aws/config`)

```ini
[default]
region = us-east-1
output = json

[profile dev]
region = us-west-2
output = table

[profile prod]
region = eu-west-1
output = json
```

## Named Profiles

Profiles let you use different credentials and settings for different environments.

### Creating a Named Profile

```bash
# Method 1: Interactive setup
aws configure --profile dev

# Method 2: Manual file edit (add to ~/.aws/credentials and ~/.aws/config)
```

### Using Named Profiles

```bash
# Use with a command
aws s3 ls --profile dev

# Set environment variable (for SDKs and tools)
export AWS_PROFILE=dev

# Use default profile (no --profile needed)
aws s3 ls
```

## AWS CLI Configure Commands

```bash
# Interactive configuration
aws configure

# Configure specific profile
aws configure --profile prod

# Set individual values
aws configure set region us-west-2
aws configure set region us-west-2 --profile prod

# Get individual values
aws configure get region
aws configure get region --profile prod

# List profiles
aws configure list-profiles

# List current configuration
aws configure list
```

## AWS CLI Environment Variables

Environment variables override configuration file settings.

| Variable | Description | Example |
|---|---|---|
| `AWS_ACCESS_KEY_ID` | Access key | `export AWS_ACCESS_KEY_ID=AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | Secret key | `export AWS_SECRET_ACCESS_KEY=...` |
| `AWS_SESSION_TOKEN` | Session token (STS) | `export AWS_SESSION_TOKEN=...` |
| `AWS_DEFAULT_REGION` | Default region | `export AWS_DEFAULT_REGION=us-east-1` |
| `AWS_DEFAULT_OUTPUT` | Output format | `export AWS_DEFAULT_OUTPUT=json` |
| `AWS_PROFILE` | Named profile | `export AWS_PROFILE=prod` |
| `AWS_CONFIG_FILE` | Config file path | `export AWS_CONFIG_FILE=/path/to/config` |
| `AWS_CA_BUNDLE` | CA certificate bundle | `export AWS_CA_BUNDLE=/path/to/cert.pem` |
| `AWS_SHARED_CREDENTIALS_FILE` | Credentials file path | `export AWS_SHARED_CREDENTIALS_FILE=/path/to/creds` |

### Credential Precedence (Highest to Lowest)

1. Command-line `--profile` flag
2. Environment variables (`AWS_ACCESS_KEY_ID`, etc.)
3. Credentials file (`~/.aws/credentials`)
4. Config file (`~/.aws/config`)
5. Container credentials (ECS/EKS)
6. EC2 Instance Profile

## AWS CLI Auto-completion

```bash
# Enable auto-completion (bash)
complete -C '/usr/local/bin/aws_completer' aws

# Enable auto-completion (zsh)
source /usr/local/share/zsh/site-functions/_aws

# Make permanent (add to ~/.bashrc or ~/.zshrc)
echo "complete -C '$(which aws_completer)' aws" >> ~/.zshrc
```

## AWS CLI Auto-prompt

Auto-prompt shows your current AWS identity in the terminal prompt.

```bash
# Enable auto-prompt
export AWS_CLI_AUTO_PROMPT=on

# Enable with partial prompts (on-partial)
export AWS_CLI_AUTO_PROMPT=on-partial
```

## Exam Quick Reference

- ✅ `~/.aws/credentials` = access keys
- ✅ `~/.aws/config` = region, output format
- ✅ Named profiles via `[profile name]` in config file
- ✅ Environment variables override config files
- ✅ Credential precedence: CLI flag > Env var > Credentials file > Config file > Container > Instance Profile
- ✅ `aws configure` to set up credentials interactively
- ✅ `aws configure list-profiles` to list all profiles
- ✅ `AWS_PROFILE` env var to switch profiles
- ✅ Auto-completion with `aws_completer`
- ✅ Auto-prompt with `AWS_CLI_AUTO_PROMPT=on`