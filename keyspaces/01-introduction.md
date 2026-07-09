# Amazon Keyspaces (Apache Cassandra)

Keyspaces is a managed Apache Cassandra-compatible wide-column database.

## Key Features
- Cassandra Query Language (CQL) compatible
- Serverless (auto-scaling)
- Multi-AZ by default
- Up to 10x faster than self-managed Cassandra

## CLI
```bash
# Create keyspace
aws keyspaces create-keyspace --keyspace-name my_keyspace

# Create table
aws keyspaces create-table     --keyspace-name my_keyspace     --table-name users     --schema-definition '{"AllColumns":[{"name":"user_id","type":"uuid"},{"name":"name","type":"text"},{"name":"email","type":"text"}],"PartitionKeys":[{"name":"user_id"}]}'     --default-time-to-live 0
```

## Q&A
**Q1: What database is Keyspaces compatible with?** A: Apache Cassandra (CQL).
**Q2: Is Keyspaces serverless?** A: Yes, auto-scaling.
**Q3: What is the difference between Keyspaces and DynamoDB?** A: Keyspaces uses CQL (Cassandra); DynamoDB uses its own API.
**Q4: Is Keyspaces multi-AZ?** A: Yes, by default.
**Q5: What use case for Keyspaces?** A: Migrating Cassandra workloads to AWS.
