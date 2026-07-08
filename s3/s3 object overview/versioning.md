# S3 Versioning

Versioning keeps **multiple variants** of an object in the same bucket, protecting against accidental overwrites and deletions.

## Key Concepts

### How Versioning Works
- Each object has a **version ID** (a unique identifier)
- When you overwrite an object, the **old version is preserved**, and a new version is created
- When you delete an object, a **delete marker** is added (the object is not actually removed)
- You can **restore previous versions** at any time

### Versioning States

| State | Behavior |
|---|---|
| **Unversioned (default)** | Each overwrite replaces the object permanently |
| **Enabled** | S3 generates a unique version ID for each write |
| **Suspended** | New writes create unversioned objects; existing versions remain |

## CLI Commands

```bash
# Enable versioning on a bucket
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Suspend versioning (existing versions are preserved)
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Suspended

# Check versioning status
aws s3api get-bucket-versioning --bucket my-bucket

# Upload an object (version ID is returned)
aws s3api put-object --bucket my-bucket --key hello.txt --body hello.txt

# Upload a new version (same key, different content)
aws s3api put-object --bucket my-bucket --key hello.txt --body hello-v2.txt

# List all versions of an object
aws s3api list-object-versions --bucket my-bucket --prefix hello.txt

# List all versions (including delete markers) in a bucket
aws s3api list-object-versions --bucket my-bucket

# Get a specific version of an object
aws s3api get-object --bucket my-bucket --key hello.txt \
  --version-id <version-id> hello-restored.txt

# Delete a specific version (permanent delete)
aws s3api delete-object --bucket my-bucket --key hello.txt \
  --version-id <version-id>

# Delete only the delete marker (restores the object)
aws s3api delete-object --bucket my-bucket --key hello.txt \
  --version-id <delete-marker-version-id>

# Restore a previous version by copying it to the same key (no version ID = latest)
aws s3 cp s3://my-bucket/hello.txt?versionId=<version-id> \
  s3://my-bucket/hello.txt
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'
key = 'documents/report.pdf'

# Enable versioning
def enable_versioning(bucket):
    response = s3.put_bucket_versioning(
        Bucket=bucket,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    print(f"Versioning enabled on {bucket}")
    return response

# Enable versioning (required before replication can be set up)
enable_versioning(bucket)

# Upload multiple versions
def upload_versions(bucket, key, versions_data):
    """Upload multiple versions of an object"""
    for i, data in enumerate(versions_data):
        response = s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=data.encode('utf-8')
        )
        print(f"Version {i+1}: {response['VersionId']}")
    return response

upload_versions(bucket, key, [
    "Version 1: Original content",
    "Version 2: Updated content",
    "Version 3: Final version"
])

# List all versions
def list_versions(bucket, prefix=''):
    """List all versions of objects"""
    response = s3.list_object_versions(Bucket=bucket, Prefix=prefix)
    
    print("Versions:")
    for version in response.get('Versions', []):
        is_latest = "✓" if version['IsLatest'] else " "
        print(f"  [{is_latest}] {version['Key']} v{version['VersionId'][:8]}... "
              f"({version['Size']} bytes, {version['LastModified']})")
    
    print("\nDelete Markers:")
    for marker in response.get('DeleteMarkers', []):
        print(f"  [DEL] {marker['Key']} ({marker['LastModified']})")

list_versions(bucket)

# Get a specific version
def get_version_content(bucket, key, version_id):
    """Get the content of a specific version"""
    response = s3.get_object(
        Bucket=bucket,
        Key=key,
        VersionId=version_id
    )
    content = response['Body'].read().decode('utf-8')
    print(f"Content: {content}")
    return content

# Restore a previous version by copying over the current
def restore_version(bucket, key, version_id):
    """Restore a specific version as the current version"""
    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': key, 'VersionId': version_id},
        Key=key
    )
    print(f"Restored version {version_id[:8]}... as current")
```

## Versioning and Delete Markers

### Normal Delete (with Versioning Enabled)
When you delete an object with versioning enabled:
```
Before: [v1, v2(current)]
Action: delete object
After:  [v1, v2, DELETE_MARKER(current)]
```
The object appears "deleted" but can be restored by removing the delete marker.

### Permanent Delete
To permanently delete a version:
```
Before: [v1, v2, DELETE_MARKER]
Action: delete v1 with --version-id
After:  [v2, DELETE_MARKER]
```

### Restoring from Delete Marker
```
Before: [v1, v2, DELETE_MARKER(current)]
Action: delete the delete marker
After:  [v1, v2(current)]
```

## Versioning and Other Features

| Feature | Versioning Interaction | Exam Impact |
|---|---|---|
| **Lifecycle Rules** | Can expire old versions or transition them | High |
| **Object Replication** | Versioning must be enabled on source AND destination | High |
| **Object Lock** | Requires versioning to be enabled | High |
| **MFA Delete** | Requires versioning; adds MFA protection to deletes | Medium |
| **Pre-signed URLs** | Can target specific version IDs | Low |

## Exam Tips

### 1. Versioning Cannot Be Disabled
Once enabled, versioning can be **suspended** but never turned off. Existing versions remain accessible.

### 2. MFA Delete with Versioning
MFA Delete can be enabled alongside versioning for extra protection — deleting a version requires multi-factor authentication.

### 3. Cost Implications
Each version counts as a separate object. If you upload the same object 100 times, you pay for 100 objects. Use lifecycle rules to expire old versions.

### 4. Replication Prerequisite
Versioning must be enabled on BOTH source and destination buckets for replication to work.

### 5. Common Exam Question
**Q:** A user accidentally deleted a critical file from an S3 bucket. Versioning is enabled. How do they recover it?
**A:** Remove the delete marker (or restore the previous version). The object still exists — only the delete marker needs to be removed.

## Exam Quick Reference
- ✅ **Protects against accidental overwrites and deletions**
- ✅ **Cannot be disabled** (only suspended)
- ✅ **Delete markers** hide objects without deleting them
- ✅ **Version ID** is unique per upload
- ✅ **Required** for replication, Object Lock, MFA Delete
- ✅ **Cost**: each version is billed separately
- ✅ Use **lifecycle rules** to manage old version costs