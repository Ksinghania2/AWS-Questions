a the import os

BASE = "/Users/kshitij/Desktop/AWS-Solutions-Architect"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content.strip() + "\n")
    print(f"OK: {path}")

# =====================================================================
# ELASTIC BEANSTALK (Major - 15 Q&A)
# =====================================================================
w("app-platform/01-elastic-beanstalk.md", """# AWS Elastic Beanstalk - PaaS for Web Applications

## KEY FEATURES
- PaaS: Upload code, Elastic Beanstalk handles deployment, scaling, load balancing, monitoring
- Supports: Java, .NET, Node.js, PHP, Python, Ruby, Go, Docker
- Environment types: Web Server (HTTP via ELB) and Worker (background via SQS)

## DEPLOYMENT STRATEGIES

| Strategy | Downtime | Capacity | Description |
|----------|----------|----------|-------------|
| All at Once | Yes | Reduced | Deploy to all instances at once |
| Rolling | No | Reduced per batch | Deploy in batches, old instances remain |
| Rolling with Batch | No | Full (new batch added) | Same as rolling but adds extra capacity |
| Immutable | No | Full | New ASG, swap when healthy |
| Blue/Green | No | Full | Separate environment, swap CNAME |

## CLI EXAMPLES

```bash
# Create application
aws elasticbeanstalk create-application --application-name my-app

# Create environment (Web Server)
aws elasticbeanstalk create-environment \
    --application-name my-app \
    --environment-name my-app-prod \
    --solution-stack-name "64bit Amazon Linux 2 v5.8.0 running Node.js 18" \
    --option-settings Namespace=aws:autoscaling:launchconfiguration,OptionName=InstanceType,Value=t3.small \
    --option-settings Namespace=aws:elasticbeanstalk:environment,OptionName=EnvironmentType,Value=LoadBalanced

# Deploy new version
aws elasticbeanstalk update-environment \
    --environment-name my-app-prod \
    --version-label v2

# Worker environment
aws elasticbeanstalk create-environment \
    --application-name my-app \
    --environment-name my-app-worker \
    --solution-stack-name "64bit Amazon Linux 2 v5.8.0 running Node.js 18" \
    --tier Name=Worker,Type=SQS/HTTP

# Blue/Green deployment (swap URLs)
aws elasticbeanstalk swap-environment-cnames \
    --source-environment-name my-app-blue \
    --destination-environment-name my-app-green

# List applications
aws elasticbeanstalk describe-applications

# List environments
aws elasticbeanstalk describe-environments --application-name my-app

# Terminate environment
aws elasticbeanstalk terminate-environment --environment-name my-app-prod
```

## EXAM TIPS
- Immutable deployment is the safest (new ASG, zero downtime)
- Blue/Green requires manual DNS swap but provides instant rollback
- Worker environment processes SQS messages
- Custom platform: Create your own platform if needed
- Use .ebextensions for advanced config

## 15 PRACTICE QUESTIONS

Q1: What is Elastic Beanstalk?
A: Platform as a Service (PaaS) for deploying web applications.

Q2: What deployment strategy has zero downtime?
A: Rolling, Rolling with Batch, Immutable, and Blue/Green.

Q3: What is the difference between Web Server and Worker environments?
A: Web Server serves HTTP traffic via ELB; Worker processes background tasks via SQS.

Q4: What is Blue/Green deployment?
A: Deploy to a separate environment, then swap CNAME/URL to switch traffic.

Q5: What is an immutable deployment?
A: Create a new ASG with new instances; if health check passes, swap to new ASG.

Q6: What is the All at Once strategy?
A: Deploy to all instances simultaneously (fastest, but causes downtime).

Q7: Can Elastic Beanstalk auto-scale?
A: Yes, it integrates with Auto Scaling Groups.

Q8: What is .ebextensions?
A: Configuration files for customizing environment (install packages, create files).

Q9: What languages does Elastic Beanstalk support?
A: Java, .NET, Node.js, PHP, Python, Ruby, Go, Docker.

Q10: What happens during a Rolling deployment?
A: Instances are updated in batches; old instances remain during update.

Q11: Can you run Elastic Beanstalk without a load balancer?
A: Yes, single-instance environments don't use an ELB.

Q12: What is the difference between Elastic Beanstalk and CloudFormation?
A: Beanstalk is a PaaS (abstracts infrastructure); CloudFormation is IaC (full control).

Q13: How do you pass environment variables to Elastic Beanstalk?
A: Via AWS Console, CLI, or .ebextensions configuration files.

Q14: What is the max size for a source bundle?
A: 512 MB.

Q15: Can Elastic Beanstalk deploy from CodePipeline?
A: Yes, it's an integration target for CodePipeline.
""")

