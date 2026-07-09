# Amazon FSx

Amazon FSx provides fully managed third-party file systems.

## FSx Types
| Type | Protocol | Use Case |
|------|----------|----------|
| **FSx for Lustre** | POSIX | HPC, ML, video processing |
| **FSx for NetApp ONTAP** | NFS, SMB, iSCSI | Enterprise data management |
| **FSx for OpenZFS** | NFS | Linux file servers |
| **FSx for Windows File Server** | SMB | Windows file shares |

## CLI
```bash
# Create FSx for Windows
aws fsx create-file-system     --file-system-type WINDOWS     --storage-capacity 300     --subnet-ids subnet-xxx     --windows-configuration '{"SelfManagedActiveDirectoryConfiguration":{"DomainName":"corp.example.com","UserName":"Admin","Password":"xxx","DnsIps":["10.0.0.2"]}}'

# Create FSx for Lustre
aws fsx create-file-system     --file-system-type LUSTRE     --storage-capacity 1200     --subnet-ids subnet-xxx     --lustre-configuration '{"DeploymentType":"PERSISTENT_1","PerUnitStorageThroughput":200}'

# Create FSx for ONTAP
aws fsx create-file-system     --file-system-type ONTAP     --storage-capacity 1024     --subnet-ids subnet-xxx     --ontap-configuration '{"DeploymentType":"MULTI_AZ_1","PreferredSubnetId":"subnet-xxx"}'

# Create backup
aws fsx create-backup --file-system-id fs-xxx
```

## Q&A
**Q1: Which FSx is best for HPC?** A: FSx for Lustre.
**Q2: Which FSx supports Windows SMB?** A: FSx for Windows File Server.
**Q3: Which FSx supports both NFS and SMB?** A: FSx for NetApp ONTAP.
**Q4: What is FSx for OpenZFS best for?** A: Linux file servers with NFS.
**Q5: Can FSx be backed up?** A: Yes, with AWS Backup or native snapshots.
