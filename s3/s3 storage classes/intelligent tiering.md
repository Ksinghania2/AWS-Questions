# S3 Intelligent-Tiering

Intelligent-Tiering **automatically moves data** between access tiers based on changing access patterns, eliminating the cost overhead of manual lifecycle management.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.9% |
| **AZ Coverage** | ≥ 3 Availability Zones |
| **Minimum object size** | 0 bytes |
| **Minimum storage duration** | 30 days (for Archive Access tiers) |
| **Monitoring fee** | Small monthly monitoring/automation fee per object |
| **Retrieval cost** | No retrieval fee (unlike IA classes) |

## How It Works

Intelligent-Tiering has **5 access tiers**:

| Tier | Access Frequency | Cost |
|---|---|---|
| **Frequent Access** | Accessed regularly | Same as Standard |
| **Infrequent Access** | 30+ days no access | Same as Standard-IA |
| **Archive Instant Access** | 90+ days no access | Same as Glacier Instant Retrieval |
| **Archive Access (optional)** | 90+ days (configurable: 90/180/270/365 days) | Same as Glacier Flexible Retrieval |
| **Deep Archive Access (optional)** | 180+ days (configurable: 180/270/365 days) | Same as Glacier Deep Archive |

The monitoring fee is only charged for objects **not in the Frequent Access tier** (typically ~$0.0025 per 1,000 objects).

## When to Use Intelligent-Tiering

### Good Use Cases
- **Unknown access patterns** — you don't know how often data will be accessed
- **Changing access patterns** — data that starts hot but becomes cold over time
- **Data lakes** — where different datasets have different access frequencies
- **Customer uploads** — some files accessed often, some never
- **Avoiding manual lifecycle management** — set it and forget it

### Not Ideal For
- Predictable access patterns (manual lifecycle is cheaper)
- Very small objects (monitoring fee may outweigh savings)
- Objects smaller than 128 KB (no savings in Infrequent Access tier)
- Data that must be archived for compliance (use explicit Glacier tiers)

## CLI Commands

