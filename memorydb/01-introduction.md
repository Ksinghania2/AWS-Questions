# Amazon MemoryDB for Redis

MemoryDB is a Redis-compatible, durable, in-memory database.

## Key Features
- Redis API compatible
- Durable (write-ahead log)
- Multi-AZ
- Microsecond reads, single-digit millisecond writes
- 6 copies of data across 3 AZs

## MemoryDB vs ElastiCache Redis
| Feature | MemoryDB | ElastiCache Redis |
|---------|----------|-------------------|
| **Persistence** | Durable (WAL) | RDB/AOF snapshots |
| **Primary use** | Primary database | Cache only |
| **Data durability** | Yes (no data loss) | Best-effort |
| **Replication** | Multi-AZ | Multi-AZ |

## CLI
```bash
# Create MemoryDB cluster
aws memorydb create-cluster     --cluster-name my-memorydb     --node-type db.r5.large     --acl-name my-acl     --subnet-group-name my-subnet-group

# Create snapshot
aws memorydb create-snapshot     --cluster-name my-memorydb     --snapshot-name my-memorydb-snapshot
```

## Q&A
**Q1: How is MemoryDB different from ElastiCache Redis?** A: MemoryDB is a durable primary database; ElastiCache is a cache.
**Q2: Does MemoryDB persist data?** A: Yes, via write-ahead log (WAL).
**Q3: What is the read/write latency?** A: Microsecond reads, single-digit ms writes.
**Q4: How many data copies does MemoryDB have?** A: 6 copies across 3 AZs.
**Q5: Use case for MemoryDB?** A: Primary database requiring microsecond performance.
