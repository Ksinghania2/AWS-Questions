# Encryption in Transit

Encryption in transit protects data as it travels between clients and S3. S3 supports **HTTPS/TLS** for all data transfers.

## How It Works

```
Client (HTTPS) → Internet → S3 Endpoint
All data encrypted with TLS during transfer
```

- **Protocol**: HTTPS (TLS 1.2+)
- **Default**: All S3 API calls use HTTPS by default
- **HTTP option**: Available for static website hosting only
- **Additional cost**: Free (included with all S3 requests)

## CLI Commands

```bash
# Force HTTPS (default behavior)
aws s3 cp file.txt s3://my-bucket/file.txt

# Verify endpoint uses HTTPS
aws s3api get-object --bucket my-bucket --key file.txt /dev/stdout \
  --debug 2>&1 | grep "endpoint"

# Use AWS PrivateLink for private connectivity (no internet)
# Create a VPC Endpoint for S3
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-12345

# Check bucket policy that enforces HTTPS
aws s3api get-bucket-policy --bucket my-bucket
```

## Enforcing HTTPS with Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket/*",
        "arn:aws:s3:::my-bucket"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

## Exam Quick Reference
- ✅ **HTTPS/TLS** is the default for all S3 API calls
- ✅ **HTTP** only available for static website hosting
- ✅ **Enforce HTTPS** via bucket policy (Deny when `aws:SecureTransport` is false)
- ✅ **AWS PrivateLink** for private connectivity (no internet)
- ✅ **Free** — no additional cost for encryption in transit
- ✅ **TLS 1.2+** recommended (older TLS versions deprecated)