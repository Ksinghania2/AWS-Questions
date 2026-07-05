# Bucket URLs

A bucket URL is how clients address an S3 bucket over the network. The URL style can affect compatibility, routing, and endpoint behavior.

## URL formats
- Virtual-hosted-style: https://my-bucket.s3.us-east-1.amazonaws.com
- Path-style: https://s3.us-east-1.amazonaws.com/my-bucket
- Dual-stack endpoints for IPv4 and IPv6 support

## Best practices
- Prefer the modern AWS-generated endpoint patterns in tools and SDKs.
- Validate endpoint behavior when using legacy clients or proxies.
- Understand region-specific routing if you are troubleshooting connectivity.
