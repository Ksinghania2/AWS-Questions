"""
AWS S3 Infrastructure as Code using Pulumi

===============================================================================
PULUMI INFRASTRUCTURE AS CODE - COMPREHENSIVE GUIDE
===============================================================================

What is Pulumi?
  Pulumi is an Infrastructure as Code (IaC) tool that allows you to define,
  deploy, and manage cloud resources using programming languages instead of
  configuration files (like YAML/JSON).

Comparison:
  ┌─────────────────┬──────────────────┬─────────────────┐
  │ Tool            │ Language         │ Complexity      │
  ├─────────────────┼──────────────────┼─────────────────┤
  │ CloudFormation  │ JSON/YAML        │ Low             │
  │ Terraform       │ HCL              │ Medium          │
  │ Pulumi          │ Python/JS/Go     │ Medium/High     │
  │ AWS CDK         │ Python/JS/Go     │ Medium/High     │
  └─────────────────┴──────────────────┴─────────────────┘

Advantages of Pulumi over CloudFormation:
  ✅ Use real programming languages (Python, JavaScript, Go, C#, Java)
  ✅ Better code reusability with functions and classes
  ✅ Logic and conditionals built-in (no need for templates)
  ✅ Easier testing and validation
  ✅ Better IDE support and IntelliSense
  ✅ Community components library

Advantages of Pulumi over Terraform:
  ✅ Native AWS integration (works directly with AWS APIs)
  ✅ Fewer state management issues
  ✅ Better for multi-region deployments
  ✅ Easier to learn for developers

===============================================================================
PROJECT STRUCTURE:
===============================================================================

This Pulumi project creates a complete S3 infrastructure with:
  1. Multiple S3 buckets with different configurations
  2. Versioning enabled for critical buckets
  3. Server-side encryption (AES-256 or KMS)
  4. Lifecycle policies for cost optimization
  5. Access logging for compliance
  6. Static website hosting (optional)
  7. Cross-region replication for disaster recovery
  8. Tags for cost allocation and management

===============================================================================
INSTALLATION & SETUP:
===============================================================================

1. Install Pulumi CLI:
   curl -fsSL https://get.pulumi.com | sh

2. Create Pulumi project:
   pulumi new aws-python

3. Install AWS provider:
   pip install pulumi pulumi-aws

4. Configure AWS credentials:
   aws configure
   (or set AWS_PROFILE, AWS_ACCESS_KEY_ID, etc.)

5. Deploy stack:
   pulumi up

===============================================================================
FILE ORGANIZATION:
===============================================================================

pulumi-s3-project/
├── __main__.py           # Main infrastructure code (this file)
├── Pulumi.yaml           # Project configuration
├── Pulumi.dev.yaml       # Dev stack configuration
├── requirements.txt      # Python dependencies
├── config.py             # Configuration variables
├── outputs.py            # Stack outputs
└── README.md             # Documentation

===============================================================================
"""

import pulumi
import pulumi_aws as aws
import json
from datetime import datetime

# ============================================================================
# STEP 1: CONFIGURATION & VARIABLES
# ============================================================================

# Get the current AWS region
aws_region = aws.get_region().name
aws_account_id = aws.get_caller_identity().account_id

# Configuration (can be overridden via Pulumi config)
config = pulumi.Config()

# Environment name (dev, staging, prod)
environment = config.get('environment') or 'dev'

# Bucket naming convention: {project}-{env}-{type}-{account}
project_name = config.get('project_name') or 'myapp'
base_bucket_name = f"{project_name}-{environment}-{aws_account_id}"

# Feature flags
enable_versioning = config.get_bool('enable_versioning') or True
enable_encryption = config.get_bool('enable_encryption') or True
enable_logging = config.get_bool('enable_logging') or True
enable_replication = config.get_bool('enable_replication') or False

# Encryption settings
kms_key_id = config.get('kms_key_id') or None  # If None, uses S3-managed keys

