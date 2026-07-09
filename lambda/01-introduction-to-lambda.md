# AWS Lambda

Lambda is a serverless compute service that runs code in response to events.

## Key Features
- **Max execution time**: 15 minutes (900 seconds)
- **Memory**: 128MB to 10,240MB (10GB)
- **Ephemeral storage**: 512MB to 10GB (/tmp)
- **Concurrency**: 1000 (soft limit, can increase)
- **Languages**: Node.js, Python, Java, Go, Ruby, .NET, custom runtimes

## Invocation Types
| Type | Description |
|------|-------------|
| **Synchronous** | Invoke, wait for response (API Gateway, Cognito) |
| **Asynchronous** | Event queued, retried (S3, SNS, EventBridge) |
| **Event Source Mapping** | Poll from source (SQS, DynamoDB Streams, Kinesis) |

## CLI
```bash
# Create function
aws lambda create-function     --function-name my-function     --runtime python3.12     --role arn:aws:iam::xxx:role/lambda-basic-role     --handler lambda_function.handler     --zip-file fileb://function.zip

# Invoke synchronously
aws lambda invoke     --function-name my-function     --payload '{"key":"value"}'     output.json

# Invoke asynchronously
aws lambda invoke     --function-name my-function     --invocation-type Event     --payload '{"key":"value"}'     output.json

# Update function code
aws lambda update-function-code     --function-name my-function     --zip-file fileb://function.zip

# Update function configuration
aws lambda update-function-configuration     --function-name my-function     --memory-size 1024     --timeout 30     --environment Variables={DB_HOST=mydb.example.com}

# Add S3 trigger
aws lambda create-event-source-mapping     --function-name my-function     --event-source-arn arn:aws:s3:::my-bucket     --events s3:ObjectCreated:*

# Add SQS trigger
aws lambda create-event-source-mapping     --function-name my-function     --event-source-arn arn:aws:sqs:us-east-1:xxx:my-queue     --batch-size 10
```

## Concurrency & DLQ
| Feature | Description |
|---------|-------------|
| **Reserved Concurrency** | Guaranteed concurrency for function |
| **Provisioned Concurrency** | Pre-initialized to eliminate cold starts |
| **DLQ** | Dead Letter Queue for failed async invocations |

```bash
# Set reserved concurrency
aws lambda put-function-concurrency     --function-name my-function     --reserved-concurrent-executions 10

# Configure DLQ for async invocations
aws lambda update-function-event-invoke-config     --function-name my-function     --destination-config OnFailure={Destination=arn:aws:sqs:us-east-1:xxx:dlq-function}
```

## Q&A
**Q1: What is the max execution time for Lambda?** A: 15 minutes (900 seconds).
**Q2: What is the max memory for Lambda?** A: 10GB (10,240MB).
**Q3: What are the three invocation types?** A: Synchronous, Asynchronous, Event Source Mapping.
**Q4: What is Provisioned Concurrency?** A: Pre-warmed instances to eliminate cold starts.
**Q5: What is a DLQ for Lambda?** A: Destination for failed async events (SQS or SNS).
**Q6: What is the max /tmp storage?** A: 10GB (default 512MB).
**Q7: What is reserved concurrency?** A: Guaranteed concurrency limit for a function.
**Q8: What is Lambda@Edge?** A: Lambda functions at CloudFront edge locations.
