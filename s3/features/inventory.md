# S3 Inventory

S3 Inventory provides **scheduled reports** listing all objects and their metadata (size, storage class, encryption, etc.).

## Key Features
- **Daily or weekly** reports (CSV, Parquet, ORC)
- **Optional fields**: Size, Storage Class, Encryption, ETag, Version ID, Tags, Last Modified
- **Encrypted reports**: SSE-S3 or SSE-KMS
- **Supports**: Versioning, large buckets (millions of objects)

```bash
# Configure inventory report
aws s3api put-bucket-inventory-configuration --bucket my-bucket \
  --id "WeeklyInventory" \
  --inventory-configuration '{
    "Destination": {
      "S3BucketDestination": {
        "Bucket": "arn:aws:s3:::my-inventory-destination",
        "Format": "CSV"
      }
    },
    "IsEnabled": true,
    "Schedule": {"Frequency": "Weekly"},
    "IncludedObjectVersions": "Current",
    "OptionalFields": ["Size", "StorageClass", "EncryptionStatus", "LastModifiedDate"]
  }'
```

## Exam Quick Reference
- ✅ **Scheduled reports** of all objects and metadata
- ✅ **Daily or weekly** frequency
- ✅ **CSV, Parquet, or ORC** format
- ✅ **Optional fields**: size, storage class, encryption, tags
- ✅ Useful for **compliance auditing**, **cost analysis**, **lifecycle management**
- ✅ Reports are stored in a **destination S3 bucket**