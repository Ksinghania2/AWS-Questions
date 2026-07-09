# AWS Secrets Manager

Securely store and rotate secrets.

## CLI
```bash
aws secretsmanager create-secret --name my-db-password --secret-string '{"username":"admin","password":"MyPass123!"}'
aws secretsmanager get-secret-value --secret-id my-db-password
aws secretsmanager rotate-secret --secret-id my-db-password
aws secretsmanager delete-secret --secret-id my-db-password --force-delete-without-recovery
```

## vs Parameter Store
| Feature | Secrets Manager | SSM Parameter Store |
|---------|----------------|---------------------|
| Rotation | Built-in | Manual |
| Cost | $0.40/secret/mo | Free (standard) |
| Encryption | KMS required | Optional |

## Q&A
**Q1: What is Secrets Manager?** A: Store and rotate secrets. **Q2: Auto-rotation?** A: Yes, via Lambda. **Q3: Difference from Parameter Store?** A: Secrets Manager has rotation. **Q4: Max size?** A: 64KB. **Q5: Native rotation for?** A: RDS, Redshift, DocumentDB.
