# Presigned URLs

Presigned URLs provide **temporary, time-limited access** to an S3 object without sharing long-term credentials.

## How They Work

```
1. User with IAM credentials generates a presigned URL
2. URL includes: endpoint, object path, expiration, signature
3. Anyone with the URL can access the object for the specified time
4. After expiration, the URL returns 403 Forbidden
```

## Key Features

| Feature | Details |
|---|---|
| **Expiration** | 1 second to 7 days (max 7 days for AWS SDK, 12 hours for CLI) |
| **Actions** | GET, PUT, POST, DELETE, HEAD |
| **Who can use** | Anyone with the URL (no AWS credentials needed) |
| **Security** | URL is signed with the creator's IAM credentials |
| **Permissions** | Same as the creator's permissions at time of creation |

## CLI Commands

```bash
# Generate a presigned URL for download (GET)
aws s3 presign s3://my-bucket/report.csv --expires-in 3600

# Generate a presigned URL for upload (PUT)
aws s3api presign --method put --bucket my-bucket --key upload.txt \
  --expires-in 3600

# Generate with specific content-type
aws s3 presign s3://my-bucket/photo.jpg --expires-in 86400

# Use presigned URL with curl
curl -O "https://my-bucket.s3.us-east-1.amazonaws.com/report.csv?X-Amz-Algorithm=..."

# Upload using presigned URL
curl -X PUT -T "file.txt" "https://my-bucket.s3.us-east-1.amazonaws.com/upload.txt?..."

# Generate presigned URL for specific version
aws s3 presign s3://my-bucket/file.txt?versionId=<version-id> --expires-in 3600
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Generate presigned URL for download
def generate_download_url(bucket, key, expiration=3600):
    """Generate a presigned URL for downloading an object"""
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    print(f"Download URL (expires in {expiration}s):")
    print(url)
    return url

generate_download_url(bucket, 'report.pdf', 3600)

# Generate presigned URL for upload
def generate_upload_url(bucket, key, expiration=3600):
    """Generate a presigned URL for uploading an object"""
    url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    print(f"Upload URL (expires in {expiration}s):")
    print(url)
    return url

generate_upload_url(bucket, 'uploads/photo.jpg', 3600)

# Generate presigned URL with specific content type
def generate_presigned_url_with_conditions(bucket, key, content_type, expiration=3600):
    """Generate a presigned URL that requires a specific content type"""
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket,
            'Key': key,
            'ContentType': content_type
        },
        ExpiresIn=expiration
    )
    print(f"Upload URL (requires Content-Type: {content_type}):")
    print(url)
    return url

generate_presigned_url_with_conditions(bucket, 'images/logo.png', 'image/png', 3600)

# Generate presigned URL for listing bucket
def generate_list_url(bucket, expiration=3600):
    """Generate a presigned URL for listing bucket contents"""
    url = s3.generate_presigned_url(
        'list_objects_v2',
        Params={'Bucket': bucket, 'MaxKeys': 10},
        ExpiresIn=expiration
    )
    print(f"List URL (expires in {expiration}s):")
    print(url)
    return url

generate_list_url(bucket, 3600)

# Generate presigned POST (for browser uploads)
def generate_presigned_post(bucket, key, expiration=3600):
    """Generate a presigned POST for browser-based uploads"""
    response = s3.generate_presigned_post(
        Bucket=bucket,
        Key=key,
        Conditions=[
            {'bucket': bucket},
            {'key': key},
            ['content-length-range', 0, 10485760]  # 10 MB max
        ],
        ExpiresIn=expiration
    )
    
    print(f"POST URL: {response['url']}")
    print("Form fields:")
    for k, v in response['fields'].items():
        print(f"  {k}: {v}")
    return response

generate_presigned_post(bucket, 'uploads/user-photo.jpg', 3600)
```

## Use Cases

| Use Case | Method | Example |
|---|---|---|
| **Share private file** | GET | Share a private report with a client |
| **Allow user upload** | PUT | Let users upload profile photos |
| **Browser uploads** | POST | HTML form uploads directly to S3 |
| **Temporary access** | GET | Grant time-limited access to a file |
| **Cross-account access** | GET/PUT | Share files across AWS accounts |

## Security Best Practices

### Do
- Set the **shortest expiration** that works for your use case
- Generate URLs using **least-privilege IAM credentials**
- Use **HTTPS** (default with presigned URLs)
- Monitor presigned URL usage with **CloudTrail**

### Don't
- Generate URLs with **7-day expiration** unless necessary
- Share presigned URLs in **public channels** (they're still credentials)
- Use presigned URLs for **internal service-to-service** communication (use IAM roles)
- Forget that the URL grants **the same permissions as the creator**

## Exam Tips

### 1. Max Expiration
- **CLI**: 12 hours (604,800 seconds max)
- **SDK**: 7 days (604,800 seconds max)

### 2. Permissions at Creation
The presigned URL inherits the permissions of the IAM user/role that created it. If the creator's permissions change after URL creation, the URL still works with the original permissions.

### 3. No IAM Required for User
The person using the presigned URL does NOT need AWS credentials. Only the URL creator needs IAM permissions.

### 4. Common Exam Question
**Q:** A company wants to allow unauthenticated users to upload files to S3 for 24 hours. What should they use?
**A:** Presigned URLs with PUT method, 24-hour expiration.

## Exam Quick Reference
- ✅ **Temporary, time-limited** access to S3 objects
- ✅ **Max 7 days** (SDK) or **12 hours** (CLI)
- ✅ **No AWS credentials** needed by the URL user
- ✅ **Same permissions** as the URL creator
- ✅ Supports **GET, PUT, POST, DELETE, HEAD**
- ✅ **HTTPS** enforced by default
- ✅ Best for **sharing, uploading, temporary access**