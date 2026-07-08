# S3 Standard-IA (Infrequent Access) Storage Class

Standard-IA is for **infrequently accessed** data that needs rapid access when needed. Cheaper storage than Standard, but charges a retrieval fee.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.9% |
| **AZ Coverage** | ≥ 3 Availability Zones |
| **Minimum object size** | 128 KB (billed as 128 KB if smaller) |
| **Minimum storage duration** | 30 days |
| **Retrieval cost** | Per GB retrieved |
| **Use case** | Infrequently accessed, but rapid access when needed |

## When to Use Standard-IA

### Good Use Cases
- Backup data that may be needed for restore
- Disaster recovery copies
- Older versions of files (with versioning enabled)
- Log data retained for compliance (accessed quarterly)
- Media files that are rarely watched/played
- Data that has been transitioned from Standard via lifecycle policy

### Not Ideal For
- Very small objects (< 128 KB) — you still pay for 128 KB
- Short-lived data (< 30 days) — minimum 30-day charge applies
- Frequently accessed data — retrieval costs will exceed Standard costs
- Data that needs the highest availability (99.99% vs 99.9%)

## CLI Commands

```bash
# Upload directly to Standard-IA
aws s3 cp file.txt s3://my-bucket/file.txt --storage-class STANDARD_IA

# Upload multiple files with a specific storage class
aws s3 sync ./logs/ s3://my-bucket/logs/ --storage-class STANDARD_IA

# Change existing Standard object to Standard-IA (copy to self)
aws s3 cp s3://my-bucket/file.txt s3://my-bucket/file.txt \
  --storage-class STANDARD_IA

# Check storage class
aws s3api head-object --bucket my-bucket --key file.txt \
  --query StorageClass --output text

# List all Standard-IA objects
aws s3api list-objects-v2 --bucket my-bucket \
  --query "Contents[?StorageClass=='STANDARD_IA'].[Key,Size]" \
  --output table

# Apply lifecycle rule to auto-transition to IA
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "transition-to-ia",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}]
    }]
  }'
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload to Standard-IA
s3.upload_file(
    'old-backup.zip',
    bucket,
    'backups/old-backup.zip',
    ExtraArgs={'StorageClass': 'STANDARD_IA'}
)
print("Uploaded as STANDARD_IA")

# Transition existing object
s3.copy_object(
    Bucket=bucket,
    CopySource={'Bucket': bucket, 'Key': 'data/file.json'},
    Key='data/file.json',
    StorageClass='STANDARD_IA'
)
print("Transitioned to STANDARD_IA")

# Calculate cost comparison
def cost_comparison(bucket, object_key, storage_size_bytes, days=30):
    """Compare Standard vs Standard-IA costs"""
    gb = storage_size_bytes / (1024**3)
    
    # Typical us-east-1 prices
    standard_storage = gb * 0.023 * (days / 30)  # $0.023/GB/month
    ia_storage = gb * 0.0125 * (days / 30)  # $0.0125/GB/month
    ia_retrieval = gb * 0.01  # $0.01/GB retrieval
    ia_total = ia_storage + ia_retrieval
    
    print(f"File size: {gb:.2f} GB")
    print(f"Standard storage ({days}d): \${standard_storage:.4f}")
    print(f"Standard-IA storage ({days}d): \${ia_storage:.4f}")
    print(f"Standard-IA retrieval: \${ia_retrieval:.4f}")
    print(f"Standard-IA total: \${ia_total:.4f}")
    
    if ia_total < standard_storage:
        print("✅ Standard-IA is cheaper")
    else:
        print("❌ Standard is cheaper (access too frequent)")

# Cost compare for a 1 GB file stored 30 days, retrieved once
cost_comparison(bucket, 'data/file.json', 1 * 1024**3, 30)
```

## Cost Analysis

### When Standard-IA is cheaper than Standard
| Monthly access frequency | 1 GB object | 100 GB object |
|---|---|---|
| Accessed 0 times | IA saves ~45% | IA saves ~45% |
| Accessed 1 time | IA saves ~40% | IA saves ~40% |
| Accessed 5 times | IA saves ~20% | IA saves ~20% |
| Accessed 10 times | ~break even | ~break even |
| Accessed 20+ times | Standard cheaper | Standard cheaper |

### Hidden Costs to Consider
- **Minimum 30-day charge**: Deleting after 10 days still bills for 30
- **Minimum 128 KB charge**: A 10 KB file is billed as 128 KB
- **Retrieval fee**: $0.01 per GB retrieved
- **Lifecycle transition cost**: $0.01 per 1,000 objects transitioned

## Exam Scenarios

### Scenario 1: Backup Retention
**Problem:** You have daily database backups that you keep for 90 days. You rarely need to restore.
**Solution:** Upload to Standard (for quick recent access), use lifecycle to transition to Standard-IA after 30 days.
```bash
aws s3 cp db-backup.sql.gz s3://backups/daily/2024-05-15.sql.gz
# Lifecycle rule transitions to IA after 30 days
```

### Scenario 2: Log Archives
**Problem:** Application logs are written daily. You query last 30 days frequently, older logs rarely.
**Solution:** Keep current month in Standard, transition previous months to Standard-IA.

## Comparison Table

| Feature | Standard | Standard-IA | One Zone-IA |
|---|---|---|---|
| Durability | 11 9's | 11 9's | 11 9's |
| Availability | 99.99% | 99.9% | 99.5% |
| AZs | ≥3 | ≥3 | 1 |
| Min object size | 0 bytes | 128 KB | 128 KB |
| Min duration | None | 30 days | 30 days |
| Retrieval fee | None | Yes ($0.01/GB) | Yes ($0.01/GB) |
| Storage cost | Higher | ~45% less | ~55% less |

## Exam Quick Reference
- ✅ **"Infrequent Access"** — lower storage cost, retrieval fee
- ✅ **≥3 AZs** for durability
- ✅ **128 KB minimum** billable object size
- ✅ **30-day minimum** storage duration charge
- ✅ **99.9% availability** (vs 99.99% for Standard)
- ✅ Ideal for **backups, older logs, DR copies**
- ✅ Can be set via lifecycle **transition after N days**