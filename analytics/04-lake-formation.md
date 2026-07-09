# AWS Lake Formation - Data Lake Management

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
aws lakeformation register-resource     --resource-arn arn:aws:s3:::my-data-lake-bucket     --role-arn arn:aws:iam::123456789012:role/LakeFormationRole     --use-service-linked-role
```

### Step 2: Grant Table Permissions
```bash
# Grant SELECT on specific table to a user
aws lakeformation grant-permissions     --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:user/data-analyst     --resource '{"Table":{"DatabaseName":"sales","Name":"orders"}}'     --permissions "SELECT" "DESCRIBE"
```

### Step 3: Grant Column-Level Permissions
```bash
# Grant access to specific columns only
aws lakeformation grant-permissions     --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:user/junior-analyst     --resource '{"TableWithColumns":{"DatabaseName":"hr","Name":"employees","ColumnNames":["name","department","title"]}}'     --permissions "SELECT"
```

### Step 4: Grant Row-Level Permissions (Data Filters)
```bash
# Create data filter for row-level security
aws lakeformation create-data-cells-filter     --name "us-sales-only"     --table-data '{"DatabaseName":"sales","Name":"orders","RowFilterExpression":"region = 'us'"}'     --table-catalog-id 123456789012

# Grant with filter
aws lakeformation grant-permissions     --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:user/regional-manager     --resource '{"DataCellsFilter":{"TableCatalogId":"123456789012","DatabaseName":"sales","Name":"orders","TableName":"orders"}}'     --permissions "SELECT"
```

### Step 5: Use Blueprint for Ingestion
```bash
# Create workflow from blueprint
aws lakeformation create-workflow     --name "daily-sales-ingest"     --description "Daily sales data ingestion"     --blueprint-name "S3_IMPORT"     --role-arn arn:aws:iam::123456789012:role/LakeFormationWorkflowRole
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
