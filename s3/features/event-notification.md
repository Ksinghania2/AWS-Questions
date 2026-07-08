# S3 Event Notifications

S3 Event Notifications trigger workflows when objects are created, deleted, or modified in your bucket.

## Supported Destinations

| Destination | Use Case |
|---|---|
| **Lambda** | Process files on upload (image resizing, data transformation) |
| **SQS** | Queue messages for decoupled processing |
| **SNS** | Send email/SMS/push notifications |
| **EventBridge** | Advanced event routing, filtering, and archiving |

## Event Types

| Event | Trigger |
|---|---|
| `s3:ObjectCreated:*` | Any object creation (PUT, POST, COPY, Multipart) |
| `s3:ObjectCreated:Put` | PUT upload |
| `s3:ObjectCreated:Post` | POST upload |
| `s3:ObjectCreated:Copy` | COPY operation |
| `s3:ObjectCreated:CompleteMultipartUpload` | Multipart upload completion |
| `s3:ObjectRemoved:*` | Any object deletion |
| `s3:ObjectRemoved:Delete` | DELETE operation |
| `s3:ObjectRemoved:DeleteMarkerCreated` | Delete marker (versioning enabled) |
| `s3:ObjectRestore:*` | Glacier restore events |
| `s3:ObjectTagging:*` | Tagging events |
| `s3:LifecycleExpiration:*` | Lifecycle expiration events |

## CLI Commands

```bash
# Configure Lambda notification
aws s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [{
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:process-file",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {"Name": "prefix", "Value": "uploads/"},
            {"Name": "suffix", "Value": ".jpg"}
          ]
        }
      }
    }]
  }'

# Configure SQS notification
aws s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration '{
    "QueueConfigurations": [{
      "QueueArn": "arn:aws:sqs:us-east-1:123456789012:my-queue",
      "Events": ["s3:ObjectCreated:*"]
    }]
  }'

# Configure SNS notification
aws s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration '{
    "TopicConfigurations": [{
      "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
      "Events": ["s3:ObjectRemoved:*"]
    }]
  }'

# Get current notification configuration
aws s3api get-bucket-notification-configuration --bucket my-bucket

# Delete notification configuration
aws s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration '{}'
```

## Python (boto3) Examples

```python
import boto3
import json

s3 = boto3.client('s3')
bucket = 'my-bucket'

# Configure Lambda notification with filter
def configure_lambda_notification(bucket, lambda_arn, prefix='', suffix=''):
    """Configure S3 to trigger Lambda on object creation"""
    config = {
        'LambdaFunctionConfigurations': [{
            'LambdaFunctionArn': lambda_arn,
            'Events': ['s3:ObjectCreated:*']
        }]
    }
    
    # Add filter if specified
    if prefix or suffix:
        rules = []
        if prefix:
            rules.append({'Name': 'prefix', 'Value': prefix})
        if suffix:
            rules.append({'Name': 'suffix', 'Value': suffix})
        config['LambdaFunctionConfigurations'][0]['Filter'] = {
            'Key': {'FilterRules': rules}
        }
    
    s3.put_bucket_notification_configuration(
        Bucket=bucket,
        NotificationConfiguration=config
    )
    print(f"Lambda notification configured for {bucket}")

configure_lambda_notification(
    bucket,
    'arn:aws:lambda:us-east-1:123456789012:function:process-image',
    prefix='uploads/',
    suffix='.jpg'
)

# Configure multiple destinations
def configure_multi_destination(bucket, lambda_arn, queue_arn, topic_arn):
    """Configure multiple notification destinations"""
    config = {
        'LambdaFunctionConfigurations': [{
            'LambdaFunctionArn': lambda_arn,
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {'FilterRules': [
                    {'Name': 'prefix', 'Value': 'images/'}
                ]}
            }
        }],
        'QueueConfigurations': [{
            'QueueArn': queue_arn,
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {'FilterRules': [
                    {'Name': 'prefix', 'Value': 'logs/'}
                ]}
            }
        }],
        'TopicConfigurations': [{
            'TopicArn': topic_arn,
            'Events': ['s3:ObjectRemoved:*']
        }]
    }
    
    s3.put_bucket_notification_configuration(
        Bucket=bucket,
        NotificationConfiguration=config
    )
    print("Multi-destination notification configured")

# Get current configuration
def get_notification_summary(bucket):
    """Get a summary of all notification configurations"""
    response = s3.get_bucket_notification_configuration(Bucket=bucket)
    
    print("Lambda configurations:")
    for config in response.get('LambdaFunctionConfigurations', []):
        print(f"  Function: {config['LambdaFunctionArn']}")
        print(f"  Events: {config['Events']}")
    
    print("SQS configurations:")
    for config in response.get('QueueConfigurations', []):
        print(f"  Queue: {config['QueueArn']}")
        print(f"  Events: {config['Events']}")
    
    print("SNS configurations:")
    for config in response.get('TopicConfigurations', []):
        print(f"  Topic: {config['TopicArn']}")
        print(f"  Events: {config['Events']}")

get_notification_summary(bucket)
```

## Event Notification Flow

```
1. Object created/deleted in S3
2. S3 evaluates notification configuration
3. S3 sends event to destination (Lambda/SQS/SNS)
4. Destination processes the event
5. (Optional) Destination triggers further actions
```

## Exam Tips

### 1. Event Filtering
You can filter events by **prefix** and **suffix** to only trigger on specific objects (e.g., only `.jpg` files in `uploads/`).

### 2. EventBridge Integration
For advanced event routing, use Amazon EventBridge instead of direct S3 notifications. EventBridge provides:
- More destinations (Step Functions, Kinesis, etc.)
- Advanced filtering and transformation
- Event archiving and replay

### 3. Permissions Required
The S3 bucket must have permissions to invoke the destination:
- **Lambda**: Add resource-based policy to Lambda
- **SQS**: Add SQS policy allowing S3 to send messages
- **SNS**: Add SNS policy allowing S3 to publish

### 4. Common Exam Question
**Q:** A company wants to automatically resize images uploaded to S3. What should they use?
**A:** S3 Event Notification → Lambda → Process image → Save resized version back to S3.

## Exam Quick Reference
- ✅ **Destinations**: Lambda, SQS, SNS, EventBridge
- ✅ **Event types**: ObjectCreated, ObjectRemoved, ObjectRestore, etc.
- ✅ **Filter by**: Prefix and suffix
- ✅ **Permissions**: Must grant S3 access to invoke the destination
- ✅ **EventBridge**: More advanced routing and filtering
- ✅ **Real-time**: Events are sent within seconds of the operation
- ✅ **No additional cost** for S3 event notifications