# =====================================================================
# SNS (Major - 15 Q&A)
# =====================================================================
w("messaging/01-sns.md", """# Amazon SNS - Simple Notification Service

## KEY FEATURES
- Pub/Sub messaging service
- Publisher sends messages to a Topic
- Subscribers receive messages via protocols (SQS, Lambda, HTTP, Email, SMS, Push)
- Fan-out: One topic can send to multiple subscribers simultaneously
- Message filtering: Filter policies for subscribers
- FIFO Topics: Ordering + deduplication (300 msgs/s)

## ARCHITECTURE

```
Publisher (Application, AWS Service, SDK)
    |
    v
SNS Topic
    |
    +--------+--------+---------+---------+
    v        v        v         v         v
  SQS     Lambda   HTTP     Email     Mobile
  Queue   Function Endpoint           Push
```

## CLI EXAMPLES

```bash
# Create Standard Topic
aws sns create-topic --name order-topic

# Create FIFO Topic
aws sns create-topic --name order-topic.fifo \
    --attributes FifoTopic=true,ContentBasedDeduplication=true

# Subscribe SQS to Topic
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:123456789012:order-topic \
    --protocol sqs \
    --notification-endpoint arn:aws:sqs:us-east-1:123456789012:order-queue

# Subscribe Lambda to Topic
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:123456789012:order-topic \
    --protocol lambda \
    --notification-endpoint arn:aws:lambda:us-east-1:123456789012:function:process-order

# Subscribe Email
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:123456789012:order-topic \
    --protocol email \
    --notification-endpoint admin@example.com

# Publish Message
aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:123456789012:order-topic \
    --message '{"order_id":123,"status":"shipped"}' \
    --subject "Order Update"

# Set Filter Policy (only receive specific messages)
aws sns set-subscription-attributes \
    --subscription-arn arn:aws:sns:us-east-1:123456789012:order-topic:sub-xxx \
    --attribute-name FilterPolicy \
    --attribute-value '{"event_type":["order_placed","payment_received"]}'

# Publish with Message Attributes
aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:123456789012:order-topic \
    --message "Order processed" \
    --message-attributes '{"event_type":{"DataType":"String","StringValue":"order_placed"}}'

# Create SMS Topic
aws sns create-topic --name sms-alerts
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:123456789012:sms-alerts \
    --protocol sms \
    --notification-endpoint "+1234567890"
```

## EXAM TIPS
- Use SNS + SQS fan-out for decoupled microservices
- SNS + SQS + Lambda = Common serverless pattern
- Message filtering reduces unnecessary processing
- FIFO topics + FIFO queues = Exactly-once processing
- SMS: Manage costs with monthly spending limits

## 15 PRACTICE QUESTIONS

Q1: What is Amazon SNS?
A: A fully managed pub/sub messaging service.

Q2: What is the fan-out pattern?
A: A single SNS topic sends messages to multiple subscribers (SQS, Lambda, HTTP) simultaneously.

Q3: What protocols does SNS support?
A: SQS, Lambda, HTTP/HTTPS, Email (JSON/text), SMS, Mobile Push.

Q4: What is a filter policy?
A: A policy on subscriptions that filters messages, so subscribers only receive relevant messages.

Q5: What is the difference between Standard and FIFO topics?
A: Standard: high throughput, best-effort ordering. FIFO: strict ordering, deduplication, 300 msg/s.

Q6: How does SNS deliver to Lambda?
A: SNS invokes the Lambda function asynchronously with the message payload.

Q7: Can SNS send messages to other AWS accounts?
A: Yes, by configuring topic policies for cross-account access.

Q8: What is message durability in SNS?
A: SNS stores messages across multiple AZs. For Lambda/SQS subscribers, retries are built-in.

Q9: How do you filter messages in SNS?
A: Using FilterPolicy attribute on subscriptions with JSON policy matching message attributes.

Q10: What is the max message size in SNS?
A: 256KB.

Q11: Can SNS send SMS internationally?
A: Yes, but you must opt-in and set spending limits.

Q12: What is raw message delivery?
A: Sends the message without SNS metadata (useful for SQS subscribers).

Q13: How does SNS handle delivery failures?
A: Retries based on policy; can send to DLQ (SQS) after exhaustion.

Q14: What is the difference between SNS and SQS?
A: SNS is pub/sub (push); SQS is queue (pull). SNS pushes to subscribers; SQS requires consumers to poll.

Q15: Can SNS be used with CloudWatch Alarms?
A: Yes, CloudWatch alarms can send notifications to SNS topics.
""")

