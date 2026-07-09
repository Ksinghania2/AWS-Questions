# Amazon Kinesis - Real-Time Streaming Data

Amazon Kinesis makes it easy to collect, process, and analyze real-time streaming data.

## Kinesis Services

| Service | Description | Use Case |
|---------|-------------|----------|
| **Data Streams** | Real-time data streaming with custom consumers | Custom processing, real-time analytics |
| **Data Firehose** | Load streaming data to destinations | S3, Redshift, OpenSearch, Splunk |
| **Video Streams** | Streaming video from devices | Media processing, ML |
| **Managed Service for Apache Flink** | Real-time stream transformations | Complex event processing |

## Kinesis Data Streams Architecture

```
Producers (Apps, SDK, KPL, Kinesis Agent)
    |
    v
Kinesis Data Streams (Shards)
    |
    +-- Shard 1 (1MB/s write, 2MB/s read)
    +-- Shard 2 (1MB/s write, 2MB/s read)
    +-- Shard N (1MB/s write, 2MB/s read)
    |
    v
Consumers (Lambda, EC2, KCL, Firehose, Flink)
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Shard** | Base throughput unit (1MB/s write, 2MB/s read, 1000 records/s) |
| **Record** | Unit of data (up to 1MB) |
| **Partition Key** | Determines which shard a record goes to |
| **Sequence Number** | Unique identifier per shard |
| **Retention Period** | 24 hours (default) to 365 days (extended) |
| **Enhanced Fan-Out** | 2MB/s per consumer (dedicated throughput) |
| **Consumer** | Application that processes records |

## Step-by-Step CLI Examples

### Step 1: Create a Data Stream
```bash
# Create stream with 3 shards
aws kinesis create-stream     --stream-name order-events     --shard-count 3

# Wait for stream to become active
aws kinesis wait stream-exists --stream-name order-events
```

### Step 2: Put Records
```bash
# Put a single record
aws kinesis put-record     --stream-name order-events     --data "{\"order_id\":123,\"customer_id\":456,\"amount\":99.99}"     --partition-key "customer_456"

# Put multiple records (batch)
aws kinesis put-records     --stream-name order-events     --records '[
        {"Data":"record1","PartitionKey":"pk1"},
        {"Data":"record2","PartitionKey":"pk2"},
        {"Data":"record3","PartitionKey":"pk3"}
    ]'
```

### Step 3: Get Shard Iterator and Read Records
```bash
# Get shard ID
SHARD_ID=$(aws kinesis describe-stream     --stream-name order-events     --query 'StreamDescription.Shards[0].ShardId'     --output text)

# Get shard iterator (TRIM_HORIZON = oldest, LATEST = newest)
SHARD_ITERATOR=$(aws kinesis get-shard-iterator     --stream-name order-events     --shard-id $SHARD_ID     --shard-iterator-type TRIM_HORIZON     --query 'ShardIterator' --output text)

# Read records
aws kinesis get-records --shard-iterator "$SHARD_ITERATOR"
```

### Step 4: Create Firehose Delivery Stream
```bash
# Firehose to S3
aws firehose create-delivery-stream     --delivery-stream-name order-firehose     --delivery-stream-type DirectPut     --s3-destination-configuration         BucketARN=arn:aws:s3:::my-firehose-data,         RoleARN=arn:aws:iam::123456789012:role/FirehoseRole,         BufferingHints={IntervalInSeconds=60,SizeInMBs=10},         CompressionFormat=GZIP

