# S3 Multipart Upload

Multipart upload improves reliability and throughput for **large object uploads** (> 100 MB, required for > 5 GB).

## Why Use Multipart Upload

| Benefit | Description |
|---|---|
| **Higher throughput** | Upload parts in parallel |
| **Fault tolerance** | Failed parts can be retried independently |
| **Pause/resume** | Upload can be paused and resumed |
| **No 5 GB limit** | Max object size is 5 TB |
| **Progress tracking** | Monitor upload progress per part |

## How It Works

```
1. Initiate multipart upload → Get UploadId
2. Upload parts (1-10,000, each 5 MB to 5 GB)
3. Complete multipart upload (S3 assembles the object)
```

## CLI Commands

```bash
# Multipart upload (automatic with aws s3 cp)
aws s3 cp large-file.iso s3://my-bucket/large-file.iso

# Force multipart threshold
aws s3 cp large-file.bin s3://my-bucket/ --cli-write-timeout 0 \
  --cli-read-timeout 0

# Manual multipart upload (s3api)
# Step 1: Initiate
UPLOAD_ID=$(aws s3api create-multipart-upload \
  --bucket my-bucket --key large-file.iso --query UploadId --output text)

# Step 2: Upload parts
aws s3api upload-part \
  --bucket my-bucket --key large-file.iso \
  --part-number 1 --body part-1.bin \
  --upload-id $UPLOAD_ID

aws s3api upload-part \
  --bucket my-bucket --key large-file.iso \
  --part-number 2 --body part-2.bin \
  --upload-id $UPLOAD_ID

# Step 3: Complete
aws s3api complete-multipart-upload \
  --bucket my-bucket --key large-file.iso \
  --upload-id $UPLOAD_ID \
  --multipart-upload '{"Parts": [{"ETag": "etag1", "PartNumber": 1}, {"ETag": "etag2", "PartNumber": 2}]}'

# List in-progress multipart uploads
aws s3api list-multipart-uploads --bucket my-bucket

# Abort a multipart upload
aws s3api abort-multipart-upload \
  --bucket my-bucket --key large-file.iso --upload-id $UPLOAD_ID
```

## Python (boto3) Examples

```python
import boto3
from boto3.s3.transfer import TransferConfig

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Automatic multipart upload with TransferConfig
def upload_large_file(bucket, key, file_path):
    """Upload a large file with multipart automatically"""
    config = TransferConfig(
        multipart_threshold=100 * 1024 * 1024,  # 100 MB threshold
        max_concurrency=10,                       # 10 parallel parts
        multipart_chunksize=50 * 1024 * 1024,    # 50 MB per part
        use_threads=True
    )
    
    s3.upload_file(
        file_path,
        bucket,
        key,
        Config=config
    )
    print(f"Uploaded {key} using multipart upload")

# upload_large_file(bucket, 'large-video.mp4', 'video.mp4')

# Manual multipart upload (for maximum control)
def manual_multipart_upload(bucket, key, file_path, part_size_mb=50):
    """Manually control multipart upload"""
    import math
    
    part_size = part_size_mb * 1024 * 1024
    file_size = os.path.getsize(file_path)
    num_parts = math.ceil(file_size / part_size)
    
    # 1. Initiate
    response = s3.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = response['UploadId']
    print(f"Initiated multipart upload: {upload_id}")
    
    # 2. Upload parts
    parts = []
    with open(file_path, 'rb') as f:
        for i in range(num_parts):
            part_number = i + 1
            data = f.read(part_size)
            
            response = s3.upload_part(
                Bucket=bucket,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=data
            )
            
            parts.append({
                'ETag': response['ETag'],
                'PartNumber': part_number
            })
            print(f"Uploaded part {part_number}/{num_parts}")
    
    # 3. Complete
    response = s3.complete_multipart_upload(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
    print(f"Multipart upload complete: {response['Location']}")

# List incomplete uploads
def list_incomplete_uploads(bucket):
    """List all incomplete multipart uploads"""
    response = s3.list_multipart_uploads(Bucket=bucket)
    
    for upload in response.get('Uploads', []):
        print(f"  {upload['Key']} (initiated: {upload['Initiated']})")
        print(f"  UploadId: {upload['UploadId']}")
    
    return response.get('Uploads', [])

# Abort old incomplete uploads
def abort_old_uploads(bucket, max_age_days=7):
    """Abort multipart uploads older than max_age_days"""
    import datetime
    
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_age_days)
    old_uploads = []
    
    response = s3.list_multipart_uploads(Bucket=bucket)
    for upload in response.get('Uploads', []):
        if upload['Initiated'] < cutoff:
            old_uploads.append(upload)
            s3.abort_multipart_upload(
                Bucket=bucket,
                Key=upload['Key'],
                UploadId=upload['UploadId']
            )
            print(f"Aborted: {upload['Key']} ({upload['UploadId']})")
    
    print(f"Aborted {len(old_uploads)} old uploads")
    return old_uploads
```

## Best Practices

| Practice | Why |
|---|---|
| **Use threshold of 100 MB** | Below this, single PUT is more efficient |
| **10 concurrent parts** | Good balance of speed and resource usage |
| **50-100 MB part size** | Optimal for most workloads |
| **Clean up incomplete uploads** | Avoid storage costs for partial uploads |
| **Use lifecycle rules** | Automatically abort incomplete uploads after 7 days |

## Exam Tips

### 1. Required for Objects > 5 GB
Objects larger than 5 GB **must** use multipart upload. The SDK does this automatically.

### 2. Parallel Uploads
Multipart upload allows parallel part uploads for better throughput.

### 3. Part Size Range
Each part must be between **5 MB and 5 GB** (except the last part).

### 4. Max Parts
Maximum **10,000 parts** per upload.

### 5. ETag Suffix
Multipart upload ETags have a `-N` suffix indicating the number of parts (e.g., `"abc123-3"` for 3 parts).

### 6. Common Exam Question
**Q:** An application needs to upload 1 TB files to S3 reliably. What feature should they use?
**A:** Multipart upload with parallel part uploads and individual part retries.

## Exam Quick Reference
- ✅ **Required** for objects > 5 GB
- ✅ **Recommended** for objects > 100 MB
- ✅ **Max 10,000 parts**
- ✅ **Part size**: 5 MB to 5 GB
- ✅ **Parallel uploads** for better throughput
- ✅ **Automatic retry** of failed parts
- ✅ **Max object size**: 5 TB
- ✅ **Clean up** incomplete uploads to avoid costs