# =====================================================================
# SQS (Major - 15 Q&A)
# =====================================================================
w("messaging/02-sqs.md", """# Amazon SQS - Simple Queue Service

## KEY FEATURES
- Fully managed message queuing for decoupling applications
- Standard Queue: Unlimited throughput, at-least-once, best-effort ordering
- FIFO Queue: 3000 msg/s (300 with batching), exactly-once, strict ordering

## QUEUE TYPES COMPARISON

| Feature | Standard | FIFO |
|---------|----------|------|
| Throughput | Unlimited | 3000 msg/s (or 300 batch) |
| Ordering | Best-effort | Strict First-In-First-Out |
| Duplicates | Possible (at-least-once) | Exactly-once |
| Message Group ID | Not required | Required for ordering |

## ARCHITECTURE

```
Producer (EC2, Lambda, App)
    |
    v
SQS Queue
    |
    v
Consumer (EC2, Lambda, App)
    - Polls messages
    - Processes
    - Deletes after processing
```

## CLI EXAMPLES

```bash
# Create Standard Queue
aws sqs create-queue --queue-name order-queue

# Create FIFO Queue
aws sqs create-queue --queue-name order-queue.fifo \
    --attributes FifoQueue=true,ContentBasedDeduplication=true

# Send Message
aws sqs send-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue \
    --message-body '{"order_id":123,"customer_id":456}' \
    --delay-seconds 0

# Send FIFO Message (requires MessageGroupId)
aws sqs send-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue.fifo \
    --message-body '{"order_id":123}' \
    --message-group-id "customer_456" \
    --message-deduplication-id "unique-123"

# Receive Messages (Long Polling - recommended)
aws sqs receive-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue \
    --max-number-of-messages 10 \
    --visibility-timeout 30 \
    --wait-time-seconds 20

# Delete Message (after processing)
aws sqs delete-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue \
    --receipt-handle RECEIPT_HANDLE_HERE

# Configure Dead Letter Queue
aws sqs set-queue-attributes \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue \
    --attributes '{"RedrivePolicy":"{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:123456789012:order-dlq\",\"maxReceiveCount\":\"5\"}"}'

# Get Queue Attributes
aws sqs get-queue-attributes \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue \
    --attribute-names All

# Purge Queue
aws sqs purge-queue \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/order-queue
```

## CONCEPTS

| Concept | Description |
|---------|-------------|
| Visibility Timeout | Period message is hidden after being read (30s default, max 12h) |
| Long Polling | Waits up to 20s for messages (reduces empty responses, saves cost) |
| Short Polling | Returns immediately (may return empty) |
| Dead Letter Queue | Queue for messages that failed processing (maxReceiveCount) |
| Delay Queue | Delays messages up to 15 minutes |
| Message Retention | 1 minute to 14 days (default 4 days) |

## 15 PRACTICE QUESTIONS

Q1: What is Amazon SQS?
A: A fully managed message queuing service for decoupling applications.

Q2: What is the difference between Standard and FIFO queues?
A: Standard: unlimited throughput, at-least-once, no ordering. FIFO: 3000/s, exactly-once, strict ordering.

Q3: What is a Dead Letter Queue (DLQ)?
A: A queue that stores messages that couldn't be processed after maxReceiveCount attempts.

Q4: What is Visibility Timeout?
A: The time a message is hidden from other consumers after being received (default 30s, max 12h).

Q5: What is Long Polling?
A: The consumer waits up to 20s for messages to arrive, reducing empty responses and costs.

Q6: What is the max message size in SQS?
A: 256KB. For larger messages, use S3 Extended Client Library.

Q7: What is message retention period?
A: The time a message stays in the queue if not consumed (1 min to 14 days, default 4 days).

Q8: What is a delay queue?
A: A queue that delays message delivery by up to 15 minutes.

Q9: How do you ensure FIFO ordering?
A: Use FIFO queue with MessageGroupId. Messages with same GroupId are processed in order.

Q10: What happens when maxReceiveCount is exceeded?
A: The message is sent to the Dead Letter Queue.

Q11: Can SQS guarantee exactly-once delivery?
A: Only with FIFO queues. Standard queues offer at-least-once.

Q12: What is the default visibility timeout?
A: 30 seconds.

Q13: Can you change queue type after creation?
A: No, you must delete and recreate with the different type.

Q14: How does SQS integrate with Lambda?
A: Lambda polls the queue (event source mapping) and invokes the function.

Q15: What is the max number of messages per receive?
A: 10 messages per receive_message call.
""")

