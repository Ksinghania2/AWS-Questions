# Amazon Redshift - Petabyte-Scale Data Warehouse

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
aws redshift create-cluster     --cluster-identifier my-warehouse     --node-type ra3.xlplus     --number-of-nodes 2     --master-username admin     --master-user-password MyS3cur3P@ss!     --vpc-security-group-ids sg-12345678     --cluster-subnet-group-name my-redshift-subnet-group     --publicly-accessible     --encrypted     --kms-key-id alias/redshift-key     --automated-snapshot-retention-period 7

# Wait for cluster to become available
aws redshift wait cluster-available --cluster-identifier my-warehouse
```

### Step 2: Configure Database
```bash
# Get cluster endpoint
aws redshift describe-clusters     --cluster-identifier my-warehouse     --query 'Clusters[0].Endpoint'     --output json

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
aws redshift create-cluster-snapshot     --snapshot-identifier my-warehouse-pre-upgrade     --cluster-identifier my-warehouse

# Restore from snapshot
aws redshift restore-from-cluster-snapshot     --cluster-identifier my-warehouse-restored     --snapshot-identifier my-warehouse-pre-upgrade
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
