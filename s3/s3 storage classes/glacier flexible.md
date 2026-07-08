# S3 Glacier Flexible Retrieval

Glacier Flexible Retrieval is for **archive data** that can tolerate retrieval times of **minutes to hours** — the traditional Glacier tier, ideal for backup, DR, and compliance.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.99% (after restore) |
| **AZ Coverage** | ≥ 3 Availability Zones |
| **Minimum object size** | 40 KB (billed as 40 KB if smaller) |
| **Minimum storage duration** | 90 days |
| **Retrieval time** | **1-5 minutes** (Expedited), **3-5 hours** (Standard), **5-12 hours** (Bulk) |
| **Retrieval cost** | Per GB + per request |
| **Storage cost** | ~80% less than Standard |
| **Restore required?** | **Yes** — must initiate restore before reading |

## Retrieval Options

| Option | Time | Cost | Use Case |
|---|---|---|---|
| **Expedited** | 1-5 minutes | Highest | Urgent access — emergency recovery |
| **Standard** | 3-5 hours | Medium | Default choice — most common |
| **Bulk** | 5-12 hours | Lowest | Large datasets, no urgency |

## When to Use Glacier Flexible

### Good Use Cases
- **Backup archives** — data you keep "just in case"
- **Disaster recovery** — secondary DR site copies
- **Compliance archives** — regulatory retention (SOX, HIPAA, GDPR)
- **Historical data** — old logs, records, transaction data
- **Media archives** — raw footage, finished projects
- **Scientific/research data** — large datasets rarely accessed

### Not Ideal For
- Data needing immediate access (use Glacier Instant or Standard)
- Frequently accessed data (retrieval costs add up)
- Short-lived data (< 90 days)
- Very time-sensitive DR with < 1 hour RTO

## CLI Commands

```bash
# Upload directly to Glacier Flexible
aws s3 cp backup.tar.gz s3://my-bucket/backups/backup.tar.gz \
  --storage-class GLACIER

# Transition via lifecycle
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "to-glacier",
      "Status": "Enabled",
      "Filter": {"Prefix": "long-term/"},
      "Transitions": [{"Days": 365, "StorageClass": "GLACIER"}]
    }]
  }'

# Initiate a restore (required before reading)
aws s3api restore-object \
  --bucket my-bucket \
  --key backups/backup.tar.gz \
  --restore-request '{"Days": 7, "GlacierJobParameters": {"Tier": "Standard"}}'

# Expedited restore (faster, more expensive)
aws s3api restore-object \
  --bucket my-bucket \
  --key backups/backup.tar.gz \
  --restore-request '{"Days": 1, "GlacierJobParameters": {"Tier": "Expedited"}}'

# Check restore status
aws s3api head-object --bucket my-bucket --key backups/backup.tar.gz \
  --query "Restore" --output text

# Copy restored object to Standard if you need frequent access
aws s3 cp s3://my-bucket/backups/backup.tar.gz s3://my-bucket/backups/backup.tar.gz \
  --storage-class STANDARD
```

## Python (boto3) Examples

```python
import boto3
import time

s3 = boto3.client('s3')
bucket = 'my-bucket'
key = 'backups/archive.tar.gz'

# Upload to Glacier
s3.upload_file(
    'archive.tar.gz',
    bucket,
    key,
    ExtraArgs={'StorageClass': 'GLACIER'}
)
print("Uploaded as GLACIER")

# Restore object
def restore_glacier_object(bucket, key, days=7, tier='Standard'):
    """Initiate restore and check status"""
    # Initiate restore
    s3.restore_object(
        Bucket=bucket,
        Key=key,
        RestoreRequest={
            'Days': days,
            'GlacierJobParameters': {'Tier': tier}
        }
    )
    print(f"Restore initiated (tier: {tier}, duration: {days} days)")
    
    # Poll for completion
    print("Waiting for restore to complete...")
    while True:
        response = s3.head_object(Bucket=bucket, Key=key)
        restore_status = response.get('Restore', '')
        
        if 'ongoing-request="false"' in restore_status:
            print("✅ Restore complete!")
            break
        elif 'ongoing-request="true"' in restore_status:
            print("  Still restoring...")
            time.sleep(30)  # Check every 30 seconds
        else:
            print(f"  Status: {restore_status}")
            time.sleep(30)
    
    # Now we can download
    response = s3.get_object(Bucket=bucket, Key=key)
    print(f"Downloaded {len(response['Body'].read())} bytes")

# restore_glacier_object(bucket, key, tier='Standard')

# List Glacier objects needing restore
def list_glacier_objects(bucket, prefix=''):
    """List all GLACIER objects and their restore status"""
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            sc = obj.get('StorageClass', 'STANDARD')
            if sc == 'GLACIER':
                # Need head-object to get restore status
                head = s3.head_object(Bucket=bucket, Key=obj['Key'])
                restore = head.get('Restore', 'Not restored')
                print(f"  {obj['Key']}: {restore[:50]}...")

list_glacier_objects(bucket)
```

## Restore Workflow

```
1. Object is in GLACIER state
2. Call restore-object with tier (Expedited/Standard/Bulk)
3. Wait for restore to complete (check Restore header)
4. Object becomes accessible for the specified Days
5. After Days expire, object returns to GLACIER state
```

## Cost Analysis (us-east-1, per GB/month)

| Scenario | Standard Cost | Glacier Cost | Savings |
|---|---|---|---|
| 1 TB stored 1 year | $282.00 | ~$36.00 | **87%** |
| 10 TB stored 1 year | $2,820.00 | ~$360.00 | **87%** |
| 1 TB + 1 restore/year | $282.00 | ~$46.00 | **84%** |

## Exam Tips

### 1. Restore is REQUIRED
Objects in Glacier Flexible cannot be read directly. You must initiate a restore and wait for it to complete. This is the most common exam mistake.

### 2. Three retrieval tiers
- **Expedited** (1-5 mins) — most expensive, for urgent needs
- **Standard** (3-5 hours) — default, good balance
- **Bulk** (5-12 hours) — cheapest, for large datasets

### 3. Provisioned capacity for Expedited
For guaranteed Expedited retrieval, provision capacity in advance — otherwise Expedited may fall back to Standard during high demand.

### 4. Minimum 90 days
Deleting before 90 days incurs a prorated charge for remaining days.

### 5. Restore Duration
You specify how many days the restored copy is accessible (e.g., 1, 7, 30 days). After that, the object goes back to Glacier.

## Exam Scenario

**Question:** A company needs to store tax records for 7 years. Records are rarely accessed but must be retrievable within 4 hours for compliance audits.

**Answer:** Glacier Flexible Retrieval with Standard tier restore (3-5 hours meets their 4-hour SLA). If they needed "immediate" access, use Glacier Instant. If they need 12+ hours and lowest cost, use Deep Archive.

## Exam Quick Reference
- ✅ **Restore required** before reading — critical exam point
- ✅ **3 retrieval tiers**: Expedited (1-5 min), Standard (3-5 hr), Bulk (5-12 hr)
- ✅ **90-day minimum** storage duration
- ✅ **40 KB minimum** billable object size
- ✅ Storage cost ~80% less than Standard
- ✅ Best for **backup, DR, compliance archives**
- ✅ **GLACIER** is the API name (not GLACIER_FLEXIBLE)