# Firehose to Redshift
aws firehose create-delivery-stream     --delivery-stream-name redshift-firehose     --redshift-destination-configuration         RoleARN=arn:aws:iam::123456789012:role/FirehoseRedshiftRole,         ClusterJDBCURL=jdbc:redshift://my-cluster.xxxxx.us-east-1.redshift.amazonaws.com:5439/dev,         CopyCommand={DataTableName=orders,DataTableColumns="data"},         Username=admin,Password=MyP@ss123!,         S3Configuration={BucketARN=arn:aws:s3:::my-firehose-temp,RoleARN=arn:aws:iam::123456789012:role/FirehoseS3Role}
```

### Step 5: Enhanced Fan-Out (EFO)
```bash
# Register consumer for dedicated throughput
aws kinesis register-stream-consumer     --stream-arn arn:aws:kinesis:us-east-1:123456789012:stream/order-events     --consumer-name my-consumer

# Subscribe to shard with EFO
aws kinesis subscribe-to-shard     --consumer-arn arn:aws:kinesis:us-east-1:123456789012:stream/order-events/consumer/my-consumer     --shard-id shardId-000000000000
```

### Step 6: Kinesis Agent (On-Premises)
```bash
# Install Kinesis Agent on EC2/on-premises
sudo yum install -y aws-kinesis-agent

# Configure /etc/aws-kinesis/agent.json
{
    "cloudwatch.emitMetrics": true,
    "kinesis.endpoint": "https://kinesis.us-east-1.amazonaws.com",
    "flows": [
        {
            "filePattern": "/var/log/app/*.log",
            "kinesisStream": "order-events"
        }
    ]
}

# Start agent
sudo service aws-kinesis-agent start
```

## 20 Practice Questions

**Q1: What is Amazon Kinesis Data Streams?**
A: A real-time data streaming service that captures and processes data in shards.

**Q2: What is a shard in Kinesis?**
A: The base throughput unit: 1MB/s write (or 1000 records/s) and 2MB/s read.

**Q3: What is the difference between Data Streams and Data Firehose?**
A: Data Streams requires custom consumers for processing; Firehose automatically delivers to destinations (S3, Redshift, OpenSearch).

**Q4: What is the default retention period for Kinesis Data Streams?**
A: 24 hours (can be extended to 365 days at additional cost).

**Q5: What is Enhanced Fan-Out?**
A: Provides 2MB/s dedicated read throughput per consumer (vs 2MB/s shared across all consumers).

**Q6: What is the maximum record size in Kinesis?**
A: 1 MB.

**Q7: What is a partition key used for?**
A: To determine which shard a record is sent to (ensures data distribution).

**Q8: What is the Kinesis Producer Library (KPL)?**
A: A library that helps write data to Kinesis with batching, compression, and retries.

**Q9: What is the Kinesis Consumer Library (KCL)?**
A: A library that helps read and process data from Kinesis with checkpointing and load balancing.

**Q10: Can Kinesis Data Streams reprocess data?**
A: Yes, by using a different shard iterator type (TRIM_HORIZON for oldest, AT_TIMESTAMP for specific time).

**Q11: What is Kinesis Data Firehose?**
A: A fully managed service for loading streaming data into S3, Redshift, OpenSearch, and Splunk.

**Q12: What buffering options does Firehose support?**
A: Size (MB) and interval (seconds) based buffering before delivery.

**Q13: What is Kinesis Video Streams?**
A: A service for streaming video from devices for playback, ML, and media processing.

**Q14: What is Managed Service for Apache Flink?**
A: A service for running Apache Flink applications on Kinesis data streams for real-time analytics.

**Q15: How does Kinesis handle data durability?**
A: Data is replicated across 3 AZs within a region.

**Q16: What is the maximum number of shards per stream?**
A: 500 (default limit, can be increased).

**Q17: What is resharding in Kinesis?**
A: Splitting or merging shards to change stream capacity.

**Q18: Can Kinesis be used with Lambda?**
A: Yes, Lambda can poll from Data Streams or be triggered by Firehose.

**Q19: What is the Kinesis Agent?**
A: A pre-built agent that monitors log files and sends data to Kinesis.

**Q20: What is the difference between Kinesis and SQS?**
A: Kinesis is for real-time streaming (multiple consumers, replay); SQS is for message queuing (single consumer, no replay).
