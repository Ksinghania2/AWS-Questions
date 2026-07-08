# S3 Transfer Acceleration

Transfer Acceleration speeds up uploads to S3 using **AWS edge locations** — data takes the fastest path to the destination region.

## How It Works

```
Client → Edge Location (AWS Global Network) → S3 Bucket Region
```

Instead of: `Client → Internet → S3 Bucket Region` (slower, unpredictable)

## CLI Commands

```bash
# Enable Transfer Acceleration
aws s3api put-bucket-accelerate-configuration \
  --bucket my-bucket \
  --accelerate-configuration Status=Enabled

# Check if enabled
aws s3api get-bucket-accelerate-configuration --bucket my-bucket

# Upload using accelerated endpoint
aws s3 cp large-file.zip s3://my-bucket/ \
  --endpoint-url https://my-bucket.s3-accelerate.amazonaws.com

# Test speed comparison
aws s3 cp large-file.zip s3://my-bucket/  # Standard
aws s3 cp large-file.zip s3://my-bucket/ --endpoint-url https://my-bucket.s3-accelerate.amazonaws.com  # Accelerated

# Use S3 Transfer Acceleration speed checker
# (Tool at: https://s3-accelerate-speedtest.s3-accelerate.amazonaws.com/en/accelerate-speed-comparsion.html)
```

## When to Use

| Scenario | Recommendation |
|---|---|
| Users are far from bucket region | ✅ Use Transfer Acceleration |
| Large uploads (> 1 GB) | ✅ Use Transfer Acceleration |
| Time-sensitive uploads | ✅ Use Transfer Acceleration |
| Users in same region as bucket | ❌ Not needed (adds latency) |
| Small uploads (< 1 GB) | ❌ Not worth it |

## Exam Quick Reference
- ✅ Uses **AWS edge locations** for optimal routing
- ✅ Best for **long-distance, large-file uploads**
- ✅ **Additional cost** (per GB transferred through edge)
- ✅ Must be **enabled on the bucket** first
- ✅ Use **`s3-accelerate.amazonaws.com`** endpoint
- ✅ **Not beneficial** for same-region or small uploads