# =====================================================================
# KMS (Major - 15 Q&A)
# =====================================================================
w("security/01-kms.md", """# AWS KMS - Key Management Service

## KEY FEATURES
- Create and manage encryption keys
- FIPS 140-2 Level 2 (Level 3 with CloudHSM)
- Integrated with most AWS services
- Envelope encryption: Encrypt data with data key, encrypt data key with KMS key
- Automatic key rotation (yearly for Customer Managed keys)

## KEY TYPES

| Key Type | Control | Rotation | Scope |
|----------|---------|----------|-------|
| AWS Managed | AWS | Automatic | Per service |
| Customer Managed | You | Optional (yearly) | Full control |
| Custom Key Store (CloudHSM) | You | Manual | FIPS 140-2 Level 3 |

## ARCHITECTURE (Envelope Encryption)

```
Plaintext (Large file)
    |
    +-- KMS GenerateDataKey -> Data Key (DEK)
    |       |
    |       +-- Encrypt Data Key with KMS Key -> Encrypted DEK
    |       +-- Plaintext DEK (in memory)
    |
    +-- Encrypt Plaintext with Data Key -> Ciphertext
    |
    Store: Ciphertext + Encrypted DEK
```

## CLI EXAMPLES

```bash
# Create Customer Managed Key
aws kms create-key \
    --description "Production encryption key" \
    --key-usage ENCRYPT_DECRYPT \
    --origin AWS_KMS \
    --tags TagKey=Environment,TagValue=Production

# Create Alias
aws kms create-alias \
    --alias-name alias/prod-key \
    --target-key-id 1234abcd-12ab-34cd-56ef-1234567890ab

# Encrypt (max 1MB)
aws kms encrypt \
    --key-id alias/prod-key \
    --plaintext fileb://secret.txt \
    --output text \
    --query CiphertextBlob > encrypted.enc

# Decrypt
aws kms decrypt \
    --ciphertext-blob fileb://encrypted.enc \
    --output text \
    --query Plaintext | base64 --decode > decrypted.txt

# Generate Data Key (for envelope encryption)
aws kms generate-data-key \
    --key-id alias/prod-key \
    --key-spec AES_256 \
    --output json

# Enable Automatic Rotation (yearly)
aws kms enable-key-rotation --key-id 1234abcd-12ab-34cd-56ef-1234567890ab

# Disable Key
aws kms disable-key --key-id 1234abcd-12ab-34cd-56ef-1234567890ab

# Schedule Key Deletion (7-30 day waiting period)
aws kms schedule-key-deletion \
    --key-id 1234abcd-12ab-34cd-56ef-1234567890ab \
    --pending-window-in-days 7

# List Keys
aws kms list-keys

# Get Key Policy
aws kms get-key-policy \
    --key-id 1234abcd-12ab-34cd-56ef-1234567890ab \
    --policy-name default
```

## EXAM TIPS
- KMS can only encrypt up to 1MB directly; use GenerateDataKey for larger data
- Key Policy + IAM Policy both required (Key Policy must trust IAM entity)
- Key deletion has 7-30 day waiting period (enforced by AWS)
- Rotation keeps same Key ID; old encrypts remain decryptable
- Cross-account: Key Policy must grant access to other account

## 15 PRACTICE QUESTIONS

Q1: What is AWS KMS?
A: Key Management Service for creating and managing encryption keys.

Q2: What is the difference between AWS Managed and Customer Managed keys?
A: AWS Managed: AWS controls rotation, policy. Customer Managed: You control rotation, policy, deletion.

Q3: What is envelope encryption?
A: Encrypting data with a data key, then encrypting that data key with a KMS key.

Q4: What is the max plaintext size KMS can encrypt directly?
A: 1MB. Use GenerateDataKey for larger data.

Q5: How often does KMS rotate Customer Managed keys?
A: Yearly (if rotation is enabled).

Q6: Can you delete a KMS key immediately?
A: No, there's a mandatory 7-30 day waiting period.

Q7: What is a Custom Key Store?
A: KMS key backed by CloudHSM for FIPS 140-2 Level 3 compliance.

Q8: What is the difference between IAM policies and Key Policies?
A: Key Policies are resource-based policies attached to the KMS key; IAM policies are identity-based. Both are needed.

Q9: Can KMS keys be used across regions?
A: No, KMS keys are regional. Must copy to other regions.

Q10: What happens to encrypted data if the KMS key is deleted?
A: The data becomes permanently undecryptable.

Q11: What is a Grant in KMS?
A: A mechanism to delegate temporary access to a KMS key without modifying the Key Policy.

Q12: Can you rotate keys manually?
A: Yes, by creating a new key and updating aliases.

Q13: What is the purpose of a KMS alias?
A: Provides a friendly name for a key (supports key rotation without updating applications).

Q14: How does KMS integrate with S3?
A: SSE-KMS uses KMS keys for S3 server-side encryption.

Q15: What is the cryptographic boundary of KMS?
A: FIPS 140-2 Level 2 (Level 3 with Custom Key Store/CloudHSM).
""")

