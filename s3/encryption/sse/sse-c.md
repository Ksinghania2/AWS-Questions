# SSE-C (Server-Side Encryption with Customer-Provided Keys)

SSE-C allows you to provide your own encryption keys. S3 performs the encryption/decryption server-side, but **you manage and supply the keys** with every request.

## How It Works

```
Client sends: data + encryption key → S3 encrypts with provided key → Stores encrypted data + SHA-256 of key
Client requests: object + same key → S3 decrypts → Returns plaintext
```

- **Key management**: Customer managed (you provide the key)
- **Encryption algorithm**: AES-256
- **Key rotation**: Manual (you provide a new key)
- **Audit trail**: Limited
- **Additional cost**: Free (no KMS charges)
- **Key storage**: NOT stored by AWS (only the SHA-256 hash of the key is stored)

## Important Notes
- You must provide the encryption key with **every request** (upload and download)
- AWS does NOT store your key — only the SHA-256 hash is stored
- If you lose the key, **the data cannot be recovered**
- Cannot be used with bucket policies that reference keys
- Cannot be used with default bucket encryption (must be specified per-object)

## CLI Commands

```bash
# Upload with SSE-C (provide encryption key)
aws s3api put-object \
  --bucket my-bucket \
  --key encrypted-file.txt \
  --body file.txt \
  --sse-customer-algorithm AES256 \
  --sse-customer-key "Mzb5l0TCUx7Xk5xuL8R0VdG4FkOq4R0VdG4FkOq4R0="

# Download with SSE-C (must provide the same key)
aws s3api get-object \
  --bucket my-bucket \
  --key encrypted-file.txt \
  --sse-customer-algorithm AES256 \
  --sse-customer-key "Mzb5l0TCUx7Xk5xuL8R0VdG4FkOq4R0VdG4FkOq4R0=" \
  decrypted-file.txt

# Get object metadata (no key needed for metadata)
aws s3api head-object \
  --bucket my-bucket \
  --key encrypted-file.txt \
  --sse-customer-algorithm AES256 \
  --sse-customer-key "Mzb5l0TCUx7Xk5xuL8R0VdG4FkOq4R0VdG4FkOq4R0="

# Generate a random key for SSE-C
openssl rand -base64 32
```

## Python (boto3) Examples

```python
import boto3
import os
import base64

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Generate an encryption key
def generate_key():
    """Generate a 256-bit (32-byte) AES key"""
    key = os.urandom(32)  # 32 bytes = 256 bits
    key_b64 = base64.b64encode(key).decode()
    print(f"Generated key (save this!): {key_b64}")
    return key_b64

# Upload with SSE-C
def upload_with_sse_c(bucket, key, file_path, encryption_key):
    """Upload a file encrypted with SSE-C"""
    with open(file_path, 'rb') as f:
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=f,
            SSECustomerAlgorithm='AES256',
            SSECustomerKey=encryption_key
        )
    print(f"Uploaded {key} with SSE-C encryption")

# Download with SSE-C
def download_with_sse_c(bucket, key, local_path, encryption_key):
    """Download and decrypt an SSE-C encrypted file"""
    response = s3.get_object(
        Bucket=bucket,
        Key=key,
        SSECustomerAlgorithm='AES256',
        SSECustomerKey=encryption_key
    )
    with open(local_path, 'wb') as f:
        f.write(response['Body'].read())
    print(f"Downloaded and decrypted {key} to {local_path}")

# Usage
my_key = generate_key()
upload_with_sse_c(bucket, 'secret-data.txt', 'secret.txt', my_key)
download_with_sse_c(bucket, 'secret-data.txt', 'restored.txt', my_key)

# Copy SSE-C encrypted object (must provide key for source)
def copy_sse_c_object(bucket, source_key, dest_key, encryption_key):
    """Copy an SSE-C encrypted object"""
    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': source_key},
        Key=dest_key,
        CopySourceSSECustomerAlgorithm='AES256',
        CopySourceSSECustomerKey=encryption_key,
        SSECustomerAlgorithm='AES256',
        SSECustomerKey=encryption_key
    )
    print(f"Copied {source_key} to {dest_key} (SSE-C preserved)")

copy_sse_c_object(bucket, 'secret-data.txt', 'backup/secret-data.txt', my_key)
```

## When to Use SSE-C

| Scenario | Recommendation |
|---|---|
| **You must manage your own keys** | ✅ SSE-C |
| **Existing on-premises key infrastructure** | ✅ SSE-C |
| **Regulatory requirement for client-controlled keys** | ✅ SSE-C |
| **Simple, managed solution needed** | ❌ Use SSE-S3 or SSE-KMS |
| **Need audit trail** | ❌ Use SSE-KMS |
| **High number of objects** | ❌ SSE-C is cumbersome (key per request) |

## SSE-C vs SSE-KMS vs SSE-S3

| Feature | SSE-S3 | SSE-KMS | SSE-C |
|---|---|---|---|
| **Who manages keys** | AWS | Customer (via KMS) | Customer (provides directly) |
| **Key stored by AWS** | Yes | Yes | **No** (only hash) |
| **Key per request** | No | No | **Yes** |
| **Audit trail** | No | Yes | No |
| **Cost** | Free | KMS charges | Free |
| **Key rotation** | Automatic | Optional | Manual |
| **Data loss risk** | None | None | **High (if key lost)** |

## Exam Tips

### 1. Key Must Be Supplied Every Time
The encryption key must be provided with every API call (upload, download, head-object, copy). This is the most important exam point.

### 2. AWS Doesn't Store Your Key
AWS only stores the SHA-256 hash of the key for verification. If you lose the key, the data is **permanently unrecoverable**.

### 3. Cannot Use with Default Encryption
SSE-C must be specified per-object. You cannot set SSE-C as a default bucket encryption.

### 4. SSL/HTTPS Required
Because you're sending encryption keys over the network, you MUST use HTTPS (which is the default for all AWS API calls).

### 5. Common Exam Question
**Q:** A company has a regulatory requirement that encryption keys must not be stored by the service provider. Which S3 encryption should they use?
**A:** SSE-C (customer-provided keys). AWS only stores the key hash, not the key itself.

## Exam Quick Reference
- ✅ **You provide the key** with every request
- ✅ **AWS does NOT store** your key (only SHA-256 hash)
- ✅ **Data unrecoverable** if key is lost
- ✅ **Must use HTTPS** (key sent over network)
- ✅ **Cannot be default** bucket encryption
- ✅ **Free** — no KMS charges
- ✅ Best for **regulatory requirements** where provider cannot hold keys