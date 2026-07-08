# S3 Standard Storage Class

S3 Standard is the **default** storage class designed for frequently accessed data with low latency and high throughput.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.99% |
| **AZ Coverage** | ≥ 3 Availability Zones |
| **Minimum object size** | 0 bytes |
| **Minimum storage duration** | None |
| **Retrieval cost** | Free |
| **Use case** | Frequently accessed, active data |

## When to Use S3 Standard

### Good Use Cases
- Active application data (user uploads, content for websites)
- Frequently accessed analytics data
- Data lakes for active querying (Athena, Redshift Spectrum)
- Static website assets (HTML, CSS, JS, images)
- Media files for active streaming/processing
- Database backups for active recovery testing

### Not Ideal For
- Infrequently accessed data (use Standard-IA instead — cheaper storage)
- Archival data (use Glacier or Deep Archive)
- Data with unknown access patterns (use Intelligent-Tiering)

## CLI Commands

```bash
# Upload with explicit Standard class (default)
aws s3 cp file.txt s3://my-bucket/file.txt --storage-class STANDARD

# Upload entire directory
aws s3 sync ./my-files/ s3://my-bucket/files/ --storage-class STANDARD

# Check storage class of an object
aws s3api head-object --bucket my-bucket --key file.txt \
  --query StorageClass --output text

# List all objects and their storage classes
aws s3api list-objects-v2 --bucket my-bucket \
  --query "Contents[].[Key, StorageClass]" --output table

# Change storage class from Standard to something else (copy to itself)
aws s3 cp s3://my-bucket/file.txt s3://my-bucket/file.txt \
  --storage-class STANDARD_IA

# Calculate storage cost estimate
aws s3api list-objects-v2 --bucket my-bucket \
  --query "sum(Contents[].Size)" --output text
```

## Python (boto3) Examples

```python
import boto3

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Upload with Standard storage class
s3.upload_file(
    'local-file.txt',
    bucket,
    'remote-file.txt',
    ExtraArgs={'StorageClass': 'STANDARD'}
)
print("Uploaded as STANDARD")

# Check storage class of all objects
def check_storage_classes(bucket, prefix=''):
    """Check what storage classes are in use"""
    paginator = s3.get_paginator('list_objects_v2')
    storage_classes = {}
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            sc = obj.get('StorageClass', 'STANDARD')
            storage_classes[sc] = storage_classes.get(sc, 0) + 1
    
    print("Storage class distribution:")
    for sc, count in storage_classes.items():
        print(f"  {sc}: {count} objects")

check_storage_classes(bucket)

# Calculate total storage size
response = s3.list_objects_v2(Bucket=bucket)
total_size = sum(obj['Size'] for obj in response.get('Contents', []))
print(f"Total storage: {total_size / (1024**3):.2f} GB")
```

## Exam Tips

### 1. Default Storage Class
If you don't specify `--storage-class`, S3 Standard is used by default. This is a common exam point — many questions assume default behavior.

### 2. Cost Components
S3 Standard costs include:
- **Storage cost** per GB/month
- **PUT/COPY/POST/LIST** request costs
- **GET/SELECT** request costs
- **Data transfer OUT** to internet (free for IN)

### 3. Performance
- First byte latency: milliseconds
- Scales to thousands of requests per second
- For higher throughput, distribute across multiple prefixes

### 4. Durability vs Availability
| Concept | S3 Standard | Meaning |
|---|---|---|
| Durability | 11 9's (99.999999999%) | Probability of object loss |
| Availability | 99.99% | Uptime per year (~53 mins downtime) |

## Cost Optimization

```python
# Estimate monthly storage cost
def estimate_monthly_cost(bucket, price_per_gb=0.023):
    """Estimate S3 Standard monthly cost (price varies by region)"""
    response = s3.list_objects_v2(Bucket=bucket)
    total_bytes = sum(obj['Size'] for obj in response.get('Contents', []))
    total_gb = total_bytes / (1024**3)
    monthly_cost = total_gb * price_per_gb
    
    print(f"Storage: {total_gb:.2f} GB")
    print(f"Monthly cost (${price_per_gb}/GB): ${monthly_cost:.2f}")
    return monthly_cost

# us-east-1 Standard price: ~$0.023/GB
estimate_monthly_cost(bucket, 0.023)
```

## Decision Flowchart
```
Is data accessed frequently?
├── YES → Is data critical and needs high durability?
│   ├── YES → S3 Standard ✅
│   └── NO → S3 Standard (still the safest choice)
└── NO → Consider Standard-IA, One Zone-IA, or Intelligent-Tiering
```

## Exam Quick Reference
- ✅ **Default storage class** if not specified
- ✅ **11 9's durability**, **99.99% availability**
- ✅ **≥ 3 AZs** for redundancy
- ✅ **No minimum** storage duration or object size
- ✅ **Millisecond** first-byte latency
- ✅ **No retrieval cost** (only storage + request costs)
- ✅ Best for **active, frequently accessed** data