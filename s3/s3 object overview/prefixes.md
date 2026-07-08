# S3 Object Prefixes

A **prefix** is the beginning of an object key that groups objects together. Prefixes are fundamental to S3 organization and performance.

## What Are Prefixes?

In S3, there are **no real folders**. A prefix is simply the string that comes before the last `/` in an object key.

| Object Key | Prefix | Object Name |
|---|---|---|
| `images/logo.png` | `images/` | `logo.png` |
| `logs/2024/05/error.log` | `logs/2024/05/` | `error.log` |
| `documents/report.pdf` | `documents/` | `report.pdf` |
| `backup.tar.gz` | (none — at root) | `backup.tar.gz` |

## Prefixes and Performance

S3 performance scales by prefix. To achieve high throughput, distribute objects across many prefixes.

### Request Rate Limits
- **3,500 PUT/COPY/POST/DELETE** requests per second **per prefix**
- **5,500 GET/HEAD** requests per second **per prefix**

### Example: Scaling with Prefixes

```
❌ Bad: All objects under one prefix
images/photo-000001.jpg
images/photo-000002.jpg
images/photo-000003.jpg
→ Max 3,500 PUTs/sec total

✅ Good: Distribute across prefixes
images/2024/05/15/photo-000001.jpg
images/2024/05/16/photo-000002.jpg
images/2024/05/17/photo-000003.jpg
→ 3,500 PUTs/sec per day prefix (much higher throughput)
```

## CLI Commands for Prefix Operations

```bash
# List objects with a prefix (filter by "folder")
aws s3 ls s3://my-bucket/images/

# List objects with a specific prefix
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --prefix "logs/2024/05/"

# List with delimiter to show "subfolders"
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --prefix "images/" \
  --delimiter "/"

# Delete all objects with a prefix
aws s3 rm s3://my-bucket/logs/2024/ --recursive

# Copy all objects with a prefix to another bucket
aws s3 cp s3://my-bucket/images/ s3://my-backup/images/ --recursive

# Count objects with a prefix
aws s3api list-objects-v2 --bucket my-bucket --prefix "documents/" \
  --query "length(Contents[])" --output text

# Get total size of objects with a prefix
aws s3api list-objects-v2 --bucket my-bucket --prefix "videos/" \
  --query "sum(Contents[].Size)" --output text
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# List objects with prefix
def list_with_prefix(bucket, prefix):
    """List all objects under a prefix"""
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    count = 0
    total_size = 0
    
    print(f"Objects under '{prefix}':")
    for obj in response.get('Contents', []):
        count += 1
        total_size += obj['Size']
        print(f"  {obj['Key']} ({obj['Size']} bytes)")
    
    print(f"\nTotal: {count} objects, {total_size / 1024 / 1024:.2f} MB")
    return count, total_size

list_with_prefix(bucket, 'logs/2024/05/')

# List common prefixes (simulates folder listing)
def list_common_prefixes(bucket, prefix=''):
    """List "folders" using delimiter"""
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
        Delimiter='/'
    )
    
    print(f"Contents at '{prefix or 'root'}':")
    for obj in response.get('Contents', []):
        print(f"  [File] {obj['Key']} ({obj['Size']} bytes)")
    
    for cp in response.get('CommonPrefixes', []):
        print(f"  [Dir]  {cp['Prefix']}")

list_common_prefixes(bucket)
list_common_prefixes(bucket, 'images/')

# Performance test: multiple prefixes
def performance_test(bucket, num_prefixes=10, num_objects_per_prefix=100):
    """Test writing to multiple prefixes"""
    import time
    
    start = time.time()
    
    for p in range(num_prefixes):
        prefix = f"perf-test/prefix-{p:04d}/"
        for o in range(num_objects_per_prefix):
            key = f"{prefix}object-{o:04d}.txt"
            s3.put_object(Bucket=bucket, Key=key, Body=b'test')
    
    elapsed = time.time() - start
    total_objects = num_prefixes * num_objects_per_prefix
    throughput = total_objects / elapsed
    
    print(f"Wrote {total_objects} objects across {num_prefixes} prefixes")
    print(f"Time: {elapsed:.2f}s")
    print(f"Throughput: {throughput:.0f} objects/sec")

# performance_test(bucket, 10, 100)
```

## Prefix-based IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/users/john.doe/*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/admin/*"
    }
  ]
}
```

## Common Prefix Patterns

| Pattern | Example | Use Case |
|---|---|---|
| **Date-based** | `logs/2024/05/15/error.log` | Time-series data, log analysis |
| **User-based** | `users/{user-id}/profile.jpg` | Multi-tenant applications |
| **Environment** | `prod/app/config.json` | Environment separation |
| **Data stage** | `raw/ → processed/ → curated/` | Data lake ETL pipelines |
| **Entity-based** | `customers/{id}/orders/{order-id}.json` | Object-oriented storage |

## Exam Tips

### 1. Prefix Performance
S3 scales by prefix. To achieve millions of requests per second, distribute across many prefixes (e.g., date-based keys).

### 2. Prefix Filters
Lifecycle rules, replication rules, and batch operations can all filter by prefix.

### 3. Prefix ≠ Folder
Remember: there are no real folders in S3. Prefixes are just the start of the object key string.

### 4. Maximum Key Length
The total key (prefix + object name) cannot exceed 1,024 bytes (UTF-8).

### 5. Common Exam Question
**Q:** An application gets 10,000 PUT requests per second to S3. How should the keys be designed?
**A:** Use at least 3 different prefixes (e.g., `YYYY/MM/DD/HH/`) to achieve 3,500 PUTs/sec × 3 = 10,500 PUTs/sec.

## Exam Quick Reference
- ✅ **Prefix = start of object key** (before last `/`)
- ✅ **3,500 PUTs/sec** per prefix
- ✅ **5,500 GETs/sec** per prefix
- ✅ Use **multiple prefixes** for high throughput
- ✅ **Date-based** prefixes (`YYYY/MM/DD/HH`) for time-series data
- ✅ Can be used in **IAM policies** and **lifecycle rules**
- ✅ **Not a real folder** — just a key naming convention
- ✅ **Max key length**: 1,024 bytes