# =====================================================================
# CLOUDWATCH (Major - 15 Q&A)
# =====================================================================
w("monitoring/01-cloudwatch.md", """# Amazon CloudWatch - Monitoring and Observability

## KEY FEATURES
- Metrics: Collect and track performance data
- Logs: Centralized log storage and analysis
- Alarms: Threshold-based alerts and actions
- Dashboards: Custom visualization
- Unified Agent: System-level metrics (RAM, disk, swap)

## METRICS TYPES

| Type | Source | Examples |
|------|--------|----------|
| Host-Level (Free) | EC2 hypervisor | CPU, Network, Disk, Status Checks |
| Custom Metrics | CloudWatch Agent, API | Memory, Disk space, Application metrics |
| AWS Service Metrics | AWS services | S3 bucket size, Lambda invocations, RDS connections |

## ARCHITECTURE

```
Applications & Services
    |
    +-- Standard Metrics (free) -> CloudWatch
    +
    +-- CloudWatch Agent -> Custom Metrics -> CloudWatch
    |       |-> Logs -> CloudWatch Logs -> Logs Insights
    |
    v
CloudWatch Alarms -> SNS -> Lambda, Auto Scaling, EC2 Actions
CloudWatch Dashboards -> Visualization
```

## CLI EXAMPLES

```bash
# Put Custom Metric
aws cloudwatch put-metric-data \
    --namespace "MyApp" \
    --metric-name "OrderProcessingTime" \
    --value 250 \
    --unit Milliseconds \
    --dimensions Environment=Production,Service=Orders

# Create Alarm (CPU > 80%)
aws cloudwatch put-metric-alarm \
    --alarm-name "HighCPU-Production" \
    --alarm-description "Alert when CPU exceeds 80% for 5 minutes" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --evaluation-periods 2 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:alert-topic \
    --ok-actions arn:aws:sns:us-east-1:123456789012:alert-topic

# Create Composite Alarm
aws cloudwatch put-composite-alarm \
    --alarm-name "SystemHealth-Combined" \
    --alarm-rule "ALARM(HighCPU) OR ALARM(HighMemory)" \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:ops-topic

# Get Metric Statistics
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 3600 \
    --statistics Average Maximum

# Create Log Group
aws logs create-log-group --log-group-name /aws/app/orders

# Create Log Stream
aws logs create-log-stream \
    --log-group-name /aws/app/orders \
    --log-stream-name prod-server-1

# Put Log Events
aws logs put-log-events \
    --log-group-name /aws/app/orders \
    --log-stream-name prod-server-1 \
    --log-events timestamp=$(date +%s%3N),message="Order processed: 12345"

# Create Metric Filter (count errors in logs)
aws logs put-metric-filter \
    --log-group-name /aws/app/orders \
    --filter-name "ErrorCount" \
    --filter-pattern "ERROR" \
    --metric-transformations metricName=ErrorCount,metricNamespace=MyApp,metricValue=1

# Get Log Events
aws logs get-log-events \
    --log-group-name /aws/app/orders \
    --log-stream-name prod-server-1
```

## STANDARD VS CUSTOM METRICS

| Aspect | Standard | Custom |
|--------|----------|--------|
| What | CPU, Network, Disk I/O, Status Checks | Memory, Disk space, Swap, App metrics |
| How | Hypervisor | CloudWatch Unified Agent |
| Cost | Free | $0.30 per metric per month |
| Detail | 1-minute (detailed) or 5-minute (basic) | 1-second granularity possible |

## 15 PRACTICE QUESTIONS

Q1: What is CloudWatch?
A: Monitoring and observability service for AWS resources and applications.

Q2: What metrics does CloudWatch provide for EC2 by default?
A: CPU Utilization, Network In/Out, Disk Read/Write, Status Checks. NOT Memory or Disk Space.

Q3: How do you get memory and disk space metrics?
A: Install the CloudWatch Unified Agent (or legacy agent).

Q4: What is a composite alarm?
A: An alarm that evaluates multiple alarms using AND/OR logic.

Q5: What is the difference between standard and detailed monitoring for EC2?
A: Standard: 5-minute intervals (free). Detailed: 1-minute intervals (paid).

Q6: What is CloudWatch Logs Insights?
A: A SQL-like query engine for analyzing log data in CloudWatch Logs.

Q7: What is a metric filter?
A: A filter that converts log events into CloudWatch metrics.

Q8: How do you create custom metrics?
A: Using `aws cloudwatch put-metric-data` or the CloudWatch Agent.

Q9: What is CloudWatch Unified Agent?
A: An agent that collects system-level metrics (CPU, memory, disk, network, processes) and logs.

Q10: Can CloudWatch alarms trigger Auto Scaling?
A: Yes, but it's recommended to use ASG scaling policies directly instead.

Q11: What is the namespace in CloudWatch?
A: A container for metrics (e.g., AWS/EC2, AWS/Lambda, custom namespaces like MyApp).

Q12: What is a dimension in CloudWatch?
A: A key-value pair that identifies a metric uniquely (e.g., InstanceId, Environment).

Q13: What is the retention period for CloudWatch Logs?
A: Configurable: 1 day to 10 years (or never expire).

Q14: Can CloudWatch monitor on-premises servers?
A: Yes, using the CloudWatch Agent on on-premises systems.

Q15: What is the difference between CloudWatch and CloudTrail?
A: CloudWatch monitors performance/events; CloudTrail records API calls for auditing.
""")

