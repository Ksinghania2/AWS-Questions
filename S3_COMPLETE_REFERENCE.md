# AWS S3 Complete Reference Guide

## Table of Contents
1. [S3 Bucket Basics](#s3-bucket-basics)
2. [Bucket Naming Rules](#bucket-naming-rules)
3. [Bucket Restrictions](#bucket-restrictions)
4. [Bucket Types & Storage Classes](#bucket-types--storage-classes)
5. [Bucket Organization (Folders)](#bucket-organization-folders)
6. [Versioning](#versioning)
7. [Encryption](#encryption)
8. [Static Website Hosting](#static-website-hosting)
9. [Access Control](#access-control)
10. [Performance & Optimization](#performance--optimization)
11. [Compliance & Durability](#compliance--durability)

---

## S3 Bucket Basics

### What is Amazon S3?
Amazon Simple Storage Service (S3) is an object storage service that offers industry-leading scalability, data availability, security, and performance.

### Key Characteristics:
- **Object Storage**: Stores data as objects (files) in containers (buckets)
- **Globally Distributed**: Available in multiple AWS regions worldwide
- **Unlimited Scalability**: Scale from KB to TB without provisioning
- **99.999999999% (11 9s) Durability**: Data is automatically replicated across availability zones
- **Highly Available**: 99.99% uptime SLA in most regions

### S3 Concepts:
| Term | Definition |
|------|-----------|
| **Bucket** | Container for objects; must have globally unique name |
| **Object** | File stored in S3; identified by key (name) |
| **Key** | Unique identifier for an object within a bucket |
| **Region** | Geographic location where bucket is created; determines latency & cost |
| **ETag** | Entity Tag; unique identifier for object version |
| **ACL** | Access Control List; legacy permission model |
| **Bucket Policy** | JSON document defining bucket-level permissions |

---

## Bucket Naming Rules

### Mandatory Rules:
1. **Length**: 3-63 characters
2. **Characters**: Lowercase letters (a-z), numbers (0-9), hyphens (-) only
3. **Start & End**: Must begin and end with letter or number (not hyphen)
4. **No IP Format**: Cannot be formatted like IP address (e.g., 192.168.1.1)
5. **Global Uniqueness**: Name must be unique across ALL AWS accounts and regions
6. **No Underscores**: Cannot contain underscores (_)
7. **No Uppercase**: All characters must be lowercase

### Valid Examples:
```
my-data-bucket
company-documents-2024
archive-v3
s3bucket123
```

### Invalid Examples:
```
My-Bucket              ❌ Contains uppercase
my_bucket              ❌ Contains underscores
my--bucket             ❌ Consecutive hyphens OK, but bad practice
-myBucket              ❌ Starts with hyphen
bucket-               ❌ Ends with hyphen
192.168.1.1            ❌ Looks like IP address
ab                     ❌ Only 2 characters (minimum 3)
```

### Naming Best Practices:
- Use descriptive names that indicate purpose
- Include date or version in name
- Use lowercase consistently
- Avoid special characters except hyphens
- Make names easy to type and remember

---

## Bucket Restrictions

### Regional Constraints:
- **Default Region**: us-east-1 (Northern Virginia)
- **Region Specific**: Each bucket belongs to one region
- **Cross-Region Transfer**: Data can be replicated between regions (Cross-Region Replication)
- **Latency**: Choose region close to your application/users

### Size & Quota Limitations:
| Limitation | Value |
|-----------|-------|
| **Object Size** | 0 bytes to 5 TB |
| **Upload Size** | Single PUT max 5 GB |
| **Multipart Upload** | Can upload 5 TB in parts |
| **Maximum Bucket Count** | 100 per account (can request increase) |
| **Key Length** | 1024 UTF-8 bytes maximum |
| **Bucket Tags** | 50 tags maximum per bucket |

### Request Rate Limits:
- **Original Limitation**: 3,500 PUT/COPY/POST/DELETE and 5,500 GET requests per second
- **Modern S3**: Partition-aware rate limiting (effectively unlimited with proper partitioning)
- **Partition Key**: First 6-8 characters of object key determine partition

### Object Retention:
- **Minimum Storage Duration**: STANDARD = 0 days (can delete immediately)
- **Lifecycle Rules**: Can transition objects between storage classes
- **Versioning**: Keeps all versions until explicitly deleted

### Access Limitations:
- **Public Access Block**: Can disable all public access at account level
- **Bucket Policies**: Limited to 20 KB
- **ACLs**: Legacy; modern approach uses bucket policies
- **Sharing**: Signed URLs, CloudFront, or public access required

---

## Bucket Types & Storage Classes

### Storage Classes Overview:

#### 1. STANDARD
- **Use Case**: Frequently accessed data, active datasets
- **Retrieval**: Immediate
- **Durability**: 99.999999999%
- **Availability**: 99.99%
- **Cost**: Highest storage cost, lowest retrieval cost
- **Minimum Duration**: None
- **Typical Usage**: Web content, frequently accessed files, databases

#### 2. STANDARD-IA (Infrequent Access)
- **Use Case**: Data accessed less than once per month
- **Retrieval**: Immediate (but retrieval charges apply)
- **Durability**: 99.999999999%
- **Availability**: 99.9%
- **Cost**: 50% cheaper storage, retrieval charges ($0.01 per GB)
- **Minimum Duration**: 30 days (charge early deletion fee if removed)
- **Typical Usage**: Backup, disaster recovery, older database backups

#### 3. INTELLIGENT-TIERING
- **Use Case**: Unknown or changing access patterns
- **Retrieval**: Automatic between STANDARD and STANDARD-IA
- **How It Works**: Moves objects to IA after 30 days of no access
- **Cost**: Slight overhead for automatic tiering
- **Minimum Duration**: 30 days for IA tier
- **Typical Usage**: Data lakes, mixed access patterns, cost optimization

#### 4. GLACIER Instant Retrieval
- **Use Case**: Data accessed quarterly
- **Retrieval**: Instant (< 1 second)
- **Durability**: 99.999999999%
- **Availability**: 99.95%
- **Cost**: ~$4/TB/month (75% cheaper than STANDARD)
- **Minimum Duration**: 90 days
- **Typical Usage**: Compliance archives, quarterly reports

#### 4. GLACIER Flexible Retrieval
- **Use Case**: Data rarely accessed, archive
- **Retrieval**: 1 minute to 5 minutes (configurable)
- **Cost**: ~$1/TB/month
- **Minimum Duration**: 90 days
- **Typical Usage**: Long-term archives, compliance requirements

#### 5. GLACIER Deep Archive
- **Use Case**: Long-term retention, compliance (7+ years)
- **Retrieval**: 12 hours to 48 hours
- **Cost**: ~$0.12/TB/month (lowest cost)
- **Minimum Duration**: 180 days
- **Typical Usage**: Regulatory archives, rarely accessed data

#### 6. Outposts
- **Use Case**: On-premises object storage
- **Hardware**: S3 on AWS Outposts (installed at your data center)
- **Use Case**: Low-latency local storage with S3 API
- **Typical Usage**: Hybrid cloud, edge computing

### Storage Class Comparison Table:
```
┌──────────────────┬──────────────┬────────┬──────────┬───────────────┐
│ Storage Class    │ Cost/Month   │ Access │ Min Days │ Use Case      │
├──────────────────┼──────────────┼────────┼──────────┼───────────────┤
│ STANDARD         │ ~$23/TB      │ Instant│ 0        │ Frequently    │
│ STANDARD-IA      │ ~$12.50/TB   │ Instant│ 30       │ Monthly       │
│ INTELLIGENT      │ ~$23/TB*     │ Auto   │ 30*      │ Mixed         │
│ GLACIER-IR       │ ~$4/TB       │ Instant│ 90       │ Quarterly     │
│ GLACIER-FR       │ ~$1/TB       │ Hours  │ 90       │ Rare          │
│ DEEP-ARCHIVE     │ ~$0.12/TB    │ Hours  │ 180      │ Archive       │
└──────────────────┴──────────────┴────────┴──────────┴───────────────┘
* Plus retrieval charges and tiering fees
```

### Selecting the Right Storage Class:
```
Access Frequency: Weekly+          → STANDARD
Access Frequency: Monthly          → STANDARD-IA
Access Frequency: Unknown/Mixed    → INTELLIGENT-TIERING
Access Frequency: Quarterly        → GLACIER Instant Retrieval
Access Frequency: Yearly           → GLACIER Flexible Retrieval
Access Frequency: Archive (7+ yrs) → DEEP ARCHIVE
```

---

## Bucket Organization (Folders)

### Folder Structure Concept:
S3 does NOT have true folders. It uses "prefixes" (key hierarchies) to simulate folder structure.

### How Prefixes Work:
- **Key**: `documents/2024/reports/Q1-report.pdf`
- **Prefix Hierarchy**:
  - `documents/`
  - `documents/2024/`
  - `documents/2024/reports/`
  - **Object Key**: `documents/2024/reports/Q1-report.pdf`

### Folder Structure Best Practices:
```
bucket-name/
├── documents/              # Department/category
│   ├── 2024/              # Year
│   │   ├── Q1/            # Quarter or month
│   │   │   ├── report.pdf
│   │   │   └── summary.txt
│   │   └── Q2/
│   └── 2023/
├── media/                 # Media files
│   ├── images/
│   │   ├── thumbnails/
│   │   └── originals/
│   └── videos/
├── archives/              # Old data
│   ├── 2022/
│   └── 2021/
└── temp/                  # Temporary uploads
    └── user-uploads/
```

### Naming Conventions for Organization:
```
Format: {category}/{year}/{month}/{type}/{filename}

Examples:
  logs/2024/01/application/error-20240115.log
  backups/database/2024/01/daily/backup-20240115.sql
  media/product-photos/2024/winter-collection/item-001.jpg
  user-data/{user-id}/documents/{date}/{filename}
```

### Organizing by Access Pattern:
```
Hot Data (Frequent Access):     bucket/current/   → STANDARD
Warm Data (Monthly Access):     bucket/recent/    → STANDARD-IA
Cold Data (Yearly Access):      bucket/archive/   → GLACIER
```

### Prefix Limitations & Considerations:
- **Prefix Length**: Keys limited to 1024 bytes total
- **Search**: Use prefix filtering to retrieve specific "folders"
- **Delete**: Must delete individual objects; no folder deletion
- **Copy**: Can copy with prefix to reorganize
- **Performance**: Well-distributed prefixes improve performance

### Using Prefixes with AWS CLI:
```bash
# List objects in "documents/2024/" prefix
aws s3api list-objects-v2 --bucket my-bucket --prefix "documents/2024/"

# Sync local folder to S3 prefix
aws s3 sync ./local-docs s3://my-bucket/documents/2024/

# Delete all objects with prefix
aws s3 rm s3://my-bucket/documents/2024/ --recursive
```

---

## Versioning

### What is Versioning?
Versioning keeps multiple versions of an object when updates occur.

### Versioning States:
```
┌─────────────────────────────────────────────────────────┐
│ NOT ENABLED (Default)                                   │
│ - No version history kept                               │
│ - Overwrites create new object (no recovery)            │
│ - VersionId = null                                      │
└─────────────────────────────────────────────────────────┘
        ↓
        Enable versioning
        ↓
┌─────────────────────────────────────────────────────────┐
│ ENABLED                                                 │
│ - All versions retained                                 │
│ - Overwrites create new version with new VersionId      │
│ - Can retrieve deleted objects (recovery)               │
│ - Storage increases for all versions                    │
└─────────────────────────────────────────────────────────┘
        ↓
        Suspend versioning
        ↓
┌─────────────────────────────────────────────────────────┐
│ SUSPENDED                                               │
│ - No new versions created                               │
│ - Existing versions remain (can't delete)               │
│ - Overwrites create null version                        │
│ - Can't re-enable (can only suspend)                    │
└─────────────────────────────────────────────────────────┘
```

### When to Use Versioning:
```
✅ USE VERSIONING:
   - Critical data requiring recovery capability
   - Compliance/regulatory requirements
   - Development environments (rollback capability)
   - Database backups
   - Configuration files (track changes)

❌ DON'T USE VERSIONING:
   - Temporary/cache files
   - Large files with frequent changes (storage cost)
   - High-volume log files
   - Performance-critical applications
```

### Version ID Behavior:
```bash
# Upload without versioning enabled
aws s3api put-object --bucket my-bucket --key file.txt --body file.txt
# Response: VersionId = null

# Enable versioning
aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled

# Upload again (creates version)
aws s3api put-object --bucket my-bucket --key file.txt --body file.txt
# Response: VersionId = "abc123xyz..."

# Upload again (creates another version)
aws s3api put-object --bucket my-bucket --key file.txt --body file.txt
# Response: VersionId = "def456uvw..."

# List all versions
aws s3api list-object-versions --bucket my-bucket --prefix file.txt
```

### Storage Cost Impact:
```
Scenario: 10 GB file uploaded daily for 30 days

WITHOUT Versioning:
  Storage = 10 GB (latest only)
  Cost ≈ $0.23/month

WITH Versioning:
  Storage = 300 GB (30 versions × 10 GB)
  Cost ≈ $6.90/month
  Increase: 30x!
```

### Lifecycle Policies with Versioning:
```yaml
# Keep only recent versions, archive old ones
Rules:
  - NoncurrentVersionTransitions:
      - Days: 30
        StorageClass: STANDARD-IA
      - Days: 90
        StorageClass: GLACIER
  - NoncurrentVersionExpiration:
      - Days: 365  # Delete versions older than 1 year
```

---

## Encryption

### Encryption Types:

#### 1. Server-Side Encryption with S3-Managed Keys (SSE-S3)
- **Key Management**: AWS manages keys for you
- **Algorithm**: AES-256
- **Overhead**: Minimal
- **Cost**: Included in S3 pricing
- **Use Case**: Standard security requirement
- **Setup**: Default encryption by bucket policy

```bash
# Enable default encryption (SSE-S3)
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

#### 2. Server-Side Encryption with KMS (SSE-KMS)
- **Key Management**: AWS Key Management Service (KMS)
- **Algorithm**: AES-256 with KMS keys
- **Overhead**: Slight delay for key operations
- **Cost**: KMS API calls charged (~$0.03 per 10k calls)
- **Use Case**: Regulatory compliance, key rotation control, audit logging
- **Key Rotation**: Automatic or manual

```bash
# Enable default encryption (SSE-KMS)
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:region:account:key/12345678"
      }
    }]
  }'
```

#### 3. Client-Side Encryption
- **Key Management**: You manage encryption before upload
- **Algorithm**: Your choice (AES-256, RSA, etc.)
- **Overhead**: Your application handles encryption
- **Cost**: No additional S3 charges
- **Use Case**: Maximum security, keys never sent to AWS

```python
# Example: Python with encryption
import boto3
from cryptography.fernet import Fernet

# Client encrypts before upload
key = Fernet.generate_key()
cipher_suite = Fernet(key)
encrypted_data = cipher_suite.encrypt(b"sensitive data")

# Upload encrypted data
s3_client = boto3.client('s3')
s3_client.put_object(
    Bucket='my-bucket',
    Key='file.encrypted',
    Body=encrypted_data
)
```

#### 4. Bucket Encryption by Default (AWS Recommended)
- **Automatic**: All objects encrypted unless specified
- **No Performance Impact**: Transparent to application
- **No Extra Cost**: Included with STANDARD pricing
- **Best Practice**: Should be enabled on all production buckets

```bash
# Enable bucket encryption by default
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": true
    }]
  }'
```

### Encryption in Transit (HTTPS)
- **Protocol**: Always use HTTPS for S3 communications
- **TLS**: 1.2 or higher
- **Bucket Policy**: Can enforce HTTPS-only access

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": [
      "arn:aws:s3:::my-bucket",
      "arn:aws:s3:::my-bucket/*"
    ],
    "Condition": {
      "Bool": {
        "aws:SecureTransport": "false"
      }
    }
  }]
}
```

### Encryption Comparison Table:
```
┌─────────────────────────────────────────────────────────────┐
│ Encryption Type   │ Key Mgmt │ Cost   │ Compliance │ Ease   │
├─────────────────────────────────────────────────────────────┤
│ SSE-S3 (AES-256)  │ AWS      │ Free   │ Basic      │ Easy   │
│ SSE-KMS           │ AWS/You  │ $0.03  │ High       │ Medium │
│ Client-Side       │ You      │ Free   │ Max        │ Hard   │
│ Default (Bucket)  │ AWS      │ Free   │ Good       │ Easy   │
└─────────────────────────────────────────────────────────────┘
```

---

## Static Website Hosting

### Overview:
S3 can host static websites directly without needing a web server.

### What is Static Website Hosting?
- **Static Files**: HTML, CSS, JavaScript, images, JSON
- **No Server Logic**: No PHP, Python, Node.js execution
- **Highly Available**: 99.99% uptime
- **Globally Distributed**: Can use CloudFront for CDN

### Requirements:
1. **Public Access**: Bucket must allow public read access
2. **Index Document**: HTML file to serve (default: index.html)
3. **Error Document**: Optional HTML for 404 errors
4. **Permissions**: Bucket policy allowing GetObject

### Static Hosting vs. Dynamic:
```
STATIC HOSTING (S3):
  - Pre-built HTML files
  - No real-time processing
  - Fast, scalable, cheap
  - Example: Documentation sites, blogs, portfolios

DYNAMIC HOSTING (EC2/Lambda):
  - Server-side processing
  - Real-time data generation
  - Database queries
  - Example: E-commerce, social media, APIs
```

### Setting Up Static Website Hosting:

#### Step 1: Enable Public Access (if needed)
```bash
# Disable block public access
aws s3api put-public-access-block --bucket my-bucket \
  --public-access-block-configuration \
  "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

#### Step 2: Add Bucket Policy for Public Read
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```

#### Step 3: Enable Static Website Hosting
```bash
aws s3api put-bucket-website --bucket my-bucket \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"}
  }'
```

#### Step 4: Upload HTML Files
```bash
aws s3 cp index.html s3://my-bucket/
aws s3 cp error.html s3://my-bucket/
aws s3 sync ./website s3://my-bucket/ --exclude ".git/*"
```

### Website Endpoint:
```
http://{bucket-name}.s3-website-{region}.amazonaws.com

Example:
  http://my-website.s3-website-us-east-1.amazonaws.com
  https://my-website.example.com (with custom domain)
```

### Custom Domain Setup:
1. Register domain with Route 53 or external registrar
2. Create CNAME or A record pointing to S3 endpoint
3. Use CloudFront for HTTPS support

### Example Website Structure:
```
my-website-bucket/
├── index.html           # Homepage
├── error.html           # 404 error page
├── css/
│   └── style.css
├── js/
│   └── script.js
├── images/
│   ├── logo.png
│   └── hero.jpg
├── about.html
├── contact.html
└── blog/
    ├── post-1.html
    └── post-2.html
```

### Redirecting Routes:
S3 website routing rules allow URL redirections:
```xml
<RoutingRules>
  <RoutingRule>
    <Condition>
      <HttpErrorCodeReturnedEquals>404</HttpErrorCodeReturnedEquals>
    </Condition>
    <Redirect>
      <HostName>mysite.com</HostName>
      <ReplaceKeyWith>error.html</ReplaceKeyWith>
    </Redirect>
  </RoutingRule>
</RoutingRules>
```

### Performance Optimization:
- **CloudFront CDN**: Distribute content globally
- **Caching**: Set Cache-Control headers
- **Compression**: Gzip CSS/JS files
- **Lazy Loading**: Load images on-demand

---

## Access Control

### Access Control Methods:

#### 1. Bucket Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Sid": "DenyUnencryptedObjectUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        }
      }
    }
  ]
}
```

#### 2. IAM Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:ListBucket",
      "s3:GetObject"
    ],
    "Resource": [
      "arn:aws:s3:::my-bucket",
      "arn:aws:s3:::my-bucket/*"
    ]
  }]
}
```

