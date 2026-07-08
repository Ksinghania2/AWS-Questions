# Bucket Naming Rules

Bucket naming is one of the most important S3 design decisions because bucket names must be globally unique and meet strict AWS constraints.

## Rules (Must Know for Exam)
- **3 to 63 characters** long
- **Lowercase letters, numbers, and hyphens** only (no uppercase, no underscores)
- Must start and end with a **letter or number**
- Cannot be formatted as an **IP address** (e.g., 192.168.1.1)
- Must be **globally unique** across all AWS accounts and all regions
- For DNS-compliant names in most regions, avoid underscores and uppercase

## Why It Matters (Exam Tip)
A bucket name becomes part of the globally visible endpoint:
```
https://<bucket-name>.s3.<region>.amazonaws.com
```
If the name contains uppercase or underscores, the URL may not resolve correctly in DNS-based access patterns.

## Good and Bad Examples
| Good Examples | Bad Examples | Why Bad |
|---|---|---|
| `my-data-bucket-2024` | `MyBucket` | Uppercase not allowed |
| `project-logs-us-east-1` | `my_bucket` | Underscores not allowed |
| `data-lake-prod-123` | `mybucket-` | Ends with hyphen |
| `backup-2024-05` | `192.168.1.1` | IP address format not allowed |
| `my-company-app-data` | `ab` | Too short (< 3 chars) |

## CLI Commands

### Create a bucket (us-east-1)
```bash
aws s3api create-bucket --bucket my-unique-bucket-12345 --region us-east-1
```

### Create a bucket (other regions - requires LocationConstraint)
```bash
aws s3api create-bucket --bucket my-unique-bucket-12345 --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2
```

### Check if a bucket name is available
```bash
# Try creating it - if it fails with "BucketAlreadyExists", the name is taken
aws s3api create-bucket --bucket my-desired-name --region us-east-1 2>&1
```

### List all buckets
```bash
aws s3 ls
# OR
aws s3api list-buckets --query "Buckets[].Name" --output table
```

## Python (boto3) Examples

```python
import boto3

s3_client = boto3.client('s3', region_name='us-east-1')

# Create a bucket in us-east-1
bucket_name = 'my-python-bucket-12345'
try:
    response = s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully")
    print(f"Location: {response['Location']}")
except Exception as e:
    print(f"Error: {e}")

# Create a bucket in another region
bucket_name = 'my-python-bucket-west-12345'
try:
    response = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
    )
    print(f"Bucket '{bucket_name}' created successfully")
except Exception as e:
    print(f"Error: {e}")

# List all buckets
response = s3_client.list_buckets()
print("Existing buckets:")
for bucket in response['Buckets']:
    print(f"  {bucket['Name']} (created: {bucket['CreationDate']})")
```

## Best Practices
- Choose a **stable, descriptive name** that won't need to change
- Keep names short enough for scripts and automation
- **Avoid exposing internal/sensitive information** in the name (e.g., `acme-corp-customer-pii-data`)
- Use a naming convention like `{environment}-{application}-{data-type}-{region}` (e.g., `prod-analytics-logs-us-east-1`)
- For cross-account access, consider prefix patterns that are unlikely to conflict

## Common Pitfalls (Exam Scenarios)
| Mistake | Consequence |
|---|---|
| Using uppercase or underscores | DNS-incompatible, may cause access errors |
| Choosing a common name | Name already taken (global uniqueness) |
| Forgetting LocationConstraint for non-us-east-1 | API error (InvalidLocationConstraint) |
| Creating bucket with special characters | Immediate validation error |
| Not checking name availability | Wasted time on error handling |

## Exam Quick Reference
- ✅ 3-63 chars, lowercase, numbers, hyphens only
- ✅ Globally unique (not just your account)
- ✅ Must start/end with letter or number
- ✅ Cannot be IP address
- ✅ `us-east-1` does NOT need LocationConstraint
- ✅ All other regions REQUIRE LocationConstraint