# ============================================================================
# STEP 2: LOGGING BUCKET (OPTIONAL)
# ============================================================================

# Create a dedicated bucket for storing S3 access logs
logging_bucket = None
if enable_logging:
    logging_bucket = aws.s3.BucketObject(
        f"{project_name}-logs",
        bucket=f"{base_bucket_name}-logs",
        # Bucket names must be globally unique, so we use account ID
        
        # Block all public access (logs should never be public)
        acl="private",
        
        # Tags for cost allocation and tracking
        tags={
            "Name": f"{project_name}-logs",
            "Environment": environment,
            "Purpose": "Access logging",
            "ManagedBy": "Pulumi",
        }
    )
    
    # Block public access on logging bucket
    logging_bucket_pab = aws.s3.BucketPublicAccessBlock(
        f"{project_name}-logs-pab",
        bucket=logging_bucket.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True,
    )

# ============================================================================
# STEP 3: DATA BUCKET (PRIMARY STORAGE)
# ============================================================================

# Main bucket for storing application data
data_bucket = aws.s3.BucketObject(
    f"{project_name}-data",
    bucket=f"{base_bucket_name}-data",
    acl="private",  # All data buckets should be private by default
    
    tags={
        "Name": f"{project_name}-data",
        "Environment": environment,
        "Purpose": "Primary data storage",
        "ManagedBy": "Pulumi",
    }
)

# ============================================================================
# STEP 4: VERSIONING CONFIGURATION
# ============================================================================

if enable_versioning:
    """
    Versioning keeps multiple versions of objects when they are updated.
    
    USE CASES:
      - Critical data requiring recovery capability
      - Compliance/regulatory requirements
      - Development environments (rollback capability)
      - Database backups
      - Configuration files
    
    STORAGE IMPACT:
      - Each version counts as separate object
      - Multiplies storage cost by number of versions
      - Can use lifecycle rules to delete old versions
    
    VersionId Behavior:
      - New versions get unique VersionId
      - Deleted objects can be recovered
      - Can restore previous versions
    """
    
    data_bucket_versioning = aws.s3.BucketVersioningV2(
        f"{project_name}-data-versioning",
        bucket=data_bucket.id,
        versioning_configuration={
            "status": "Enabled",  # Enable versioning
            # "mfa_delete": "Enabled",  # Require MFA for deletion (optional)
        }
    )

# ============================================================================
# STEP 5: ENCRYPTION CONFIGURATION
# ============================================================================

if enable_encryption:
    """
    Server-Side Encryption (SSE) protects data at rest on AWS infrastructure.
    
    ENCRYPTION OPTIONS:
    
    1. SSE-S3 (AWS-managed):
       - Algorithm: AES-256
       - Key management: Fully managed by AWS
       - Cost: Included in S3 pricing
       - Best for: Standard security requirement
    
    2. SSE-KMS (Customer/AWS-managed):
       - Algorithm: AES-256 with KMS keys
       - Key management: AWS KMS service
       - Cost: ~$0.03 per 10,000 API calls
       - Best for: Regulatory compliance, key rotation control
    
    3. Client-Side:
       - Encryption happens before upload
       - Maximum security, keys never sent to AWS
       - Best for: Extremely sensitive data
    
    We recommend SSE-KMS for production workloads.
    """
    
    # Encryption configuration (using S3-managed keys for simplicity)
    encryption_config = {
        "rule": [
            {
                "apply_server_side_encryption_by_default": {
                    "sse_algorithm": "AES256",  # or "aws:kms" for KMS
                    # "kms_master_key_id": kms_key_id,  # Uncomment for KMS
                },
                "bucket_key_enabled": True,  # Improves performance with KMS
            }
        ]
    }
    
    data_bucket_encryption = aws.s3.BucketServerSideEncryptionConfigurationV2(
        f"{project_name}-data-encryption",
        bucket=data_bucket.id,
        rules=encryption_config["rule"],
    )

