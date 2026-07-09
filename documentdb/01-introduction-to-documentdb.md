# Amazon DocumentDB

DocumentDB is a MongoDB-compatible document database service.

## Key Features
- MongoDB 3.6, 4.0, 5.0 compatibility
- Auto-scaling storage (up to 64TB)
- 6 copies of data across 3 AZs
- Isolated instance for workloads
- Built-in security (KMS encryption, VPC isolation)

## CLI
```bash
# Create cluster
aws docdb create-db-cluster     --db-cluster-identifier my-docdb     --engine docdb     --master-username admin     --master-user-password MyPass123!     --vpc-security-group-ids sg-xxx

# Create instance
aws docdb create-db-instance     --db-instance-identifier my-docdb-instance     --db-instance-class db.r5.large     --engine docdb     --db-cluster-identifier my-docdb
```

## Q&A
**Q1: What is DocumentDB compatible with?** A: MongoDB 3.6/4.0/5.0.
**Q2: How many data copies does DocumentDB have?** A: 6 copies across 3 AZs.
**Q3: What is the max storage?** A: 64TB (auto-scaling).
**Q4: Is DocumentDB a document store?** A: Yes, stores JSON-like documents.
**Q5: Can you migrate MongoDB to DocumentDB?** A: Yes, using DMS or native tools.
