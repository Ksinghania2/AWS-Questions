# AWS CLI Named Profiles

Named profiles allow you to manage multiple AWS configurations from a single machine, switching between accounts/regions easily.

## What Are Named Profiles?

A named profile is a collection of settings (credentials, region, output format) stored under a profile name in the AWS CLI config files.

## Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| **Credentials File** | `~/.aws/credentials` | Stores access key ID and secret access key |
| **Config File** | `~/.aws/config` | Stores region, output format, and profile-specific settings |

## Creating Named Profiles

### Method 1: `aws configure --profile`

```bash
# Create a profile named "dev"
aws configure --profile dev
# AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name [None]: us-east-1
# Default output format [None]: json
```

### Method 2: Manual Edit

```bash
# Edit ~/.aws/credentials
cat >> ~/.aws/credentials << 'EOF'
[dev]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[prod]
aws_access_key_id = AKIAIPRODEXAMPLE
aws_secret_access_key = ProdSecretKeyEXAMPLE
EOF

# Edit ~/.aws/config
cat >> ~/.aws/config << 'EOF'
[profile dev]
region = us-east-1
output = json

[profile prod]
region = us-west-2
output = json
EOF
```

## Using Named Profiles

```bash
# Use a specific profile
aws s3 ls --profile dev

# Set environment variable to use a profile
export AWS_PROFILE=dev
aws s3 ls  # Uses dev profile

# Override profile for a single command
AWS_PROFILE=prod aws ec2 describe-instances
```

## Profile Inheritance (Source Profile)

```bash
# ~/.aws/config
[profile dev]
region = us-east-1
role_arn = arn:aws:iam::123456789012:role/Developer
source_profile = dev-user

[profile dev-user]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

## Listing Profiles

```bash
# List all profiles
aws configure list-profiles

# View current profile details
aws configure list

# View specific profile
aws configure list --profile dev
```

## CLI Examples

```bash
# Create multiple profiles for different environments
aws configure --profile development
aws configure --profile staging
aws configure --profile production

# Use different profiles for different services
aws s3 ls --profile development
aws ec2 describe-instances --profile production --region eu-west-1

# Copy profile configuration
aws configure --profile dev-backup
# Enter same credentials as dev
```

## Exam Tips

- ✅ **Default profile**: Used when no `--profile` flag or `AWS_PROFILE` env var is set
- ✅ **Profile names**: Case-sensitive, stored in `[profile name]` format in config file
- ✅ **Source profile**: Used for role assumption (chained authentication)
- ✅ **Best practice**: Use separate profiles for each environment/account
- ✅ **Security**: Never commit credentials file to version control
- ✅ **MFA**: Profiles can be configured to require MFA for role assumption

## Q&A

**Q1: How do you switch between AWS accounts using CLI?**
A: Use named profiles with `--profile` flag or set `AWS_PROFILE` environment variable.

**Q2: What is the difference between `~/.aws/credentials` and `~/.aws/config`?**
A: Credentials file stores access keys; config file stores region, output format, and profile settings.

**Q3: Can a named profile assume a role from another profile?**
A: Yes, using `source_profile` and `role_arn` in the config file.

**Q4: How do you list all configured profiles?**
A: `aws configure list-profiles`

**Q5: What happens if you don't specify a profile?**
A: The `[default]` profile is used automatically.

**Q6: Can you have multiple profiles with the same region?**
A: Yes, profiles are independent and can share the same region.

**Q7: How do you set a profile for all commands in a session?**
A: Export `AWS_PROFILE=profile-name` environment variable.