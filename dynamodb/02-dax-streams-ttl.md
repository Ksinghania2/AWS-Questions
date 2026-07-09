# DynamoDB DAX, Streams & TTL

## DynamoDB Accelerator (DAX)
In-memory cache for DynamoDB with microsecond latency.

```bash
# Create DAX cluster
aws dax create-cluster     --cluster-name my-dax     --node-type dax.r5.large     --replication-factor 3     --iam-role-arn arn:aws:iam::xxx:role/DAXServiceRole     --subnet-group-name my-dax-subnet-group     --security-group-ids sg-xxx
```

## DynamoDB Streams
Captures item-level changes (Create, Update, Delete) for downstream processing.

```bash
# Enable streams
aws dynamodb update-table     --table-name Orders     --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES

# Read from stream
aws dynamodbstreams get-shard-iterator     --stream-arn arn:aws:dynamodb:us-east-1:xxx:table/Orders/stream/xxx     --shard-id shard-xxx     --shard-iterator-type TRIM_HORIZON
```

## Time to Live (TTL)
Auto-deletes expired items without cost or throughput consumption.

```bash
# Enable TTL
aws dynamodb update-time-to-live     --table-name Sessions     --time-to-live-specification Enabled=true,AttributeName=ExpiryTime
```

## Q&A
**Q1: What is DAX?** A: In-memory cache for DynamoDB (microsecond latency).
**Q2: What are DynamoDB Streams used for?** A: Real-time item change processing (Lambda triggers).
**Q3: What is TTL?** A: Auto-deletes items at specified timestamp (no cost).
**Q4: What stream view types are available?** A: KEYS_ONLY, NEW_IMAGE, OLD_IMAGE, NEW_AND_OLD_IMAGES.
**Q5: Does TTL cost money?** A: No, deletions are free.
