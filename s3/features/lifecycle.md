# S3 Lifecycle Rules

Lifecycle rules **automate transitions** between storage classes and **expire** objects based on age, helping you optimize costs automatically.

## What Lifecycle Rules Can Do

### Transition Actions
Move objects to cheaper storage classes after a specified number of days:

| Transition | Days | Target Class |
|---|---|---|
| Standard → Standard-IA | 30 days | STANDARD_IA |
| Standard-IA → Glacier Instant | 90 days | GLACIER_IR |
| Glacier Instant → Glacier Flexible | 120 days | GLACIER |
| Glacier Flexible → Deep Archive | 180 days | DEEP_ARCHIVE |

### Expiration Actions
Delete objects after a specified period:

| Expiration | Days | Effect |
|---|---|---|
| Current version | After N days | Permanently deleted |
| Previous versions | After N days | Permanently deleted |
| Incomplete multipart uploads | After N days | Aborted and cleaned up |

## CLI Commands

```bash
# Create a lifecycle rule that transitions old data to IA, then Glacier
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "archive-rule",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"},
        {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
      ],
      "Expiration": {"Days": 2555}
    }]
  }'

# Rule for expiring previous versions
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "expire-old-versions",
      "Status": "Enabled",
      "Filter": {"Prefix": ""},
      "NoncurrentVersionExpiration": {"NoncurrentDays": 90}
    }]
  }'

# Abort incomplete multipart uploads
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "abort-incomplete-multipart",
      "Status": "Enabled",
      "Filter": {"Prefix": ""},
      "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}
    }]
  }'

# Get current lifecycle rules
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket

# Delete lifecycle rules
aws s3api delete-bucket-lifecycle --bucket my-bucket
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Comprehensive lifecycle rule
def setup_complete_lifecycle(bucket):
    """Set up a complete lifecycle policy"""
    lifecycle = {
        'Rules': [
            {
                'ID': 'transition-standard-to-ia',
                'Status': 'Enabled',
                'Filter': {'Prefix': ''},  # Apply to all objects
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 90, 'StorageClass': 'GLACIER'},
                    {'Days': 365, 'StorageClass': 'DEEP_ARCHIVE'}
                ]
            },
            {
                'ID': 'expire-old-versions',
                'Status': 'Enabled',
                'Filter': {'Prefix': ''},
                'NoncurrentVersionTransitions': [
                    {'NoncurrentDays': 30, 'StorageClass': 'STANDARD_IA'}
                ],
                'NoncurrentVersionExpiration': {'NoncurrentDays': 365}
            },
            {
                'ID': 'cleanup-incomplete-uploads',
                'Status': 'Enabled',
                'Filter': {'Prefix': ''},
                'AbortIncompleteMultipartUpload': {
                    'DaysAfterInitiation': 7
                }
            },
            {
                'ID': 'expire-logs-after-7-years',
                'Status': 'Enabled',
                'Filter': {
                    'And': {
                        'Prefix': 'logs/',
                        'Tags': [
                            {'Key': 'retention', 'Value': '7years'}
                        ]
                    }
                },
                'Expiration': {'Days': 2555}  # 7 years
            }
        ]
    }
    
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration=lifecycle
    )
    print("Lifecycle policy configured with 4 rules")

setup_complete_lifecycle(bucket)

# Get lifecycle info
def get_lifecycle_summary(bucket):
    """Get a summary of all lifecycle rules"""
    response = s3.get_bucket_lifecycle_configuration(Bucket=bucket)
    
    for rule in response.get('Rules', []):
        print(f"Rule: {rule['ID']}")
        print(f"  Status: {rule['Status']}")
        print(f"  Filter: {rule.get('Filter', {})}")
        
        for transition in rule.get('Transitions', []):
            print(f"  → {transition['StorageClass']} after {transition['Days']} days")
        
        if 'Expiration' in rule:
            print(f"  → Delete after {rule['Expiration']['Days']} days")
        
        if 'NoncurrentVersionExpiration' in rule:
            print(f"  → Delete noncurrent after {rule['NoncurrentVersionExpiration']['NoncurrentDays']} days")
        
        print()

get_lifecycle_summary(bucket)
```

## Common Lifecycle Patterns

### Pattern 1: Log Rotation
```
Standard (0 days) → Standard-IA (30 days) → Glacier (90 days) → Delete (365 days)
```

### Pattern 2: Backup Archival
```
Standard (0 days) → Glacier (30 days) → Deep Archive (180 days) → Delete (2555 days)
```

### Pattern 3: Version Management
```
Current version: Standard (keep permanently)
Previous versions: → Standard-IA (30 days noncurrent) → Delete (365 days noncurrent)
```

## Exam Tips

### 1. Minimum Days
Lifecycle transitions have minimum day requirements:
- Standard → IA: 30 days
- IA → Glacier: 30 days
- Standard → Glacier: 90 days (older rule)
- Any → Deep Archive: 180 days

### 2. Cannot Transition Back
Lifecycle transitions are **one-way** — you can only move to cheaper storage, never back to more expensive storage.

### 3. Tag-based Filtering
Lifecycle rules can filter by **prefix**, **tags**, or **both** (using AND condition).

### 4. Incomplete Multipart Upload Cleanup
Always add a rule to abort incomplete multipart uploads after 7 days to avoid storage costs for partial uploads.

### 5. Common Exam Question
**Q:** A company stores logs for 30 days in Standard, then wants to archive for 7 years at the lowest cost. What lifecycle rules?
**A:** Standard (0-30 days) → Standard-IA (30-90 days) → Glacier (90-365 days) → Deep Archive (365-2555 days) → Delete (2555 days).

## Exam Quick Reference
- ✅ **Transitions** move objects to cheaper storage
- ✅ **Expiration** deletes objects after N days
- ✅ **One-way** — cannot transition to more expensive classes
- ✅ **30-day minimum** between most transitions
- ✅ **Tag and prefix** filtering supported
- ✅ **Noncurrent versions** can be managed separately
- ✅ **Clean up** incomplete multipart uploads automatically