# Amazon Elastic Block Store (EBS)

EBS provides persistent block storage volumes for EC2 instances.

## Key Features
- **Persistent**: Data persists after instance termination
- **Replicated**: Automatically replicated within AZ
- **Snapshots**: Backup to S3, cross-region copy
- **Encryption**: At-rest encryption (KMS)
- **Multi-Attach**: Attach to multiple Nitro instances (io1/io2)

## CLI
```bash
# Create volume
aws ec2 create-volume --volume-type gp3 --size 100 --availability-zone us-east-1a

# Attach volume
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/sdf

# Create snapshot
aws ec2 create-snapshot --volume-id vol-xxx --description "Pre-update backup"

# Copy snapshot to another region
aws ec2 copy-snapshot --source-region us-east-1 --source-snapshot-id snap-xxx --region eu-west-1

# Create volume from snapshot
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone us-east-1a

# Delete volume
aws ec2 delete-volume --volume-id vol-xxx
```

## Q&A
**Q1: Is EBS data persistent?** A: Yes, survives instance termination (unless "Delete on Termination" is set).
**Q2: Is EBS replicated within an AZ?** A: Yes, automatically.
**Q3: How do you back up EBS volumes?** A: Create snapshots (stored in S3).
**Q4: Can you copy snapshots across regions?** A: Yes, for DR.
**Q5: What is the max EBS volume size?** A: 64 TiB.
