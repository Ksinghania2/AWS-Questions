# S3 Glacier Deep Archive

Glacier Deep Archive is the **lowest-cost** storage class in S3, designed for data that is accessed **rarely** (once or twice per year) and can tolerate **12-48 hour retrieval times**.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.99% (after restore) |
| **AZ Coverage** | ≥ 3 Availability Zones |
| **Minimum object size** | 40 KB (billed as 40 KB if smaller) |
| **Minimum storage duration** | **180 days** |
| **Retrieval time** | **12 hours** (Standard), **48 hours** (Bulk) |
| **Retrieval cost** | Per GB + per request |
| **Storage cost** | ~95% less than Standard |
| **Restore required?** | **Yes** — must initiate restore before reading |

## Retrieval Options

| Option | Time | Cost | Use Case |
|---|---|---|---|
| **Standard** | 12 hours | Medium | Default — most common |
| **Bulk** | 48 hours | Lowest | Large datasets, no urgency |

> **Note:** Deep Archive does NOT have an Expedited retrieval option (unlike Glacier Flexible).

## When to Use Glacier Deep Archive

### Good Use Cases
- **Regulatory archives** — 7+ year retention (SOX, HIPAA, GDPR)
- **Scientific data** — research data that may never be accessed again
- **Media masters** — original raw footage kept for legal/archival purposes
- **Old backups** — backup tapes/files that are kept "just in case"
- **Financial records** — transaction data retained for regulatory compliance
- **Security logs** — logs retained for forensic investigation (rarely needed)

### Not Ideal For
- Data that may need access within hours (use Glacier Flexible)
- Data needing immediate access (use Glacier Instant or Standard)
- Frequently accessed data (retrieval costs make it expensive)
- Short-lived data (< 180 days)
- DR with RTO < 12 hours

## CLI Commands

```bash
# Upload directly to Deep Archive
aws s3 cp old-records.tar.gz s3://my-bucket/archives/old-records.tar.gz \
  --storage-class DEEP_ARCHIVE

# Transition via lifecycle
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "to-deep-archive",
      "Status": "Enabled",
      "Filter": {"Prefix": "compliance/"},
      "Transitions": [{"Days": 365, "StorageClass": "DEEP_ARCHIVE"}]
    }]
  }'

# Initiate restore (12-48 hours)
aws s3api restore-object \
  --bucket my-bucket \
  --key archives/old-records.tar.gz \
  --restore-request '{"Days": 7, "GlacierJobParameters": {"Tier": "Standard"}}'

# Bulk restore (cheaper, 48 hours)
aws s3api restore-object \
  --bucket my-bucket \
  --key archives/old-records.tar.gz \
  --restore-request '{"Days": 7, "GlacierJobParameters": {"Tier": "Bulk"}}'

# Check restore status
aws s3api head-object --bucket my-bucket --key archives/old-records.tar.gz \
  --query "Restore" --output text

# List all Deep Archive objects
aws s3api list-objects-v2 --bucket my-bucket \
  --query "Contents[?StorageClass=='DEEP_ARCHIVE'].[Key,Size]" \
  --output table
```

## Python (boto3) Examples

