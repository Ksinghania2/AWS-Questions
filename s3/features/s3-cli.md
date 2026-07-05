# S3 CLI

The AWS CLI provides a straightforward way to manage S3 buckets, objects, policies, and replication from the command line.

## Common commands
- aws s3 ls
- aws s3 mb s3://my-bucket
- aws s3 cp file.txt s3://my-bucket/file.txt
- aws s3 sync ./data s3://my-bucket/data

## Best practices
- Use profiles for multiple accounts.
- Prefer s3api for API-level control.
- Test commands first in a non-production environment.
