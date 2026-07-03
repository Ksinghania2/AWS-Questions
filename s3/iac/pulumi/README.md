# AWS S3 Infrastructure as Code with Pulumi

## Complete Guide to Infrastructure Management

This project demonstrates enterprise-grade S3 bucket management using Pulumi, including comprehensive documentation on Pulumi concepts and best practices.

---

## 📚 Table of Contents

1. [What is Pulumi?](#what-is-pulumi)
2. [Pulumi vs. Other Tools](#pulumi-vs-other-tools)
3. [Project Structure](#project-structure)
4. [Installation & Setup](#installation--setup)
5. [Configuration](#configuration)
6. [Deployment](#deployment)
7. [Stack Management](#stack-management)
8. [Outputs & Exports](#outputs--exports)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## What is Pulumi?

### Overview
Pulumi is an Infrastructure as Code (IaC) tool that allows you to define, deploy, and manage cloud resources using **real programming languages** instead of configuration files or custom DSLs.

### Supported Languages
- **Python** ← This project uses Python
- **JavaScript/TypeScript**
- **Go**
- **C#/.NET**
- **Java**

### Key Concepts

#### Stack
A stack is an instance of your Pulumi program. Think of it as an environment:
- `dev` - Development environment
- `staging` - Staging/QA environment
- `prod` - Production environment

Each stack can have different configurations and deployments.

#### Resource
A resource is a cloud entity managed by Pulumi:
```python
s3_bucket = aws.s3.BucketObject("my-bucket", bucket="my-bucket-name")
```

#### Output
Outputs export values from your stack for use by other systems:
```python
pulumi.export("bucket_name", s3_bucket.id)
```

#### Config
Configuration values that can differ per stack:
```python
config = pulumi.Config()
environment = config.get('environment') or 'dev'
```

---

## Pulumi vs. Other Tools

### Comparison Matrix

| Feature | Pulumi | Terraform | CloudFormation | AWS CDK |
|---------|--------|-----------|----------------|---------|
| Language | Python/JS/Go | HCL | JSON/YAML | Python/JS/Go |
| State Management | Built-in | Manual | Built-in | Built-in |
| Learning Curve | Medium | Medium | Low | High |
| IDE Support | Excellent | Good | Poor | Good |
| Testing | Easy | Moderate | Difficult | Easy |
| Debugging | Good | Good | Poor | Good |
| Multi-Cloud | No* | Yes | No | No |
| Cost | Free | Free | Free | Free |
| Community | Growing | Large | Large | Growing |

*Pulumi supports AWS, Azure, Google Cloud, Kubernetes

### When to Use Pulumi

#### ✅ Use Pulumi When:
- You want to use programming languages for infrastructure
- You need complex logic (loops, conditions, functions)
- You're in an AWS-heavy organization
- You want better IDE support and testing
- Your team has programming expertise
- You need code reusability and abstraction
- You prefer Python/JavaScript/Go over HCL

#### ❌ Don't Use Pulumi When:
- You need multi-cloud support
- You have large Terraform codebase
- Your team only knows declarative languages
- You need the largest community (Terraform)
- You're migrating from CloudFormation

---

## Project Structure

```
s3/iac/pulumi/
├── __main__.py                 # Main infrastructure code
├── Pulumi.yaml                 # Project metadata & default config
├── Pulumi.dev.yaml             # Dev stack configuration
├── Pulumi.prod.yaml            # Prod stack configuration (create if needed)
├── requirements.txt            # Python dependencies
├── venv/                        # Virtual environment (after setup)
└── README.md                    # This file

Pulumi.dev.yaml (Dev Stack):
├── aws:region: us-east-1
├── project_name: myapp
├── environment: dev
├── enable_versioning: true
└── enable_encryption: true

Pulumi.prod.yaml (Prod Stack - Example):
├── aws:region: us-west-2
├── project_name: myapp
├── environment: prod
├── enable_versioning: true
├── enable_encryption: true
└── kms_key_id: arn:aws:kms:...
```

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- AWS CLI configured
- AWS credentials with S3 permissions
- Git (recommended)

### Step 1: Install Pulumi CLI

**macOS (Homebrew):**
```bash
brew install pulumi
```

**Linux:**
```bash
curl -fsSL https://get.pulumi.com | sh
# Add to PATH: export PATH=$HOME/.pulumi/bin:$PATH
```

**Windows (Chocolatey):**
```bash
choco install pulumi
```

**Verify Installation:**
```bash
pulumi version
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure AWS Credentials

```bash
# Use AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

### Step 4: Create Pulumi Account (Optional)

```bash
pulumi login
# Follow prompts to create free account
# Or use local file backend:
pulumi login --local
```

### Step 5: Select/Create Stack

```bash
# List available stacks
pulumi stack list

# Select dev stack
pulumi stack select dev

# Or create new stack
pulumi stack init staging
```

---

## Configuration

### Configuration Methods

#### Method 1: Command Line

```bash
# Set configuration value
pulumi config set project_name myapp

# Set boolean value
pulumi config set enable_versioning true

# Set for specific stack
pulumi config set --stack dev environment dev
```

#### Method 2: Pulumi.yaml Files

Edit `Pulumi.dev.yaml`:
```yaml
aws:region: us-east-1
project_name: myapp
environment: dev
enable_versioning: true
enable_encryption: true
enable_logging: true
```

#### Method 3: Environment Variables

```bash
export PULUMI_AWS_REGION=us-west-2
export PULUMI_CONFIG_PASSPHRASE=yourpassphrase
```

### Reading Configuration in Code

```python
config = pulumi.Config()

# Get string value with default
project_name = config.get('project_name') or 'myapp'

# Get boolean value
enable_versioning = config.get_bool('enable_versioning') or True

# Get required value (fails if not set)
kms_key_id = config.require('kms_key_id')

# Get nested value from AWS provider
aws_region = aws.get_region().name
```

### Configuration Per Stack

Create stack-specific files:

**Pulumi.dev.yaml** - Development
```yaml
aws:region: us-east-1
environment: dev
enable_logging: true
enable_replication: false
```

**Pulumi.prod.yaml** - Production
```yaml
aws:region: us-east-1
environment: prod
enable_logging: true
enable_replication: true
kms_key_id: arn:aws:kms:us-east-1:123456789:key/12345678-1234-1234-1234-123456789012
```

---

## Deployment

### Preview Changes

Before deploying, see what resources will be created/modified:

```bash
# Preview changes
pulumi preview

# Detailed preview
pulumi preview -v

# Save preview for review
pulumi preview --json > preview.json
```

### Deploy Stack

```bash
# Deploy interactively (prompts before changes)
pulumi up

# Deploy without prompts (useful for CI/CD)
pulumi up --yes

# Deploy with specific stack
pulumi up --stack dev

# Deploy with configuration override
pulumi up -c aws:region=us-west-2
```

### Monitor Deployment

```bash
# Watch resources as they're created
pulumi up --show-resources

# Follow logs
pulumi up -v

# Get live stack outputs
pulumi stack output
```

### Destroy Infrastructure

```bash
# Interactive destruction
pulumi destroy

# Force destruction without prompts
pulumi destroy --yes

# Destroy specific resource
pulumi destroy --target urn:pulumi:...
```

---

## Stack Management

### List Stacks

```bash
# List all stacks for current project
pulumi stack list

# Select a stack
pulumi stack select dev

# Show current stack
pulumi stack

# Detailed stack info
pulumi stack --show-resources
```

### Create New Stack

```bash
# Create and select new stack
pulumi stack init production

# Switch to stack
pulumi stack select production

# Configure stack
pulumi config set environment prod
pulumi config set enable_replication true
```

### Stack History

```bash
# View deployment history
pulumi stack history

# Show specific version
pulumi stack history -v

# Rollback to previous version
pulumi stack export | pulumi stack import  # Export/import states
```

---

## Outputs & Exports

### Exporting Values

```python
# Export bucket name
pulumi.export("data_bucket_name", data_bucket.id)

# Export bucket ARN
pulumi.export("data_bucket_arn", data_bucket.arn)

# Export configuration
pulumi.export("environment", environment)
```

### Accessing Outputs

```bash
# Get all outputs
pulumi stack output

# Get specific output
pulumi stack output data_bucket_name

# Get output as JSON
pulumi stack output --json

# Get in JSON format and filter
pulumi stack output --json | jq '.data_bucket_name.value'
```

### Using Outputs in Scripts

```bash
# Store output in variable
BUCKET_NAME=$(pulumi stack output data_bucket_name)

# Use in AWS CLI
aws s3 ls s3://$BUCKET_NAME

# Pass to other tools
aws s3 sync ./local s3://$BUCKET_NAME
```

---

## Best Practices

### 1. **Version Control**

```bash
# Add to .gitignore
Pulumi.prod.yaml       # Prod config (use manual/secrets management)
*.key                  # Encryption keys
__pycache__/          # Python cache
.pulumi/              # Pulumi state files
venv/                 # Virtual environment
```

### 2. **Stack Organization**

```
Project Structure:
pulumi-project/
├── dev/              # Dev stack
├── staging/          # Staging stack
├── prod/             # Prod stack (restricted access)
└── shared/           # Shared resources
```

### 3. **Configuration Management**

```python
# Use config for differences between stacks
config = pulumi.Config()

# Not this (hardcoded):
bucket_name = "my-prod-bucket"

# Do this (configurable):
environment = config.get('environment') or 'dev'
bucket_name = f"my-{environment}-bucket"
```

### 4. **Resource Tagging**

```python
# Define standard tags
standard_tags = {
    "Environment": environment,
    "Project": project_name,
    "ManagedBy": "Pulumi",
    "CreatedDate": datetime.now().isoformat(),
}

# Apply to all resources
resource = aws.s3.BucketObject(
    "my-bucket",
    bucket="my-bucket",
    tags=standard_tags
)
```

### 5. **Error Handling**

```python
# Check configuration exists
try:
    kms_key_id = config.require('kms_key_id')
except pulumi.automation.CommandError:
    pulumi.error("kms_key_id must be configured for encryption")

# Conditional resource creation
if environment == "prod":
    enable_replication = True
else:
    enable_replication = False
```

### 6. **Code Organization**

Instead of one large file, organize code:

```
├── __main__.py           # Main entry point
├── s3.py                 # S3 bucket configurations
├── networking.py         # VPC and networking
├── iam.py               # IAM roles and policies
├── monitoring.py        # CloudWatch alarms
└── config.py            # Shared configuration
```

### 7. **Testing**

```python
# Pulumi allows Python unit tests
import unittest
import pulumi

class S3Tests(unittest.TestCase):
    def test_bucket_name_format(self):
        # Verify bucket naming convention
        self.assertTrue(bucket_name.startswith("my-"))
    
    def test_versioning_enabled(self):
        # Verify versioning is configured
        self.assertEqual(versioning_status, "Enabled")
```

### 8. **Documentation**

```python
# Add comments explaining why, not what
def create_bucket():
    """
    Create S3 bucket with encryption.
    
    Encryption required for compliance with SOC2.
    Uses AES-256 (S3-managed) for cost efficiency.
    """
    # Implementation
```

### 9. **Secrets Management**

```bash
# Set encrypted secrets
pulumi config set --secret db_password "mypassword"

# Use secrets in code
config = pulumi.Config()
db_password = config.require_secret('db_password')

# Secret values never appear in output
pulumi stack output  # Shows "[secret]" for secrets
```

### 10. **CI/CD Integration**

```bash
# GitHub Actions example
- name: Deploy with Pulumi
  run: |
    pulumi login --local
    pulumi stack select prod
    pulumi up --yes
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "error: failed to decrypt configuration"

```bash
# Solution: Set passphrase
export PULUMI_CONFIG_PASSPHRASE="your_passphrase"

# Or remove encryption for local backend
pulumi login --local
```

#### Issue 2: "error: permission denied" for S3 operations

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check IAM permissions
aws iam get-user
aws iam list-attached-user-policies --user-name your-user
```

#### Issue 3: "error: resource already exists"

```bash
# Check if bucket already exists
aws s3 ls

# Import existing resource
pulumi import aws:s3:BucketObject my-bucket existing-bucket-name

# Or destroy and recreate
pulumi destroy
pulumi up
```

#### Issue 4: Preview hangs or takes too long

```bash
# Cancel preview
Ctrl+C

# Try with fewer resources or refresh
pulumi preview --refresh=false
```

#### Issue 5: Stack conflicts or lock files

```bash
# Force unlock stack
pulumi stack select dev
pulumi cancel

# Or use local backend
pulumi login --local
```

### Debugging

```bash
# Verbose output
pulumi up -v

# Debug-level logging
PULUMI_LOG_LEVEL=debug pulumi up

# View resource IDs
pulumi stack -v

# Show resource dependencies
pulumi stack graph

# Export stack state
pulumi stack export > state.json

# Import state
pulumi stack import < state.json
```

### Getting Help

```bash
# View documentation
pulumi help
pulumi help up
pulumi help config

# Check Pulumi logs
cat ~/.pulumi/logs/*.log

# Visit Pulumi documentation
https://www.pulumi.com/docs/

# Community discussion
https://pulumi.slack.com
```

---

## Advanced Topics

### Cross-Stack References

```python
# Stack A: Create resource
bucket = aws.s3.BucketObject("my-bucket", bucket="my-bucket")
pulumi.export("bucket_name", bucket.id)

# Stack B: Reference from another stack
other_stack = pulumi.automation.select_stack("other-stack")
bucket_name = other_stack.get_output("bucket_name")
```

### Automation API

```python
# Programmatically deploy stacks
import pulumi.automation as auto

def create_stack(stack_name):
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name="my-project",
        program=pulumi_program
    )
    
    up_result = stack.up()
    return up_result.outputs
```

### Custom Providers

Create reusable components:

```python
class S3WithLogging:
    def __init__(self, name, bucket_name, log_bucket):
        self.bucket = aws.s3.BucketObject(name, bucket=bucket_name)
        self.logging = aws.s3.BucketLoggingV2(
            f"{name}-logging",
            bucket=self.bucket.id,
            target_bucket=log_bucket
        )
```

---

## Summary

Pulumi provides a modern approach to infrastructure management by leveraging programming languages. This project demonstrates:

✅ **S3 Bucket Management**: Creation, versioning, encryption, lifecycle policies
✅ **Configuration Management**: Per-stack configuration using YAML
✅ **Infrastructure as Code**: Programmatic, testable infrastructure
✅ **Best Practices**: Tagging, security, organization
✅ **Production-Ready**: Suitable for enterprise deployments

For more information, visit [Pulumi Documentation](https://www.pulumi.com/docs/).
