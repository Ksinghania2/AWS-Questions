# Multi-AZ vs Read Replicas

## Multi-AZ (High Availability)
- Synchronous replication to standby in another AZ
- Automatic failover
- No performance benefit (standby is inactive)
- Same region only
- Backup taken from standby (no I/O suspension)

## Read Replicas (Scalability)
- Asynchronous replication
- Can be in another region
- Improves read performance (active copies)
- Can be promoted to standalone DB
- MySQL, PostgreSQL, MariaDB, Oracle, SQL Server

## CLI
```bash
# Create read replica
aws rds create-db-instance-read-replica     --db-instance-identifier my-db-ro     --source-db-instance-identifier my-db     --db-instance-class db.t3.large     --region us-west-2  # Cross-region

# Promote read replica to standalone
aws rds promote-read-replica     --db-instance-identifier my-db-ro

# Describe replicas
aws rds describe-db-instances     --filters "Name=read-replica-source-db-instance-identifier,Values=my-db"

# Failover Multi-AZ (reboot with failover)
aws rds reboot-db-instance     --db-instance-identifier my-db     --force-failover
```

## Comparison
| Feature | Multi-AZ | Read Replicas |
|---------|----------|---------------|
| Purpose | High Availability | Read scaling |
| Replication | Synchronous | Asynchronous |
| Standby active? | No | Yes (can serve reads) |
| Cross-region? | No | Yes |
| Failover | Automatic | Manual (promote) |
| Max replicas | N/A | 5 (MySQL), 15 (Aurora) |
| Cost | 2x instances | Replica instances |

## Q&A
**Q1: What is the main purpose of Multi-AZ?** A: High availability (automatic failover).
**Q2: What is the main purpose of Read Replicas?** A: Read scalability and cross-region DR.
**Q3: How many read replicas can MySQL have?** A: Up to 5.
**Q4: Can read replicas be in another region?** A: Yes.
**Q5: Can you promote a read replica to a standalone DB?** A: Yes.
**Q6: Is Multi-AZ replication synchronous or asynchronous?** A: Synchronous.
**Q7: Is Read Replica replication synchronous or asynchronous?** A: Asynchronous.
**Q8: What happens to backups in Multi-AZ?** A: Backups are taken from the standby (no I/O suspension).
