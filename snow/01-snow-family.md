# AWS Snow Family

AWS Snow Family provides physical devices to transfer data to/from AWS when network transfer is impractical.

## Device Comparison
| Device | Storage | Compute | Use Case |
|--------|---------|---------|----------|
| **Snowcone** | 8TB HDD + 14TB SSD | 4 vCPU, 8GB RAM | Small data, edge computing |
| **Snowball Edge Storage** | 80TB | 24 vCPU, 32GB RAM | Large data migration |
| **Snowball Edge Compute** | 42TB | 104 vCPU, 416GB RAM + GPU | Edge ML, processing |
| **Snowmobile** | 100PB | N/A | Exabyte-scale migration |

## CLI
```bash
# Create job
aws snowball create-job     --job-type IMPORT     --job-type LOCAL_USE     --resources '{"S3Resources":[{"BucketArn":"arn:aws:s3:::my-bucket"}]}'     --address-id addr-xxx     --role-arn arn:aws:iam::xxx:role/snowball-role

# List jobs
aws snowball list-jobs

# Get job status
aws snowball describe-job --job-id JOBID

# Cancel job
aws snowball cancel-job --job-id JOBID
```

## Q&A
**Q1: When to use Snow Family?** A: When network transfer is too slow or expensive (over a week).
**Q2: What is the largest Snow device?** A: Snowmobile (100PB).
**Q3: Which device has GPU?** A: Snowball Edge Compute.
**Q4: What is the smallest device?** A: Snowcone (8TB).
**Q5: Is data encrypted on Snow devices?** A: Yes, with KMS.