#### 3. Access Control Lists (ACLs) - Legacy
```
Options: private, public-read, public-read-write, authenticated-read
```

#### 4. Signed URLs
```python
import boto3
from datetime import timedelta

s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'private-file.pdf'
    },
    ExpiresIn=3600  # 1 hour
)
print(url)  # URL valid for 1 hour only
```

#### 5. Block Public Access Settings
```bash
# Block all public access (recommended default)
aws s3api put-public-access-block --bucket my-bucket \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### Principle of Least Privilege:
```
1. Start with no access (default)
2. Grant minimum necessary permissions
3. Use specific ARNs (not *)
4. Review permissions regularly
5. Remove unnecessary access

✅ GOOD:
"Resource": "arn:aws:s3:::my-bucket/public/*"  # Specific prefix

❌ BAD:
"Resource": "*"  # All buckets
```

---

## Performance & Optimization

### Key Performance Factors:

#### 1. Request Rate Optimization
```
Original Limit: 3,500 PUT/COPY/POST/DELETE, 5,500 GET per second
Modern S3: Partition-aware rate limiting

Partition Key = First 6-8 chars of object key

Good (distributed across partitions):
  user-001/file1.txt → partition: user-0
  user-002/file2.txt → partition: user-0
  user-003/file3.txt → partition: user-0
  (Each 5,500 requests/sec limit)

