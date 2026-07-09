# EC2 Instance Types & Families

EC2 instances are categorized into families optimized for different workloads.

## Instance Family Categories

| Family | Name | Use Case |
|--------|------|----------|
| **C** | Compute Optimized | Compute-intensive apps, batch processing |
| **R** | Memory Optimized | Memory-intensive apps, databases |
| **X** | Memory Intensive | Large-scale in-memory apps, SAP HANA |
| **M** | General Purpose | Balanced compute, memory, networking |
| **I** | Storage Optimized | I/O-intensive, NoSQL DBs, data warehousing |
| **D** | Dense Storage | HDD-backed storage, big data, Hadoop |
| **G** | Graphics Optimized | GPU-intensive, machine learning |
| **P** | GPU Compute | High-performance computing, ML |
| **F** | FPGA | Custom hardware acceleration |
| **T** | Burstable | Low-cost general purpose with burst |
| **H** | High Throughput | Disk throughput optimized |

## Naming Convention

```
c5n.4xlarge
││ │  └── Size (4xlarge)
││ └────── Network optimized
│└──────── Generation (5th)
└───────── Family (Compute)
```

## CLI Examples

```bash
# List all instance types
aws ec2 describe-instance-types --query 'InstanceTypes[].InstanceType'

# Get details of specific type
aws ec2 describe-instance-types --instance-types c5n.4xlarge

# List types by family
aws ec2 describe-instance-types \
    --filters "Name=instance-type,Values=c5*" \
    --query 'InstanceTypes[].InstanceType'

# Get vCPU and memory
aws ec2 describe-instance-types \
    --instance-types c5.xlarge \
    --query 'InstanceTypes[0].{vCPU:VCpuInfo.DefaultVCpus,Memory:MemoryInfo.SizeInMiB}'
```

## Current Generation Types

| Family | Current Gen | Features |
|--------|-------------|----------|
| **M** | m7g, m7i, m6i, m6g | Arm (Graviton) or x86 |
| **C** | c7g, c7i, c6i, c6g | Highest vCPU-to-memory ratio |
| **R** | r7g, r7i, r6i, r6g | 8:1 memory-to-vCPU ratio |
| **T** | t4g, t3, t3a | Burstable CPU credits |
| **I** | i4i, i3, i3en | NVMe SSD storage |
| **G** | g5, g4dn | NVIDIA GPUs |

## Key Exam Points

- ✅ **C family**: Highest vCPU-to-memory ratio
- ✅ **R family**: Highest memory-to-vCPU ratio (8:1)
- ✅ **M family**: Balanced (4:1 memory-to-vCPU)
- ✅ **I family**: High I/O with NVMe SSD
- ✅ **T family**: Burstable (CPU credits)
- ✅ **G/P families**: GPU for ML/graphics
- ✅ **Graviton (g)**: ARM-based, better price-performance
- ✅ **Nitro (n suffix)**: Enhanced networking, EBS-optimized

## Q&A

**Q1: What instance family would you choose for a CPU-intensive batch job?**
A: Compute Optimized (C family).

**Q2: Which instance family is best for an in-memory cache like Redis?**
A: Memory Optimized (R or X family).

**Q3: What does "c5n.4xlarge" tell you?**
A: Compute family, 5th gen, network optimized, 4xlarge size.

**Q4: What is the T family used for?**
A: Burstable instances for low-cost general purpose workloads.

**Q5: What is a Graviton instance?**
A: ARM-based processor (AWS custom) offering better price-performance.

**Q6: Which instance family has the highest memory-to-vCPU ratio?**
A: R family (8:1 ratio).

**Q7: What does the "g" suffix in m6g mean?**
A: Graviton (ARM) processor.

**Q8: Which family is optimized for NoSQL databases?**
A: Storage Optimized (I family).

**Q9: What is the benefit of Nitro instances?**
A: Enhanced networking, EBS-optimized by default, better security.

**Q10: Which instance families have GPUs?**
A: G (Graphics), P (Compute GPU).