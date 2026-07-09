w("analytics/01-athena.md", """# Amazon Athena

Athena is a serverless query service that analyzes data stored in S3 using standard SQL.

## Key Features
- Serverless (no infrastructure to manage)
- Pay per query (based on data scanned)
- Works with S3, Glue Data Catalog
- Supports CSV, JSON, Parquet, ORC, Avro
- Integrates with QuickSight

## Performance Optimization
- **Partitioning**: Reduces data scanned
- **Columnar formats**: Parquet/ORC (saves 30-90%)
- **Compression**: Gzip, Snappy, Zstd
- **Bucketing**: Further reduces data scanned

## CLI
```bash
# Create database
aws athena start-query-execution \
    --query-string "CREATE DATABASE my_database" \
    --result-configuration OutputLocation=s3://my-athena-results/

# Create table
aws athena start-query-execution \
    --query-string "CREATE EXTERNAL TABLE IF NOT EXISTS my_database.orders (
        order_id INT,
        customer_id INT,
        order_date STRING,
        amount DOUBLE
    ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    LOCATION 's3://my-bucket/orders/'
    TBLPROPERTIES ('skip.header.line.count'='1')" \
    --result-configuration OutputLocation=s3://my-athena-results/

# Run query
aws athena start-query-execution \
    --query-string "SELECT customer_id, SUM(amount) as total FROM my_database.orders GROUP BY customer_id ORDER BY total DESC LIMIT 10" \
    --result-configuration OutputLocation=s3://my-athena-results/

# Get query results
aws athena get-query-results --query-execution-id QUERYID

# Get query execution
aws athena get-query-execution --query-execution-id QUERYID
```

## Q&A
**Q1: What is Athena?** A: Serverless SQL query service for S3 data.
**Q2: How is Athena priced?** A: Pay per query (per TB scanned).
**Q3: What file format gives the best performance?** A: Parquet/ORC (columnar, compressed).
**Q4: How do you reduce costs?** A: Partition data, use columnar formats, compress.
**Q5: Can Athena query on-premises data?** A: No, only S3 and Federated sources.
""")