Bad (all in same partition):
  sequential-0001/data.txt
  sequential-0002/data.txt
  sequential-0003/data.txt
  (All compete for same 5,500 req/sec limit)
```

#### 2. Multipart Upload for Large Files
```bash
# Automatically uses multipart for large files
aws s3 cp large-file.zip s3://my-bucket/ --storage-class STANDARD_IA

# Manual multipart for control
aws s3api create-multipart-upload --bucket my-bucket --key large-file.zip

# Upload parts in parallel
for i in {1..10}; do
  aws s3api upload-part --bucket my-bucket --key large-file.zip \
    --part-number $i --body "part-$i" --upload-id "upload-id"
done

# Complete upload
aws s3api complete-multipart-upload --bucket my-bucket --key large-file.zip \
  --upload-id "upload-id" --multipart-upload '{"Parts":[...]}'
```

#### 3. CloudFront Integration
```
S3 Bucket → CloudFront Edge Locations → Users
             (Caches content globally)

Benefits:
- Reduced latency (users served from closest edge)
- Reduced S3 costs (fewer origin requests)
- DDoS protection
- SSL/TLS support
```

#### 4. Object Metadata Optimization
```bash
# Add caching headers for static assets
aws s3api put-object --bucket my-bucket --key style.css \
  --body style.css \
  --cache-control "max-age=31536000"  # 1 year

