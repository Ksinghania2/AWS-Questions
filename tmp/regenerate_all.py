import os

BASE = "/Users/kshitij/Desktop/AWS-Solutions-Architect"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content.strip() + "\n")
    print(f"OK: {path}")

# =====================================================================
# REDSHIFT (Major - 20 Q&A)
# =====================================================================
w("analytics/02-redshift.md", """# Amazon Redshift - Petabyte-Scale Data Warehouse

Amazon Redshift is a fully managed, petabyte-scale data warehouse service in the cloud. It uses columnar storage and massively parallel processing (MPP) to run complex analytical queries.

## Architecture

```
Client Tools (SQL Workbench, QuickSight, Tableau)
    |
    v
Leader Node (SQL endpoint, query planning)
    |
    +--------+--------+--------+
    v        v        v        v
Compute Node 1  Node 2  Node 3  Node N
    |        |        |        |
    v        v        v        v
    [Local SSD or Managed Storage (RA3)]
```

## Node Types

| Type | Storage | Use Case |
|------|---------|----------|
| **DC2** (Dense Compute) | Local SSD (NVMe) | High performance, smaller datasets |
| **DS2** (Dense Storage) | Local HDD | Large datasets, lower cost |
| **RA3** (Managed Storage) | Managed storage (S3) | Separate compute and storage, auto-scaling |

## Key Features

| Feature | Description |
|---------|-------------|
| Columnar Storage | Stores data by column, not row (better compression, faster scans) |
| MPP Architecture | Distributes queries across multiple nodes |
| Redshift Spectrum | Query data directly in S3 without loading into Redshift |
| Automatic Tuning | Sort keys, distribution keys, compression encodings |
| Concurrency Scaling | Auto-adds cluster capacity for concurrent queries |
| AQUA (Advanced Query Accelerator) | Hardware-accelerated caching for faster queries |
| Materialized Views | Pre-computed query results for faster access |
| Automated Snapshot | Backup to S3 with configurable retention |

## Step-by-Step CLI Examples

### Step 1: Create a Redshift Cluster
```bash
# Create cluster in a VPC
aws redshift create-cluster \
    --cluster-identifier my-warehouse \
    --node-type ra3.xlplus \
    --number-of-nodes 2 \
    --master-username admin \
    --master-user-password MyS3cur3P@ss! \
    --vpc-security-group-ids sg-12345678 \
    --cluster-subnet-group-name my-redshift-subnet-group \
    --publicly-accessible \
    --encrypted \
    --kms-key-id alias/redshift-key \
    --automated-snapshot-retention-period 7

# Wait for cluster to become available
aws redshift wait cluster-available --cluster-identifier my-warehouse
```

### Step 2: Configure Database
```bash
# Get cluster endpoint
aws redshift describe-clusters \
    --cluster-identifier my-warehouse \
    --query 'Clusters[0].Endpoint' \
    --output json

# Connect using psql
psql -h my-warehouse.xxxxxx.us-east-1.redshift.amazonaws.com -U admin -d dev -p 5439

# Create schema and tables
CREATE SCHEMA sales;
CREATE TABLE sales.orders (
    order_id BIGINT IDENTITY(1,1),
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2),
    status VARCHAR(20)
)
SORTKEY (order_date)
DISTKEY (customer_id);
```

### Step 3: Load Data from S3
```bash
# Copy data from S3
COPY sales.orders
FROM 's3://my-data-bucket/orders/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3Role'
CSV
IGNOREHEADER 1
REGION 'us-east-1';
```

### Step 4: Create Snapshots
```bash
# Manual snapshot
aws redshift create-cluster-snapshot \
    --snapshot-identifier my-warehouse-pre-upgrade \
    --cluster-identifier my-warehouse

# Restore from snapshot
aws redshift restore-from-cluster-snapshot \
    --cluster-identifier my-warehouse-restored \
    --snapshot-identifier my-warehouse-pre-upgrade
```

### Step 5: Pause/Resume (Cost Savings)
```bash
# Pause when not in use (saves compute costs)
aws redshift pause-cluster --cluster-identifier my-warehouse

# Resume when needed
aws redshift resume-cluster --cluster-identifier my-warehouse
```

### Step 6: Redshift Spectrum (Query S3 Directly)
```sql
-- Create external schema pointing to S3
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'spectrum_db'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftSpectrumRole';

-- Query S3 data directly
SELECT customer_id, COUNT(*) as order_count
FROM spectrum_schema.orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
ORDER BY order_count DESC;
```

## Distribution Styles

| Style | Description | When to Use |
|-------|-------------|-------------|
| **KEY** | Distribute by column value | Joins on that column (collocation) |
| **ALL** | Full copy on every node | Small dimension tables |
| **EVEN** | Round-robin distribution | Default, when no clear key |

## Sort Keys

| Type | Description |
|------|-------------|
| **Compound** | Most efficient for prefix columns (e.g., date, category) |
| **Interleaved** | Equal weight to all columns (e.g., multiple filter columns) |

## 20 Practice Questions

**Q1: What is Amazon Redshift?**
A: A fully managed, petabyte-scale data warehouse using columnar storage and MPP.

**Q2: What is the difference between DC2 and RA3 nodes?**
A: DC2 uses local SSD (fixed compute+storage); RA3 separates compute from managed storage (S3), allowing independent scaling.

**Q3: What is Redshift Spectrum?**
A: A feature that allows querying data directly in S3 without loading it into Redshift clusters.

**Q4: How do you save costs on Redshift?**
A: Pause the cluster when not in use, use RA3 nodes, use concurrency scaling only when needed.

**Q5: What is the automated snapshot retention period?**
A: 1 to 35 days (default 1 day).

**Q6: What is a distribution key?**
A: Determines how data is distributed across compute nodes (KEY, ALL, EVEN).

**Q7: What is a sort key?**
A: Defines the order of data within each node for efficient range filtering.

**Q8: What is the difference between compound and interleaved sort keys?**
A: Compound is best for prefix column queries; interleaved gives equal weight to all columns.

**Q9: What is concurrency scaling?**
A: Auto-adds cluster capacity to handle concurrent queries without performance degradation.

**Q10: What is AQUA?**
A: Advanced Query Accelerator - hardware-accelerated caching for faster query performance.

**Q11: How does Redshift encrypt data?**
A: At rest using KMS or CloudHSM; in transit using SSL.

**Q12: Can Redshift be paused?**
A: Yes, pausing stops compute costs while retaining data in managed storage.

**Q13: What is the maximum storage for RA3 nodes?**
A: Up to 8 PB per cluster (managed storage).

**Q14: What is a materialized view in Redshift?**
A: Pre-computed query results that can be refreshed incrementally for faster access.

**Q15: How do you load data from S3 into Redshift?**
A: Using the COPY command with an IAM role.

**Q16: What is VACUUM in Redshift?**
A: Reclaims space from deleted rows and re-sorts data.

**Q17: What is ANALYZE in Redshift?**
A: Updates table statistics for the query optimizer.

**Q18: Can Redshift query data across multiple AWS accounts?**
A: Yes, using Spectrum with cross-account S3 bucket policies.

**Q19: What is the maximum number of nodes in a Redshift cluster?**
A: 128 nodes (can be increased with Service Quotas).

**Q20: What is the difference between Redshift and Athena?**
A: Redshift is a provisioned data warehouse (faster for complex queries, higher cost); Athena is serverless (pay per query, no cluster management).
""")

