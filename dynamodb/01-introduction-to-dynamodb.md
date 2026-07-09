# Amazon DynamoDB

DynamoDB is a fully managed NoSQL key-value and document database.

## Key Concepts
| Concept | Description |
|---------|-------------|
| **Table** | Collection of items |
| **Item** | Single record (up to 400KB) |
| **Partition Key** | Primary key for distribution |
| **Sort Key** | Optional secondary key for sorting |
| **GSI** | Global Secondary Index (different PK/SK) |
| **LSI** | Local Secondary Index (same PK, different SK) |

## Read Consistency
| Model | Description |
|-------|-------------|
| **Eventually Consistent** | Default, reads may be stale (half the cost) |
| **Strongly Consistent** | Always latest data (higher cost) |

## CLI
```bash
# Create table
aws dynamodb create-table     --table-name Users     --attribute-definitions AttributeName=UserId,AttributeType=S     --key-schema AttributeName=UserId,KeyType=HASH     --billing-mode PAY_PER_REQUEST

# Create table with GSI
aws dynamodb create-table     --table-name Orders     --attribute-definitions AttributeName=OrderId,AttributeType=S AttributeName=CustomerId,AttributeType=S AttributeName=Status,AttributeType=S     --key-schema AttributeName=OrderId,KeyType=HASH     --global-secondary-indexes IndexName=CustomerIndex,KeySchema=[{AttributeName=CustomerId,KeyType=HASH},{AttributeName=Status,KeyType=RANGE}],Projection={ProjectionType=ALL}     --billing-mode PAY_PER_REQUEST

# Put item
aws dynamodb put-item     --table-name Users     --item '{"UserId":{"S":"user1"},"Name":{"S":"Alice"},"Email":{"S":"alice@example.com"}}'

# Get item
aws dynamodb get-item     --table-name Users     --key '{"UserId":{"S":"user1"}}'

# Query (efficient - uses PK)
aws dynamodb query     --table-name Orders     --index-name CustomerIndex     --key-condition-expression "CustomerId = :cid"     --expression-attribute-values '{":cid":{"S":"cust123"}}'

# Scan (inefficient - reads entire table)
aws dynamodb scan --table-name Orders

# Update item
aws dynamodb update-item     --table-name Users     --key '{"UserId":{"S":"user1"}}'     --update-expression "SET #n = :name"     --expression-attribute-names '{"#n":"Name"}'     --expression-attribute-values '{":name":{"S":"Alice Updated"}}'
```

## Q&A
**Q1: What is the max item size in DynamoDB?** A: 400KB.
**Q2: What is the difference between query and scan?** A: Query uses PK for efficient lookups; Scan reads entire table.
**Q3: What is a GSI?** A: Global Secondary Index - different PK/SK for alternative access patterns.
**Q4: What is an LSI?** A: Local Secondary Index - same PK, different SK (must be created at table creation).
**Q5: What are the two read consistency models?** A: Eventually Consistent (default) and Strongly Consistent.
**Q6: What are the billing modes?** A: On-Demand (pay per request) and Provisioned (RCU/WCU).
**Q7: What is DynamoDB Streams?** A: Time-ordered log of item changes (for triggers, replication).
**Q8: What is TTL?** A: Time to Live - auto-deletes items after a specified timestamp.
