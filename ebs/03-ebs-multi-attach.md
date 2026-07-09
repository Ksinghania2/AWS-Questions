# EBS Multi-Attach

Attach a single io1/io2 volume to multiple Nitro-based EC2 instances simultaneously.

## Requirements
- Volume type: io1 or io2
- All instances must be in the same AZ
- All instances must be Nitro-based
- Max 16 instances per volume
- File system must be cluster-aware (XFS, GFS2)

## CLI
```bash
# Create multi-attach enabled volume
aws ec2 create-volume     --volume-type io2     --size 100     --iops 10000     --availability-zone us-east-1a     --multi-attach-enabled

# Attach to multiple instances
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/sdf
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-yyy --device /dev/sdf
```

## Q&A
**Q1: What volume types support Multi-Attach?** A: io1 and io2 only.
**Q2: Max instances per volume?** A: 16.
**Q3: Do instances need to be in the same AZ?** A: Yes.
**Q4: What instance type is required?** A: Nitro-based instances.
**Q5: Use case for Multi-Attach?** A: Clustered databases (Teradata, SAP), shared storage.
