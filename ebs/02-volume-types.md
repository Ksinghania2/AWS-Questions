# EBS Volume Types

## SSD Volumes
| Type | Max IOPS | Max Throughput | Use Case |
|------|----------|----------------|----------|
| **gp3** | 16,000 | 1000 MB/s | General purpose (baseline 3000 IOPS free) |
| **gp2** | 16,000 | 250 MB/s | Legacy general purpose |
| **io1** | 64,000 | 1000 MB/s | High-performance DBs |
| **io2** | 64,000 | 1000 MB/s | Higher durability (99.999%) |
| **io2 Block Express** | 256,000 | 4000 MB/s | Largest, highest performance |

## HDD Volumes
| Type | Max IOPS | Max Throughput | Use Case |
|------|----------|----------------|----------|
| **st1** | 500 | 500 MB/s | Throughput-optimized (big data, logs) |
| **sc1** | 250 | 250 MB/s | Cold storage (infrequent access) |

## CLI
```bash
# Create gp3 volume
aws ec2 create-volume --volume-type gp3 --size 100 --iops 5000 --throughput 250

# Create io2 volume
aws ec2 create-volume --volume-type io2 --size 100 --iops 10000

# Modify volume type
aws ec2 modify-volume --volume-id vol-xxx --volume-type gp3 --iops 5000

# Describe volumes
aws ec2 describe-volumes --volume-ids vol-xxx
```

## Q&A
**Q1: Which volume type is best for boot volumes?** A: gp3 (general purpose SSD).
**Q2: Which volume type is best for high-performance databases?** A: io2 Block Express (highest IOPS).
**Q3: What is the baseline IOPS for gp3?** A: 3000 IOPS (included in price).
**Q4: What is the difference between st1 and sc1?** A: st1 is throughput-optimized; sc1 is cold (lowest cost).
**Q5: Can you change volume type without downtime?** A: Yes, using modify-volume (online).
