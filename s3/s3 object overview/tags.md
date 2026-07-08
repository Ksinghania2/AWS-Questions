# S3 Object Tags

Object tags are **key-value pairs** used to categorize and manage objects. Unlike metadata, tags are **natively searchable** and can be used in **IAM policies** and **lifecycle rules**.

## Key Features

| Feature | Details |
|---|---|
| **Max tags per object** | 10 |
| **Max key length** | 128 characters (UTF-8) |
| **Max value length** | 256 characters (UTF-8) |
| **Searchable?** | **Yes** — via `s3:ExistingObjectTag/<key>` condition key |
| **Cost** | Free (no additional charge) |
| **Prefix** | None (unlike metadata which uses `x-amz-meta-`) |

## CLI Commands

```bash
# Upload object with tags
aws s3api put-object \
  --bucket my-bucket \
  --key report.pdf \
  --body report.pdf \
  --tagging "department=finance&project=audit&retention=7years"

# Add tags to existing object
aws s3api put-object-tagging \
  --bucket my-bucket \
  --key report.pdf \
  --tagging '{"TagSet": [{"Key": "department", "Value": "finance"}, {"Key": "status", "Value": "active"}]}'

# Get tags of an object
aws s3api get-object-tagging --bucket my-bucket --key report.pdf

# Delete all tags from an object
aws s3api delete-object-tagging --bucket my-bucket --key report.pdf

# List objects with specific tag (requires API, no direct CLI filter)
# Use --query to filter locally
aws s3api list-objects-v2 --bucket my-bucket \
  --query "Contents[?contains(Key, 'report')].[Key,Size]"

# Copy object preserving tags
aws s3api copy-object \
  --bucket my-bucket \
  --copy-source my-bucket/report.pdf \
  --key report-archive.pdf \
  --tagging-directive COPY

# Copy object with new tags
aws s3api copy-object \
  --bucket my-bucket \
  --copy-source my-bucket/report.pdf \
  --key report-archive.pdf \
  --tagging "department=archive" \
  --tagging-directive REPLACE
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload with tags
def upload_with_tags(bucket, key, file_path, tags):
    """Upload a file with tags"""
    tag_string = '&'.join(f'{k}={v}' for k, v in tags.items())
    
    s3.upload_file(
        file_path,
        bucket,
        key,
        ExtraArgs={'Tagging': tag_string}
    )
    print(f"Uploaded {key} with tags: {tags}")

upload_with_tags(bucket, 'documents/report.pdf', 'report.pdf', {
    'department': 'finance',
    'project': 'audit-2024',
    'retention': '7years',
    'classification': 'confidential'
})

# Get tags
def get_object_tags(bucket, key):
    """Get all tags for an object"""
    response = s3.get_object_tagging(Bucket=bucket, Key=key)
    tags = response['TagSet']
    
    print(f"Tags for {key}:")
    for tag in tags:
        print(f"  {tag['Key']}: {tag['Value']}")
    
    return tags

get_object_tags(bucket, 'documents/report.pdf')

# Filter objects by tag (using IAM conditions or external indexing)
def list_objects_by_tag(bucket, tag_key, tag_value, prefix=''):
    """List objects with a specific tag value"""
    # Note: S3 doesn't natively filter by tags in list operations
    # This is a client-side filter
    paginator = s3.get_paginator('list_objects_v2')
    matching = []
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            tags = s3.get_object_tagging(Bucket=bucket, Key=obj['Key'])
            tag_dict = {t['Key']: t['Value'] for t in tags['TagSet']}
            
            if tag_dict.get(tag_key) == tag_value:
                matching.append(obj['Key'])
    
    print(f"Objects with {tag_key}={tag_value}:")
    for key in matching:
        print(f"  {key}")
    
    return matching

list_objects_by_tag(bucket, 'department', 'finance')

# Copy with tags
def copy_with_tags(source_bucket, source_key, dest_bucket, dest_key, new_tags=None):
    """Copy object, optionally replacing tags"""
    if new_tags:
        # Replace tags
        tag_string = '&'.join(f'{k}={v}' for k, v in new_tags.items())
        s3.copy_object(
            Bucket=dest_bucket,
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Key=dest_key,
            Tagging=tag_string,
            TaggingDirective='REPLACE'
        )
        print(f"Copied {source_key} to {dest_key} with new tags: {new_tags}")
    else:
        # Preserve tags
        s3.copy_object(
            Bucket=dest_bucket,
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Key=dest_key,
            TaggingDirective='COPY'
        )
        print(f"Copied {source_key} to {dest_key} preserving tags")

copy_with_tags(bucket, 'documents/report.pdf', bucket, 'archive/report.pdf', {'status': 'archived'})
```

## Tags in IAM Policies

Tags can be used in IAM policies to control access based on object tags.

### Example: Allow access only to objects with tag classification=public
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/classification": "public"
        }
      }
    }
  ]
}
```

### Example: Require specific tag when uploading
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "s3:RequestObjectTagKeys": ["department", "classification"],
          "s3:RequestObjectTag/classification": ["confidential", "internal", "public"]
        }
      }
    }
  ]
}
```

## Tags in Lifecycle Rules

```bash
# Lifecycle rule that applies only to objects with a specific tag
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "archive-confidential",
      "Status": "Enabled",
      "Filter": {
        "And": {
          "Prefix": "documents/",
          "Tags": [{"Key": "classification", "Value": "confidential"}]
        }
      },
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ]
    }]
  }'
```

## Tags vs Metadata Comparison

| Feature | Tags | Metadata |
|---|---|---|
| **Searchable in IAM policies** | ✅ Yes (`s3:ExistingObjectTag`) | ❌ No |
| **Searchable in S3** | ❌ No (client-side only) | ❌ No |
| **Max count/size** | 10 tags, 128+256 chars each | 2 KB total |
| **Cost** | Free | Free |
| **Update without copying** | ✅ Yes (put-object-tagging) | ❌ No (must copy) |
| **Use in lifecycle filters** | ✅ Yes | ❌ No |
| **Use in cost allocation** | ✅ Yes (AWS billing tags) | ❌ No |

## Exam Quick Reference
- ✅ **10 tags** max per object
- ✅ **128 chars** key, **256 chars** value
- ✅ **Searchable** via IAM policy condition `s3:ExistingObjectTag`
- ✅ **Usable in lifecycle rules** as filters
- ✅ **Cost allocation** tagging supported
- ✅ **Updateable** without copying the object
- ✅ **Different from metadata** — tags are queryable, metadata is not
- ✅ **No additional cost** for tagging