# AWS Backup

AWS Backup is a centralized backup service for automating backups across AWS services.

## Supported Services
- EC2 (EBS snapshots)
- RDS (DB snapshots)
- Aurora
- DynamoDB
- EFS
- FSx
- Storage Gateway (Volume Gateway)

## CLI
```bash
# Create backup plan
aws backup create-backup-plan     --backup-plan '{
        "BackupPlanName": "Daily-Backups",
        "Rules": [{
            "RuleName": "Daily-Retain-30",
            "TargetBackupVaultName": "Default",
            "ScheduleExpression": "cron(0 5 * * ? *)",
            "StartWindowMinutes": 60,
            "CompletionWindowMinutes": 120,
            "Lifecycle": {"DeleteAfterDays": 30}
        }]
    }'

# Assign resources
aws backup create-backup-selection     --backup-plan-id plan-xxx     --backup-selection '{
        "SelectionName": "All-EC2",
        "IamRoleArn": "arn:aws:iam::xxx:role/AWSBackupDefaultRole",
        "Resources": ["arn:aws:ec2:*:*:instance/*"]
    }'

# Start on-demand backup
aws backup start-backup-job     --backup-vault-name Default     --resource-arn arn:aws:ec2:us-east-1:xxx:volume/vol-xxx

# List backup jobs
aws backup list-backup-jobs

# Restore backup
aws backup start-restore-job     --recovery-point-arn arn:aws:backup:us-east-1:xxx:recovery-point:xxx     --metadata '{"resourceType":"EC2","availabilityZone":"us-east-1a"}'
```

## Q&A
**Q1: What is AWS Backup?** A: Centralized backup service for multiple AWS services.
**Q2: What schedule format does AWS Backup use?** A: Cron expressions.
**Q3: What is a backup vault?** A: Container for backups with optional lock (WORM).
**Q4: Can AWS Backup cross regions?** A: Yes, with copy actions.
**Q5: What is a backup plan?** A: Rules defining schedule, retention, and vault.
