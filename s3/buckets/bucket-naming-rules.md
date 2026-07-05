# Bucket Naming Rules

Bucket naming is one of the most important S3 design decisions because bucket names must be globally unique and meet strict AWS constraints.

## Rules
- 3 to 63 characters long
- Lowercase letters, numbers, and hyphens only
- Must start and end with a letter or number
- Cannot be an IP address
- Must be unique across all AWS accounts globally

## Why it matters
A bucket name becomes part of the globally visible endpoint identity for the bucket, so naming mistakes can cause failures or conflicts.

## Good and bad examples
- Good: my-data-bucket-2024
- Bad: MyBucket, my_bucket, mybucket-

## Best practices
- Choose a stable, descriptive name.
- Keep names short enough for scripts and automation.
- Avoid exposing internal or sensitive information in the name.
