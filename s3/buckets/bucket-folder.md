# S3 Folders and Directory Structure

S3 does not use a traditional folder hierarchy like a filesystem (NTFS, ext4). Instead, S3 uses a **flat key-value store** where object keys can contain `/` characters to simulate folders.

## How S3 "Folders" Really Work

### Flat Namespace
All objects in a bucket exist in a single flat namespace. There are no real directories.

### Prefixes as Folders
When you see `images/logo.png`, the `/` is just part of the object key. The "folder" `images/` is simply a common prefix shared by all objects whose keys start with `images/`.

### Zero-Length Objects as Folder Markers
When you create a "folder" in the AWS Console, it creates a zero-length object with the key ending in `/` (e.g., `images/`). This is just a visual helper for the console UI.

## CLI Demonstration

```bash
# Create a "folder" (creates zero-length marker object)
aws s3api put-object --bucket my-bucket --key images/

# Upload to a "subfolder" (key with prefix)
aws s3 cp photo.jpg s3://my-bucket/images/photo.jpg
aws s3 cp logo.png s3://my-bucket/images/icons/logo.png

# List objects with prefix filtering
aws s3 ls s3://my-bucket/images/

# List with delimiter (shows "folders")
aws s3api list-objects \
  --bucket my-bucket \
  --delimiter / \
  --prefix images/

# List without delimiter (shows all objects flat)
aws s3api list-objects --bucket my-bucket --prefix images/
```

## Key Concepts

### Delimiter (`/`)
When you use `--delimiter /`, S3 groups objects by their top-level prefixes. This is how the AWS Console shows "folders".

### Prefix
A prefix is the start of an object key. It's used to filter and group objects.

### Common Prefixes
These are the unique prefixes between the delimiter characters. S3 returns these when you use a delimiter — they appear as "subfolders".

## Python Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# List "folders" at the top level
def list_folders(bucket):
    """List top-level "folders" using delimiter"""
    response = s3.list_objects_v2(
        Bucket=bucket,
        Delimiter='/'
    )
    print("Folders (Common Prefixes):")
    for prefix in response.get('CommonPrefixes', []):
        print(f"  /{prefix['Prefix']}")
    
    print("\nFiles at root level:")
    for obj in response.get('Contents', []):
        print(f"  {obj['Key']} ({obj['Size']} bytes)")

list_folders(bucket)

# List contents of a specific "folder"
def list_folder_contents(bucket, prefix):
    """List all objects under a prefix"""
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
        Delimiter='/'
    )
    
    print(f"\nContents of /{prefix}:")
    for obj in response.get('Contents', []):
        print(f"  {obj['Key']} ({obj['Size']} bytes)")

list_folder_contents(bucket, 'images/')

# Create multiple nested "folders" programmatically
prefixes = ['logs/2024/', 'logs/2024/01/', 'logs/2024/02/', 'data/raw/', 'data/processed/']
for prefix in prefixes:
    s3.put_object(Bucket=bucket, Key=prefix)  # Zero-length marker

print(f"Created {len(prefixes)} folder markers")
```

## Best Practices

### Do Use Prefixes For:
- **Logical grouping**: `users/{user-id}/profile.jpg`
- **Date partitioning**: `logs/2024/05/15/error.log` (important for Athena/Glue)
- **Environment separation**: `prod/`, `staging/`, `dev/`
- **Access control via policies**: Restrict access by prefix

### Don't Use Deep Nesting
S3 has no performance penalty for deep prefixes, but:
- Object keys are limited to 1024 bytes
- Deep nesting makes management harder
- For high-performance workloads, distribute objects across many prefixes (not for folder structure, but for request rate scaling — 3,500 PUTs/second per prefix)

### Request Rate Scaling
- S3 supports **3,500 PUT/COPY/POST/DELETE** or **5,500 GET/HEAD requests** per second **per prefix**
- To achieve higher throughput, distribute across multiple prefixes
- Example: Instead of `images/photo.jpg`, use `images/2024/05/15/photo.jpg` (different prefix each day)

## Exam Scenarios

### Scenario 1: Prefix-based IAM Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::company-data/users/*"
  }]
}
```
This grants access only to objects with the prefix `users/`.

### Scenario 2: Athena Partitioning
```sql
CREATE EXTERNAL TABLE logs (
  message string,
  level string
)
PARTITIONED BY (year string, month string, day string)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://my-logs-bucket/';
```
S3 prefixes like `year=2024/month=05/day=15/` map to Hive partitions.

### Scenario 3: Listing Optimization
For buckets with millions of objects, use `list_objects_v2` with pagination:
```bash
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --prefix logs/2024/05/ \
  --max-items 1000 \
  --starting-token <NextToken>
```

## Exam Quick Reference
- ✅ S3 has a **flat namespace** — "folders" are just key prefixes
- ✅ Use **`/` as delimiter** to simulate directory listing
- ✅ **Zero-length objects** with keys ending in `/` serve as folder markers
- ✅ **3,500 PUTs/sec per prefix** (distribute objects for higher throughput)
- ✅ **5,500 GETs/sec per prefix**
- ✅ **1024 bytes max key length** — includes all prefix/path characters
- ✅ No performance penalty for prefix depth (unlike traditional filesystems)