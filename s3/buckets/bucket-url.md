# Bucket URL Formats and Endpoints

Understanding S3 bucket URL formats is critical for configuring access, setting up static websites, and troubleshooting connectivity.

## S3 Endpoint Formats

### 1. Path-Style URL (Legacy - older regions only)
```
https://s3.<region>.amazonaws.com/<bucket-name>/<object-key>
```
Example: `https://s3.us-east-1.amazonaws.com/my-bucket/photo.jpg`

### 2. Virtual-Hosted Style URL (Recommended - modern regions)
```
https://<bucket-name>.s3.<region>.amazonaws.com/<object-key>
```
Example: `https://my-bucket.s3.us-east-1.amazonaws.com/photo.jpg`

### 3. Global Endpoint (DNS-based routing)
```
https://<bucket-name>.s3.amazonaws.com/<object-key>
```
Example: `https://my-bucket.s3.amazonaws.com/photo.jpg` (routes to bucket's region)

### 4. Static Website Endpoint
```
http://<bucket-name>.s3-website-<region>.amazonaws.com
```
Example: `http://my-website-bucket.s3-website-us-east-1.amazonaws.com`

### 5. Transfer Acceleration Endpoint
```
https://<bucket-name>.s3-accelerate.amazonaws.com/<object-key>
```
Example: `https://my-bucket.s3-accelerate.amazonaws.com/photo.jpg`

### 6. Dual-Stack Endpoint (IPv4 + IPv6)
```
https://<bucket-name>.s3.dualstack.<region>.amazonaws.com/<object-key>
```
Example: `https://my-bucket.s3.dualstack.us-east-1.amazonaws.com/photo.jpg`

### 7. FIPS 140-2 Endpoint (GovCloud/Compliance)
```
https://<bucket-name>.s3-fips.<region>.amazonaws.com/<object-key>
```
Example: `https://my-bucket.s3-fips.us-east-1.amazonaws.com/photo.jpg`

### 8. Access Point Endpoint
```
https://<access-point-name>-<account-id>.s3-accesspoint.<region>.amazonaws.com
```
Example: `https://my-access-point-123456789012.s3-accesspoint.us-east-1.amazonaws.com`

## CLI Commands to Verify Endpoints

```bash
# Get bucket location (region)
aws s3api get-bucket-location --bucket my-bucket --query LocationConstraint

# Get the DNS-style endpoint
aws s3 presign s3://my-bucket/test.txt --expires-in 60

# Test virtual-hosted style access
curl -I https://my-bucket.s3.us-east-1.amazonaws.com/test.txt

# Test dual-stack endpoint
curl -I https://my-bucket.s3.dualstack.us-east-1.amazonaws.com/test.txt

# Enable Transfer Acceleration
aws s3api put-bucket-accelerate-configuration \
  --bucket my-bucket \
  --accelerate-configuration Status=Enabled

# Test Transfer Acceleration endpoint
curl -I https://my-bucket.s3-accelerate.amazonaws.com/test.txt

# Test static website endpoint
curl -I http://my-website-bucket.s3-website-us-east-1.amazonaws.com/index.html
```

## Python (boto3) - Generate URLs

```python
import boto3

s3 = boto3.client('s3')
bucket_name = 'my-bucket'
object_key = 'test.txt'

# Generate presigned URLs using different endpoints
# Virtual-hosted style (default)
url_virtual = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_key},
    ExpiresIn=3600
)
print(f"Virtual-hosted URL:\n{url_virtual}\n")

# Path-style (requires configuring)
from botocore.config import Config
s3_path = boto3.client('s3', config=Config(
    s3={'addressing_style': 'path'}
))
url_path = s3_path.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_key},
    ExpiresIn=3600
)
print(f"Path-style URL:\n{url_path}\n")

# Get bucket website URL
def get_bucket_url(bucket_name):
    """Helper to get the correct URL format for a bucket"""
    response = s3.get_bucket_location(Bucket=bucket_name)
    region = response['LocationConstraint'] or 'us-east-1'
    return f"https://{bucket_name}.s3.{region}.amazonaws.com"

print(f"Bucket URL: {get_bucket_url(bucket_name)}")

# Check if website hosting is enabled
def get_website_url(bucket_name):
    """Get the static website URL if configured"""
    try:
        s3.get_bucket_website(Bucket=bucket_name)
        response = s3.get_bucket_location(Bucket=bucket_name)
        region = response['LocationConstraint'] or 'us-east-1'
        return f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
    except:
        return "Website hosting not enabled"

print(f"Website URL: {get_website_url(bucket_name)}")
```

## URL Format Comparison Table

| Format | Example | When to Use |
|---|---|---|
| Virtual-hosted | `bucket.s3.region.amazonaws.com` | Modern, recommended, most common |
| Path-style | `s3.region.amazonaws.com/bucket` | Legacy buckets (created before Sept 2020) |
| Global | `bucket.s3.amazonaws.com` | When region doesn't need to be specified |
| Website | `bucket.s3-website-region.amazonaws.com` | Only for static website hosting |
| Accelerate | `bucket.s3-accelerate.amazonaws.com` | Fast uploads across long distances |
| Dual-stack | `bucket.s3.dualstack.region.amazonaws.com` | When IPv6 is required |
| FIPS | `bucket.s3-fips.region.amazonaws.com` | FedRAMP/FIPS compliance |
| Access Point | `accesspoint-acctid.s3-accesspoint.region.amazonaws.com` | When using S3 Access Points |

## Common Issues with URL Formats

### Issue 1: Path-style deprecation
Buckets created after September 30, 2020, in all regions except `us-east-1`, `us-west-1`, `us-west-2`, `eu-west-1`, `ap-southeast-1`, `ap-northeast-1`, `sa-east-1` do NOT support path-style URLs.

### Issue 2: Website endpoint uses HTTP, not HTTPS
The static website hosting endpoint (`s3-website-*.amazonaws.com`) only supports HTTP by default. Use CloudFront if HTTPS is required.

### Issue 3: Bucket name with dots in virtual-hosted style
If a bucket name contains dots (e.g., `my.bucket.com`), virtual-hosted style URLs may cause SSL certificate issues because the wildcard cert is for `*.s3.amazonaws.com`, not `*.*.s3.amazonaws.com`.

## Exam Quick Reference
- ✅ **Virtual-hosted** is the modern/recommended URL format
- ✅ **Path-style** is legacy (disabled for buckets created after Sept 2020)
- ✅ **Website endpoints** start with `http://` (no HTTPS by default)
- ✅ **Transfer Acceleration** uses `s3-accelerate.amazonaws.com`
- ✅ **Dual-stack** endpoints support both IPv4 and IPv6
- ✅ **FIPS endpoints** are for compliance requirements
- ✅ **Access Point endpoints** enable granular access management