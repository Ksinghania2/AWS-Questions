# Amazon Aurora

Aurora is a MySQL/PostgreSQL-compatible relational database built for the cloud.

## Key Features
- **6 copies of data** across 3 AZs (2 copies per AZ)
- **Auto-scaling storage** (10GB to 128TB)
- **15 read replicas** (vs 5 for MySQL RDS)
- **Failover in < 30 seconds**
- **Aurora Serverless**: Auto-scaling compute
- **Global Database**: 5 secondary regions, < 1 sec replication

## Aurora vs RDS MySQL
| Feature | Aurora | RDS MySQL |
|---------|--------|-----------|
| Storage | Auto-scales to 128TB | Fixed, up to 16TB |
| Read replicas | 15 | 5 |
| Failover | < 30s (instant) | 1-2 minutes |
| Data copies | 6 (3 AZs) | 2 (1 AZ) |
| Performance | 5x MySQL, 3x PostgreSQL | Baseline |

## CLI
```bash
# Create cluster
aws rds create-db-cluster     --db-cluster-identifier my-aurora-cluster     --engine aurora-mysql     --master-username admin     --master-user-password MyPass123!     --vpc-security-group-ids sg-xxx     --db-subnet-group-name my-subnet-group

# Create writer instance
aws rds create-db-instance     --db-instance-identifier my-aurora-writer     --db-cluster-identifier my-aurora-cluster     --db-instance-class db.r5.large     --engine aurora-mysql

# Create reader instance
aws rds create-db-instance     --db-instance-identifier my-aurora-reader-1     --db-cluster-identifier my-aurora-cluster     --db-instance-class db.r5.large     --engine aurora-mysql     --promotion-tier 1

# Create Aurora Global Database
aws rds create-db-cluster     --db-cluster-identifier my-global-aurora     --engine aurora-mysql     --master-username admin     --master-user-password MyPass123!     --global-cluster-identifier my-global-cluster

# Add secondary region
aws rds create-db-cluster     --db-cluster-identifier my-aurora-secondary     --engine aurora-mysql     --global-cluster-identifier my-global-cluster     --region eu-west-1

# Aurora Serverless v2
aws rds create-db-cluster     --db-cluster-identifier my-serverless     --engine aurora-mysql     --serverless-v2-scaling-configuration MinCapacity=1,MaxCapacity=32
```

## Q&A
**Q1: How many copies of data does Aurora store?** A: 6 copies across 3 AZs.
**Q2: How many read replicas does Aurora support?** A: 15 (vs 5 for MySQL RDS).
**Q3: What is Aurora Serverless?** A: Auto-scaling compute capacity (for intermittent workloads).
**Q4: What is Aurora Global Database?** A: Cross-region replication with < 1 sec latency.
**Q5: How fast is Aurora failover?** A: Under 30 seconds.
**Q6: What is the max storage for Aurora?** A: 128 TB (auto-scaling).
**Q7: What is the difference between Aurora and RDS MySQL?** A: Aurora is 5x faster, 15 replicas, auto-scaling storage.
