# S3 Select

S3 Select enables **server-side filtering** of data using SQL expressions, reducing the amount of data transferred to the client.

## Benefits
- **Less data transferred** → lower cost, faster results
- **Server-side processing** — no need to download entire objects
- **Supports**: CSV, JSON, Parquet files (including compressed: GZIP, BZIP2)

```bash
aws s3api select-object-content \
  --bucket my-bucket --key data.csv \
  --expression "SELECT s.name, s.age FROM S3Object s WHERE s.age > 21" \
  --expression-type SQL \
  --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}, "CompressionType": "NONE"}' \
  --output-serialization '{"CSV": {}}' output.csv
```

## Exam Quick Reference
- ✅ **Filter data server-side** using SQL
- ✅ Supports **CSV, JSON, Parquet**
- ✅ Supports **GZIP, BZIP2** compression
- ✅ **Lower cost** (less data processed and transferred)
- ✅ **Faster** for extracting subsets of large files
- ✅ **Glacier Select** — same feature for Glacier objects