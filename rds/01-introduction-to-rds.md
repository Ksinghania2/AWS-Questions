# Amazon RDS (Relational Database Service)

RDS provides managed relational databases in the cloud.

## Supported Engines
- MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Db2

## Key Features
- **Automated backups**: Daily snapshots + transaction logs
- **Multi-AZ**: Synchronous standby replica in another AZ
- **Read Replicas**: Asynchronous copies for read scaling
- **Auto-scaling**: Storage grows automatically
- **Encryption**: KMS at rest, SSL/TLS in transit
- **Maintenance**: Automated patching

## CLI
```bash
# Create DB instance
aws rds create-db-instance     --db-instance-identifier my-db     --db-instance-class db.t3.medium     --engine mysql     --master-username admin     --master-user-password MyPass123!     --allocated-storage 100     --vpc-security-group-ids sg-xxx     --db-subnet-group-name my-subnet-group     --backup-retention-period 7     --multi-az     --storage-encrypted

# Take snapshot
aws rds create-db-snapshot     --db-instance-identifier my-db     --db-snapshot-identifier my-db-snapshot-$(date +%Y-%m-%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot     --db-instance-identifier my-db-restored     --db-snapshot-identifier my-db-snapshot-2024-01-01

# Modify instance
aws rds modify-db-instance     --db-instance-identifier my-db     --db-instance-class db.t3.large     --apply-immediately
```

## Q&A
**Q1: What database engines does RDS support?** A: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Db2.
**Q2: What is the max backup retention period?** A: 35 days.
**Q3: Can you take manual snapshots?** A: Yes, retained until deleted.
**Q4: What is Multi-AZ?** A: Synchronous standby in another AZ for HA.
**Q5: Does Multi-AZ improve read performance?** A: No, use Read Replicas for reads.
