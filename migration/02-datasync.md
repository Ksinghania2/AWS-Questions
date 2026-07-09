# AWS DataSync

DataSync automates and accelerates moving data between on-premises and AWS storage.

## Key Features
- **Agent-based**: Install agent on-premises
- **Automatic**: Encryption, validation, scheduling
- **Fast**: Up to 10x faster than open-source tools
- **Supported sources**: NFS, SMB, HDFS, S3, EFS, FSx
- **Incremental**: Only transfers changed data

## CLI
```bash
# Create agent (download and activate from on-premises)
aws datasync create-agent     --agent-name my-agent     --activation-key abc123-def456-ghi789

# Create source location (NFS)
aws datasync create-location-nfs     --server-hostname nfs-server.corp.example.com     --on-prem-config AgentArns=arn:aws:datasync:us-east-1:xxx:agent/agent-xxx     --mount-options Version=NFSv4

# Create destination location (S3)
aws datasync create-location-s3     --s3-bucket-arn arn:aws:s3:::my-bucket     --s3-config '{"BucketAccessRoleArn":"arn:aws:iam::xxx:role/DataSyncS3Role"}'     --subdirectory "/data"

# Create task
aws datasync create-task     --source-location-arn arn:aws:datasync:us-east-1:xxx:location/src-xxx     --destination-location-arn arn:aws:datasync:us-east-1:xxx:location/dst-xxx     --name "Daily-Backup"     --options VerifyMode=POINT_IN_TIME_CONSISTENT

# Start task
aws datasync start-task-execution --task-arn arn:aws:datasync:us-east-1:xxx:task/task-xxx
```

## Q&A
**Q1: What is DataSync?** A: Automated data transfer service from on-premises to AWS.
**Q2: What component runs on-premises?** A: DataSync Agent.
**Q3: What sources does DataSync support?** A: NFS, SMB, HDFS, S3, EFS, FSx.
**Q4: How much faster is DataSync than open-source?** A: Up to 10x faster.
**Q5: Can DataSync schedule transfers?** A: Yes, via CloudWatch Events or EventBridge.
