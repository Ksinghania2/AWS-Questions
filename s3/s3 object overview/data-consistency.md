# S3 Data Consistency Model

S3 provides **strong read-after-write consistency** for all operations. This means after a successful write or delete, subsequent reads immediately reflect the change.

## Consistency Model Overview

| Operation | Before 2020 (Eventual) | Now (Strong) |
|---|---|---|
| **PUT new object** | Read-after-write consistency | **Strong consistency** |
| **PUT overwrite** | Eventual consistency | **Strong consistency** |
| **DELETE object** | Eventual consistency | **Strong consistency** |
| **LIST bucket** | Eventual consistency | **Strong consistency** |

## What Strong Consistency Means

### After a PUT (new object)
```bash
# Upload a file
aws s3 cp report.pdf s3://my-bucket/report.pdf

# Immediately read it — guaranteed to work
aws s3 cp s3://my-bucket/report.pdf ./downloaded-report.pdf
# ✅ Always succeeds
```

### After a PUT (overwrite)
```bash
# Upload version 1
aws s3 cp report-v1.pdf s3://my-bucket/report.pdf

# Immediately overwrite with version 2
aws s3 cp report-v2.pdf s3://my-bucket/report.pdf

# Read immediately — guaranteed to get version 2
aws s3 cp s3://my-bucket/report.pdf ./downloaded-report.pdf
# ✅ Always gets the latest version
```

### After a DELETE
```bash
# Delete an object
aws s3 rm s3://my-bucket/report.pdf

# List immediately — guaranteed to not show the deleted object
aws s3 ls s3://my-bucket/
# ✅ Always reflects the deletion
```

## CLI Commands to Verify Consistency

```bash
# Test read-after-write
echo "test data" > test.txt
aws s3 cp test.txt s3://my-bucket/test.txt
aws s3api get-object --bucket my-bucket --key test.txt /dev/stdout
# Output: "test data" (immediately available)

# Test read-after-overwrite
echo "version 1" > test.txt
aws s3 cp test.txt s3://my-bucket/test.txt
echo "version 2" > test.txt
aws s3 cp test.txt s3://my-bucket/test.txt
aws s3api get-object --bucket my-bucket --key test.txt /dev/stdout
# Output: "version 2" (immediately the latest)

# Test read-after-delete
aws s3 rm s3://my-bucket/test.txt
aws s3 ls s3://my-bucket/test.txt
# Output: (empty — immediately deleted)
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Demonstrate strong consistency
def demonstrate_consistency(bucket, key='consistency-test.txt'):
    """Show that S3 provides strong consistency"""
    import time
    
    # 1. Write
    print("1. Writing object...")
    s3.put_object(Bucket=bucket, Key=key, Body=b'Test data')
    
    # 2. Immediate read (strong consistency)
    print("2. Reading immediately...")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode()
    print(f"   Content: '{content}' ✅")
    
    # 3. Overwrite
    print("3. Overwriting object...")
    s3.put_object(Bucket=bucket, Key=key, Body=b'Updated data')
    
    # 4. Immediate read after overwrite
    print("4. Reading immediately after overwrite...")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode()
    print(f"   Content: '{content}' ✅ (always gets latest)")
    
    # 5. Delete
    print("5. Deleting object...")
    s3.delete_object(Bucket=bucket, Key=key)
    
    # 6. Immediate list after delete
    print("6. Listing immediately after delete...")
    response = s3.list_objects_v2(Bucket=bucket, Prefix=key)
    objects = response.get('Contents', [])
    print(f"   Objects found: {len(objects)} ✅ (immediately reflects delete)")
    
    print("\n✅ S3 provides strong consistency for all operations")

demonstrate_consistency(bucket)

# Practical example: Atomic updates
def atomic_update(bucket, key, new_content):
    """Use strong consistency for reliable updates"""
    # Write new content
    s3.put_object(Bucket=bucket, Key=key, Body=new_content.encode())
    
    # Immediately verify (guaranteed to work)
    response = s3.get_object(Bucket=bucket, Key=key)
    actual = response['Body'].read().decode()
    
    if actual == new_content:
        print(f"✅ Atomic update successful: {key}")
        return True
    else:
        print(f"❌ Update failed (should never happen with strong consistency)")
        return False

atomic_update(bucket, 'config/app-config.json', '{"version": 2, "debug": true}')
```

## Why Strong Consistency Matters

### Before Strong Consistency (Pre-2020)
```
Time 0:  PUT object A
Time 1:  GET object A → ❌ 404 (not found yet)
Time 2:  GET object A → ✅ 200 (found)
Time 3:  DELETE object A
Time 4:  GET object A → ✅ 200 (still visible!)
Time 5:  GET object A → ❌ 404 (finally gone)
```

### With Strong Consistency (Current)
```
Time 0:  PUT object A
Time 1:  GET object A → ✅ 200 (immediately available)
Time 2:  DELETE object A
Time 3:  GET object A → ❌ 404 (immediately gone)
```

## Exam Scenarios

### Scenario 1: File Processing Pipeline
**Problem:** A Lambda function processes files uploaded to S3. Before strong consistency, the Lambda might trigger before the file was fully visible.
**Solution:** With strong consistency, the Lambda can immediately read the file when triggered by S3 Event Notifications.

### Scenario 2: Database Backups
**Problem:** A backup script uploads a database dump and immediately checks if the backup was successful.
**Solution:** With strong consistency, the verification read is guaranteed to work.

### Scenario 3: Configuration Updates
**Problem:** An application reads configuration from S3. When the config is updated, the app needs to see the new version immediately.
**Solution:** Strong consistency ensures the app always sees the latest configuration.

## Exam Quick Reference
- ✅ **Strong read-after-write consistency** for PUT, overwrite, DELETE, and LIST
- ✅ **No more eventual consistency** (changed in December 2020)
- ✅ **Immediate visibility** after any write operation
- ✅ **Same consistency** for new objects, overwrites, and deletes
- ✅ **No special handling needed** — just read after write
- ✅ **Critical for** data pipelines, config management, and real-time processing