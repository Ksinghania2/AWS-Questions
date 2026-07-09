import os, shutil

BASE = "/Users/kshitij/Desktop/AWS-Solutions-Architect"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content.strip() + "\n")
    print(f"OK: {path}")

# =====================================================================
# 1. ANALYTICS - ATHENA (Major - 20 Q&A)
# =====================================================================
w("analytics/01-athena.md", """# Amazon Athena - Serverless SQL Query Service

Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. Athena is serverless, so there is no infrastructure to manage, and you pay only for the queries that you run.

## How Athena Works

1. Data resides in S3 (CSV, JSON, Parquet, ORC, Avro)
2. You define a schema in the Glue Data Catalog (or use a crawler)
3. You run SQL queries using standard syntax
4. Athena scans the data and returns results
5. You pay only for the data scanned

## Architecture

```
S3 Bucket (Data Source)
    |
    v
Athena Query Engine (Serverless)
    |
    +-- Glue Data Catalog (Schema)
    +-- Federated Query (Lambda, DynamoDB, RDS)
    |
    v
Query Results -> S3 Output Location
```

## Key Features

| Feature | Benefit |
|---------|---------|
| Serverless | No infrastructure to manage |
| Pay-per-query | $5 per TB of data scanned |
| Standard SQL | Supports ANSI SQL, DDL, DML |
| Multiple formats | CSV, JSON, Parquet, ORC, Avro, Log files |
| Partitioning | Reduces cost by scanning only relevant data |
| Compression | Works with gzip, snappy, zstd |
| Federated Query | Query data outside S3 via Lambda connectors |

## Performance Optimization Strategies

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| Partition data | 30-90% reduction | Partition by date/region/category |
| Use columnar formats | 30-75% reduction | Use Parquet or ORC instead of CSV |
| Compress files | 50-70% reduction | Use snappy, gzip, or zstd |
| Convert to columnar | 75-90% reduction | Convert CSV to Parquet |
| Bucketing | Further optimization | Hash-based data organization |

## Step-by-Step CLI Examples

### Step 1: Create a Database
```bash
# Create a database in Glue Data Catalog
aws athena start-query-execution \
    --query-string "CREATE DATABASE IF NOT EXISTS sales_db" \
    --result-configuration OutputLocation=s3://my-athena-results/
```

### Step 2: Create an External Table
```bash
# Create table pointing to S3 data
aws athena start-query-execution \
    --query-string "CREATE EXTERNAL TABLE IF NOT EXISTS sales_db.orders (
        order_id INT,
        customer_id INT,
        order_date STRING,
        amount DOUBLE,
        status STRING
    )
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    LOCATION 's3://my-sales-data/orders/'
    TBLPROPERTIES ('projection.enabled'='true')" \
    --result-configuration OutputLocation=s3://my-athena-results/
```

### Step 3: Create Partitioned Table (Cost Optimization)
```bash
# Partition by date for cost savings
aws athena start-query-execution \
    --query-string "CREATE EXTERNAL TABLE sales_db.orders_partitioned (
        order_id INT,
        customer_id INT,
        amount DOUBLE,
        status STRING
    )
    PARTITIONED BY (order_date STRING)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION 's3://my-sales-data/orders_partitioned/'
    TBLPROPERTIES ('skip.header.line.count'='1')" \
    --result-configuration OutputLocation=s3://my-athena-results/

# Load partitions
aws athena start-query-execution \
    --query-string "MSCK REPAIR TABLE sales_db.orders_partitioned" \
    --result-configuration OutputLocation=s3://my-athena-results/
```

### Step 4: Run Queries
```bash
# Basic query
QUERY_ID=$(aws athena start-query-execution \
    --query-string "SELECT customer_id, SUM(amount) as total_spent
                    FROM sales_db.orders
                    WHERE order_date >= '2024-01-01'
                    GROUP BY customer_id
                    ORDER BY total_spent DESC
                    LIMIT 10" \
    --result-configuration OutputLocation=s3://my-athena-results/ \
    --query 'QueryExecutionId' --output text)

# Check query status
aws athena get-query-execution --query-execution-id $QUERY_ID

# Get results when complete
aws athena get-query-results --query-execution-id $QUERY_ID
```

### Step 5: Use CTAS (Create Table As Select)
```bash
# Convert CSV to Parquet for future cost savings
aws athena start-query-execution \
    --query-string "CREATE TABLE sales_db.orders_parquet
                    WITH (
                        format = 'PARQUET',
                        parquet_compression = 'SNAPPY',
                        external_location = 's3://my-sales-data/optimized/orders/'
                    ) AS
                    SELECT * FROM sales_db.orders" \
    --result-configuration OutputLocation=s3://my-athena-results/
```

### Step 6: Federated Query Example
```bash
# Create Lambda connector to query CloudWatch Logs
# Requires Lambda function deployed via Serverless Application Repository
SELECT request_id, timestamp, message
FROM "lambda:cloudwatch_logs"."/aws/lambda/my-function"
WHERE timestamp > current_date - interval '1' day
LIMIT 100
```

## Integration with Other Services

| Service | Integration |
|---------|-------------|
| AWS Glue | Data Catalog for schema management |
| Amazon QuickSight | BI dashboards on Athena results |
| AWS Lake Formation | Fine-grained access control |
| AWS Lambda | Federated query connectors |
| Amazon S3 | Data storage location |
| AWS CloudTrail | Query CloudTrail logs directly |

## Exam Tips

| Tip | Details |
|-----|---------|
| Pricing | $5.00 per TB of data scanned |
| Cost reduction | Partition data, use columnar formats, compress files |
| CTAS | Convert data to Parquet using CTAS for cost savings |
| Partitions | Use MSCK REPAIR TABLE or ALTER TABLE ADD PARTITION |
| Maximum results | 1,000 rows per query (use LIMIT or pagination) |
| Federated Query | Query multiple data sources using Lambda connectors |
| Performance | Use columnar formats (Parquet/ORC) for best performance |
| ACID | Not ACID compliant - use for analytics, not transactions |
| Concurrent queries | Up to 20 concurrent queries (default) |
| Query history | 45 days of query history available |

## Real-World Scenario

**Scenario**: You work for a retail company with 2TB of daily sales data in S3 as CSV files. Queries are slow and expensive. How do you optimize?

**Solution**:
1. Convert CSV to Parquet using CTAS (reduces data 70%)
2. Partition by date (reduces scan to relevant days)
3. Compress with Snappy (reduces storage 60%)
4. Result: ~$5/TB becomes ~$0.15/TB (95%+ savings)

## 20 Practice Questions

**Q1: What is Amazon Athena?**
A: Serverless interactive query service that analyzes data in S3 using standard SQL.

**Q2: How is Athena priced?**
A: Pay per query based on the amount of data scanned ($5 per TB).

**Q3: What file format provides the best performance in Athena?**
A: Columnar formats like Parquet or ORC (reduces data scanned by 30-90%).

**Q4: How do you reduce Athena costs?**
A: Partition data, use columnar formats (Parquet/ORC), compress files, use CTAS to convert data.

**Q5: Can Athena query data in RDS or on-premises?**
A: Yes, using Athena Federated Query with Lambda connectors.

**Q6: What is the maximum result size per query?**
A: 1,000 rows (use LIMIT or pagination for more).

**Q7: What is CTAS in Athena?**
A: Create Table As Select - creates a new table from query results, useful for format conversion.

**Q8: How do partitions work in Athena?**
A: Partitions divide data into subdirectories (e.g., s3://bucket/year=2024/month=01/). Athena scans only relevant partitions.

**Q9: What is MSCK REPAIR TABLE used for?**
A: To load partition metadata into the Glue Data Catalog automatically.

**Q10: Can Athena query CloudTrail logs?**
A: Yes, Athena has a pre-built schema for CloudTrail logs.

**Q11: What compression formats does Athena support?**
A: gzip, snappy, zstd, and lz4.

**Q12: Is Athena ACID compliant?**
A: No, Athena is for analytical workloads, not transactional.

**Q13: What is the Glue Data Catalog's role in Athena?**
A: It stores table schemas and partition metadata that Athena uses to locate and interpret data.

**Q14: How many concurrent queries can Athena run by default?**
A: 20 concurrent queries (can be increased with Service Quotas).

**Q15: What is the query history retention period?**
A: 45 days.

**Q16: Can Athena write results to a different account's S3 bucket?**
A: Yes, with proper bucket policies and cross-account permissions.

**Q17: What is the difference between Athena and Redshift Spectrum?**
A: Both query S3. Athena is serverless (no cluster needed); Redshift Spectrum requires a Redshift cluster but offers more complex analytics.

**Q18: How do you encrypt Athena query results?**
A: Results are stored in S3; use S3 encryption (SSE-S3, SSE-KMS, or SSE-C).

**Q19: Can Athena be used with AWS Lake Formation?**
A: Yes, Lake Formation provides fine-grained access control (row/cell-level) for Athena queries.

**Q20: What is the best practice for Athena cost optimization?**
A: Partition by common filter columns, use Parquet format, compress with Snappy, and use CTAS to convert existing data.
""")

print("Created analytics/01-athena.md (full version with 20 Q&A)")