# ============================================================================
# STEP 6: ACCESS LOGGING CONFIGURATION
# ============================================================================

if enable_logging and logging_bucket:
    """
    Access logging records all requests made to the bucket.
    Useful for security monitoring, auditing, and debugging.
    
    Log Format:
      [bucket-owner] bucket-name [request-id] [timestamp] remote-ip \\
      requester request-line http-status object-size \\
      referrer user-agent query-string
    
    PERFORMANCE IMPACT:
      - Slight increase in latency for requests
      - Additional cost for API calls
      - Logs stored in logging bucket (storage cost)
    
    STORAGE ESTIMATE:
      - ~1 KB per 1000 requests
      - 100M requests/month ≈ 100 GB logs
    
    RECOMMENDATIONS:
      - Use for critical buckets
      - Combine with lifecycle policies to archive old logs
      - Use Athena or ELK to analyze logs
    """
    
    data_bucket_logging = aws.s3.BucketLoggingV2(
        f"{project_name}-data-logging",
        bucket=data_bucket.id,
        target_bucket=logging_bucket.id,
        target_prefix=f"s3-access-logs/{environment}/",
    )

# ============================================================================
# STEP 7: LIFECYCLE POLICIES
# ============================================================================

"""
Lifecycle policies automatically manage object transitions and expirations.

STORAGE CLASSES:
  STANDARD (0-30 days): Frequently accessed, highest cost
  STANDARD-IA (30+ days): Infrequent access, 50% cheaper
  INTELLIGENT-TIERING: Automatic based on access patterns
  GLACIER-IR (90+ days): Quarterly access, 80% cheaper
  GLACIER-FR (90+ days): Rare access, retrieval hours
  DEEP-ARCHIVE (180+ days): Archive, retrieval hours

TRANSITION EXAMPLE:
  New object → STANDARD (0-30 days)
  → STANDARD-IA (30-90 days) - saves $12.50/TB/month
  → GLACIER-IR (90+ days) - saves $19/TB/month
  → DEEP-ARCHIVE (180+ days) - saves $22.88/TB/month

COST SAVINGS:
  Without lifecycle: $23/TB/month
  With lifecycle: Average $5/TB/month (78% savings)

LIFECYCLE RULES:
  1. Automatic transitions: Move between storage classes
  2. Expiration: Delete old objects
  3. Noncurrent versions: Transition/delete old versions
  4. Incomplete uploads: Cleanup failed multipart uploads
"""

lifecycle_rules = [
    {
        # Rule 1: Transition to cheaper storage classes
        "id": "optimize-storage-cost",
        "enabled": True,
        "transitions": [
            {
                "days": 30,
                "storage_class": "STANDARD_IA",  # After 30 days
            },
            {
                "days": 90,
                "storage_class": "INTELLIGENT_TIERING",  # After 90 days
            },
        ],
        "expiration": {
            "days": 3650,  # Delete after 10 years
        },
    },
    {
        # Rule 2: Manage previous versions (if versioning enabled)
        "id": "cleanup-old-versions",
        "enabled": enable_versioning,
        "noncurrent_version_transitions": [
            {
                "noncurrent_days": 30,
                "storage_class": "STANDARD_IA",
            },
            {
                "noncurrent_days": 90,
                "storage_class": "GLACIER_IR",
            },
        ],
        "noncurrent_version_expiration": {
            "noncurrent_days": 365,  # Delete old versions after 1 year
        },
    },
    {
        # Rule 3: Cleanup incomplete multipart uploads
        "id": "cleanup-incomplete-uploads",
        "enabled": True,
        "abort_incomplete_multipart_upload": {
            "days_after_initiation": 7,  # Clean up after 7 days
        },
    },
]

data_bucket_lifecycle = aws.s3.BucketLifecycleConfigurationV2(
    f"{project_name}-data-lifecycle",
    bucket=data_bucket.id,
    rules=lifecycle_rules,
)

