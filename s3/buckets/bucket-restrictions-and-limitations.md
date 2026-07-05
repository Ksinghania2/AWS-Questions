# Bucket Restrictions and Limitations

S3 buckets are flexible, but they also come with important constraints that affect architecture and operations.

## Important limitations
- Bucket names are globally unique.
- Bucket names cannot contain uppercase letters, underscores, or spaces.
- Buckets cannot be nested inside one another.
- S3 uses a flat namespace and relies on prefixes for logical grouping.

## Operational impact
These constraints shape how you name buckets, organize objects, and design multi-account or multi-region solutions.

## Best practices
- Plan names early in the design process.
- Use prefixes and tags for structure.
- Review feature availability by region before building production workflows.
