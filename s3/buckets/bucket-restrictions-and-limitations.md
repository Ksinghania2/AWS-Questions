# Bucket Restrictions and Limitations

Understanding S3 bucket restrictions is critical for designing scalable, error-free storage solutions.

## Key Restrictions

| Restriction | Details | Exam Impact |
|---|---|---|
| **Global uniqueness** | Bucket names must be unique across ALL AWS accounts globally | High |
| **No uppercase/underscores** | Only lowercase letters, numbers, and hyphens | High |
| **100 buckets per account** | Soft limit, can be increased via support ticket | Medium |
| **No nesting** | Buckets cannot be created inside other buckets | High |
| **No spaces** | Spaces are not allowed in bucket names | Medium |
| **Region-locked** | A bucket exists in exactly one region; data never leaves that region unless replicated | High |
| **No rename** | You cannot rename a bucket; you must delete and recreate it | Medium |
| **No live region migration** | To move a bucket to another region, use replication or manually copy data | Medium |

## Soft Limits vs Hard Limits

### Soft Limits (Can Be Increased)
- **100 buckets per AWS account** by default (can be raised to 1,000+ with support ticket)
- **Unlimited objects per bucket** (no hard cap on object count)

### Hard Limits (Cannot Be Changed)
- Bucket name: 3-63 characters
- Object key: 1-1024 bytes (UTF-8 encoded)
- Single object size: 5 TB max
- Single PUT upload: 5 GB max (use multipart for larger)
- Multipart upload part size: 5 MB to 5 GB, max 10,000 parts

## CLI Commands to Check Limits

```bash
# Check current bucket count
aws s3api list-buckets --query "length(Buckets[])" --output text

# Check service quotas (requires service-quotas API)
aws service-quotas get-service-quota \
  --service-code s3 \
  --quota-code L-DC2B2D3D

# Request a quota increase
aws service-quotas request-service-quota-increase \
  --service-code s3 \
  --quota-code L-DC2B2D3D \
  --desired-value 500
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')

# List all buckets and count them
response = s3.list_buckets()
buckets = response['Buckets']
print(f"Total buckets: {len(buckets)}")
for bucket in buckets:
    print(f"  - {bucket['Name']} ({bucket['CreationDate']})")

# Check bucket region
bucket_name = 'my-existing-bucket'
response = s3.get_bucket_location(Bucket=bucket_name)
region = response['LocationConstraint'] or 'us-east-1'
print(f"Bucket '{bucket_name}' is in region: {region}")

# Attempt to create a bucket with invalid name (will fail)
try:
    s3.create_bucket(Bucket='Invalid_Bucket_Name')
except Exception as e:
    print(f"Expected error: {e}")
```

## Common Exam Scenarios

### Scenario 1: Cross-Region Access
**Question:** Can a bucket in us-east-1 be accessed from us-west-2?
**Answer:** Yes, but there will be latency and data transfer costs. Use Cross-Region Replication (CRR) if low latency is needed.

### Scenario 2: Renaming a Bucket
**Question:** How do you rename a bucket?
**Answer:** You cannot rename a bucket. You must:
1. Create a new bucket with the desired name
2. Copy all objects to the new bucket
3. Update all references/applications
4. Delete the old bucket

### Scenario 3: Moving Data Between Regions
**Question:** How do you move data from us-east-1 to eu-west-1?
**Answer:** Options:
- **CRR (Cross-Region Replication):** Automatic, ongoing replication
- **AWS CLI sync:** `aws s3 sync s3://source-bucket s3://dest-bucket`
- **S3 Batch Operations:** For large-scale copy jobs
- **AWS DataSync:** For large, one-time transfers

## Exam Quick Reference
- ✅ 100 buckets per account (soft limit)
- ✅ Unlimited objects per bucket
- ✅ Max object size: 5 TB
- ✅ Max PUT size: 5 GB (use multipart for >5 GB)
- ✅ Buckets cannot be nested
- ✅ Buckets cannot be renamed
- ✅ Buckets are region-specific
- ✅ No automatic cross-region data movement