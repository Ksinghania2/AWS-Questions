# S3 Object Metadata

Every S3 object has **metadata** — key-value pairs that describe the object. Metadata can be **system-defined** or **user-defined**.

## Types of Metadata

### System Metadata
Automatically set by S3, cannot be modified directly.

| Metadata | Description | Example |
|---|---|---|
| `Content-Type` | MIME type of the object | `application/pdf`, `image/jpeg` |
| `Content-Length` | Size in bytes | `1024` |
| `ETag` | Object hash (MD5 for plain PUT, multipart hash for multipart) | `"abc123..."` |
| `Last-Modified` | Date/time of last modification | `2024-05-15T10:30:00Z` |
| `Storage-Class` | Storage class of the object | `STANDARD`, `GLACIER` |
| `Version-Id` | Version ID (if versioning enabled) | `null` or UUID |

### User-Defined Metadata
Custom metadata you can set when uploading an object.

- Must start with prefix `x-amz-meta-`
- Max 2 KB total for all user metadata
- Values are stored as strings
- Can be set during PUT or POST operations

## CLI Commands

```bash
# Upload with custom metadata
aws s3api put-object \
  --bucket my-bucket \
  --key report.pdf \
  --body report.pdf \
  --metadata "department=finance,project=audit-2024,retention=7years" \
  --content-type "application/pdf"

# View all metadata of an object
aws s3api head-object --bucket my-bucket --key report.pdf

# View specific metadata fields
aws s3api head-object --bucket my-bucket --key report.pdf \
  --query "Metadata" --output json

# Get Content-Type only
aws s3api head-object --bucket my-bucket --key report.pdf \
  --query "ContentType" --output text

# Get Last-Modified
aws s3api head-object --bucket my-bucket --key report.pdf \
  --query "LastModified" --output text

# Get ETag
aws s3api head-object --bucket my-bucket --key report.pdf \
  --query "ETag" --output text

# Update metadata (requires copying the object to itself)
aws s3api copy-object \
  --bucket my-bucket \
  --copy-source my-bucket/report.pdf \
  --key report.pdf \
  --metadata "department=engineering,project=updated" \
  --metadata-directive REPLACE

# Note: --metadata-directive REPLACE replaces all metadata
# Use COPY to preserve existing metadata and only change specified fields
```

## Python (boto3) Examples

```python
import boto3
import json

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload with metadata
def upload_with_metadata(bucket, key, file_path, metadata, content_type=None):
    """Upload a file with custom metadata"""
    extra_args = {
        'Metadata': metadata
    }
    if content_type:
        extra_args['ContentType'] = content_type
    
    s3.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
    print(f"Uploaded {key} with metadata: {metadata}")

upload_with_metadata(
    bucket,
    'documents/report.pdf',
    'report.pdf',
    {
        'department': 'finance',
        'project': 'audit-2024',
        'retention': '7years',
        'created-by': 'john.doe@company.com'
    },
    content_type='application/pdf'
)

# Read metadata
def get_object_metadata(bucket, key):
    """Get all metadata for an object"""
    response = s3.head_object(Bucket=bucket, Key=key)
    
    print(f"Object: {key}")
    print(f"  Size: {response['ContentLength']} bytes")
    print(f"  Content-Type: {response.get('ContentType', 'N/A')}")
    print(f"  ETag: {response['ETag']}")
    print(f"  Last-Modified: {response['LastModified']}")
    print(f"  Storage-Class: {response.get('StorageClass', 'STANDARD')}")
    print(f"  Version-Id: {response.get('VersionId', 'null')}")
    
    if 'Metadata' in response and response['Metadata']:
        print("  User Metadata:")
        for k, v in response['Metadata'].items():
            print(f"    {k}: {v}")
    
    return response

get_object_metadata(bucket, 'documents/report.pdf')

# Update metadata (copy to self)
def update_metadata(bucket, key, new_metadata):
    """Update metadata by copying object to itself"""
    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': key},
        Key=key,
        Metadata=new_metadata,
        MetadataDirective='REPLACE'
    )
    print(f"Updated metadata for {key}")

update_metadata(bucket, 'documents/report.pdf', {
    'department': 'engineering',
    'status': 'reviewed',
    'reviewed-by': 'jane.smith@company.com'
})

# Search objects by metadata (using S3 Select or external indexing)
# Note: S3 does not natively support metadata-based queries
# You need to use external indexing (e.g., DynamoDB) for metadata search
def index_metadata_to_dynamodb(bucket, prefix=''):
    """Example: Index S3 metadata in DynamoDB for searchability"""
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            head = s3.head_object(Bucket=bucket, Key=obj['Key'])
            metadata = head.get('Metadata', {})
            
            # In production, you'd write this to DynamoDB
            print(f"Object: {obj['Key']}")
            print(f"  Metadata: {json.dumps(metadata, indent=4)}")

index_metadata_to_dynamodb(bucket)
```

## Common Metadata Use Cases

| Use Case | Metadata Example | Benefit |
|---|---|---|
| **Data classification** | `classification: confidential` | Access control policies |
| **Retention management** | `retention: 7years` | Lifecycle rule targeting |
| **Provenance tracking** | `source: etl-job-42` | Audit trail |
| **Content description** | `author: john.doe` | Search/discovery |
| **Processing status** | `status: processed` | Workflow automation |

## Important Notes

### 1. Metadata is NOT searchable natively
S3 does not provide a way to query objects by metadata. You must use external indexing (DynamoDB, Athena, Elasticsearch) for metadata-based searches.

### 2. Metadata size limit
Total user metadata cannot exceed **2 KB** (including both keys and values).

### 3. Metadata keys are lowercase
When you set metadata with uppercase letters, S3 converts them to lowercase. `Department: Finance` becomes `department: Finance`.

### 4. Metadata directive
When copying an object:
- **REPLACE**: Replaces all metadata with the new values
- **COPY**: Preserves the source object's metadata

### 5. Content-Type is important
Setting the correct `Content-Type` is critical for:
- Static website hosting (browser needs correct MIME type)
- Presigned URLs (client needs to know how to handle the file)

## Exam Quick Reference
- ✅ **System metadata**: Content-Type, Content-Length, ETag, Last-Modified, Storage-Class
- ✅ **User metadata**: Custom key-value pairs with `x-amz-meta-` prefix
- ✅ **2 KB max** for all user metadata
- ✅ **Not searchable** natively — needs external indexing
- ✅ **Metadata keys** are converted to lowercase
- ✅ **REPLACE vs COPY** directive when updating via copy-object
- ✅ **Content-Type** is critical for web serving and presigned URLs