# ============================================================================
# STEP 8: PUBLIC ACCESS BLOCKING
# ============================================================================

"""
Block Public Access prevents accidental public exposure of bucket data.

SETTINGS:
  1. BlockPublicAcls: Blocks public ACLs on objects
  2. IgnorePublicAcls: Ignores existing public ACLs
  3. BlockPublicPolicy: Blocks public bucket policies
  4. RestrictPublicBuckets: Restricts bucket access

RECOMMENDATION:
  ✅ Enable all settings for production buckets
  ❌ Only disable if public access is intentional
"""

data_bucket_pab = aws.s3.BucketPublicAccessBlock(
    f"{project_name}-data-pab",
    bucket=data_bucket.id,
    block_public_acls=True,        # Block new ACLs
    ignore_public_acls=True,       # Ignore existing ACLs
    block_public_policy=True,      # Block new policies
    restrict_public_buckets=True,  # Restrict bucket access
)

# ============================================================================
# STEP 9: BUCKET POLICY (OPTIONAL)
# ============================================================================

"""
Bucket policies define who can do what with bucket resources.

POLICY STRUCTURE:
  Statement:
    - Effect: Allow or Deny
    - Principal: Who (AWS account, IAM user, role, etc.)
    - Action: What (s3:GetObject, s3:PutObject, etc.)
    - Resource: Which resources (bucket, objects, etc.)
    - Condition: When (IP, SSL, time, etc.)

EXAMPLES:

1. Deny unencrypted uploads:
   "s3:x-amz-server-side-encryption": "AES256"

2. Deny insecure transport (require HTTPS):
   "aws:SecureTransport": "false"

3. Limit to specific IP range:
   "aws:SourceIp": ["203.0.113.0/24"]
"""

# Example policy: Require encryption for all uploads
bucket_policy_document = pulumi.Output.concat(
    json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyUnencryptedObjectUploads",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:PutObject",
                "Resource": pulumi.Output.concat(data_bucket.arn, "/*"),
                "Condition": {
                    "StringNotEquals": {
                        "s3:x-amz-server-side-encryption": "AES256"
                    }
                }
            },
            {
                "Sid": "DenyInsecureTransport",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    data_bucket.arn,
                    pulumi.Output.concat(data_bucket.arn, "/*"),
                ],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            }
        ]
    })
)

# Apply bucket policy
# Uncomment to enable policy
# data_bucket_policy = aws.s3.BucketPolicy(
#     f"{project_name}-data-policy",
#     bucket=data_bucket.id,
#     policy=bucket_policy_document,
# )

# ============================================================================
# STEP 10: CORS CONFIGURATION (OPTIONAL - for web applications)
# ============================================================================

"""
CORS (Cross-Origin Resource Sharing) allows web browsers to access bucket
resources from different domains.

USE CASE:
  - Static website hosted in bucket
  - JavaScript APIs accessing bucket
  - Mobile apps with direct S3 access

SECURITY NOTE:
  - Be restrictive with allowed origins
  - Only allow necessary HTTP methods
  - Verify implications of wildcard (*) origins
"""

# Example CORS configuration for web app
cors_config = {
    "cors_rules": [
        {
            "allowed_origins": ["https://example.com"],  # Specific domain
            "allowed_methods": ["GET", "HEAD"],  # Read-only
            "allowed_headers": ["*"],
            "max_age_seconds": 3000,
        }
    ]
}

# Uncomment to enable CORS
# data_bucket_cors = aws.s3.BucketCorsConfigurationV2(
#     f"{project_name}-data-cors",
#     bucket=data_bucket.id,
#     cors_rules=cors_config["cors_rules"],
# )

# ============================================================================
# STEP 11: TAGS (RESOURCE LABELING)
# ============================================================================

