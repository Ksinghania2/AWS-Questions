# S3 Object Checksums

Checksums ensure **data integrity** — verifying that data hasn't been corrupted during upload, download, or storage.

## Built-in Checksum Mechanisms

### ETag
Every S3 object has an **ETag** (entity tag), which acts as a hash of the object content.

| Upload Method | ETag Value |
|---|---|
| **Single PUT (< 5 GB)** | MD5 hash of the object |
| **Multipart upload** | MD5 of the concatenation of each part's MD5 |
| **SSE-KMS or SSE-C** | Not MD5 (different hash) |

### SHA-256 Checksums (Added 2022)
S3 now supports **additional checksum algorithms** for better integrity validation:

| Algorithm | Bits | Use Case |
|---|---|---|
| **SHA-256** | 256 bits | Recommended for most workloads |
| **SHA-1** | 160 bits | Legacy compatibility |
| **CRC-32** | 32 bits | Faster computation, less collision resistance |
| **CRC-32C** | 32 bits | Faster hardware-accelerated CRC |

## CLI Commands

```bash
# Upload with checksum validation (SHA-256 computed automatically)
aws s3 cp file.txt s3://my-bucket/file.txt

# Upload and specify checksum algorithm
aws s3api put-object \
  --bucket my-bucket \
  --key file.txt \
  --body file.txt \
  --checksum-algorithm SHA256

# Get object checksum information
aws s3api head-object --bucket my-bucket --key file.txt \
  --query "ChecksumAlgorithm,ETag,ChecksumSHA256"

# Download with checksum verification
aws s3 cp s3://my-bucket/file.txt ./downloaded-file.txt

# Upload using s3api with explicit checksum
aws s3api put-object \
  --bucket my-bucket \
  --key data.bin \
  --body data.bin \
  --checksum-algorithm SHA256 \
  --checksum-sha256-base64 <base64-encoded-hash>
```

## Python (boto3) Examples

```python
import boto3
import hashlib
import base64

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload with SHA-256 checksum
def upload_with_checksum(bucket, key, file_path):
    """Upload a file with SHA-256 checksum validation"""
    # Calculate SHA-256 locally
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    
    checksum = base64.b64encode(sha256.digest()).decode()
    
    # Upload with checksum
    response = s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=open(file_path, 'rb'),
        ChecksumAlgorithm='SHA256',
        ChecksumSHA256=checksum
    )
    
    print(f"Uploaded {key}")
    print(f"  ETag: {response['ETag']}")
    print(f"  SHA-256: {checksum}")
    return response

# Verify checksum on download
def download_and_verify(bucket, key, expected_sha256=None):
    """Download and verify checksum"""
    response = s3.get_object(
        Bucket=bucket,
        Key=key,
        ChecksumMode='ENABLED'  # Request server-side checksum validation
    )
    
    content = response['Body'].read()
    
    # If we have an expected checksum, verify it
    if expected_sha256:
        actual = hashlib.sha256(content).hexdigest()
        if actual == expected_sha256:
            print(f"✅ Checksum verified for {key}")
        else:
            print(f"❌ Checksum MISMATCH for {key}")
    
    return content

# Upload and download with verification
upload_with_checksum(bucket, 'data/report.pdf', 'report.pdf')
data = download_and_verify(bucket, 'data/report.pdf')

# List objects and show checksum info
def list_checksum_info(bucket, prefix=''):
    """List objects and their checksum information"""
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            head = s3.head_object(Bucket=bucket, Key=obj['Key'])
            checksum_algo = head.get('ChecksumAlgorithm', ['None'])
            print(f"{obj['Key']}:")
            print(f"  Size: {obj['Size']} bytes")
            print(f"  ETag: {head['ETag']}")
            print(f"  Checksum Algorithms: {checksum_algo}")
            
            if 'ChecksumSHA256' in head:
                print(f"  SHA-256: {head['ChecksumSHA256'][:32]}...")

list_checksum_info(bucket)

# Multipart upload with checksum
def multipart_upload_with_checksum(bucket, key, file_path):
    """Multipart upload with checksum validation"""
    from boto3.s3.transfer import TransferConfig
    
    config = TransferConfig(
        multipart_threshold=100 * 1024 * 1024,  # 100 MB
        multipart_chunksize=50 * 1024 * 1024,   # 50 MB parts
        use_threads=True
    )
    
    # Use the S3 transfer manager for automatic multipart with checksums
    s3.upload_file(
        file_path,
        bucket,
        key,
        Config=config,
        ExtraArgs={
            'ChecksumAlgorithm': 'SHA256'
        }
    )
    print(f"Multipart upload with SHA-256 complete: {key}")

# multipart_upload_with_checksum(bucket, 'large/video.mp4', 'video.mp4')
```

## Why Checksums Matter

### Without Checksums
```
Client sends file → S3 stores it
Data corrupts during transfer? ❌ Client doesn't know
Client downloads → compares hash manually
```

### With Checksums
```
Client sends file + SHA-256 → S3 verifies during upload
                                        ↓
                              Corrupted? → Reject and retry
                              Valid?     → Store with checksum
                                                
Client downloads + requests checksum → S3 validates
                                        ↓
                              Corrupted? → Retry
                              Valid?     ✅ Data is intact
```

## Exam Tips

### 1. Default Behavior
Single PUT operations already compute and verify MD5 checksums automatically. The newer SHA-256/CRC checksums are optional but recommended.

### 2. ChecksumMode=ENABLED
When downloading, set `ChecksumMode='ENABLED'` to have S3 verify the object's checksum before sending data.

### 3. Multipart Uploads
For multipart uploads, each part's checksum is verified independently, and the final ETag is computed from the part checksums.

### 4. Common Exam Question
**Q:** A company needs to ensure data integrity for regulatory compliance during S3 transfers. What should they use?
**A:** Enable additional checksums (SHA-256) in addition to the default MD5/ETag. Use `ChecksumAlgorithm` parameter when uploading.

## Exam Quick Reference
- ✅ **ETag** = default MD5-based checksum for single PUTs
- ✅ **SHA-256, SHA-1, CRC-32, CRC-32C** are additional checksum algorithms
- ✅ **ChecksumAlgorithm** parameter to enable additional checksums
- ✅ **ChecksumMode=ENABLED** for download verification
- ✅ **No additional cost** for checksums
- ✅ **Automatic validation** on upload (MD5 always enabled)
- ✅ Every object gets data integrity protection