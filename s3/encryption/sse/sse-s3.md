# SSE-S3 (Server-Side Encryption with S3-Managed Keys)

SSE-S3 is the **simplest** encryption option — AWS manages the encryption keys entirely. S3 encrypts data at rest using **AES-256**.

## How It Works

```
Client uploads → S3 encrypts with AES-256 → Stores encrypted data
Client requests → S3 decrypts automatically → Returns plaintext
```

- **Key management**: Fully managed by AWS
- **Encryption algorithm**: AES-256
- **Key rotation**: Automatic (AWS handles it)
- **Audit trail**: Limited (no CloudTrail for key usage)
- **Additional cost**: **Free** (no extra charge)

## CLI Commands

```bash
# Upload with SSE-S3 encryption
aws s3 cp file.txt s3://my-bucket/file.txt --sse AES256

# Upload with SSE-S3 using s3api
aws s3api put-object \
  --bucket my-bucket \
  --key file.txt \
  --body file.txt \
  --server-side-encryption AES256

# Set default encryption on bucket (all objects encrypted by default)
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        }
      }
    ]
  }'

# Check encryption status of an object
aws s3api head-object --bucket my-bucket --key file.txt \
  --query "ServerSideEncryption" --output text

# Check default encryption on bucket
aws s3api get-bucket-encryption --bucket my-bucket

# Remove default encryption
aws s3api delete-bucket-encryption --bucket my-bucket
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload with SSE-S3
def upload_with_sse_s3(bucket, key, file_path):
    """Upload a file encrypted with SSE-S3"""
    s3.upload_file(
        file_path,
        bucket,
        key,
        ExtraArgs={'ServerSideEncryption': 'AES256'}
    )
    print(f"Uploaded {key} with SSE-S3 encryption")

upload_with_sse_s3(bucket, 'report.pdf', 'report.pdf')

# Enable default encryption on bucket
def enable_default_sse_s3(bucket):
    """Enable default SSE-S3 encryption on a bucket"""
    s3.put_bucket_encryption(
        Bucket=bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }
            ]
        }
    )
    print(f"Default SSE-S3 encryption enabled on {bucket}")

enable_default_sse_s3(bucket)

# Check if an object is encrypted
def check_encryption(bucket, key):
    """Check the encryption status of an object"""
    response = s3.head_object(Bucket=bucket, Key=key)
    sse = response.get('ServerSideEncryption', 'None')
    print(f"{key}: {sse}")
    return sse

check_encryption(bucket, 'report.pdf')

# List all objects and their encryption status
def list_encryption_status(bucket, prefix=''):
    """List all objects and their encryption status"""
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            head = s3.head_object(Bucket=bucket, Key=obj['Key'])
            sse = head.get('ServerSideEncryption', 'NONE')
            print(f"  {obj['Key']}: {sse}")

list_encryption_status(bucket)
```

## When to Use SSE-S3

| Scenario | Recommendation |
|---|---|
| **General data encryption** | ✅ SSE-S3 (simplest, free) |
| **Compliance requirements** | ✅ SSE-S3 (AES-256 is compliant) |
| **Need key audit trail** | ❌ Use SSE-KMS instead |
| **Need customer-managed keys** | ❌ Use SSE-KMS or SSE-C |
| **Need encryption for all objects** | ✅ Enable default encryption |

## Exam Tips

### 1. Default Encryption
You can set **default encryption** on a bucket. If enabled, all objects are automatically encrypted with SSE-S3 (or SSE-KMS) even if the upload doesn't specify encryption.

### 2. No Extra Cost
SSE-S3 is **free** — you only pay for S3 storage, not for the encryption itself.

### 3. Automatic Key Rotation
AWS automatically rotates the keys used by SSE-S3. You don't need to manage key rotation.

### 4. No Audit Trail
SSE-S3 does NOT provide a CloudTrail audit trail of when keys were used. For auditability, use SSE-KMS.

### 5. Common Exam Question
**Q:** A company needs to encrypt all data at rest in S3 with minimal management overhead and no additional cost. What should they use?
**A:** SSE-S3 (AES-256). It's free, fully managed, and requires no key management.

## Exam Quick Reference
- ✅ **AES-256** encryption
- ✅ **AWS-managed keys** (no customer management)
- ✅ **Free** — no additional cost
- ✅ **Automatic key rotation**
- ✅ **No audit trail** (use SSE-KMS if needed)
- ✅ Can be set as **default encryption** on bucket
- ✅ **Simplest** encryption option