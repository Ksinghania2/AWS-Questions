# EC2 Placement Groups

Placement groups control the physical placement of EC2 instances to optimize for performance, availability, or fault isolation.

## Types of Placement Groups

| Type | Strategy | Use Case |
|------|----------|----------|
| **Cluster** | Low latency, high throughput | HPC, tightly-coupled apps |
| **Spread** | Fault isolation | Critical instances |
| **Partition** | Large distributed systems | Hadoop, Cassandra, Kafka |

## Cluster Placement Group

Groups instances close together in a single AZ for low-latency networking.

```
┌─────────────────────────────┐
│   Cluster Placement Group   │
│   ┌──────┐ ┌──────┐        │
│   │ EC2  │ │ EC2  │        │
│   │   A   │ │   B   │      │
│   └──────┘ └──────┘        │
│   ┌──────┐ ┌──────┐        │
│   │ EC2  │ │ EC2  │        │
│   │   C   │ │   D   │      │
│   └──────┘ └──────┘        │
│   Same AZ, Same Rack       │
└─────────────────────────────┘
```

### CLI Examples
```bash
# Create cluster placement group
aws ec2 create-placement-group \
    --group-name "HPC-Cluster" \
    --strategy cluster \
    --tag-specifications ResourceType=placement-group,Tags=[{Key=Project,Value=HPC}]

# Launch instances in cluster
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type p3dn.24xlarge \
    --placement GroupName=HPC-Cluster \
    --count 4
```

## Spread Placement Group

Each instance is placed on a separate rack with independent power and networking.

```
┌──────────────────────────────────────────────┐
│         Spread Placement Group               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ EC2 A    │  │ EC2 B    │  │ EC2 C    │  │
│  │ Rack 1   │  │ Rack 2   │  │ Rack 3   │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│  Across different AZs or same AZ            │
└──────────────────────────────────────────────┘
```

### CLI Examples
```bash
# Create spread placement group
aws ec2 create-placement-group \
    --group-name "Critical-Apps" \
    --strategy spread

# Launch instances in spread group
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type m5.large \
    --placement GroupName=Critical-Apps \
    --count 7  # Max 7 per AZ
```

## Partition Placement Group

Divides instances into logical partitions. Each partition is isolated from others.

```
┌──────────────────────────────────────────────┐
│         Partition Placement Group            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Partition│  │ Partition│  │ Partition│  │
│  │ 1        │  │ 2        │  │ 3        │  │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │  │
│  │ │EC2 A │ │  │ │EC2 D │ │  │ │EC2 G │ │  │
│  │ │EC2 B │ │  │ │EC2 E │ │  │ │EC2 H │ │  │
│  │ │EC2 C │ │  │ │EC2 F │ │  │ │EC2 I │ │  │
│  │ └──────┘ │  │ └──────┘ │  │ └──────┘ │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│  Max 7 partitions per AZ                  │
└──────────────────────────────────────────────┘
```

### CLI Examples
```bash
# Create partition placement group
aws ec2 create-placement-group \
    --group-name "Hadoop-Cluster" \
    --strategy partition \
    --partition-count 5  # Max 7 per AZ

# Launch instances specifying partition
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type i3.2xlarge \
    --placement GroupName=Hadoop-Cluster,PartitionNumber=2

# Get partition info
aws ec2 describe-instances \
    --instance-ids i-1234567890abcdef0 \
    --query 'Reservations[0].Instances[0].Placement.PartitionNumber'
```

## Comparison

| Feature | Cluster | Spread | Partition |
|---------|---------|--------|-----------|
| **Latency** | Lowest (single rack) | Normal | Normal |
| **AZ Scope** | Single AZ | Multi-AZ | Multi-AZ |
| **Max instances/AZ** | 15+ | 7 | 7 partitions |
| **Fault tolerance** | Low | High | Medium |
| **Use case** | HPC | Critical apps | Big data |
| **Instance types** | Same recommended | Any | Any |

## Exam Tips

- ✅ **Cluster**: Single AZ, low latency, HPC
- ✅ **Spread**: Separate hardware, high availability, max 7/AZ
- ✅ **Partition**: Rack isolation, big data, max 7 partitions/AZ
- ✅ **Cannot merge** placement groups
- ✅ **Cannot move** existing instances (must stop/start or AMI)
- ✅ **Cluster groups** require same instance type
- ✅ **Cluster groups** do not span AZs

## Q&A

**Q1: What placement group is best for HPC workloads?**
A: Cluster placement group for lowest network latency.

**Q2: What is the maximum number of instances in a spread placement group per AZ?**
A: 7 instances per AZ.

**Q3: What placement group is recommended for Cassandra clusters?**
A: Partition placement group for rack isolation.

**Q4: Can a cluster placement group span multiple AZs?**
A: No, it must be in a single AZ.

**Q5: What is the maximum number of partitions per AZ?**
A: 7 partitions per AZ.

**Q6: Can you change placement groups after launching an instance?**
A: You must stop/start the instance or create a new AMI.

**Q7: What is the main benefit of spread placement groups?**
A: Instances are on different physical hardware (fault isolation).

**Q8: What placement group provides the lowest latency?**
A: Cluster placement group (same rack).

**Q9: Can spread placement groups span multiple AZs?**
A: Yes, instances can be in different AZs.

**Q10: What are partition placement groups typically used for?**
A: Big data workloads like Hadoop, Cassandra, HDFS, Kafka.
