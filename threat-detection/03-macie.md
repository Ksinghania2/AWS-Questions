# Amazon Macie

Discover and protect sensitive data in S3.

## CLI
```bash
aws macie2 enable-macie --finding-publishing-frequency FIFTEEN_MINUTES
aws macie2 describe-buckets
aws macie2 create-classification-job --name "Sensitive-Data-Scan" --job-type ONE_TIME --s3-job-definition '{"bucketDefinitions":[{"accountId":"xxx","buckets":["my-bucket"]}]}'
aws macie2 list-findings
```

## Q&A
**Q1: What is Macie?** A: Sensitive data discovery. **Q2: Data types?** A: PII, PHI, credentials. **Q3: Services?** A: Primarily S3. **Q4: Classification method?** A: ML-based. **Q5: Automation?** A: Via EventBridge.
