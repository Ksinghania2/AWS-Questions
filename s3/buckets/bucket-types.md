# Bucket Types

S3 buckets are commonly used for several workload patterns, and the intended purpose often determines the configuration you choose.

## Common bucket types
- General-purpose buckets for application data and backups
- Static website hosting buckets
- Logging buckets for access and application logs
- Data lake buckets for analytics and machine learning

## Design guidance
Choose the bucket purpose before enabling advanced features such as versioning, replication, or public website hosting.

## Best practices
- Keep bucket purpose and lifecycle policy aligned.
- Separate production data from test and development data.
- Use access controls that match the workload.
