# Amazon SNS

Pub/sub messaging service.

## CLI
```bash
aws sns create-topic --name my-topic
aws sns subscribe --topic-arn arn:aws:sns:us-east-1:xxx:my-topic --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:xxx:my-queue
aws sns publish --topic-arn arn:aws:sns:us-east-1:xxx:my-topic --message "Hello" --subject "Alert"
aws sns set-subscription-attributes --subscription-arn arn:aws:sns:us-east-1:xxx:sub-xxx --attribute-name FilterPolicy --attribute-value '{"event_type":["order_placed"]}'
```

## Fan-Out Pattern
One SNS topic -> Multiple SQS queues + Lambda + HTTP

## Q&A
**Q1: What is SNS?** A: Pub/sub messaging. **Q2: Protocols?** A: SQS, Lambda, HTTP, Email, SMS, Push. **Q3: What is fan-out?** A: One message to multiple subscribers. **Q4: What is filter policy?** A: Filters messages per subscriber. **Q5: FIFO topics?** A: Yes, ordering + deduplication.