# =====================================================================
# CLOUDTRAIL (Major - 15 Q&A)
# =====================================================================
w("monitoring/03-cloudtrail.md", """# AWS CloudTrail - API Activity Auditing

## KEY FEATURES
- Records all API activity in your account
- Auditing, security analysis, compliance
- 90 days of Event History (free)
- Custom trails for extended retention and data events

## EVENT TYPES

| Event Type | Description | Cost | Examples |
|------------|-------------|------|----------|
| Management | Control plane operations | Free (90 days) | CreateVPC, TerminateInstances, CreateUser |
| Data Events | Resource operations | Paid | GetObject, PutItem, InvokeFunction |
| Insights | Anomalous activity | Paid | Unusual API patterns, spikes |

## ARCHITECTURE

```
AWS API Calls
    |
    v
CloudTrail
    |
    +-- Event History (90 days, free)
    |
    +-- Trail -> S3 Bucket (custom delivery)
    |       |
    |       +-- CloudWatch Logs (real-time alerting)
    |       +-- Athena (SQL queries)
    |
    +-- Insights (ML-based anomaly detection)
```

## CLI EXAMPLES

```bash
# Create Multi-Region Trail
aws cloudtrail create-trail \
    --name my-audit-trail \
    --s3-bucket-name my-cloudtrail-logs-123456789012 \
    --is-multi-region-trail \
    --enable-log-file-validation \
    --tags Key=Environment,Value=Production

# Start Logging
aws cloudtrail start-logging --name my-audit-trail

# Create Organization Trail
aws cloudtrail create-trail \
    --name org-trail \
    --s3-bucket-name my-org-trail-logs \
    --is-organization-trail \
    --is-multi-region-trail

# Enable Data Events (S3 Object-Level)
aws cloudtrail put-event-selectors \
    --trail-name my-audit-trail \
    --event-selectors '[{
        "ReadWriteType": "All",
        "IncludeManagementEvents": true,
        "DataResources": [{
            "Type": "AWS::S3::Object",
            "Values": ["arn:aws:s3:::my-bucket/"]
        }]
    }]'

# Lookup Events (Last 90 days)
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=EventName,AttributeValue=CreateVpc \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-31T00:00:00Z \
    --max-results 50

# Describe Trails
aws cloudtrail describe-trails

# Get Trail Status
aws cloudtrail get-trail-status --name my-audit-trail

# Update Trail (enable log validation)
aws cloudtrail update-trail \
    --name my-audit-trail \
    --enable-log-file-validation

# Stop Logging
aws cloudtrail stop-logging --name my-audit-trail

# Delete Trail
aws cloudtrail delete-trail --name my-audit-trail
```

## EXAM TIPS
- Management events are FREE for 90 days via Event History
- Data events (S3, Lambda) incur additional cost
- Organization Trail: Single trail for all accounts in AWS Organizations
- Enable log file validation to verify integrity
- Integrate with CloudWatch for real-time alerting
- Use Athena to query CloudTrail logs in S3

## 15 PRACTICE QUESTIONS

Q1: What is AWS CloudTrail?
A: A service that records API activity in your AWS account for auditing, compliance, and security.

Q2: What is the difference between Management and Data events?
A: Management events (free) record control plane operations; Data events (paid) record resource-level operations.

Q3: How long is Event History retained?
A: 90 days (free). Custom trails can retain logs indefinitely in S3.

Q4: What is CloudTrail Insights?
A: A feature that uses ML to detect anomalous API activity (paid).

Q5: What is an Organization Trail?
A: A trail that logs API activity for all accounts in AWS Organizations.

Q6: How do you validate CloudTrail log integrity?
A: Enable log file validation (uses SHA-256 hash and digital signatures).

Q7: Can CloudTrail be integrated with CloudWatch?
A: Yes, send events to CloudWatch Logs for real-time alerting.

Q8: What is a multi-region trail?
A: A trail that logs activity in all AWS regions.

Q9: How do you turn on data events for S3?
A: Use `put-event-selectors` to track S3 object-level operations.

Q10: What is the S3 bucket policy requirement for CloudTrail?
A: CloudTrail writes to S3 using a bucket policy that grants write access.

Q11: Can CloudTrail logs be encrypted?
A: Yes, using default SSE-S3 or SSE-KMS.

Q12: What is log file validation?
A: Creates digest files that verify log files haven't been tampered with.

Q13: Can CloudTrail track Lambda invocations?
A: Yes, as a Data Event.

Q14: How do you query CloudTrail logs in S3?
A: Using Athena with the pre-built CloudTrail table schema.

Q15: What is the difference between CloudTrail and CloudWatch?
A: CloudTrail records API calls (who did what); CloudWatch monitors performance (CPU, memory, etc.).
""")