# =====================================================================
# GLUE (Major - 20 Q&A)
# =====================================================================
w("analytics/03-glue.md", """# AWS Glue - Serverless ETL Service

AWS Glue is a fully managed extract, transform, and load (ETL) service that makes it easy to prepare and load data for analytics.

## Architecture

```
Data Sources (S3, RDS, DynamoDB, JDBC)
    |
    v
Glue Crawler (Discovers schema)
    |
    v
Glue Data Catalog (Central metadata repository)
    |
    v
Glue ETL Job (Apache Spark - Python/Scala)
    |
    v
Target (S3, Redshift, RDS, Athena)
```

## Key Components

| Component | Description |
|-----------|-------------|
| **Data Catalog** | Central metadata repository for all table definitions |
| **Crawler** | Scans data sources, infers schema, populates Data Catalog |
| **ETL Job** | Apache Spark-based transformation code |
| **Workflow** | Orchestrates multiple crawlers and jobs |
| **Trigger** | Starts jobs based on schedule or event |
| **Glue Studio** | Visual ETL development interface |
| **Glue DataBrew** | Visual data preparation (no code) |
| **Glue Elastic Views** | Materialized views across multiple data stores |

## Step-by-Step CLI Examples

### Step 1: Create a Database in Data Catalog
```bash
aws glue create-database --database-input '{"Name":"sales_db"}'
```

### Step 2: Create a Crawler
```bash
aws glue create-crawler \
    --name s3-sales-crawler \
    --role arn:aws:iam::123456789012:role/GlueServiceRole \
    --database-name sales_db \
    --targets '{"S3Targets":[{"Path":"s3://my-sales-data/orders/"}]}' \
    --schedule "cron(0 6 * * ? *)" \
    --schema-change-policy '{"UpdateBehavior":"UPDATE_IN_DATABASE","DeleteBehavior":"LOG"}'
```

### Step 3: Start the Crawler
```bash
aws glue start-crawler --name s3-sales-crawler
```

### Step 4: Create an ETL Job
```bash
# Upload ETL script to S3
aws s3 cp etl_script.py s3://my-glue-scripts/etl_script.py

# Create job
aws glue create-job \
    --name sales-etl-job \
    --role arn:aws:iam::123456789012:role/GlueServiceRole \
    --command '{"Name":"glueetl","ScriptLocation":"s3://my-glue-scripts/etl_script.py","PythonVersion":"3"}' \
    --default-arguments '{"--job-bookmark-option":"job-bookmark-enable","--enable-metrics":"true"}' \
    --max-retries 1 \
    --timeout 60 \
    --glue-version "4.0" \
    --number-of-workers 10 \
    --worker-type "G.1X"
```

### Step 5: Start Job Run
```bash
aws glue start-job-run --job-name sales-etl-job
```

### Step 6: Monitor Job
```bash
# List job runs
aws glue get-job-runs --job-name sales-etl-job

# Get job run details
aws glue get-job-run --job-name sales-etl-job --run-id jr_xxxxx
```

### Sample ETL Script (Python)
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from Data Catalog
orders = glueContext.create_dynamic_frame.from_catalog(
    database="sales_db",
    table_name="orders"
)

# Transform: filter and aggregate
from pyspark.sql.functions import col, sum
result = orders.toDF() \
    .filter(col("status") == "COMPLETED") \
    .groupBy("customer_id") \
    .agg(sum("amount").alias("total_spent"))

# Write to S3 in Parquet
result.write.mode("overwrite") \
    .parquet("s3://my-sales-data/processed/customer_totals/")

job.commit()
```

## 20 Practice Questions

**Q1: What is AWS Glue?**
A: A fully managed serverless ETL service for preparing and loading data.

**Q2: What is the Glue Data Catalog?**
A: A central metadata repository that stores table definitions, schemas, and partition information.

**Q3: What is a Glue Crawler?**
A: A component that scans data sources, infers schemas, and populates the Data Catalog.

**Q4: What programming languages does Glue ETL support?**
A: Python and Scala (both running on Apache Spark).

**Q5: What is Glue Studio?**
A: A visual interface for creating and monitoring ETL jobs without writing code.

**Q6: What is Glue DataBrew?**
A: A visual data preparation tool for cleaning and normalizing data without code.

**Q7: What is a Glue Workflow?**
A: Orchestrates multiple crawlers, jobs, and triggers into a single ETL pipeline.

**Q8: What is job bookmarking in Glue?**
A: Tracks processed data to avoid reprocessing on subsequent runs.

**Q9: What is the difference between Glue and Athena?**
A: Glue is for ETL (transform and load); Athena is for querying data in place.

**Q10: What data sources can Glue connect to?**
A: S3, RDS, DynamoDB, Redshift, JDBC, Kinesis, Kafka.

**Q11: What is Glue Elastic Views?**
A: Creates materialized views that combine data from multiple sources.

**Q12: How does Glue handle schema evolution?**
A: Crawlers can detect schema changes and update the Data Catalog automatically.

**Q13: What is the Glue job timeout limit?**
A: Maximum 2,880 minutes (48 hours).

**Q14: What worker types are available in Glue?**
A: G.1X (16GB RAM), G.2X (32GB RAM), G.4X (64GB RAM), G.8X (128GB RAM).

**Q15: Can Glue be triggered by events?**
A: Yes, using EventBridge rules or Glue Triggers.

**Q16: What is the difference between Glue and Lake Formation?**
A: Glue is for ETL; Lake Formation is for data lake security and governance.

**Q17: How does Glue handle data partitioning?**
A: Automatically detects partitions during crawling and uses them for efficient processing.

**Q18: What is the Glue DynamicFrame?**
A: A Glue-specific data abstraction that handles schema evolution and errors gracefully.

**Q19: Can Glue process streaming data?**
A: Yes, Glue Streaming ETL jobs can process data from Kinesis and Kafka.

**Q20: What is the cost model for Glue?**
A: Pay per DPU (Data Processing Unit) per hour for ETL jobs; Data Catalog is free.
""")

