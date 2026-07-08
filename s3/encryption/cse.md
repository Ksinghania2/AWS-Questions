# Client-Side Encryption (CSE)

Client-Side Encryption means **you encrypt the data before uploading** to S3. AWS never sees the unencrypted data.

## How It Works

```
1. Client encrypts data locally (before upload)
2. Upload encrypted data to S3
3. S3 stores the encrypted blob (cannot read it)
4. Client downloads encrypted data
5. Client decrypts locally
```

- **Key management**: Fully customer managed
- **Encryption location**: Client-side (in your application)
- **AWS visibility**: **None** — AWS cannot read the data
- **Additional cost**: No S3 charges, but you manage keys
- **Security**: Maximum (AWS never sees plaintext)

## Implementation Options

### 1. S3 Encryption Client (Amazon S3 Encryption SDK)
The S3 Encryption Client (part of the AWS SDK) automatically encrypts data client-side before upload and decrypts after download.

### 2. Manual Encryption
Use any encryption library (OpenSSL, crypto libraries) to encrypt files before uploading.

### 3. Third-Party Tools
Use tools like gpg, VeraCrypt, or CloudBerry to encrypt before uploading.

## CLI Commands

```bash
# Manual client-side encryption using OpenSSL
# Encrypt locally
openssl enc -aes-256-cbc -salt -in file.txt -out file.txt.enc -pass pass:your-password

# Upload encrypted file
aws s3 cp file.txt.enc s3://my-bucket/file.txt.enc

# Download encrypted file
aws s3 cp s3://my-bucket/file.txt.enc file.txt.enc

# Decrypt locally
openssl enc -d -aes-256-cbc -in file.txt.enc -out file.txt -pass pass:your-password

# Encrypt with key file
openssl rand -base64 32 > encryption.key
openssl enc -aes-256-cbc -salt -in file.txt -out file.txt.enc -pass file:encryption.key
```

## Python Examples

```python
import boto3
from cryptography.fernet import Fernet
import base64
import os

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Generate a key
def generate_key():
    """Generate a Fernet encryption key"""
    key = Fernet.generate_key()
    print(f"Save this key securely: {key.decode()}")
    return key

# Client-side encrypt and upload
def encrypt_and_upload(bucket, key, file_path, encryption_key):
    """Encrypt file locally, then upload to S3"""
    # Read file
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Encrypt
    f = Fernet(encryption_key)
    encrypted_data = f.encrypt(data)
    
    # Upload encrypted
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=encrypted_data,
        Metadata={'encryption': 'client-side-fernet'}
    )
    print(f"Uploaded encrypted {key} ({len(encrypted_data)} bytes)")

# Download and decrypt
def download_and_decrypt(bucket, key, local_path, encryption_key):
    """Download from S3 and decrypt locally"""
    # Download encrypted data
    response = s3.get_object(Bucket=bucket, Key=key)
    encrypted_data = response['Body'].read()
    
    # Decrypt
    f = Fernet(encryption_key)
    decrypted_data = f.decrypt(encrypted_data)
    
    # Save
    with open(local_path, 'wb') as f:
        f.write(decrypted_data)
    print(f"Downloaded and decrypted to {local_path}")

# Usage
key = generate_key()
encrypt_and_upload(bucket, 'secret.txt', 'secret.txt', key)
download_and_decrypt(bucket, 'secret.txt', 'restored.txt', key)

# Using AWS Encryption SDK approach (conceptual)
def client_side_encryption_demo():
    """Demonstrate client-side encryption flow"""
    print("Client-Side Encryption Flow:")
    print("1. Data: 'This is sensitive information'")
    print("2. Encrypt locally with your key")
    print("3. Upload encrypted blob to S3")
    print("4. S3 sees only encrypted bytes (no plaintext)")
    print("5. Download encrypted blob")
    print("6. Decrypt locally with your key")
    print("7. Result: 'This is sensitive information'")
    print("\n✅ AWS never has access to your plaintext data")

client_side_encryption_demo()
```

## Security Comparison

| Aspect | SSE-S3 | SSE-KMS | SSE-C | **CSE** |
|---|---|---|---|---|
| **AWS can read data?** | Yes | Yes | No (no key) | **No** |
| **Encryption occurs** | S3 server | S3 server | S3 server | **Client** |
| **Key stored by AWS?** | Yes | Yes | Hash only | **No** |
| **Control** | Lowest | Medium | High | **Highest** |
| **Complexity** | Lowest | Medium | High | **Highest** |

## When to Use Client-Side Encryption

| Scenario | Recommendation |
|---|---|
| **Maximum security required** | ✅ CSE |
| **Regulatory: AWS cannot see plaintext** | ✅ CSE |
| **Data must be encrypted before leaving premises** | ✅ CSE |
| **Simple encryption, minimal management** | ❌ Use SSE-S3 |
| **Need audit trail** | ❌ Use SSE-KMS |

## Exam Tips

### 1. AWS Cannot Read the Data
With CSE, AWS never has access to the encryption key, so S3 cannot decrypt and read your data. This is the main differentiator from server-side options.

### 2. Key Management Is Your Responsibility
If you lose the encryption key, the data is **permanently unrecoverable**.

### 3. Metadata Is Still Visible
While the object body is encrypted, object metadata (key name, size, storage class) is still visible to AWS.

### 4. Common Exam Question
**Q:** A financial institution must ensure that AWS administrators cannot read customer data stored in S3. Which encryption method?
**A:** Client-Side Encryption (CSE). Server-side options (SSE-S3, SSE-KMS, SSE-C) all decrypt data on AWS servers, meaning AWS could theoretically access it.

## Exam Quick Reference
- ✅ **Encrypt before upload** — AWS never sees plaintext
- ✅ **Maximum security** — full customer control
- ✅ **Key management** is your responsibility
- ✅ **Data unrecoverable** if key is lost
- ✅ **Metadata visible** to AWS (key name, size)
- ✅ Use **AWS Encryption SDK** or manual encryption
- ✅ Best for **maximum security, compliance, zero-trust**