# AWS CLI Environment Variables

Environment variables override settings in config/credentials files and profiles. They're essential for CI/CD pipelines, Docker containers, and temporary configuration changes.

## Priority Order (Highest to Lowest)

1. **Command-line flags** (e.g., `--region`, `--profile`)
2. **Environment variables**
3. **CLI configuration file** (`~/.aws/config`)
4. **CLI credentials file** (`~/.aws/credentials`)

## Core Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `AWS_ACCESS_KEY_ID` | IAM access key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_SESSION_TOKEN` | STS temporary session token | `IQoJb3JpZ2luX2Vj...` |
| `AWS_DEFAULT_REGION` | Default region | `us-east-1` |
| `AWS_DEFAULT_OUTPUT` | Output format | `json` / `table` / `text` |
| `AWS_PROFILE` | Named profile to use | `dev` |
| `AWS_CONFIG_FILE` | Custom config file path | `/path/to/config` |
| `AWS_SHARED_CREDENTIALS_FILE` | Custom credentials file path | `/path/to/credentials` |
| `AWS_CA_BUNDLE` | CA certificate bundle path | `/etc/certs/ca-bundle.crt` |
| `AWS_METADATA_SERVICE_TIMEOUT` | IMDS timeout in seconds | `5` |
| `AWS_METADATA_SERVICE_NUM_ATTEMPTS` | IMDS retry count | `3` |

## Common Usage Patterns

### Basic Authentication
```bash
# Set credentials as environment variables
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1

# Run commands
aws s3 ls
aws ec2 describe-instances
```

### Using Profiles
```bash
# Switch profiles by changing environment variable
export AWS_PROFILE=production
aws s3 ls  # Uses production profile

# Unset to revert to default
unset AWS_PROFILE
```

### Temporary Credentials (STS)
```bash
# Assume role and set temporary credentials
credentials=$(aws sts assume-role \
  --role-arn "arn:aws:iam::123456789012:role/MyRole" \
  --role-session-name "MySession" \
  --query 'Credentials' \
  --output text)

export AWS_ACCESS_KEY_ID=$(echo $credentials | awk '{print $1}')
export AWS_SECRET_ACCESS_KEY=$(echo $credentials | awk '{print $2}')
export AWS_SESSION_TOKEN=$(echo $credentials | awk '{print $3}')

# Now all commands use the assumed role
aws s3 ls
```

### CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- name: Deploy to S3
  run: aws s3 sync ./dist s3://my-bucket/
```

### Custom Config File Location
```bash
# Use a project-specific config file
export AWS_CONFIG_FILE=./.aws-config
export AWS_SHARED_CREDENTIALS_FILE=./.aws-credentials

aws s3 ls
```

## Docker Usage
```bash
# Pass environment variables to Docker container
docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
           -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
           -e AWS_DEFAULT_REGION=us-east-1 \
           amazon/aws-cli s3 ls
```

## Security Best Practices
```bash
# NEVER hardcode credentials in scripts
# BAD: Hardcoded
AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"  # Don't do this!

# GOOD: Use environment variables or IAM roles
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile prod)

# Use aws sts get-caller-identity to verify
aws sts get-caller-identity
```

## Exam Tips

- ✅ **Environment variables override config files** but not command-line flags
- ✅ `AWS_PROFILE` is the easiest way to switch between accounts
- ✅ `AWS_SESSION_TOKEN` is **required** when using temporary credentials (STS)
- ✅ In EC2, prefer **IAM roles** over environment variables
- ✅ **AWS_DEFAULT_REGION** and **AWS_REGION** both work (DEFAULT_REGION takes precedence)
- ✅ Environment variables are **session-only** - lost when terminal closes

## Q&A

**Q1: What is the priority order for AWS CLI credential resolution?**
A: CLI flags > Environment variables > Config file > Credentials file

**Q2: How do you switch AWS profiles without editing files?**
A: Set `AWS_PROFILE=profile-name` environment variable.

**Q3: What environment variable is required with STS temporary credentials?**
A: `AWS_SESSION_TOKEN` alongside `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

**Q4: Can you use a custom credentials file path?**
A: Yes, set `AWS_SHARED_CREDENTIALS_FILE` to the custom path.

**Q5: What's the difference between `AWS_DEFAULT_REGION` and `AWS_REGION`?**
A: Both work; `AWS_DEFAULT_REGION` is preferred by AWS CLI v2.

**Q6: How do you verify which credentials are currently active?**
A: Run `aws sts get-caller-identity` to show the active identity.

**Q7: Why should EC2 instances use IAM roles instead of environment variables?**
A: Roles are more secure (no hardcoded keys), automatically rotate credentials, and are easier to manage at scale.

**Q8: What happens if you set both `AWS_PROFILE` and `AWS_ACCESS_KEY_ID`?**
A: The explicit environment variables (`AWS_ACCESS_KEY_ID`) take precedence over the profile.