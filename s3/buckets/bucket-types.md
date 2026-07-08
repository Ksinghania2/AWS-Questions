# Bucket Types and Common Use Cases

S3 buckets are not typed in the traditional sense — every bucket can store any type of object. However, buckets are typically used for specific purposes depending on the workload.

## Common Bucket Use Patterns

### 1. General-Purpose Data Lake Bucket
Stores raw and processed data for analytics, AI/ML, and ETL pipelines.

**Characteristics:**
- Multiple prefixes for logical data organization (`/raw/`, `/processed/`, `/curated/`)
- Often combined with AWS Glue, Athena, and Redshift Spectrum
- Lifecycle policies to transition old data to cheaper storage

```bash
# Create prefixes for data lake organization
aws s3api put-object --bucket my-datalake --key raw/   # Creates "directory" marker
aws s3api put-object --bucket my-datalake --key processed/
aws s3api put-object --bucket my-datalake --key curated/
```

### 2. Static Website Hosting Bucket
Hosts HTML, CSS, JS, and other static assets for public websites.

**Requirements:**
- Enable static website hosting
- Configure index document and error document
- Make objects publicly readable (or use CloudFront + OAI)

```bash
# Enable static website hosting
aws s3api put-bucket-website --bucket my-website-bucket \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"}
  }'

# Make objects public via bucket policy
aws s3api put-bucket-policy --bucket my-website-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-website-bucket/*"
  }]
}'
```

### 3. Backup and Archive Bucket
Stores backups, snapshots, and long-term archives.

**Characteristics:**
- Lifecycle rules to transition to Glacier/Deep Archive
- Often uses versioning and Object Lock for compliance
- May use S3 Replication for off-site backup

```bash
# Upload with storage class for archival
aws s3 cp backup.zip s3://my-archive-bucket/backups/backup-2024.zip \
  --storage-class GLACIER

# Enable versioning for backup protection
aws s3api put-bucket-versioning --bucket my-archive-bucket \
  --versioning-configuration Status=Enabled
```

### 4. Log Storage Bucket
Stores access logs, application logs, and audit trails.

**Characteristics:**
- Often combined with S3 Inventory for auditing
- Lifecycle rules for log rotation
- Server Access Logging enabled

```bash
# Enable server access logging
aws s3api put-bucket-logging --bucket my-app-bucket \
  --bucket-logging-status '{
    "LoggingEnabled": {
      "TargetBucket": "my-log-bucket",
      "TargetPrefix": "s3-access-logs/"
    }
  }'
```

### 5. CloudTrail / Config Bucket
Stores AWS CloudTrail logs or AWS Config history for compliance.

```bash
# Create bucket for CloudTrail logs
aws s3api create-bucket --bucket my-trail-logs --region us-east-1

# Attach policy to allow CloudTrail to write
# (Policy must be configured to allow CloudTrail service principal)
```

### 6. Media/Content Bucket
Stores videos, images, audio files, and other media assets.

**Characteristics:**
- Often uses Transfer Acceleration for fast uploads
- Multipart upload for large files
- Combined with CloudFront for CDN delivery

```bash
# Enable Transfer Acceleration
aws s3api put-bucket-accelerate-configuration \
  --bucket my-media-bucket \
  --accelerate-configuration Status=Enabled

# Upload large file with multipart
aws s3 cp large-video.mp4 s3://my-media-bucket/videos/ \
  --expected-size 1048576000
```

### 7. Cross-Region Replication Destination Bucket
Receives replicated objects from another region for DR or compliance.

**Requirements:**
- Versioning must be enabled
- Appropriate bucket policy to allow replication
- Same bucket name can be used in different regions

```bash
# Enable versioning on destination
aws s3api put-bucket-versioning --bucket my-dr-bucket \
  --versioning-configuration Status=Enabled
```

## Bucket Design Decision Matrix

| Use Case | Versioning | Encryption | Lifecycle | Replication | Public Access |
|---|---|---|---|---|---|
| Data Lake | Optional | SSE-S3/KMS | Yes | Optional | Blocked |
| Static Website | Optional | N/A (public) | Optional | No | Enabled |
| Backup/Archive | Recommended | SSE-KMS | Yes | Recommended | Blocked |
| Log Storage | Recommended | SSE-S3 | Yes | Optional | Blocked |
| CloudTrail | Required | SSE-KMS | Yes | Recommended | Blocked |
| Media Content | Optional | SSE-S3 | Yes | Optional | Via CloudFront |

## Python (boto3) Example - Creating Multiple Bucket Types

```python
import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')

def create_website_bucket(name):
    """Create a bucket configured for static website hosting"""
    s3.create_bucket(Bucket=name)
    
    # Enable website hosting
    s3.put_bucket_website(
        Bucket=name,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}
        }
    )
    
    # Make public
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{name}/*"
        }]
    }
    s3.put_bucket_policy(Bucket=name, Policy=json.dumps(policy))
    
    print(f"Website bucket '{name}' created")
    print(f"URL: http://{name}.s3-website-us-east-1.amazonaws.com")

def create_archive_bucket(name):
    """Create a bucket optimized for archival storage"""
    s3.create_bucket(Bucket=name)
    
    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    
    # Add lifecycle rules for archiving
    lifecycle = {
        'Rules': [
            {
                'ID': 'archive-rule',
                'Status': 'Enabled',
                'Filter': {'Prefix': ''},
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 90, 'StorageClass': 'GLACIER'},
                    {'Days': 365, 'StorageClass': 'DEEP_ARCHIVE'}
                ],
                'Expiration': {'Days': 2555}  # 7 years
            }
        ]
    }
    s3.put_bucket_lifecycle_configuration(
        Bucket=name,
        LifecycleConfiguration=lifecycle
    )
    
    print(f"Archive bucket '{name}' created with lifecycle rules")

# Usage
create_website_bucket('my-docs-site-12345')
create_archive_bucket('my-archive-12345')
```

## Exam Tips
- **S3 has no built-in "bucket types"** — the type is determined by configuration
- A single bucket can serve multiple purposes using **prefixes**
- **Versioning + Lifecycle + Replication** is the gold standard for backup/DR
- **Static website hosting** requires public access (or CloudFront)
- **CloudTrail buckets** must have versioning enabled (requirement)
- **Cross-account access** requires both bucket policy and IAM permissions