```bash
# Upload to Intelligent-Tiering
aws s3 cp file.txt s3://my-bucket/file.txt --storage-class INTELLIGENT_TIERING

# Sync directory
aws s3 sync ./data/ s3://my-bucket/data/ --storage-class INTELLIGENT_TIERING

# Change existing object to Intelligent-Tiering
aws s3 cp s3://my-bucket/data.csv s3://my-bucket/data.csv \
  --storage-class INTELLIGENT_TIERING

# Check current tier of an Intelligent-Tiering object
aws s3api head-object --bucket my-bucket --key data.csv \
  --query "StorageClass" --output text

# Note: Current tier info is in the response header
aws s3api head-object --bucket my-bucket --key data.csv

# Enable Archive Access tier (optional)
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket my-bucket \
  --id "ArchiveConfig" \
  --intelligent-tiering-configuration '{
    "Id": "ArchiveConfig",
    "Status": "Enabled",
    "Tierings": [
      {"Days": 90, "AccessTier": "ARCHIVE_ACCESS"},
      {"Days": 180, "AccessTier": "DEEP_ARCHIVE_ACCESS"}
    ]
  }'
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload to Intelligent-Tiering
s3.upload_file(
    'data.csv',
    bucket,
    'analytics/data.csv',
    ExtraArgs={'StorageClass': 'INTELLIGENT_TIERING'}
)
print("Uploaded to Intelligent-Tiering")

# List Intelligent-Tiering objects
def list_intelligent_tiering_objects(bucket, prefix=''):
    """List all Intelligent-Tiering objects"""
    paginator = s3.get_paginator('list_objects_v2')
    count = 0
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            sc = obj.get('StorageClass', 'STANDARD')
            if sc == 'INTELLIGENT_TIERING':
                count += 1
                print(f"  {obj['Key']} ({obj['Size']/1024:.1f} KB)")
    
    print(f"Total Intelligent-Tiering objects: {count}")
    return count

list_intelligent_tiering_objects(bucket)

# Configure Intelligent-Tiering with Archive Access
def configure_intelligent_tiering(bucket):
    """Enable Intelligent-Tiering with optional Archive tiers"""
    config = {
        'Id': 'MyIntelligentTieringConfig',
        'Status': 'Enabled',
        'Tierings': [
            {
                'Days': 90,
                'AccessTier': 'ARCHIVE_ACCESS'
            },
            {
                'Days': 365,
                'AccessTier': 'DEEP_ARCHIVE_ACCESS'
            }
        ]
    }
    
    s3.put_bucket_intelligent_tiering_configuration(
        Bucket=bucket,
        Id='MyIntelligentTieringConfig',
        IntelligentTieringConfiguration=config
    )
    print("Intelligent-Tiering Archive Access configured")

configure_intelligent_tiering(bucket)

# Cost comparison: Intelligent-Tiering vs manual lifecycle
def cost_comparison(object_count, total_gb, access_count_per_month):
    """Compare costs for different strategies"""
    # Intelligent-Tiering monitoring fee
    it_monitoring = (object_count / 1000) * 0.0025  # $0.0025 per 1,000 objects
    
    # Assume 50% of data stays in Frequent, 50% in Infrequent
    frequent_gb = total_gb * 0.5
    infrequent_gb = total_gb * 0.5
    
    frequent_cost = frequent_gb * 0.023
    infrequent_cost = infrequent_gb * 0.0125
    it_total = frequent_cost + infrequent_cost + it_monitoring
    
    # Manual Standard + lifecycle
    manual_total = total_gb * 0.023  # All Standard
    
    print(f"Objects: {object_count}, Storage: {total_gb:.1f} GB")
    print(f"Intelligent-Tiering: \${it_total:.2f}/month")
    print(f"All Standard:        \${manual_total:.2f}/month")
    
    if it_total < manual_total:
        print(f"✅ Intelligent-Tiering saves \${manual_total - it_total:.2f}/month")
    else:
        print("❌ Standard is cheaper (data too frequently accessed)")

cost_comparison(10000, 500, 100000)
```

## Exam Scenarios

### Scenario 1: Unknown Access Pattern
**Problem:** A media company uploads thousands of videos daily. Access patterns are unpredictable — some go viral, most are never watched.
**Solution:** Use Intelligent-Tiering. Frequently accessed videos stay in the Frequent tier; rarely accessed ones auto-move to Infrequent tier.

### Scenario 2: Long-term Data Lake
**Problem:** A data lake stores 10 years of analytics data. Recent data is queried daily, older data is queried quarterly or never.
**Solution:** Intelligent-Tiering with Archive Access enabled. After 90 days, data moves to Archive Instant. After 365 days, data moves to Deep Archive.

### Scenario 3: Avoiding Lifecycle Management
**Problem:** The operations team doesn't want to maintain complex lifecycle rules for every bucket.
**Solution:** Use Intelligent-Tiering as the default storage class. No lifecycle rules needed.

## Intelligent-Tiering vs Lifecycle Rules

| Aspect | Intelligent-Tiering | Lifecycle Rules |
|---|---|---|
| **Automation** | Fully automatic | Rule-based, manual setup |
| **Flexibility** | Pre-defined tiers | Any class, any timing |
| **Cost** | Monitoring fee per object | No monitoring fee |
| **Control** | Less control | Full control over transitions |
| **Best for** | Unknown/changing patterns | Well-known, predictable patterns |

## Exam Quick Reference
- ✅ **Automatically moves** objects between access tiers
- ✅ **No retrieval fees** (unlike IA/Glacier classes)
- ✅ **Monitoring fee** only for objects not in Frequent Access tier
- ✅ **5 access tiers** (Frequent, Infrequent, Archive Instant, Archive, Deep Archive)
- ✅ **Archive/Deep Archive tiers** are optional (enable if needed)
- ✅ Best for **unpredictable access patterns**
- ✅ **No minimum storage duration** for Frequent/Infrequent tiers