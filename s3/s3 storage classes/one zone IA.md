# S3 One Zone-IA Storage Class

One Zone-IA stores data in a **single Availability Zone**, making it the least resilient but most cost-effective infrequent access option.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.5% |
| **AZ Coverage** | **1** Availability Zone (⚠️ risk if AZ fails) |
| **Minimum object size** | 128 KB (billed as 128 KB if smaller) |
| **Minimum storage duration** | 30 days |
| **Retrieval cost** | Per GB retrieved |
| **Use case** | Non-critical, reproducible, or secondary data |

## When to Use One Zone-IA

### Good Use Cases
- **Secondary backup copies** (primary is in Standard or another region)
- **Replicable data** — data you can regenerate if lost
- **Transient data** — logs or temp files that can be recreated
- **Non-critical media** — thumbnails, transcoded copies
- **Cross-Region Replication destination** — if source still has the original

### ⚠️ Not Suitable For
- Primary data that would be expensive to recreate
- Compliance data requiring multi-AZ durability
- Data that must survive an AZ failure
- Critical business records or customer data

## CLI Commands

```bash
# Upload directly to One Zone-IA
aws s3 cp temp-data.txt s3://my-bucket/temp/temp-data.txt \
  --storage-class ONEZONE_IA

# Sync directory to One Zone-IA
aws s3 sync ./cache/ s3://my-bucket/cache/ --storage-class ONEZONE_IA

# Change existing object to One Zone-IA
aws s3 cp s3://my-bucket/data.json s3://my-bucket/data.json \
  --storage-class ONEZONE_IA

# Check storage class of an object
aws s3api head-object --bucket my-bucket --key temp/temp-data.txt \
  --query "StorageClass" --output text

# List all One Zone-IA objects
aws s3api list-objects-v2 --bucket my-bucket \
  --query "Contents[?StorageClass=='ONEZONE_IA'].[Key,Size]" \
  --output table

# Lifecycle rule to transition to One Zone-IA
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "to-onezone-ia",
      "Status": "Enabled",
      "Filter": {"Prefix": "cache/"},
      "Transitions": [{"Days": 1, "StorageClass": "ONEZONE_IA"}]
    }]
  }'
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload to One Zone-IA
s3.upload_file(
    'temp-processed-file.json',
    bucket,
    'processing/temp-file.json',
    ExtraArgs={'StorageClass': 'ONEZONE_IA'}
)
print("Uploaded as ONEZONE_IA")

# List objects by storage class
def list_by_storage_class(bucket, storage_class='ONEZONE_IA'):
    """List all objects with a specific storage class"""
    paginator = s3.get_paginator('list_objects_v2')
    matching = []
    
    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get('Contents', []):
            if obj.get('StorageClass', 'STANDARD') == storage_class:
                matching.append(obj['Key'])
    
    print(f"Objects with {storage_class}: {len(matching)}")
    for key in matching[:10]:  # Show first 10
        print(f"  {key}")
    return matching

list_by_storage_class(bucket)

# Estimate savings vs Standard-IA
def compare_onezone_cost(bucket, prefix=''):
    """Compare costs: Standard vs Standard-IA vs One Zone-IA"""
    from datetime import datetime
    
    total_bytes = 0
    total_objects = 0
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            total_bytes += obj['Size']
            total_objects += 1
    
    gb = total_bytes / (1024**3)
    
    print(f"Storage: {gb:.2f} GB in {total_objects} objects\n")
    print("Monthly cost comparison (us-east-1):")
    print(f"  Standard:      ${gb * 0.023:.2f}")
    print(f"  Standard-IA:   ${gb * 0.0125:.2f} (plus retrieval fees)")
    print(f"  One Zone-IA:   ${gb * 0.01:.2f}  (plus retrieval fees)")
    print(f"\nPotential savings with One Zone-IA:")
    print(f"  vs Standard:    ${gb * 0.013:.2f}/month ({gb * 0.013 / (gb * 0.023) * 100:.0f}%)")
```

## When to Choose One Zone-IA vs Standard-IA vs Standard

| Factor | Standard | Standard-IA | One Zone-IA |
|---|---|---|---|
| **Cost** | Highest | Medium | **Lowest** |
| **Durability** | 11 9's (3+ AZs) | 11 9's (3+ AZs) | 11 9's (1 AZ) |
| **Availability** | 99.99% | 99.9% | 99.5% |
| **AZ failure** | Survives | Survives | **Data lost** |
| **Best for** | Critical data | Infrequent access | Non-critical, reproducible |

### Decision Guide
```
Can the data be recreated if the AZ fails?
├── NO  → Use Standard or Standard-IA
└── YES → Is the data accessed infrequently?
    ├── YES → One Zone-IA ✅
    └── NO  → Standard (but reconsider if One Zone-IA is appropriate)
```

## Exam Tips

### 1. Key Exam Differentiator
One Zone-IA is the **only** storage class that stores data in a **single Availability Zone**. If you see a question about cost savings where data can be recreated, this is the answer.

### 2. Common Exam Scenario
**Question:** A company stores thumbnail images that can be regenerated from originals. They want the lowest storage cost for infrequently accessed thumbnails.
**Answer:** S3 One Zone-IA (not Glacier — thumbnails need quick access, not archival).

### 3. Important Caveats
- **Not suitable for primary data** — you MUST be able to recreate the data
- **Same minimums as Standard-IA**: 128 KB minimum, 30-day minimum
- **11 9's durability** still applies (within that one AZ — but AZ failure = data loss)
- **Cannot use** with S3 Object Lock (requires multi-AZ)
- **Cannot use** with some compliance features

## Exam Quick Reference
- ✅ **Single AZ** — risk of data loss if AZ fails
- ✅ **Lowest cost** among IA classes
- ✅ **128 KB minimum** billable size
- ✅ **30-day minimum** storage duration
- ✅ **99.5% availability**
- ✅ Best for **recreatable, non-critical, secondary data**
- ✅ **Not suitable** for compliance or primary data