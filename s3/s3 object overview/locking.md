# S3 Object Lock

S3 Object Lock prevents objects from being **deleted or overwritten** for a fixed period or indefinitely. It's essential for **compliance** and **WORM** (Write Once, Read Many) storage.

## Key Concepts

### Retention Modes

| Mode | Description | Changeable? |
|---|---|---|
| **GOVERNANCE** | Users with special permissions can override | Permissions can bypass |
| **COMPLIANCE** | No one can override (not even root) | Absolutely locked |

### Retention Periods

| Setting | Description |
|---|---|
| **Retention Period** | Lock objects for a fixed number of days/years |
| **Legal Hold** | Indefinite lock until explicitly removed |

## Prerequisites
- **Versioning must be enabled** on the bucket
- Object Lock can only be enabled at **bucket creation time** (cannot be added later)

## CLI Commands

```bash
# Create bucket with Object Lock enabled
aws s3api create-bucket \
  --bucket my-locked-bucket \
  --region us-east-1 \
  --object-lock-enabled-for-bucket

# Put an object with governance retention
aws s3api put-object \
  --bucket my-locked-bucket \
  --key compliance-report.pdf \
  --body report.pdf \
  --object-lock-mode GOVERNANCE \
  --object-lock-retain-until-date 2025-12-31 \
  --object-lock-legal-hold-status ON

# Set default retention on bucket
aws s3api put-object-lock-configuration \
  --bucket my-locked-bucket \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "GOVERNANCE",
        "Days": 365
      }
    }
  }'

# Get lock configuration
aws s3api get-object-lock-configuration --bucket my-locked-bucket

# Get legal hold status of an object
aws s3api get-object-legal-hold --bucket my-locked-bucket --key report.pdf

# Get retention settings of an object
aws s3api get-object-retention --bucket my-locked-bucket --key report.pdf

# Bypass governance retention and delete (requires s3:BypassGovernanceRetention permission)
aws s3api delete-object \
  --bucket my-locked-bucket \
  --key compliance-report.pdf \
  --bypass-governance-retention \
  --version-id <version-id>
```

## Python (boto3) Examples

```python
import boto3
from datetime import datetime, timedelta

s3 = boto3.client('s3')
bucket = 'my-locked-bucket'

# Create bucket with Object Lock
def create_locked_bucket(bucket_name):
    """Create a bucket with Object Lock enabled"""
    s3.create_bucket(
        Bucket=bucket_name,
        ObjectLockEnabledForBucket=True
    )
    
    # Enable versioning (required for Object Lock)
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    
    # Set default retention
    s3.put_object_lock_configuration(
        Bucket=bucket_name,
        ObjectLockConfiguration={
            'ObjectLockEnabled': 'Enabled',
            'Rule': {
                'DefaultRetention': {
                    'Mode': 'GOVERNANCE',
                    'Days': 365
                }
            }
        }
    )
    print(f"Bucket '{bucket_name}' created with Object Lock")

# Upload with compliance mode (cannot be overridden by anyone)
def upload_compliance_locked(bucket, key, file_path):
    """Upload an object with COMPLIANCE retention (absolute lock)"""
    # Retention date = 7 years from now
    retain_until = datetime.now() + timedelta(days=365*7)
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=open(file_path, 'rb'),
        ObjectLockMode='COMPLIANCE',
        ObjectLockRetainUntilDate=retain_until
    )
    print(f"Uploaded with COMPLIANCE lock until {retain_until}")

# Upload with legal hold (indefinite lock)
def upload_with_legal_hold(bucket, key, file_path):
    """Upload an object with legal hold (indefinite)"""
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=open(file_path, 'rb'),
        ObjectLockLegalHoldStatus='ON'
    )
    print(f"Uploaded with Legal Hold")

# Remove legal hold
def remove_legal_hold(bucket, key, version_id):
    """Remove a legal hold from an object"""
    s3.put_object_legal_hold(
        Bucket=bucket,
        Key=key,
        VersionId=version_id,
        LegalHold={'Status': 'OFF'}
    )
    print(f"Legal hold removed from {key}")

# List locked objects
def list_locked_objects(bucket, prefix=''):
    """List objects and their lock status"""
    paginator = s3.get_paginator('list_object_versions')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for version in page.get('Versions', []):
            head = s3.head_object(
                Bucket=bucket,
                Key=version['Key'],
                VersionId=version['VersionId']
            )
            
            lock_mode = head.get('ObjectLockMode', 'None')
            legal_hold = head.get('ObjectLockLegalHoldStatus', 'OFF')
            
            print(f"{version['Key']} (v{version['VersionId'][:8]}):")
            print(f"  Lock Mode: {lock_mode}")
            print(f"  Legal Hold: {legal_hold}")

list_locked_objects(bucket)
```

## Compliance vs Governance

| Aspect | GOVERNANCE | COMPLIANCE |
|---|---|---|
| **Who can override** | Users with `s3:BypassGovernanceRetention` | **Nobody** (not even root) |
| **Use case** | Internal policies, temporary holds | Regulatory compliance, SEC/FINRA |
| **Changeable?** | Yes (with bypass permission) | No (absolutely final) |
| **Cost** | Same | Same |

## Object Lock Use Cases

| Use Case | Mode | Period |
|---|---|---|
| **SEC Rule 17a-4** (financial records) | COMPLIANCE | 7 years |
| **HIPAA** (medical records) | COMPLIANCE | 6 years |
| **GDPR** (personal data) | GOVERNANCE | Retention period |
| **Internal audit** | GOVERNANCE | 3 years |
| **eDiscovery** (legal hold) | Legal Hold | Indefinite |
| **Backup protection** | GOVERNANCE | 30-90 days |

## Exam Tips

### 1. Must Be Enabled at Bucket Creation
Object Lock **cannot** be added to an existing bucket. It must be enabled when the bucket is created.

### 2. Versioning Required
Object Lock requires versioning to be enabled on the bucket.

### 3. Default Retention
You can set a default retention period that applies automatically to all objects.

### 4. Legal Hold vs Retention
- **Retention Period**: Fixed time (days/years)
- **Legal Hold**: Indefinite (removed manually)

### 5. Common Exam Question
**Q:** A bank needs to store financial records for 7 years with WORM protection that cannot be overridden. What should they use?
**A:** S3 Object Lock with **COMPLIANCE** mode for 7 years retention (not GOVERNANCE, because compliance officers need to be sure records cannot be modified).

## Exam Quick Reference
- ✅ **WORM** (Write Once, Read Many) protection
- ✅ **Versioning must be enabled** first
- ✅ **Must be enabled at bucket creation** (cannot be retrofitted)
- ✅ **GOVERNANCE**: Can be bypassed with special permissions
- ✅ **COMPLIANCE**: Absolute lock, no one can override
- ✅ **Legal Hold**: Indefinite lock, manually removed
- ✅ **90-day minimum** for certain retention modes
- ✅ **Key exam topic** for financial, healthcare, and compliance scenarios