# =====================================================================
# GUARDDUTY (Major - 15 Q&A)
# =====================================================================
w("threat-detection/01-guardduty.md", """# Amazon GuardDuty - Threat Detection

## KEY FEATURES
- Intelligent threat detection using ML and anomaly detection
- Analyses: VPC Flow Logs, CloudTrail events, DNS logs
- Detects: Unauthorized access, crypto mining, compromised credentials, malware

## FINDINGS SEVERITY

| Level | Score | Examples |
|-------|-------|----------|
| Low | 1-3 | Port scanning, suspicious user agent |
| Medium | 4-6 | Unusual API calls, failed login attempts |
| High | 7-8.9 | Crypto mining, API calls from known bad IPs |
| Critical | 9-10 | Compromised credentials, data exfiltration |

## CLI EXAMPLES

```bash
# Enable GuardDuty
aws guardduty create-detector --enable

# List Detectors
aws guardduty list-detectors

# List Findings
aws guardduty list-findings \
    --detector-id DETECTOR_ID \
    --max-results 50

# Get Finding Details
aws guardduty get-findings \
    --detector-id DETECTOR_ID \
    --finding-ids FINDING_ID

# Archive Finding
aws guardduty archive-findings \
    --detector-id DETECTOR_ID \
    --finding-ids FINDING_ID

# Create Filter
aws guardduty create-filter \
    --detector-id DETECTOR_ID \
    --name "Critical-Findings" \
    --finding-criteria '{"Criterion":{"severity":{"Gte":7}}}' \
    --action ARCHIVE

# Update Detector (Disable)
aws guardduty update-detector \
    --detector-id DETECTOR_ID \
    --enable false

# List IPSets (Trusted IPs)
aws guardduty list-ip-sets --detector-id DETECTOR_ID

# List ThreatIntelSets (Malicious IPs)
aws guardduty list-threat-intel-sets --detector-id DETECTOR_ID
```

## EXAM TIPS
- Regional service (enable in each region)
- No agents needed (analyzes existing logs)
- Findings sent to EventBridge, Security Hub, or S3
- Use Filters to auto-archive false positives
- 30-day free trial, then pay per volume

## 10 PRACTICE QUESTIONS

Q1: What is GuardDuty?
A: An intelligent threat detection service that uses ML to detect malicious activity.

Q2: What data sources does GuardDuty analyze?
A: VPC Flow Logs, CloudTrail events (management + data), DNS logs.

Q3: What severity levels does GuardDuty use?
A: Low (1-3), Medium (4-6), High (7-8.9), Critical (9-10).

Q4: Is GuardDuty regional or global?
A: Regional - must be enabled in each region.

Q5: Does GuardDuty require agents?
A: No, it's agentless and analyzes existing logs.

Q6: How do you respond to GuardDuty findings automatically?
A: Use EventBridge rules to trigger Lambda functions for auto-remediation.

Q7: What is a Trusted IP List?
A: A list of IPs that GuardDuty won't report as threats (whitelist).

Q8: What is a Threat List?
A: A list of known malicious IPs that GuardDuty monitors against (blacklist).

Q9: How long is the GuardDuty free trial?
A: 30 days.

Q10: Can GuardDuty detect crypto mining?
A: Yes, it's one of the common findings (crypto mining activity).
""")

# =====================================================================
# ADDING MISSING TOPICS
# =====================================================================

# CloudFormation (Major - 15 Q&A)
w("cloudformation/01-introduction.md", """# AWS CloudFormation - Infrastructure as Code

## KEY FEATURES
- Infrastructure as Code (IaC) for AWS resources
- Declarative templates (YAML/JSON)
- Stack-based resource management
- Change sets for previewing changes
- Drift detection for manual changes
- Nested stacks for modularity

## TEMPLATE STRUCTURE

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: My application stack
Parameters:
  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues: [t3.micro, t3.small, t3.medium]
Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-0abcdef1234567890
      SecurityGroups: [!Ref InstanceSecurityGroup]
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH access
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
Outputs:
  InstanceIP:
    Description: Public IP of the instance
    Value: !GetAtt MyEC2Instance.PublicIp
```

## CLI EXAMPLES

```bash
# Create Stack
aws cloudformation create-stack \
    --stack-name my-app-stack \
    --template-body file://template.yaml \
    --parameters ParameterKey=InstanceType,ParameterValue=t3.micro \
    --capabilities CAPABILITY_IAM

# Deploy (Create or Update)
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name my-app-stack \
    --parameter-overrides InstanceType=t3.small \
    --capabilities CAPABILITY_IAM

# Create Change Set (Preview)
aws cloudformation create-change-set \
    --stack-name my-app-stack \
    --template-body file://template.yaml \
    --change-set-name my-upgrade \
    --parameters ParameterKey=InstanceType,ParameterValue=t3.large

# Execute Change Set
aws cloudformation execute-change-set \
    --change-set-name my-upgrade \
    --stack-name my-app-stack

# Delete Stack
aws cloudformation delete-stack --stack-name my-app-stack

# Detect Drift
aws cloudformation detect-stack-drift --stack-name my-app-stack

# List Stack Resources
aws cloudformation list-stack-resources --stack-name my-app-stack

# Describe Stack Events
aws cloudformation describe-stack-events --stack-name my-app-stack

# Create StackSet (multi-account)
aws cloudformation create-stack-set \
    --stack-set-name my-org-stack \
    --template-body file://template.yaml \
    --capabilities CAPABILITY_IAM

# Create Stack Instances (from StackSet)
aws cloudformation create-stack-instances \
    --stack-set-name my-org-stack \
    --accounts 123456789012 234567890123 \
    --regions us-east-1 eu-west-1
```

## 15 PRACTICE QUESTIONS

Q1: What is CloudFormation?
A: Infrastructure as Code service for modeling and provisioning AWS resources.

Q2: What is a Stack?
A: A collection of AWS resources created from a CloudFormation template.

Q3: What is a Change Set?
A: A preview of changes before applying them to a stack.

Q4: What is Drift Detection?
A: Detects manual changes to resources outside of CloudFormation.

Q5: What are the template formats?
A: JSON and YAML.

Q6: What is a Nested Stack?
A: A stack within another stack for modularity and reusability.

Q7: What is a StackSet?
A: Allows creating stacks across multiple accounts and regions.

Q8: What is the difference between CloudFormation and Elastic Beanstalk?
A: CloudFormation is IaC (full control); Elastic Beanstalk is PaaS (abstracted infrastructure).

Q9: What is a CloudFormation Resource?
A: An AWS resource defined in the template (e.g., AWS::EC2::Instance).

Q10: What is a Parameter?
A: Input values passed to the template (e.g., instance type, environment name).

Q11: What is an Output?
A: Values exposed by the stack (e.g., DNS name, load balancer URL).

Q12: What happens when you delete a stack?
A: All resources in the stack are deleted (based on DeletionPolicy).

Q13: What is a Mapping?
A: Static lookup table (e.g., region to AMI ID mapping).

Q14: What is a Condition?
A: Controls whether a resource is created (e.g., create resource only in production).

Q15: What is Rollback on failure?
A: Default behavior: if stack creation fails, AWS rolls back and deletes created resources.
""")

