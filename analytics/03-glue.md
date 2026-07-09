# AWS Glue - Serverless ETL Service

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
aws glue create-crawler     --name s3-sales-crawler     --role arn:aws:iam::123456789012:role/GlueServiceRole     --database-name sales_db     --targets '{"S3Targets":[{"Path":"s3://my-sales-data/orders/"}]}'     --schedule "cron(0 6 * * ? *)"     --schema-change-policy '{"UpdateBehavior":"UPDATE_IN_DATABASE","DeleteBehavior":"LOG"}'
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
aws glue create-job     --name sales-etl-job     --role arn:aws:iam::123456789012:role/GlueServiceRole     --command '{"Name":"glueetl","ScriptLocation":"s3://my-glue-scripts/etl_script.py","PythonVersion":"3"}'     --default-arguments '{"--job-bookmark-option":"job-bookmark-enable","--enable-metrics":"true"}'     --max-retries 1     --timeout 60     --glue-version "4.0"     --number-of-workers 10     --worker-type "G.1X"
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
result = orders.toDF()     .filter(col("status") == "COMPLETED")     .groupBy("customer_id")     .agg(sum("amount").alias("total_spent"))

# Write to S3 in Parquet
result.write.mode("overwrite")     .parquet("s3://my-sales-data/processed/customer_totals/")

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
