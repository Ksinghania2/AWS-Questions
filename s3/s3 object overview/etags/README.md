# S3 ETags

An **ETag** (Entity Tag) is a hash value assigned to every S3 object. It's used for **data integrity verification** and **conditional operations**.

## How ETags Are Computed

| Upload Method | ETag Calculation |
|---|---|
| **Single PUT (< 5 GB)** | MD5 hash of the entire object |
| **Multipart upload** | MD5 of the concatenation of each part's MD5 hash, with a part-count suffix (e.g., `"abc123-3"` for 3 parts) |
| **SSE-KMS encryption** | Not MD5 (different hash, not pre-computable) |
| **SSE-C encryption** | MD5 of the encrypted object |

## CLI Commands

```bash
# Get ETag of an object
aws s3api head-object --bucket my-bucket --key file.txt \
  --query "ETag" --output text

# Use ETag for conditional operations
# Download only if ETag matches (data hasn't changed)
aws s3api get-object \
  --bucket my-bucket \
  --key file.txt \
  --if-match "abc123def456" \
  downloaded.txt

# Download only if ETag has changed
aws s3api get-object \
  --bucket my-bucket \
  --key file.txt \
  --if-none-match "abc123def456" \
  downloaded.txt

# Upload and verify ETag
ETAG=$(aws s3api put-object --bucket my-bucket --key test.txt --body test.txt --query ETag --output text)
echo "Uploaded with ETag: $ETAG"

# Compare local MD5 with S3 ETag (for single PUT objects)
LOCAL_MD5=$(md5 -q test.txt)  # macOS
# LOCAL_MD5=$(md5sum test.txt | awk '{print $1}')  # Linux
echo "Local MD5: $LOCAL_MD5"
echo "S3 ETag:   $ETAG"
```

## Python (boto3) Examples

```python
import boto3
import hashlib

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Get ETag
def get_etag(bucket, key):
    """Get the ETag of an object"""
    response = s3.head_object(Bucket=bucket, Key=key)
    etag = response['ETag'].strip('"')  # Remove quotes
    print(f"ETag for {key}: {etag}")
    return etag

etag = get_etag(bucket, 'file.txt')

# Conditional download (only if changed)
def download_if_changed(bucket, key, local_path, known_etag):
    """Download only if the object has changed"""
    try:
        response = s3.get_object(
            Bucket=bucket,
            Key=key,
            IfNoneMatch=known_etag  # 304 Not Modified if same
        )
        # Object has changed
        with open(local_path, 'wb') as f:
            f.write(response['Body'].read())
        print(f"Downloaded updated version of {key}")
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NotModified':
            print(f"{key} has not changed (304)")
            return False
        raise

# download_if_changed(bucket, 'config.json', 'config.json', '"abc123"')

# Verify single-PUT ETag matches local MD5
def verify_etag(bucket, key, local_file):
    """Verify that a local file matches the S3 ETag (single PUT only)"""
    # Get S3 ETag
    response = s3.head_object(Bucket=bucket, Key=key)
    s3_etag = response['ETag'].strip('"')
    
    # Compute local MD5
    md5 = hashlib.md5()
    with open(local_file, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    local_md5 = md5.hexdigest()
    
    if s3_etag == local_md5:
        print(f"✅ ETag matches: {s3_etag}")
        return True
    else:
        print(f"❌ ETag mismatch:")
        print(f"   S3:    {s3_etag}")
        print(f"   Local: {local_md5}")
        return False

verify_etag(bucket, 'file.txt', 'file.txt')

# Detect multipart upload ETag
def is_multipart_upload(etag):
    """Check if an ETag indicates a multipart upload"""
    etag_clean = etag.strip('"')
    if '-' in etag_clean:
        parts = etag_clean.split('-')[1]
        print(f"Multipart upload: {parts} parts")
        return True
    else:
        print("Single PUT upload")
        return False

is_multipart_upload('"abc123-3"')  # 3 parts
is_multipart_upload('"def456"')     # Single PUT
```

## ETag Use Cases

| Use Case | How ETag Helps |
|---|---|
| **Data integrity** | Verify object wasn't corrupted during upload |
| **Cache validation** | Conditional GETs with `If-None-Match` |
| **Change detection** | Check if an object was modified |
| **Concurrent access** | Prevent overwrite conflicts with `If-Match` |
| **Multipart detection** | ETag with `-N` suffix indicates multipart upload |

## Important Notes

### 1. ETag ≠ MD5 for Multipart
For multipart uploads, the ETag is NOT a simple MD5. It's the MD5 of the concatenation of each part's MD5, followed by `-{partCount}`.

### 2. SSE-KMS Changes ETag
When using SSE-KMS, the ETag is not an MD5 hash and cannot be pre-computed.

### 3. ETag Quotes
The ETag value is always returned with double quotes (e.g., `"abc123"`). Strip them when comparing.

### 4. Not a Cryptographic Hash
ETags are for integrity checking, not security. They don't provide cryptographic guarantees.

## Exam Quick Reference
- ✅ **ETag = MD5** for single PUT objects
- ✅ **ETag = MD5-MD5 + `-N`** for multipart uploads (N = part count)
- ✅ **Not MD5** when using SSE-KMS
- ✅ Used for **conditional operations** (`If-Match`, `If-None-Match`)
- ✅ Used for **data integrity verification**
- ✅ Always returned in **quotes** (strip for comparison)
- ✅ **Not a security feature** — integrity only