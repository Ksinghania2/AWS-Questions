# Static Website Hosting

S3 can host **static websites** (HTML, CSS, JavaScript) directly from a bucket without a web server.

## How It Works

```
User's browser → S3 Website Endpoint → S3 bucket
http://my-bucket.s3-website-us-east-1.amazonaws.com
```

## Configuration Steps

### Step 1: Enable Static Website Hosting
```bash
aws s3api put-bucket-website --bucket my-website-bucket \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"}
  }'
```

### Step 2: Make Objects Public
```bash
# Option A: Bucket policy (makes all objects public)
aws s3api put-bucket-policy --bucket my-website-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-website-bucket/*"
  }]
}'

# Option B: Make objects public individually
aws s3 cp index.html s3://my-website-bucket/index.html --acl public-read
```

### Step 3: Upload Website Files
```bash
aws s3 sync ./my-website/ s3://my-website-bucket/
```

### Step 4: Access the Website
```
# Website endpoint format:
http://<bucket-name>.s3-website-<region>.amazonaws.com

# Example:
http://my-website-bucket.s3-website-us-east-1.amazonaws.com
```

## CLI Commands

```bash
# Enable website hosting
aws s3 website s3://my-bucket --index-document index.html --error-document error.html

# Upload files
aws s3 sync ./dist/ s3://my-bucket/ --delete

# Get the website endpoint
aws s3api get-bucket-website --bucket my-bucket --query "Endpoint" --output text

# Disable website hosting (remove configuration)
aws s3api delete-bucket-website --bucket my-bucket
```

## Python (boto3) Examples

```python
import boto3
import json

s3 = boto3.client('s3')
bucket = 'my-website-bucket'

# Configure for static website hosting
def configure_website(bucket, index='index.html', error='error.html'):
    """Configure a bucket for static website hosting"""
    s3.put_bucket_website(
        Bucket=bucket,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': index},
            'ErrorDocument': {'Key': error}
        }
    )
    
    # Make public
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket}/*"
        }]
    }
    s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
    
    # Get the website URL
    region = s3.get_bucket_location(Bucket=bucket)['LocationConstraint'] or 'us-east-1'
    url = f"http://{bucket}.s3-website-{region}.amazonaws.com"
    
    print(f"Website configured!")
    print(f"URL: {url}")
    return url

configure_website(bucket)

# Upload a simple website
def deploy_website(bucket, html_content, css_content='', js_content=''):
    """Deploy a simple website to S3"""
    # Upload index.html
    s3.put_object(
        Bucket=bucket,
        Key='index.html',
        Body=html_content.encode(),
        ContentType='text/html'
    )
    
    if css_content:
        s3.put_object(
            Bucket=bucket,
            Key='style.css',
            Body=css_content.encode(),
            ContentType='text/css'
        )
    
    if js_content:
        s3.put_object(
            Bucket=bucket,
            Key='app.js',
            Body=js_content.encode(),
            ContentType='application/javascript'
        )
    
    print("Website deployed!")

# Deploy a simple page
deploy_website(bucket, 
    '<!DOCTYPE html><html><head><title>My Site</title></head><body><h1>Hello S3!</h1></body></html>'
)
```

## HTTPS with CloudFront

The S3 website endpoint supports **HTTP only**. For HTTPS, use CloudFront:

```bash
# Create a CloudFront distribution with S3 origin
aws cloudfront create-distribution \
  --origin-domain-name my-bucket.s3-website-us-east-1.amazonaws.com \
  --default-root-object index.html
```

## Redirects

```bash
# Redirect all requests to another domain
aws s3api put-bucket-website --bucket my-bucket \
  --website-configuration '{
    "RedirectAllRequestsTo": {"HostName": "www.newdomain.com", "Protocol": "https"}
  }'

# Condition-based redirects
aws s3api put-bucket-website --bucket my-bucket \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "error.html"},
    "RoutingRules": [
      {
        "Condition": {"KeyPrefixEquals": "old-page.html"},
        "Redirect": {"ReplaceKeyWith": "new-page.html"}
      }
    ]
  }'
```

## Exam Tips

### 1. HTTP Only
S3 website endpoints do NOT support HTTPS. For HTTPS, use CloudFront in front of S3.

### 2. Public Access Required
The bucket must allow public read access (either via bucket policy or ACL).

### 3. Custom Domain
Use Route 53 or another DNS provider to point a custom domain to the S3 website endpoint.

### 4. Index and Error Documents
- **Index document**: Usually `index.html`
- **Error document**: Usually `error.html`

### 5. Common Exam Question
**Q:** A company hosts a static website on S3 and needs HTTPS. What should they do?
**A:** Place CloudFront in front of the S3 bucket with a custom SSL certificate.

## Exam Quick Reference
- ✅ **Static content only** (HTML, CSS, JS, images)
- ✅ **HTTP only** (use CloudFront for HTTPS)
- ✅ **Bucket policy** must allow public access
- ✅ **Index document**: Required (e.g., `index.html`)
- ✅ **Error document**: Optional (e.g., `error.html`)
- ✅ **Custom domain**: Via Route 53 or DNS CNAME
- ✅ **No server-side processing** (no PHP, Python, etc.)