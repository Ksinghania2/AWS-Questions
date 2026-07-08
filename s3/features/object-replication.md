# S3 Object Replication

Replication **automatically copies objects** between buckets for durability, compliance, and low-latency data access.

## Types of Replication

| Type | Source → Destination | Use Case |
|---|---|---|
| **CRR** (Cross-Region Replication) | Different regions | DR, compliance, latency |
| **SRR** (Same-Region Replication) | Same region | Log aggregation, dev/test sync |

## Requirements
- **Versioning must be enabled** on both source and destination buckets
- Source bucket must have an **IAM role** granting S3 replication permissions
- Destination bucket must have a **bucket policy** allowing replication (if cross-account)

## Exam Quick Reference
- ✅ **Versioning required** on source AND destination
- ✅ **CRR** = different regions, **SRR** = same region
- ✅ Can replicate to **same account** or **different account**
- ✅ Supports **encrypted objects** (SSE-S3, SSE-KMS with multi-region keys)
- ✅ **Delete markers** are not replicated by default
- ✅ **Lifecycle rules** on destination can further transition replicated data
- ✅ **Replication time**: Most objects replicated within 15 minutes
- ✅ **Batch replication**: S3 Batch Replication for existing objects

```bash
aws s3api put-bucket-replication --bucket source-bucket \
  --replication-configuration file://replication.json

# replication.json example:
{
  "Role": "arn:aws:iam::123456789012:role/s3-replication-role",
  "Rules": [{
    "Status": "Enabled",
    "Filter": {"Prefix": "critical/"},
    "Destination": {
      "Bucket": "arn:aws:s3:::destination-bucket",
      "StorageClass": "STANDARD_IA"
    }
  }]
}
```

## Exam Scenarios
- **"DR compliance requires data in another region"** → CRR
- **"Logs must be aggregated in one bucket"** → SRR
- **"Replicate data encrypted with KMS"** → Use multi-region KMS keys
- **"Only replicate critical data"** → Use prefix filtering in replication rules