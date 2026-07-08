# SSE-KMS (Server-Side Encryption with AWS KMS Keys)

SSE-KMS provides **server-side encryption** using **AWS Key Management Service** (KMS) keys, giving you **control over key management**, **audit trails**, and **separation of duties**.

## How It Works

```
Client uploads with SSE-KMS → S3 requests KMS to encrypt → Stores encrypted data
Client requests object → S3 requests KMS to decrypt → Returns plaintext
```

- **Key management**: Customer-managed via KMS
- **Encryption algorithm**: AES-256 (via KMS)
- **Key rotation**: Optional (automatic or manual)
- **Audit trail**: ✅ Full CloudTrail logging of every KMS API call
- **Additional cost**: **KMS key usage charges apply**
- **Control**: Create, rotate, disable, and audit keys

## Key Types

| Key Type | Description | Use Case |
|---|---|---|
| **AWS Managed KMS Key** (aws/s3) | Default KMS key for S3 | Simple setup, free |
| **Customer Managed Key** (CMK) | You create and manage | More control, auditability |
| **Multi-Region Key** | Replicated across regions | Cross-region replication with encryption |

## CLI Commands

```bash
# Upload with SSE-KMS (using default aws/s3 key)
aws s3 cp file.txt s3://my-bucket/file.txt --sse aws:kms

# Upload with SSE-KMS (using specific KMS key)
aws s3api put-object \
  --bucket my-bucket \
  --key file.txt \
  --body file.txt \
  --server-side-encryption aws:kms \
  --ssekms-key-id arn:aws:kms:us-east-1:123456789012:key/abc123-...

# Upload with SSE-KMS using s3 cp
aws s3 cp secret.txt s3://my-bucket/secret.txt \
  --sse aws:kms \
  --sse-kms-key-id alias/my-s3-key

# Set default encryption with SSE-KMS
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "aws:kms",
          "KMSMasterKeyID": "alias/my-s3-key"
        }
      }
    ]
  }'

# Check if object uses SSE-KMS
aws s3api head-object --bucket my-bucket --key file.txt \
  --query "ServerSideEncryption" --output text

# Get the KMS key ID used
aws s3api head-object --bucket my-bucket --key file.txt \
  --query "SSEKMSKeyId" --output text

# Create a KMS key for S3
aws kms create-key --description "S3 encryption key"
aws kms create-alias --alias-name alias/my-s3-key --target-key-id <key-id>

# List KMS keys
aws kms list-keys
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'
kms_key_id = 'arn:aws:kms:us-east-1:123456789012:key/abc123-...'

# Upload with SSE-KMS
def upload_with_sse_kms(bucket, key, file_path, kms_key_id=None):
    """Upload a file encrypted with SSE-KMS"""
    extra_args = {
        'ServerSideEncryption': 'aws:kms'
    }
    if kms_key_id:
        extra_args['SSEKMSKeyId'] = kms_key_id
    
    s3.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
    print(f"Uploaded {key} with SSE-KMS")

upload_with_sse_kms(bucket, 'confidential.pdf', 'confidential.pdf', kms_key_id)

# Enable default SSE-KMS on bucket
def enable_default_sse_kms(bucket, kms_key_alias='alias/my-s3-key'):
    """Set default SSE-KMS encryption on bucket"""
    s3.put_bucket_encryption(
        Bucket=bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': kms_key_alias
                    }
                }
            ]
        }
    )
    print(f"Default SSE-KMS encryption enabled on {bucket}")

enable_default_sse_kms(bucket)

# List objects encrypted with SSE-KMS
def list_kms_encrypted_objects(bucket, prefix=''):
    """List objects that use SSE-KMS"""
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            head = s3.head_object(Bucket=bucket, Key=obj['Key'])
            if head.get('ServerSideEncryption') == 'aws:kms':
                print(f"  {obj['Key']} (KMS key: {head.get('SSEKMSKeyId', 'N/A')})")

list_kms_encrypted_objects(bucket)

# Download KMS-encrypted object (automatic decryption)
def download_kms_object(bucket, key, local_path):
    """Download a KMS-encrypted object (automatically decrypted)"""
    response = s3.get_object(Bucket=bucket, Key=key)
    with open(local_path, 'wb') as f:
        f.write(response['Body'].read())
    print(f"Downloaded and decrypted {key} to {local_path}")

download_kms_object(bucket, 'confidential.pdf', 'confidential-decrypted.pdf')
```

## KMS Key Policy for S3

To allow an IAM role/user to use SSE-KMS, you need a KMS key policy like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/S3EncryptionRole"
      },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "Resource": "*"
    }
  ]
}
```

## SSE-S3 vs SSE-KMS

| Feature | SSE-S3 | SSE-KMS |
|---|---|---|
| **Key management** | AWS managed | Customer managed |
| **Cost** | Free | KMS charges apply |
| **Audit trail** | ❌ No | ✅ Yes (CloudTrail) |
| **Key rotation** | Automatic | Optional (auto/manual) |
| **Separate permissions** | No | Yes (kms:Encrypt, kms:Decrypt) |
| **Multi-region keys** | N/A | ✅ Supported |
| **Performance** | Faster | Slightly slower (KMS API call) |

## Exam Tips

### 1. KMS API Rate Limits
SSE-KMS makes a KMS API call for every upload/download. KMS has rate limits (~5,500-30,000 requests per second per region). For very high-throughput workloads, consider SSE-S3 instead.

### 2. KMS Key Policy
You need both S3 and KMS permissions to upload/download objects with SSE-KMS. The KMS key policy must grant the user/role access.

### 3. CloudTrail Audit
Each KMS `Encrypt` and `Decrypt` call is logged in CloudTrail, giving you a full audit trail of when objects were accessed.

### 4. Default Encryption
You can set SSE-KMS as the default encryption on a bucket. All objects without explicit encryption will use SSE-KMS.

### 5. Common Exam Question
**Q:** A hospital needs to encrypt medical records in S3 and must track who accesses the data. Which encryption should they use?
**A:** SSE-KMS with a customer-managed key. SSE-S3 doesn't provide audit trails, and SSE-C requires managing keys client-side.

## Exam Quick Reference
- ✅ **Customer-managed keys** via KMS
- ✅ **Full audit trail** (CloudTrail logs every KMS API call)
- ✅ **Additional cost** (KMS key usage)
- ✅ **Separate permissions** (S3 + KMS)
- ✅ **Key rotation**: Manual or automatic
- ✅ **Multi-region keys** supported
- ✅ **KMS rate limits** may affect high-throughput workloads
- ✅ Best for **compliance, regulated industries, audit requirements**