# Add content encoding for compression
aws s3api put-object --bucket my-bucket --key data.json \
  --body data.json.gz \
  --content-encoding gzip
```

#### 5. S3 Transfer Acceleration
```bash
# Enable transfer acceleration on bucket
aws s3api put-bucket-accelerate-configuration --bucket my-bucket \
  --accelerate-configuration Status=Enabled

# Use accelerated endpoint
aws s3 cp large-file.zip s3://my-bucket.s3-accelerate.amazonaws.com/
```

### Performance Monitoring:
```bash
# CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name NumberOfObjects \
  --dimensions Name=BucketName,Value=my-bucket \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 86400 \
  --statistics Average
```

---

## Compliance & Durability

### Durability & Availability:
```
Durability: 99.999999999% (11 9s)
  - Chance of data loss: 1 in 10 billion
  - Equivalent to: 1 file lost every 10,000 years with 1M files

Availability: 99.99%
  - Service will be unavailable: ~52.6 minutes/year
  - SLA covers access failures, not data loss
```

### Durability Mechanism:
```
Single S3 Object:
  ├── AZ 1: Data copy
  ├── AZ 2: Data copy
  └── AZ 3: Data copy
     (Automatically replicated across 3+ availability zones)
```

### Compliance Features:

#### Object Lock (Governance/Compliance)
```bash
# Enable Object Lock on bucket (at creation only)
aws s3api create-bucket --bucket my-bucket \
  --object-lock-enabled-for-bucket

