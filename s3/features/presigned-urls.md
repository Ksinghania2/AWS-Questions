# Presigned URLs

Presigned URLs provide temporary, time-limited access to an S3 object without sharing long-term credentials.

## Why they are useful
- Secure temporary downloads
- Support external sharing without permanent IAM access
- Enable controlled uploads from clients

## Example
```bash
aws s3 presign s3://my-bucket/report.csv --expires-in 3600
```
