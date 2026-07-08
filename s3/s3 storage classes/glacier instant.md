# S3 Glacier Instant Retrieval

Glacier Instant Retrieval is for **long-lived archive data** that needs **millisecond retrieval** — the fastest retrieval option among the Glacier family.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.9% |
| **AZ Coverage** | ≥ 3 Availability Zones |
| **Minimum object size** | 128 KB (billed as 128 KB if smaller) |
| **Minimum storage duration** | 90 days |
| **Retrieval cost** | Per GB retrieved (higher than Standard-IA) |
| **Retrieval time** | **Milliseconds** (same as Standard) |
| **Storage cost** | ~68% less than Standard |

## When to Use Glacier Instant Retrieval

### Good Use Cases
- **Archived data that may need immediate access** (e.g., recent archives, compliance data)
- **Backup data with SLA for rapid recovery**
- **Media archives** that need instant playback on request
- **Healthcare/medical records** that must be retained but may be needed urgently
- **Data behind CloudFront** where cold start is not acceptable

### Not Ideal For
- Data that can tolerate minutes-to-hours retrieval (use Glacier Flexible or Deep Archive)
- Frequently accessed data (Standard or Standard-IA is cheaper)
- Short-lived data (< 90 days)
- Very small objects (< 128 KB)

## CLI Commands

```bash
# Upload directly to Glacier Instant Retrieval
aws s3 cp archive.zip s3://my-bucket/archives/archive.zip \
  --storage-class GLACIER_IR

# Transition existing object
aws s3 cp s3://my-bucket/old-data.db s3://my-bucket/old-data.db \
  --storage-class GLACIER_IR

# Lifecycle rule to transition to Glacier Instant after 90 days
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "to-glacier-ir",
      "Status": "Enabled",
      "Filter": {"Prefix": "archives/"},
      "Transitions": [{"Days": 90, "StorageClass": "GLACIER_IR"}]
    }]
  }'

# Check storage class (returns GLACIER_IR)
aws s3api head-object --bucket my-bucket --key archives/archive.zip \
  --query StorageClass --output text

# Restore is NOT needed for Glacier IR — it's already accessible
aws s3 cp s3://my-bucket/archives/archive.zip ./restored-archive.zip
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload to Glacier Instant Retrieval
s3.upload_file(
    'old-backup.db',
    bucket,
    'archives/old-backup.db',
    ExtraArgs={'StorageClass': 'GLACIER_IR'}
)
print("Uploaded as GLACIER_IR")

# No restore needed — read directly
response = s3.get_object(Bucket=bucket, Key='archives/old-backup.db')
print(f"Downloaded {len(response['Body'].read())} bytes directly (no restore required)")

# List Glacier IR objects
def list_glacier_ir_objects(bucket, prefix=''):
    """List all Glacier Instant Retrieval objects"""
    paginator = s3.get_paginator('list_objects_v2')
    total_size = 0
    count = 0
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            sc = obj.get('StorageClass', 'STANDARD')
            if sc == 'GLACIER_IR':
                count += 1
                total_size += obj['Size']
                print(f"  {obj['Key']} ({obj['Size']/1024/1024:.2f} MB)")
    
    print(f"\nTotal: {count} objects, {total_size/1024/1024/1024:.2f} GB")
    return count, total_size

list_glacier_ir_objects(bucket)

# Set up complete lifecycle: Standard → IA → Glacier IR
def setup_archive_lifecycle(bucket):
    """Set up a complete lifecycle for archiving"""
    lifecycle = {
        'Rules': [
            {
                'ID': 'transition-to-ia',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'production/'},
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 90, 'StorageClass': 'GLACIER_IR'}
                ]
            }
        ]
    }
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration=lifecycle
    )
    print("Lifecycle configured: Standard → Standard-IA → Glacier IR")

setup_archive_lifecycle(bucket)
```

## Glacier Family Comparison

| Feature | Glacier Instant | Glacier Flexible | Glacier Deep Archive |
|---|---|---|---|
| **Retrieval time** | **Milliseconds** | Minutes to hours | 12-48 hours |
| **Min storage duration** | 90 days | 90 days | 180 days |
| **Storage cost** | Low | Lower | Lowest |
| **Retrieval cost** | Higher | Medium | Lower |
| **Restore required?** | **No** | Yes | Yes |
| **Use case** | Rapid archive access | Backup/DR, compliance | Deepest archival |

## Cost Analysis

| Scenario | Standard | Glacier IR | Savings |
|---|---|---|---|
| 1 GB stored 12 months, never accessed | $0.276 | ~$0.108 | **61%** |
| 1 GB stored 12 months, accessed 1x | $0.286 | ~$0.118 | **59%** |
| 1 TB stored 12 months, never accessed | $282.00 | ~$108.00 | **62%** |
| 1 TB stored 12 months, accessed 10x | $382.00 | ~$208.00 | **46%** |

## Exam Tips

### 1. "Instant" means milliseconds
Glacier Instant Retrieval objects can be read **immediately** — no restore initiation needed. This is the key differentiator from Glacier Flexible and Deep Archive.

### 2. Minimum 90 days
Deleting a Glacier IR object before 90 days incurs a charge for the remaining days.

### 3. Cost per GB retrieved
Glacier IR has retrieval costs, unlike Standard. But unlike Glacier Flexible, there's no per-request restore fee.

### 4. Common Exam Question
**Q:** You need to archive data for 7 years but may need instantaneous access for compliance audits. Which storage class?
**A:** Glacier Instant Retrieval (not Standard — too expensive; not Glacier Flexible — too slow)

## Exam Quick Reference
- ✅ **Millisecond retrieval** — fastest in Glacier family
- ✅ **No restore required** — read directly like Standard
- ✅ **90-day minimum** storage duration
- ✅ **128 KB minimum** billable object size
- ✅ Storage cost ~68% less than Standard
- ✅ Best for archives that may need **immediate access**
- ✅ **Not suitable** for frequently accessed data