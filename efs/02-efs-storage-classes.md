# EFS Storage Classes & Lifecycle Management

## Storage Classes
| Class | Durability | Retrieval | Cost |
|-------|------------|-----------|------|
| **EFS Standard** | 11x9s | Instant | Higher |
| **EFS IA** | 11x9s | Instant | Lower (cheaper storage, higher read cost) |
| **EFS Archive** | 11x9s | 24-48 hours | Lowest |

## Lifecycle Management
Automatically moves files between classes based on last access time.

```bash
# Create lifecycle policy
aws efs put-lifecycle-configuration     --file-system-id fs-xxx     --lifecycle-policies '[
        {"TransitionToIA": "AFTER_30_DAYS"},
        {"TransitionToArchive": "AFTER_90_DAYS"},
        {"TransitionToPrimaryStorageClass": "AFTER_1_ACCESS"}
    ]'
```

## Throughput Modes
| Mode | Description | Use Case |
|------|-------------|----------|
| **Bursting** | Scales with storage size | General purpose |
| **Provisioned** | Fixed throughput | High throughput needs |
| **Elastic** | Auto-scales throughput | Unpredictable workloads |

```bash
# Set provisioned throughput
aws efs update-file-system     --file-system-id fs-xxx     --provisioned-throughput-mebibytes 100
```

## Q&A
**Q1: What is EFS IA?** A: Infrequent Access - lower cost for files accessed less often.
**Q2: How does lifecycle management work?** A: Moves files based on last access time (e.g., after 30 days).
**Q3: What is the retrieval time for Archive?** A: 24-48 hours.
**Q4: What are the throughput modes?** A: Bursting, Provisioned, Elastic.
**Q5: Can files in IA be accessed instantly?** A: Yes, but there's a read cost.