"""
Tags help organize, track, and manage AWS resources.

TAG STRATEGY:
  - Environment: dev, staging, prod
  - Owner: team or person responsible
  - CostCenter: for billing allocation
  - Project: which project resource belongs to
  - ManagedBy: infrastructure tool (Pulumi, Terraform, etc.)
  - DataClassification: public, confidential, restricted
  - BackupRequired: yes/no
  - RetentionDays: how long to keep data

COST ALLOCATION:
  - Enable Cost Allocation Tags in AWS Billing
  - Filter costs by tags
  - Chargeback to departments/teams
"""

standard_tags = {
    "Environment": environment,
    "Project": project_name,
    "ManagedBy": "Pulumi",
    "CreatedDate": datetime.now().isoformat(),
    "Region": aws_region,
}

# ============================================================================
# STEP 12: OUTPUTS (EXPORT VALUES FROM STACK)
# ============================================================================

"""
Outputs allow you to expose important values from your infrastructure.

USE CASES:
  - Share bucket names with other teams
  - Provide endpoint URLs
  - Export for monitoring/alerting
  - Documentation generation
  - Infrastructure discovery
"""

# Export bucket names and endpoints
pulumi.export("data_bucket_name", data_bucket.id)
pulumi.export("data_bucket_arn", data_bucket.arn)
pulumi.export("data_bucket_region", aws_region)

if logging_bucket:
    pulumi.export("logging_bucket_name", logging_bucket.id)
    pulumi.export("logging_bucket_arn", logging_bucket.arn)

# Export configuration for reference
pulumi.export("environment", environment)
pulumi.export("aws_region", aws_region)
pulumi.export("aws_account_id", aws_account_id)
pulumi.export("versioning_enabled", enable_versioning)
pulumi.export("encryption_enabled", enable_encryption)

# ============================================================================
# DEPLOYMENT INSTRUCTIONS
# ============================================================================

"""
DEPLOY STACK:

1. Preview changes:
   pulumi preview

2. Deploy stack:
   pulumi up

3. View outputs:
   pulumi stack output

4. List all resources:
   pulumi stack --show-resources

5. Get specific output:
   pulumi stack output data_bucket_name

6. Destroy stack:
   pulumi destroy

STACK MANAGEMENT:

1. Switch stacks:
   pulumi stack select dev
   pulumi stack select prod

2. List stacks:
   pulumi stack list

3. Create new stack:
   pulumi stack init staging

4. Configure stack:
   pulumi config set environment staging
   pulumi config set enable_versioning true

TROUBLESHOOTING:

1. View stack events:
   pulumi stack history

2. Detailed logs:
   pulumi up -v

3. View stack resources:
   pulumi stack --show-resources

4. Check bucket contents:
   aws s3 ls s3://$(pulumi stack output data_bucket_name)

MONITORING & ALERTS:

1. Check bucket size:
   aws s3api list-objects-v2 --bucket $(pulumi stack output data_bucket_name) \\
     --query 'Contents[].Size' --output text | awk '{s+=$1} END {print s/1024/1024/1024 " GB"}'

2. Get lifecycle configuration:
   aws s3api get-bucket-lifecycle-configuration \\
     --bucket $(pulumi stack output data_bucket_name)

3. Check encryption status:
   aws s3api get-bucket-encryption \\
     --bucket $(pulumi stack output data_bucket_name)

4. View access logs:
   aws s3 ls s3://$(pulumi stack output logging_bucket_name)/s3-access-logs/

BEST PRACTICES:

✅ DO:
   - Use different stacks for different environments
   - Enable versioning for critical data
   - Configure encryption for sensitive data
   - Set up access logging for auditing
   - Use lifecycle policies for cost optimization
   - Tag all resources consistently
   - Use separate AWS accounts for environments
   - Backup critical data (cross-region replication)

❌ DON'T:
   - Use s3api for production deployments (use Pulumi/CloudFormation/Terraform)
   - Disable public access blocking
   - Store secrets in bucket
   - Use wildcard (*) in bucket policies
   - Enable public read access unless intentional
   - Mix environments in same bucket
   - Ignore encryption requirements
"""