```python
import boto3
import time

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload to Deep Archive
s3.upload_file(
    'compliance-records-2020.tar.gz',
    bucket,
    'compliance/2020/records.tar.gz',
    ExtraArgs={'StorageClass': 'DEEP_ARCHIVE'}
)
print("Uploaded as DEEP_ARCHIVE")

# Initiate and monitor restore
def restore_deep_archive(bucket, key, days=7, tier='Standard'):
    """Restore a Deep Archive object and wait for completion"""
    print(f"Initiating {tier} restore for {key}...")
    
    s3.restore_object(
        Bucket=bucket,
        Key=key,
        RestoreRequest={
            'Days': days,
            'GlacierJobParameters': {'Tier': tier}
        }
    )
    
    # Poll for completion
    print("Waiting for restore (this may take 12-48 hours)...")
    print("In production, use S3 Event Notifications or SQS instead of polling")
    
    for i in range(10):  # Check 10 times with 30-second intervals
        response = s3.head_object(Bucket=bucket, Key=key)
        restore = response.get('Restore', '')
        
        if 'ongoing-request="false"' in restore:
            print("✅ Restore complete!")
            return True
        elif 'ongoing-request="true"' in restore:
            print(f"  Check {i+1}: Still restoring...")
            time.sleep(30)
        else:
            print(f"  Status: {restore}")
            time.sleep(30)
    
    print("Restore still in progress. Check back later.")
    return False

# restore_deep_archive(bucket, 'compliance/2020/records.tar.gz')

# Calculate cost savings
def deep_archive_cost_savings(bucket, prefix=''):
    """Compare costs across storage classes"""
    paginator = s3.get_paginator('list_objects_v2')
    total_bytes = 0
    count = 0
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            total_bytes += obj['Size']
            count += 1
    
    gb = total_bytes / (1024**3)
    
    print(f"Storage: {gb:.2f} GB in {count} objects\n")
    print("Annual cost comparison (us-east-1):")
    print(f"  Standard:        ${gb * 0.023 * 12:.2f}")
    print(f"  Standard-IA:     ${gb * 0.0125 * 12:.2f}")
    print(f"  Glacier Flexible: ${gb * 0.0036 * 12:.2f}")
    print(f"  Glacier Deep Archive: ${gb * 0.00099 * 12:.2f}")
    print(f"\nSavings with Deep Archive:")
    print(f"  vs Standard:  {((gb*0.023*12) - (gb*0.00099*12)) / (gb*0.023*12) * 100:.0f}%")

deep_archive_cost_savings(bucket)
```

## Cost Comparison (Annual, us-east-1)

| Storage Class | 1 TB/Year | 10 TB/Year | 100 TB/Year |
|---|---|---|---|
| **Standard** | $282.00 | $2,820.00 | $28,200.00 |
| **Standard-IA** | $153.00 | $1,530.00 | $15,300.00 |
| **Glacier Flexible** | $43.20 | $432.00 | $4,320.00 |
| **Glacier Deep Archive** | **$11.88** | **$118.80** | **$1,188.00** |

## Storage Class Lifecycle Path

```
Standard (Day 0)
  ↓ 30 days
Standard-IA (Day 30)
  ↓ 90 days
Glacier Instant (Day 120)
  ↓ 90 days
Glacier Flexible (Day 210)
  ↓ 180 days
Glacier Deep Archive (Day 390)
  ↓ 2555 days (7 years)
Expire (Delete)
```

## Exam Tips

### 1. 180-Day Minimum
Deep Archive has the longest minimum storage duration (180 days). Deleting before 180 days incurs a prorated charge.

### 2. No Expedited Retrieval
Unlike Glacier Flexible, Deep Archive does NOT have an Expedited retrieval option. Maximum speed is 12 hours (Standard tier).

### 3. 40 KB Minimum
Objects smaller than 40 KB are billed as 40 KB.

### 4. Common Exam Question
**Q:** A company needs to store financial records for 10 years. They expect to access them at most once per year for audits. What is the MOST cost-effective storage?
**A:** S3 Glacier Deep Archive (lowest cost, 12-hour retrieval is acceptable for annual audits)

### 5. Restore Required
Like Glacier Flexible, you MUST initiate a restore before reading. The object is not directly accessible.

## Exam Quick Reference
- ✅ **Lowest cost** storage class in S3
- ✅ **180-day minimum** storage duration
- ✅ **40 KB minimum** billable object size
- ✅ **12 hours** (Standard) or **48 hours** (Bulk) retrieval
- ✅ **No Expedited** retrieval option
- ✅ **Restore required** before reading
- ✅ Best for **long-term archival, compliance, regulatory retention**
- ✅ ~95% cheaper than Standard