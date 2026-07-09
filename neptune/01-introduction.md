# Amazon Neptune

Neptune is a fully managed graph database service.

## Key Features
- Property Graph and RDF (Resource Description Framework)
- Supports Gremlin, SPARQL, openCypher
- 6 copies of data across 3 AZs
- Up to 15 read replicas
- Point-in-time recovery

## CLI
```bash
# Create cluster
aws neptune create-db-cluster     --db-cluster-identifier my-neptune     --engine neptune     --vpc-security-group-ids sg-xxx

# Create instance
aws neptune create-db-instance     --db-instance-identifier my-neptune-writer     --db-instance-class db.r5.large     --engine neptune     --db-cluster-identifier my-neptune
```

## Q&A
**Q1: What is a graph database?** A: Stores data as nodes and edges (relationships).
**Q2: What query languages does Neptune support?** A: Gremlin, SPARQL, openCypher.
**Q3: What is the difference between Property Graph and RDF?** A: Property Graph uses Gremlin/openCypher; RDF uses SPARQL.
**Q4: How many read replicas does Neptune support?** A: Up to 15.
**Q5: Use case for Neptune?** A: Social networks, fraud detection, recommendation engines.