# Set retention period
aws s3api put-object-retention --bucket my-bucket --key file.txt \
  --retention Mode=GOVERNANCE,RetainUntilDate=2025-12-31T23:59:59Z

# Compliance mode (cannot be overridden by anyone)
aws s3api put-object-retention --bucket my-bucket --key file.txt \
  --retention Mode=COMPLIANCE,RetainUntilDate=2025-12-31T23:59:59Z

# Legal hold
aws s3api put-object-legal-hold --bucket my-bucket --key file.txt \
  --legal-hold Status=ON
```

#### MFA Delete
```bash
# Enable versioning with MFA delete requirement
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "device-serial-number token-code"
```

#### Immutability Policies
```json
{
  "Rules": [{
    "Id": "ArchiveRule",
    "Status": "Enabled",
    "NoncurrentVersionTransitions": [{
      "NoncurrentDays": 30,
      "StorageClass": "GLACIER"
    }],
    "NoncurrentVersionExpiration": {
      "NoncurrentDays": 365
    },
    "Expiration": {
      "Days": 3650
    }
  }]
}
```

### Audit & Monitoring:
```bash
# Enable access logging
aws s3api put-bucket-logging --bucket my-bucket \
  --bucket-logging-status '{
    "LoggingEnabled": {
      "TargetBucket": "log-bucket",
      "TargetPrefix": "s3-logs/"
    }
  }'