# =====================================================================
# LAKE FORMATION (Medium - 10 Q&A)
# =====================================================================
w("analytics/04-lake-formation.md", """# AWS Lake Formation - Data Lake Management

AWS Lake Formation simplifies building, securing, and managing data lakes. It provides centralized permissions, automated data ingestion, and fine-grained access control.

## Architecture

```
Data Sources (S3, RDS, DynamoDB, On-premises)
    |
    v
Lake Formation (Blueprints, Crawlers, Permissions)
    |
    v
Data Lake (S3 Bucket)
    |
    +-- Glue Data Catalog (with Lake Formation permissions)
    |       |
    |       v
    |   Athena, Redshift Spectrum, EMR, QuickSight
    |
    +-- Row/Column level security
    +-- Cell-level filtering
```

## Key Features

| Feature | Description |
|---------|-------------|
| Centralized Permissions | Manage access to data lake resources from one place |
| Row-Level Security | Filter rows based on user/role |
| Column-Level Security | Hide sensitive columns (PII, SSN) |
| Cell-Level Security | Filter specific cells based on conditions |
| Blueprints | Pre-built templates for data ingestion |
| Automated Ingestion | Schedule and automate data loading |
| Access Control | Grant/revoke permissions on databases, tables, columns |

## Step-by-Step CLI Examples

### Step 1: Register S3 Bucket as Data Lake
```bash
aws lakeformation register-resource \
    --resource-arn arn:aws:s3:::my-data-lake-bucket \
    --role-arn arn:aws:iam::123456789012:role/LakeFormationRole \
    --use-service-linked-role
```

### Step 2: Grant Table Permissions
```bash
# Grant SELECT on specific table to a user
aws lakeformation grant-permissions \
    --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:user/data-analyst \
    --resource '{"Table":{"DatabaseName":"sales","Name":"orders"}}' \
    --permissions "SELECT" "DESCRIBE"
```

### Step 3: Grant Column-Level Permissions
```bash
# Grant access to specific columns only
aws lakeformation grant-permissions \
    --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:user/junior-analyst \
    --resource '{"TableWithColumns":{"DatabaseName":"hr","Name":"employees","ColumnNames":["name","department","title"]}}' \
    --permissions "SELECT"
```

### Step 4: Grant Row-Level Permissions (Data Filters)
```bash
# Create data filter for row-level security
aws lakeformation create-data-cells-filter \
    --name "us-sales-only" \
    --table-data '{"DatabaseName":"sales","Name":"orders","RowFilterExpression":"region = 'us'"}' \
    --table-catalog-id 123456789012

# Grant with filter
aws lakeformation grant-permissions \
    --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:user/regional-manager \
    --resource '{"DataCellsFilter":{"TableCatalogId":"123456789012","DatabaseName":"sales","Name":"orders","TableName":"orders"}}' \
    --permissions "SELECT"
```

### Step 5: Use Blueprint for Ingestion
```bash
# Create workflow from blueprint
aws lakeformation create-workflow \
    --name "daily-sales-ingest" \
    --description "Daily sales data ingestion" \
    --blueprint-name "S3_IMPORT" \
    --role-arn arn:aws:iam::123456789012:role/LakeFormationWorkflowRole
```

## 10 Practice Questions

**Q1: What is AWS Lake Formation?**
A: A service for building, securing, and managing data lakes with centralized permissions.

**Q2: What is the difference between Glue and Lake Formation?**
A: Glue is for ETL (data transformation); Lake Formation is for data lake security and governance.

**Q3: Can Lake Formation control row-level access?**
A: Yes, using Data Cells Filters with row filter expressions.

**Q4: Can Lake Formation control column-level access?**
A: Yes, you can grant access to specific columns only.

**Q5: What is a Lake Formation blueprint?**
A: A pre-built template for automated data ingestion from various sources.

**Q6: What services integrate with Lake Formation?**
A: Athena, Redshift Spectrum, EMR, QuickSight, Glue.

**Q7: How does Lake Formation enforce permissions?**
A: By intercepting requests through the Glue Data Catalog and applying access policies.

**Q8: What is a Data Cells Filter?**
A: A filter that restricts access to specific rows and columns in a table.

**Q9: Can Lake Formation manage cross-account access?**
A: Yes, using resource-based policies and RAM (Resource Access Manager).

**Q10: What happens when you register an S3 bucket with Lake Formation?**
A: Lake Formation takes over permission management for that bucket, replacing IAM policies.
""")

