# S3 CLI Commands Reference

Comprehensive guide to all S3 CLI commands for exam preparation.

## `aws s3` Commands (High-Level)

```bash
# List buckets
aws s3 ls

# List objects in a bucket
aws s3 ls s3://my-bucket/
aws s3 ls s3://my-bucket/path/ --recursive
aws s3 ls s3://my-bucket/ --human-readable --summarize

# Create bucket
aws s3 mb s3://my-unique-bucket

# Remove bucket
aws s3 rb s3://my-bucket
aws s3 rb s3://my-bucket --force  # Remove non-empty bucket

# Copy objects
aws s3 cp file.txt s3://my-bucket/
aws s3 cp s3://my-bucket/file.txt ./
aws s3 cp s3://source-bucket/file.txt s3://dest-bucket/
aws s3 cp . s3://my-bucket/ --recursive --exclude "*.tmp" --include "*.txt"

# Move objects
aws s3 mv file.txt s3://my-bucket/
aws s3 mv s3://my-bucket/file.txt s3://my-bucket/new-location/

# Remove objects
aws s3 rm s3://my-bucket/file.txt
aws s3 rm s3://my-bucket/path/ --recursive

# Sync directories
aws s3 sync ./local-dir s3://my-bucket/remote-dir
aws s3 sync s3://my-bucket/remote-dir ./local-dir
aws s3 sync . s3://my-bucket/ --delete  # Remove files not in source

# Website
aws s3 website s3://my-bucket --index-document index.html --error-document error.html

# Presign URL
aws s3 presign s3://my-bucket/file.txt --expires-in 3600
```

## `aws s3api` Commands (API-Level)

```bash
# Create bucket
aws s3api create-bucket --bucket my-bucket --region us-east-1
aws s3api create-bucket --bucket my-bucket --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# Put object
aws s3api put-object --bucket my-bucket --key hello.txt --body hello.txt
aws s3api put-object --bucket my-bucket --key hello.txt --body hello.txt \
  --server-side-encryption AES256 --storage-class STANDARD_IA

# Get object
aws s3api get-object --bucket my-bucket --key hello.txt output.txt
aws s3api get-object --bucket my-bucket --key hello.txt output.txt \
  --version-id <version-id>

# List objects
aws s3api list-objects --bucket my-bucket
aws s3api list-objects-v2 --bucket my-bucket --prefix "logs/"
aws s3api list-objects-v2 --bucket my-bucket --max-items 100

# Delete object
aws s3api delete-object --bucket my-bucket --key hello.txt
aws s3api delete-object --bucket my-bucket --key hello.txt --version-id <id>

# Head object (get metadata without downloading)
aws s3api head-object --bucket my-bucket --key file.txt

# Multipart upload
aws s3api create-multipart-upload --bucket my-bucket --key large.iso
aws s3api upload-part --bucket my-bucket --key large.iso --part-number 1 \
  --body part-1 --upload-id <id>
aws s3api complete-multipart-upload --bucket my-bucket --key large.iso \
  --upload-id <id> --multipart-upload file://parts.json
aws s3api abort-multipart-upload --bucket my-bucket --key large.iso --upload-id <id>

# Versioning
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled
aws s3api get-bucket-versioning --bucket my-bucket
aws s3api list-object-versions --bucket my-bucket

# Encryption
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
  }'
aws s3api get-bucket-encryption --bucket my-bucket

# Lifecycle
aws s3api put-bucket-lifecycle-configuration --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket

# Policy
aws s3api put-bucket-policy --bucket my-bucket --policy file://policy.json
aws s3api get-bucket-policy --bucket my-bucket
aws s3api delete-bucket-policy --bucket my-bucket

# Website
aws s3api put-bucket-website --bucket my-bucket \
  --website-configuration file://website.json
aws s3api get-bucket-website --bucket my-bucket

# Tagging
aws s3api put-bucket-tagging --bucket my-bucket \
  --tagging '{"TagSet": [{"Key": "env", "Value": "prod"}]}'
aws s3api get-bucket-tagging --bucket my-bucket

# Acceleration
aws s3api put-bucket-accelerate-configuration --bucket my-bucket \
  --accelerate-configuration Status=Enabled
aws s3api get-bucket-accelerate-configuration --bucket my-bucket

# Replication
aws s3api put-bucket-replication --bucket my-bucket \
  --replication-configuration file://replication.json
aws s3api get-bucket-replication --bucket my-bucket

# Notifications
aws s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration file://notification.json
aws s3api get-bucket-notification-configuration --bucket my-bucket

# Select
aws s3api select-object-content --bucket my-bucket --key data.csv \
  --expression "SELECT * FROM S3Object s WHERE s.year = '2024'" \
  --expression-type SQL \
  --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}}' \
  --output-serialization '{"CSV": {}}' output.csv

# ACL
aws s3api get-bucket-acl --bucket my-bucket
aws s3api put-object-acl --bucket my-bucket --key file.txt --acl public-read

# CORS
aws s3api put-bucket-cors --bucket my-bucket \
  --cors-configuration file://cors.json
aws s3api get-bucket-cors --bucket my-bucket

# Location
aws s3api get-bucket-location --bucket my-bucket

# Logging
aws s3api put-bucket-logging --bucket my-bucket \
  --bucket-logging-status file://logging.json
aws s3api get-bucket-logging --bucket my-bucket
```

## Output Formatting

```bash
# JSON (default)
aws s3api list-objects-v2 --bucket my-bucket

# Table format
aws s3api list-objects-v2 --bucket my-bucket --output table

# Text format
aws s3api list-objects-v2 --bucket my-bucket --output text

# JMESPath queries
aws s3api list-objects-v2 --bucket my-bucket --query "Contents[].Key"
aws s3api list-objects-v2 --bucket my-bucket \
  --query "Contents[?Size > '1000'].[Key,Size]"
aws s3 ls --query "Buckets[].Name" --output table
```

## Exam Quick Reference
- ✅ `aws s3` = high-level (cp, mv, sync, ls, rm, mb, rb, presign, website)
- ✅ `aws s3api` = API-level (fine-grained control)
- ✅ `--query` with JMESPath for filtering output
- ✅ `--output` options: json, text, table, yaml
- ✅ `--recursive` for directories
- ✅ `--exclude` and `--include` for filtering (used with --recursive)
- ✅ `--dryrun` to preview changes without executing