# Enable CloudTrail
aws cloudtrail create-trail --name s3-trail \
  --s3-bucket-name trail-bucket

# Enable S3 inventory
aws s3api put-bucket-inventory-configuration --bucket my-bucket \
  --id inventory-config --inventory-configuration '{...}'
```

---

## Common Use Cases

### 1. Data Backup & Disaster Recovery
```yaml
Bucket Configuration:
  - Versioning: Enabled
  - Replication: Cross-region for disaster recovery
  - Lifecycle: Archive after 30 days, delete after 365 days
  - Encryption: SSE-KMS with key rotation
```

### 2. Data Lake / Analytics
```yaml
Bucket Structure:
  raw-data/          # Raw incoming data
  processed/         # Cleaned, processed data
  analytics/         # Analysis results
  
Technology:
  - Athena: SQL queries on S3 data
  - Glue: Data cataloging and ETL
  - Redshift Spectrum: Data warehouse queries
```

### 3. Content Delivery / Media
```yaml
Bucket Configuration:
  - CloudFront: Global distribution
  - Multiple Storage Classes: Hot/warm/cold based on access
  - Versioning: Track content changes
  - Caching: Aggressive cache headers
```

### 4. Application Backups
```yaml
Schedule: Daily automated backups
Retention: 30-day rolling window
Encryption: KMS with separate key
Verification: Periodic restore tests
```

---

## Cost Optimization Tips

1. **Use Right Storage Class**
   - STANDARD for frequent access
   - INTELLIGENT-TIERING for unknown patterns
   - GLACIER for archival

2. **Enable Lifecycle Policies**
   - Auto-transition to cheaper tiers
   - Auto-delete old versions

3. **Reduce Requests**
   - Batch operations
   - Use CloudFront to cache

4. **Monitor Storage Growth**
   - S3 Storage Lens for insights
   - Set up alerts for unexpected growth

5. **Remove Incomplete Multipart Uploads**
   - Accumulate storage costs
   - Use lifecycle rules to delete old uploads

---

## Quick Reference Commands

```bash
# Create bucket
aws s3api create-bucket --bucket my-bucket \
  --create-bucket-configuration LocationConstraint=us-west-2

# List buckets
aws s3 ls

# Upload file
aws s3 cp file.txt s3://my-bucket/

# Download file
aws s3 cp s3://my-bucket/file.txt ./

# List bucket contents
aws s3 ls s3://my-bucket/ --recursive

# Sync local folder
aws s3 sync ./local-folder s3://my-bucket/

# Enable versioning
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Set encryption
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '...'

# Enable static website
aws s3api put-bucket-website --bucket my-bucket \
  --website-configuration '...'

# Delete object
aws s3 rm s3://my-bucket/file.txt

# Delete bucket (must be empty)
aws s3 rm s3://my-bucket --recursive
aws s3api delete-bucket --bucket my-bucket
```

---

This comprehensive guide covers all major S3 features, best practices, and use cases for managing cloud storage effectively.
