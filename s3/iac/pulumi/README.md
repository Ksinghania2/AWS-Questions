# Pulumi Example

Pulumi lets you create AWS resources using Python code.

## Simple example
```python
import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket('demo-bucket')
pulumi.export('bucket_name', bucket.id)
```

## Basic steps
```bash
pip install -r requirements.txt
pulumi up
```

This is just a basic start.