# =====================================================================
# KINESIS (Major - 20 Q&A)
# =====================================================================
w("analytics/05-kinesis.md", """# Amazon Kinesis - Real-Time Streaming Data

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
aws kinesis create-stream \
    --stream-name order-events \
    --shard-count 3

# Wait for stream to become active
aws kinesis wait stream-exists --stream-name order-events
```

### Step 2: Put Records
```bash
# Put a single record
aws kinesis put-record \
    --stream-name order-events \
    --data "{\\"order_id\\":123,\\"customer_id\\":456,\\"amount\\":99.99}" \
    --partition-key "customer_456"

# Put multiple records (batch)
aws kinesis put-records \
    --stream-name order-events \
    --records '[
        {"Data":"record1","PartitionKey":"pk1"},
        {"Data":"record2","PartitionKey":"pk2"},
        {"Data":"record3","PartitionKey":"pk3"}
    ]'
```

### Step 3: Get Shard Iterator and Read Records
```bash
# Get shard ID
SHARD_ID=$(aws kinesis describe-stream \
    --stream-name order-events \
    --query 'StreamDescription.Shards[0].ShardId' \
    --output text)

# Get shard iterator (TRIM_HORIZON = oldest, LATEST = newest)
SHARD_ITERATOR=$(aws kinesis get-shard-iterator \
    --stream-name order-events \
    --shard-id $SHARD_ID \
    --shard-iterator-type TRIM_HORIZON \
    --query 'ShardIterator' --output text)

# Read records
aws kinesis get-records --shard-iterator "$SHARD_ITERATOR"
```

### Step 4: Create Firehose Delivery Stream
```bash
# Firehose to S3
aws firehose create-delivery-stream \
    --delivery-stream-name order-firehose \
    --delivery-stream-type DirectPut \
    --s3-destination-configuration \
        BucketARN=arn:aws:s3:::my-firehose-data, \
        RoleARN=arn:aws:iam::123456789012:role/FirehoseRole, \
        BufferingHints={IntervalInSeconds=60,SizeInMBs=10}, \
        CompressionFormat=GZIP

# Firehose to Redshift
aws firehose create-delivery-stream \
    --delivery-stream-name redshift-firehose \
    --redshift-destination-configuration \
        RoleARN=arn:aws:iam::123456789012:role/FirehoseRedshiftRole, \
        ClusterJDBCURL=jdbc:redshift://my-cluster.xxxxx.us-east-1.redshift.amazonaws.com:5439/dev, \
        CopyCommand={DataTableName=orders,DataTableColumns="data"}, \
        Username=admin,Password=MyP@ss123!, \
        S3Configuration={BucketARN=arn:aws:s3:::my-firehose-temp,RoleARN=arn:aws:iam::123456789012:role/FirehoseS3Role}
```

### Step 5: Enhanced Fan-Out (EFO)
```bash
# Register consumer for dedicated throughput
aws kinesis register-stream-consumer \
    --stream-arn arn:aws:kinesis:us-east-1:123456789012:stream/order-events \
    --consumer-name my-consumer

# Subscribe to shard with EFO
aws kinesis subscribe-to-shard \
    --consumer-arn arn:aws:kinesis:us-east-1:123456789012:stream/order-events/consumer/my-consumer \
    --shard-id shardId-000000000000
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
""")

print("=== Analytics files regenerated ===")
print("Created: analytics/02-redshift.md, 03-glue.md, 04-lake-formation.md, 05-kinesis.md")