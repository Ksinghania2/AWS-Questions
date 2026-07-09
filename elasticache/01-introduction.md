# Amazon ElastiCache

ElastiCache provides managed Redis and Memcached in-memory caches.

## Redis vs Memcached
| Feature | Redis | Memcached |
|---------|-------|-----------|
| **Data structures** | Strings, lists, sets, hashes | Simple key-value |
| **Persistence** | Yes (RDB/AOF) | No |
| **Replication** | Multi-AZ, read replicas | No replication |
| **Backup/Restore** | Yes | No |
| **Lua scripting** | Yes | No |
| **Use case** | Caching, sessions, geospatial | Simple caching |

## Cache Invalidation Strategies
| Strategy | Description | Pro/Con |
|----------|-------------|---------|
| **Lazy Loading** | Cache on read miss | Stale data possible, handles failures |
| **Write-Through** | Write to DB + cache simultaneously | Fresh data, higher write latency |
| **TTL** | Auto-expiration | Simple, may serve stale data |

## CLI
```bash
# Create Redis cluster
aws elasticache create-cache-cluster     --cache-cluster-id my-redis     --engine redis     --cache-node-type cache.r5.large     --num-cache-nodes 1     --multi-az-location-mode cross-az

# Create Redis (cluster mode)
aws elasticache create-replication-group     --replication-group-id my-redis-cluster     --replication-group-description "Redis cluster"     --engine redis     --cache-node-type cache.r5.large     --num-node-groups 3     --replicas-per-node-group 1

# Create Memcached cluster
aws elasticache create-cache-cluster     --cache-cluster-id my-memcached     --engine memcached     --cache-node-type cache.r5.large     --num-cache-nodes 3

# Describe clusters
aws elasticache describe-cache-clusters
```

## Q&A
**Q1: What is the difference between Redis and Memcached?** A: Redis supports data structures, persistence, replication; Memcached is simple key-value.
**Q2: What is lazy loading?** A: Cache data on first read miss (cache-aside pattern).
**Q3: What is write-through?** A: Update cache immediately when writing to DB.
**Q4: Which supports Multi-AZ failover?** A: Redis (not Memcached).
**Q5: Which supports backup and restore?** A: Redis only.
