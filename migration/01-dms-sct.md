# AWS Database Migration Service (DMS) & SCT

DMS migrates databases to AWS with minimal downtime.

## DMS Components
- **Source Endpoint**: Origin database
- **Target Endpoint**: Destination database
- **Replication Instance**: EC2 instance running the migration
- **Task**: Defines what to migrate and how

## Migration Types
| Type | Description | Use Case |
|------|-------------|----------|
| Full Load | Copy all data at once | Small DBs, one-time |
| Full Load + CDC | Initial load + continuous replication | Minimal downtime |
| CDC Only | Continuous change replication | Ongoing sync |

## CLI
```bash
# Create replication instance
aws dms create-replication-instance     --replication-instance-identifier my-rep-instance     --replication-instance-class dms.t3.medium     --allocated-storage 100

# Create endpoints
aws dms create-endpoint     --endpoint-identifier source-mysql     --endpoint-type source     --engine-name mysql     --mysql-settings ServerName=mysql.example.com,Port=3306,Username=admin,Password=xxx

aws dms create-endpoint     --endpoint-identifier target-rds     --endpoint-type target     --engine-name aurora     --aurora-settings ServerName=my-cluster.cluster-xxx.us-east-1.rds.amazonaws.com,Port=3306,Username=admin,Password=xxx

# Create task
aws dms create-replication-task     --replication-task-identifier migrate-mysql-to-aurora     --source-endpoint-arn arn:aws:dms:us-east-1:xxx:endpoint:xxx     --target-endpoint-arn arn:aws:dms:us-east-1:xxx:endpoint:yyy     --replication-instance-arn arn:aws:dms:us-east-1:xxx:rep:zzz     --migration-type full-load-and-cdc     --table-mappings file://table-mappings.json

# Start task
aws dms start-replication-task     --replication-task-arn arn:aws:dms:us-east-1:xxx:task:ttt

# SCT (Schema Conversion Tool)
# Used when migrating to different engine (e.g., Oracle to Aurora)
# aws sct is a separate tool (GUI/CLI)
```

## Q&A
**Q1: What is DMS?** A: Database Migration Service for migrating DBs to AWS.
**Q2: What is SCT?** A: Schema Conversion Tool - converts schema when changing DB engines.
**Q3: What migration type provides minimal downtime?** A: Full Load + CDC (ongoing replication).
**Q4: When must SCT be used?** A: When migrating to a different database engine.
**Q5: Can DMS migrate from on-premises to AWS?** A: Yes, source can be on-premises.
