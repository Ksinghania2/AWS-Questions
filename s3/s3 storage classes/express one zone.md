# S3 Express One Zone

S3 Express One Zone is a **high-performance, single-AZ** storage class designed for **latency-sensitive applications** that need consistent single-digit millisecond data access.

## Key Characteristics

| Attribute | Value |
|---|---|
| **Durability** | 99.999999999% (11 9's) |
| **Availability** | 99.5% |
| **AZ Coverage** | **1** Availability Zone |
| **Minimum object size** | 0 bytes |
| **Minimum storage duration** | None |
| **Retrieval cost** | None |
| **Storage cost** | Higher than Standard |
| **Performance** | **Single-digit millisecond** latency |
| **Use case** | High-performance, latency-sensitive apps |

## Key Features

### S3 Express Buckets (Different from Regular Buckets)
- Uses a **new bucket type** called "directory buckets"
- Bucket name format: `<name>--<az-id>--x-s3` (e.g., `my-bucket--usw2-az1--x-s3`)
- Accessed via a **regional endpoint** (not global)
- **10x better performance** than S3 Standard
- Designed for **millions of requests per minute**

### When to Use Express One Zone

**Good Use Cases:**
- **Real-time analytics** — low-latency data ingestion
- **Machine learning training** — fast data loading
- **High-frequency trading** — microsecond-level performance
- **Gaming leaderboards** — real-time score updates
- **IoT data ingestion** — millions of device events per second
- **Ad tech** — real-time bidding data

**Not Ideal For:**
- Data that must survive an AZ failure
- Compliance data requiring multi-AZ
- Infrequently accessed data (Standard is cheaper)
- Long-term archival

## CLI Commands

```bash
# Create an S3 Express One Zone directory bucket
# Note: Must specify the AZ through which the bucket is accessed
aws s3api create-bucket \
  --bucket my-bucket--usw2-az1--x-s3 \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2,BucketType=Directory

# Upload to Express One Zone
aws s3 cp data.json s3://my-bucket--usw2-az1--x-s3/data.json

# List objects
aws s3 ls s3://my-bucket--usw2-az1--x-s3/

# Get object
aws s3 cp s3://my-bucket--usw2-az1--x-s3/data.json ./downloaded.json

# Delete bucket (must be empty first)
aws s3 rb s3://my-bucket--usw2-az1--x-s3 --force
```

## Python (boto3) Examples

```python
import boto3

# S3 Express One Zone uses a different endpoint
s3express = boto3.client('s3', region_name='us-west-2')

# Create a directory bucket
bucket_name = 'my-express-bucket--usw2-az1--x-s3'
try:
    response = s3express.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2',
            'Bucket': {
                'Type': 'Directory',
                'DataRedundancy': 'SingleAvailabilityZone'
            }
        }
    )
    print(f"Express bucket created: {bucket_name}")
except Exception as e:
    print(f"Error: {e}")

# Upload with high performance
s3express.upload_file(
    'real-time-data.json',
    bucket_name,
    'events/2024/05/15/data.json'
)
print("Uploaded to Express One Zone")

# Read with low latency
response = s3express.get_object(
    Bucket=bucket_name,
    Key='events/2024/05/15/data.json'
)
print(f"Read {len(response['Body'].read())} bytes with low latency")

# Performance benchmark
import time

def benchmark_s3express(bucket, key, iterations=100):
    """Benchmark read performance"""
    times = []
    for i in range(iterations):
        start = time.time()
        s3express.get_object(Bucket=bucket, Key=key)
        elapsed = (time.time() - start) * 1000  # ms
        times.append(elapsed)
    
    avg = sum(times) / len(times)
    print(f"Average read latency: {avg:.2f} ms")
    print(f"Min: {min(times):.2f} ms, Max: {max(times):.2f} ms")
    return avg

# benchmark_s3express(bucket_name, 'events/2024/05/15/data.json')
```

## Express One Zone vs Standard

| Feature | Express One Zone | Standard |
|---|---|---|
| **Latency** | Single-digit ms | Tens of ms |
| **Throughput** | Millions of requests/min | Thousands/sec per prefix |
| **AZs** | 1 | ≥ 3 |
| **Availability** | 99.5% | 99.99% |
| **Cost** | Higher | Lower |
| **Bucket type** | Directory bucket | Regular bucket |
| **Endpoint** | Regional (AZ-specific) | Global |
| **Best for** | Performance-critical apps | General purpose |

## Exam Tips

### 1. New Bucket Type
S3 Express One Zone uses "directory buckets" — a different bucket type with a special naming convention (`<name>--<az-id>--x-s3`).

### 2. Single AZ
Like One Zone-IA, data is stored in a single AZ. If the AZ fails, data is lost.

### 3. Performance
10x better performance than S3 Standard. Designed for applications that need consistent single-digit millisecond latency.

### 4. Cost
More expensive than Standard. Use only when performance requirements justify the cost.

### 5. Common Exam Question
**Q:** An application needs to process millions of real-time events per second with consistent single-digit millisecond latency. Which S3 storage class?
**A:** S3 Express One Zone (not Standard — not fast enough; not One Zone-IA — not designed for performance)

## Exam Quick Reference
- ✅ **Single-digit millisecond** latency
- ✅ **10x performance** vs Standard
- ✅ **Single AZ** — data lost if AZ fails
- ✅ **Directory bucket** type (special naming)
- ✅ **Regional endpoint** (not global)
- ✅ **Higher cost** than Standard
- ✅ Best for **real-time, high-throughput, latency-sensitive** apps