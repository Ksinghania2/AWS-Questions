# AWS S3 Theory Guide — Complete Exam Revision

This comprehensive guide covers ALL S3 concepts for the AWS Solutions Architect exam. Each section includes key theory, CLI commands, Python examples, and exam tips.

## Table of Contents
1. [What is S3?](#1-what-is-s3)
2. [Core Concepts](#2-core-s3-concepts)
3. [Bucket Naming & Restrictions](#3-bucket-naming--restrictions)
4. [Storage Classes](#4-s3-storage-classes)
5. [Versioning](#5-versioning)
6. [Encryption](#6-encryption)
7. [Access Control](#7-access-control-in-s3)
8. [Lifecycle Rules](#8-lifecycle-rules)
9. [Static Website Hosting](#9-static-website-hosting)
10. [Multipart Upload](#10-multipart-upload)
11. [Object Replication](#11-object-replication)
12. [Presigned URLs](#12-presigned-urls)
13. [Object Lock (WORM)](#13-object-lock-worm)
14. [Event Notifications](#14-event-notifications)
15. [Performance Optimization](#15-performance-optimization)
16. [Consistency Model](#16-consistency-model)
17. [S3 Select & Glacier Select](#17-s3-select--glacier-select)
18. [Exam Cheat Sheet](#18-exam-cheat-sheet)

---

## 1. What is S3?
Amazon S3 (Simple Storage Service) is **object storage** — not block storage, not a file system.

| Property | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.99% (Standard) |
| **Max object size** | 5 TB |
| **Max bucket limit** | 100 per account (soft limit) |
| **Min object size** | 0 bytes |

```bash
aws s3 ls
aws s3 mb s3://my-unique-bucket
```

## 2. Core S3 Concepts

### Bucket → Container for objects (globally unique name)
### Object → File + metadata + key
### Key → Full path of the object (e.g., `images/logo.png`)
### Prefix → Start of the key (simulates folders)
### Metadata → System-defined (Content-Type, ETag) or user-defined (x-amz-meta-*)

### Prefix Performance
- **3,500 PUTs/sec per prefix**
- **5,500 GETs/sec per prefix**
- Distribute across many prefixes for high throughput (e.g., `YYYY/MM/DD/HH/`)

```bash
aws s3api list-objects-v2 --bucket my-bucket --prefix "logs/2024/"
aws s3api list-objects-v2 --bucket my-bucket --delimiter "/"
```

## 3. Bucket Naming & Restrictions

| Rule | Detail |
|---|---|
| Length | 3-63 characters |
| Characters | Lowercase letters, numbers, hyphens only |
| Start/End | Must start and end with letter or number |
| IP address | Cannot be formatted as IP |
| Global uniqueness | Yes — across ALL AWS accounts |

### Important: LocationConstraint
```bash
# us-east-1 does NOT need LocationConstraint
aws s3api create-bucket --bucket my-bucket --region us-east-1

# All other regions REQUIRE LocationConstraint
aws s3api create-bucket --bucket my-bucket --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2
```

## 4. S3 Storage Classes

| Class | Durability | Availability | AZs | Min Duration | Min Size | Retrieval | Cost |
|---|---|---|---|---|---|---|---|
| **Standard** | 11 9's | 99.99% | ≥3 | None | 0 B | Instant | Highest |
| **Standard-IA** | 11 9's | 99.9% | ≥3 | 30 days | 128 KB | Instant + fee | ~45% less |
| **One Zone-IA** | 11 9's* | 99.5% | 1 | 30 days | 128 KB | Instant + fee | ~55% less |
| **Intelligent-Tiering** | 11 9's | 99.9% | ≥3 | None (IA: 30d) | 0 B | Instant | Monitoring fee |
| **Glacier Instant** | 11 9's | 99.9% | ≥3 | 90 days | 128 KB | Millisecond + fee | ~68% less |
| **Glacier Flexible** | 11 9's | 99.99% | ≥3 | 90 days | 40 KB | 1-5 min / 3-5 hr / 5-12 hr | ~80% less |
| **Glacier Deep Archive** | 11 9's | 99.99% | ≥3 | 180 days | 40 KB | 12 hr / 48 hr | ~95% less |
| **Express One Zone** | 11 9's* | 99.5% | 1 | None | 0 B | Single-digit ms | Higher |

*\*11 9's durability within the AZ only*

### Glacier Retrieval Tiers
| Class | Expedited | Standard | Bulk |
|---|---|---|---|
| **Glacier Flexible** | 1-5 min | 3-5 hr | 5-12 hr |
| **Glacier Deep Archive** | N/A | 12 hr | 48 hr |

### Exam: Restore Required?
| Class | Restore Needed? |
|---|---|
| Standard | ❌ No |
| Standard-IA | ❌ No |
| One Zone-IA | ❌ No |
| Intelligent-Tiering | ❌ No |
| Glacier Instant | ❌ No |
| Glacier Flexible | ✅ **Yes** |
| Glacier Deep Archive | ✅ **Yes** |

```bash
# Upload to specific class
aws s3 cp file.txt s3://my-bucket/ --storage-class STANDARD_IA

# Restore from Glacier
aws s3api restore-object \
  --bucket my-bucket --key archive.zip \
  --restore-request '{"Days": 7, "GlacierJobParameters": {"Tier": "Standard"}}'
```

## 5. Versioning

| State | Behavior |
|---|---|
| **Unversioned** (default) | Overwrites replace permanently |
| **Enabled** | Each overwrite creates a new version |
| **Suspended** | New writes are unversioned, old versions remain |

### Key Points
- **Cannot be disabled** once enabled (only suspended)
- **Required** for replication, Object Lock, MFA Delete
- **Delete markers** hide objects (restore by removing marker)
- Each version costs money — use lifecycle to expire old versions

```bash
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Restore from delete marker
aws s3api delete-object --bucket my-bucket --key file.txt \
  --version-id <delete-marker-version-id>
```

## 6. Encryption

| Method | Keys Managed By | Audit Trail | Cost | AWS Can Read? |
|---|---|---|---|---|
| **SSE-S3** | AWS | ❌ No | Free | Yes |
| **SSE-KMS** | Customer (KMS) | ✅ Yes | KMS charges | Yes |
| **SSE-C** | Customer (provided per request) | ❌ No | Free | **No** (no key) |
| **DSSE-KMS** | Both S3 + KMS | ✅ Yes | Higher | Yes |
| **CSE** (Client-Side) | Customer (encrypted before upload) | N/A | Free | **No** |

### SSE-KMS Key Types
- **AWS Managed** (`aws/s3`) — free, automatic rotation
- **Customer Managed (CMK)** — you control, rotation optional, audit trail
- **Multi-Region Key** — cross-region replication with encryption

### Encryption in Transit
- **HTTPS/TLS** is default for all S3 API calls
- Enforce HTTPS via bucket policy: `aws:SecureTransport` condition
- Static website endpoints: **HTTP only** (use CloudFront for HTTPS)

```bash
# SSE-S3
aws s3 cp file.txt s3://my-bucket/ --sse AES256

# SSE-KMS
aws s3 cp file.txt s3://my-bucket/ --sse aws:kms --sse-kms-key-id alias/my-key

# Enforce HTTPS
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": ["arn:aws:s3:::my-bucket/*", "arn:aws:s3:::my-bucket"],
    "Condition": {"Bool": {"aws:SecureTransport": "false"}}
  }]
}'
```

## 7. Access Control in S3

| Method | Scope | Use Case |
|---|---|---|
| **IAM Policies** | Users, groups, roles | Control what identities can do |
| **Bucket Policies** | Bucket level | Cross-account access, public access |
| **ACLs** | Object/bucket level | Legacy — not recommended |
| **Access Points** | Per-application | Granular, multi-tenant access |
| **Block Public Access** | Account/bucket level | Protect against accidental public access |
| **Object Ownership** | Bucket level | Disable ACLs, enforce bucket owner |

### Bucket Policy vs IAM Policy
- **Bucket Policy**: Controls access at bucket level, can grant cross-account access
- **IAM Policy**: Controls what a specific identity can do across all resources

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-public-bucket/*"
  }]
}
```

## 8. Lifecycle Rules

### Transition Actions — One-way (can only move to cheaper storage)
```
Standard (Day 0) → Standard-IA (Day 30) → Glacier IR (Day 90) → Glacier (Day 120) → Deep Archive (Day 180) → Delete (Day 2555)
```

### Expiration Actions
- Delete objects after N days
- Delete previous versions after N noncurrent days
- Abort incomplete multipart uploads after N days

```bash
aws s3api put-bucket-lifecycle-configuration --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "archive-rule",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }]
  }'
```

## 9. Static Website Hosting

| Feature | Detail |
|---|---|
| **Protocol** | HTTP only (use CloudFront for HTTPS) |
| **Index document** | Required (e.g., `index.html`) |
| **Error document** | Optional (e.g., `error.html`) |
| **Public access** | Required (bucket policy or ACL) |
| **Custom domain** | Via Route 53 or DNS |
| **Redirects** | Supported (all requests or conditional) |

```bash
aws s3api put-bucket-website --bucket my-bucket \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"}
  }'
```

## 10. Multipart Upload

| Detail | Value |
|---|---|
| **Recommended for** | Objects > 100 MB |
| **Required for** | Objects > 5 GB |
| **Max parts** | 10,000 |
| **Part size** | 5 MB to 5 GB |
| **Max object size** | 5 TB |

```bash
aws s3 cp large-file.iso s3://my-bucket/large-file.iso  # Automatic multipart
```

## 11. Object Replication

| Type | Description |
|---|---|
| **CRR** (Cross-Region Replication) | Different regions — DR, compliance, latency |
| **SRR** (Same-Region Replication) | Same region — compliance, log aggregation |

### Requirements
- Versioning enabled on **both** source and destination
- Appropriate IAM role for S3 to replicate
- Can replicate to same or different account

```bash
aws s3api put-bucket-replication --bucket source-bucket \
  --replication-configuration file://replication.json
```

## 12. Presigned URLs

| Detail | Value |
|---|---|
| **Max expiration (SDK)** | 7 days |
| **Max expiration (CLI)** | 12 hours |
| **Requires credentials** | URL creator only (user doesn't need AWS creds) |
| **Actions** | GET, PUT, POST, DELETE, HEAD |

```bash
aws s3 presign s3://my-bucket/report.pdf --expires-in 3600
```

## 13. Object Lock (WORM)

| Mode | Description | Can Override? |
|---|---|---|
| **GOVERNANCE** | Users with bypass permission can delete | Yes (with permission) |
| **COMPLIANCE** | No one can delete (not even root) | **Absolutely not** |
| **Legal Hold** | Indefinite hold until manually removed | Remove hold |

### Requirements
- Must be enabled at bucket creation time
- Versioning must be enabled

```bash
aws s3api create-bucket --bucket my-locked-bucket \
  --object-lock-enabled-for-bucket --region us-east-1
```

## 14. Event Notifications

S3 can send events to:
- **Lambda** — Process files on upload
- **SQS** — Queue messages for processing
- **SNS** — Send notifications
- **EventBridge** — Advanced event routing

Event types: `s3:ObjectCreated:*`, `s3:ObjectRemoved:*`, `s3:ObjectRestore:*`

```bash
aws s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [{
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:process-file",
      "Events": ["s3:ObjectCreated:*"]
    }]
  }'
```

## 15. Performance Optimization

| Technique | Benefit |
|---|---|
| **Use multiple prefixes** | 3,500 PUTs/sec per prefix → scale horizontally |
| **Multipart upload** | Parallel uploads for large files |
| **Transfer Acceleration** | Faster uploads using AWS edge locations |
| **S3 Byte-Range Fetches** | Parallel downloads of large files |
| **S3 Select** | Server-side filtering (less data transferred) |
| **CloudFront** | CDN caching for frequently accessed objects |

```bash
# Enable Transfer Acceleration
aws s3api put-bucket-accelerate-configuration \
  --bucket my-bucket --accelerate-configuration Status=Enabled

# Use accelerated endpoint
aws s3 cp large-file.zip s3://my-bucket/ --endpoint-url https://my-bucket.s3-accelerate.amazonaws.com
```

## 16. Consistency Model

As of December 2020, S3 provides **strong read-after-write consistency** for ALL operations:

| Operation | Consistency |
|---|---|
| PUT new object | ✅ Strong (immediately readable) |
| PUT overwrite | ✅ Strong (immediately latest version) |
| DELETE | ✅ Strong (immediately reflected) |
| LIST | ✅ Strong (immediately reflects changes) |

## 17. S3 Select & Glacier Select

Retrieve only a subset of data using SQL expressions:
- **S3 Select**: Query CSV, JSON, Parquet files in S3
- **Glacier Select**: Query archived data in Glacier
- **Benefits**: Less data transferred, lower cost, faster results

```bash
aws s3api select-object-content \
  --bucket my-bucket --key data.csv \
  --expression "SELECT * FROM S3Object s WHERE s.\"year\" = '2024'" \
  --expression-type SQL \
  --input-serialization '{"CSV": {}, "CompressionType": "NONE"}' \
  --output-serialization '{"CSV": {}}' output.csv
```

---

## 18. Exam Cheat Sheet

### Storage Class Decision Flowchart
```
Q: How frequently is data accessed?
├── Frequently → Standard ✅
├── Infrequently → Is data critical?
│   ├── Yes → Standard-IA ✅
│   └── No → One Zone-IA ✅
├── Unknown → Intelligent-Tiering ✅
└── Rarely (archive) → How fast retrieval?
    ├── Milliseconds → Glacier Instant ✅
    ├── Minutes to Hours → Glacier Flexible ✅
    └── 12-48 Hours → Glacier Deep Archive ✅
```

### Must-Know Numbers
| Concept | Number |
|---|---|
| S3 durability | 11 9's (99.999999999%) |
| Standard availability | 99.99% |
| Max object size | 5 TB |
| Max single PUT | 5 GB |
| Max multipart parts | 10,000 |
| Min part size (multipart) | 5 MB |
| Max buckets per account | 100 (soft limit) |
| Bucket name length | 3-63 chars |
| Object key max length | 1,024 bytes |
| Presigned URL max (SDK) | 7 days |
| Presigned URL max (CLI) | 12 hours |
| PUTs/sec per prefix | 3,500 |
| GETs/sec per prefix | 5,500 |
| Glacier Flexible restore (Expedited) | 1-5 min |
| Glacier Flexible restore (Standard) | 3-5 hr |
| Glacier Deep Archive restore (Standard) | 12 hr |

### Common Exam Scenarios

1. **"Must encrypt all data at rest with minimal cost/effort"** → SSE-S3 (AES-256, free, automatic)
2. **"Need audit trail of who accessed encrypted data"** → SSE-KMS (CloudTrail logs KMS calls)
3. **"Provider cannot store encryption keys"** → SSE-C (customer-provided keys) or Client-Side Encryption
4. **"Financial records - WORM protection, cannot be overridden"** → Object Lock with COMPLIANCE mode
5. **"Cost-effective archive with millisecond retrieval"** → Glacier Instant Retrieval
6. **"Lowest cost archival storage"** → Glacier Deep Archive
7. **"Unpredictable access patterns, auto-tiering"** → Intelligent-Tiering
8. **"High-throughput real-time analytics"** → Express One Zone (single-digit ms latency)
9. **"Allow temporary file sharing without IAM"** → Presigned URLs
10. **"Static website with HTTPS"** → S3 + CloudFront
11. **"Deleted file recovery"** → Versioning (remove delete marker)
12. **"Cross-region disaster recovery"** → CRR (Cross-Region Replication)
13. **"Performance > 3,500 PUTs/sec"** → Distribute objects across multiple prefixes
14. **"Glacier object cannot be read directly"** → Must initiate restore first
15. **"IAM user saved credentials in code"** → Use IAM roles instead

### Encryption Comparison
```
SSE-S3:    Upload → S3 encrypts → Store → S3 decrypts → Download
SSE-KMS:   Upload → KMS encrypts → Store → KMS decrypts → Download
SSE-C:     Upload + key → S3 encrypts → Store (hash only) → Download + key → S3 decrypts
CSE:       Encrypt locally → Upload encrypted → Store → Download encrypted → Decrypt locally
```

### URL Formats
```
Standard:    https://bucket.s3.region.amazonaws.com/key
Website:     http://bucket.s3-website-region.amazonaws.com
Accelerate:  https://bucket.s3-accelerate.amazonaws.com/key
Dual-stack:  https://bucket.s3.dualstack.region.amazonaws.com/key
FIPS:        https://bucket.s3-fips.region.amazonaws.com/key
Access Pt:   https://name-accountid.s3-accesspoint.region.amazonaws.com
```

### Tag vs Metadata
| Feature | Tags | Metadata |
|---|---|---|
| IAM policy searchable | ✅ Yes | ❌ No |
| Update without copy | ✅ Yes | ❌ No |
| Max | 10 tags | 2 KB total |
| Lifecycle filter | ✅ Yes | ❌ No |
| Cost allocation | ✅ Yes | ❌ No |