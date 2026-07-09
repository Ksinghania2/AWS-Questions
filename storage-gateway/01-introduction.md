# AWS Storage Gateway

Storage Gateway provides hybrid cloud storage between on-premises and AWS.

## Gateway Types
| Type | Protocol | Use Case |
|------|----------|----------|
| **S3 File Gateway** | NFS/SMB | File storage backed by S3 |
| **FSx File Gateway** | SMB | Windows file shares |
| **Volume Gateway (Cached)** | iSCSI | Primary data in S3, cache locally |
| **Volume Gateway (Stored)** | iSCSI | Primary data on-premises, backups to S3 |
| **Tape Gateway** | iSCSI VTL | Virtual tape library for backup |

## CLI
```bash
# Create gateway (activated from on-premises VM)
aws storagegateway create-gateway     --gateway-name my-file-gateway     --gateway-timezone GMT     --gateway-type FILE_S3     --gateway-region us-east-1

# Create S3 file share
aws storagegateway create-nfs-file-share     --client-token "share-$(date +%s)"     --gateway-arn arn:aws:storagegateway:us-east-1:xxx:gateway/sgw-xxx     --location-arn arn:aws:s3:::my-bucket     --role arn:aws:iam::xxx:role/StorageGatewayS3Role

# List gateways
aws storagegateway list-gateways

# Describe gateway
aws storagegateway describe-gateway-information --gateway-arn arn:aws:storagegateway:us-east-1:xxx:gateway/sgw-xxx
```

## Q&A
**Q1: What is Storage Gateway?** A: Hybrid cloud storage connecting on-premises to AWS.
**Q2: What protocol does Volume Gateway use?** A: iSCSI (block storage).
**Q3: What protocol does File Gateway use?** A: NFS or SMB (file storage).
**Q4: What is the difference between cached and stored volumes?** A: Cached - primary in S3, cache locally; Stored - primary local, backup to S3.
**Q5: What is Tape Gateway?** A: Virtual tape library (VTL) for backup software.
