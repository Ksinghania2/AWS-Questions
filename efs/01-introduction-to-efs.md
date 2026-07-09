# Amazon Elastic File System (EFS)

EFS provides scalable, elastic NFS file storage for Linux EC2 instances.

## Key Features
- **NFSv4 protocol**: Shared file system across multiple instances
- **Multi-AZ**: Accessible from all AZs in a region
- **Elastic**: Grows and shrinks automatically
- **Linux only**: Not supported for Windows
- **POSIX compliant**: Standard file system permissions

## CLI
```bash
# Create EFS file system
aws efs create-file-system     --creation-token my-efs-$(date +%s)     --performance-mode generalPurpose     --throughput-mode bursting     --tags Key=Name,Value=MyEFS

# Create mount target (one per AZ)
aws efs create-mount-target     --file-system-id fs-xxx     --subnet-id subnet-xxx     --security-groups sg-xxx

# Describe file systems
aws efs describe-file-systems

# Describe mount targets
aws efs describe-mount-targets --file-system-id fs-xxx
```

## Mount on EC2
```bash
# Install NFS client
sudo yum install -y nfs-utils  # Amazon Linux
# sudo apt install -y nfs-common  # Ubuntu

# Mount EFS
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-xxx.efs.us-east-1.amazonaws.com:/ /mnt/efs

# Auto-mount via fstab
echo "fs-xxx.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0" | sudo tee -a /etc/fstab
```

## Q&A
**Q1: What protocol does EFS use?** A: NFSv4.
**Q2: Can EFS be shared across AZs?** A: Yes, mount targets in each AZ.
**Q3: Does EFS support Windows?** A: No, Linux only.
**Q4: Does EFS grow automatically?** A: Yes, elastic storage.
**Q5: What are the performance modes?** A: General Purpose and Max I/O.
