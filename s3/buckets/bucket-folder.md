# Bucket Folders and Prefixes

S3 does not use real folders the way a local filesystem does. Instead, it uses object keys and prefixes to organize data logically inside a bucket.

## Why this matters
- Prefixes are the primary mechanism for grouping objects.
- They help you build logical structures such as reports/2024/ or images/products/.
- They make lifecycle rules, replication, and analytics easier to manage.

## Key concepts
- A prefix is everything before the last slash in an object key.
- Objects with the same prefix are often treated as belonging to the same logical group.
- Prefixes are frequently used with S3 Inventory and lifecycle policies.

## Example
```bash
aws s3 cp report.csv s3://my-bucket/reports/2024/report.csv
```

## Best practices
- Use clear prefixes rather than trying to mimic a traditional directory tree.
- Keep naming consistent across applications.
- Combine prefixes with tags and lifecycle policies for governance.