# Systems Manager (SSM) - (Major - 15 Q&A)
w("systems-manager/01-introduction.md", """# AWS Systems Manager (SSM) - Operations Management

## KEY FEATURES
- Centralized management of EC2 and on-premises resources
- Session Manager: SSH/RDP without open ports or bastion hosts
- Run Command: Execute commands remotely
- Patch Manager: Automated OS patching
- Parameter Store: Secure storage for config data
- Automation: Runbooks for common tasks
- Inventory: Collect OS/application metadata
- Compliance: Track patch compliance status

## SSM AGENT
Required on EC2 instances and on-premises servers for SSM to work.

## CLI EXAMPLES

```bash
# Start Session (no SSH key needed, no open port 22)
aws ssm start-session --target i-1234567890abcdef0

# Run Command on Multiple Instances
aws ssm send-command \
    --document-name "AWS-RunShellScript" \
    --targets Key=tag:Environment,Values=Production \
    --parameters commands=["sudo yum update -y"] \
    --comment "Security patch all production instances"

# Get Parameter (from Parameter Store)
aws ssm get-parameters \
    --names /myapp/database/url \
    --with-decryption

# Put Parameter
aws ssm put-parameter \
    --name /myapp/database/password \
    --value "MyS3cur3P@ss!" \
    --type SecureString \
    --key-id alias/ssm-key \
    --overwrite

# Create Patch Baseline
aws ssm create-patch-baseline \
    --name "Production-Patch-Baseline" \
    --operating-system AMAZON_LINUX_2 \
    --approval-rules '{"PatchFilters":[{"Key":"CLASSIFICATION","Values":["Security"]}],"ApproveAfterDays":7}'

# Get Inventory
aws ssm list-inventory-entries \
    --instance-id i-1234567890abcdef0 \
    --type-name "AWS:Application"

# Describe Patch Compliance
aws ssm describe-patch-group-state \
    --patch-group "Production"

# Create Automation Document
aws ssm create-document \
    --name "StopStartInstances" \
    --content file://automation.yaml \
    --document-type Automation
```

## 15 PRACTICE QUESTIONS

Q1: What is AWS Systems Manager?
A: A suite of tools for managing EC2 and on-premises resources at scale.

Q2: What is Session Manager?
A: Connect to EC2 instances via browser/CLI without SSH keys, bastion hosts, or open ports.

Q3: What is Parameter Store?
A: Secure hierarchical storage for configuration data and secrets.

Q4: What is the difference between Parameter Store and Secrets Manager?
A: Parameter Store is free (standard) but has no automatic rotation; Secrets Manager has rotation but costs $0.40/secret/month.

Q5: What is Run Command?
A: Remotely execute commands on multiple instances without SSH.

Q6: What is Patch Manager?
A: Automates OS patching with approval rules and maintenance windows.

Q7: What is the SSM Agent?
A: Software installed on EC2/on-premises that enables SSM features.

Q8: Does Session Manager work on instances without public IPs?
A: Yes, through VPC Endpoints (no internet gateway needed).

Q9: What is a Maintenance Window?
A: A schedule for performing potentially disruptive operations.

Q10: What is Automation in SSM?
A: Runbooks for automated operational tasks (stop instances, create AMIs, etc.).

Q11: What is Inventory?
A: Collects metadata about managed instances (installed apps, OS config, network config).

Q12: How does SSM securely connect to instances without open ports?
A: The SSM Agent initiates an outbound connection to AWS SSM endpoints.

Q13: What types does Parameter Store support?
A: String, StringList, SecureString (KMS encrypted).

Q14: What is a Patch Baseline?
A: Defines which patches are approved for installation.

Q15: Can SSM manage on-premises servers?
A: Yes, by installing the SSM Agent and registering with AWS.
""")

print("=== BATCH COMPLETE ===")
print("Created: app-platform, messaging, security, monitoring, threat-detection files")
print("Created new: cloudformation, systems-manager")