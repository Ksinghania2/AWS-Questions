# Amazon EventBridge

Serverless event bus.

## Event Sources
- AWS services
- Custom apps
- SaaS (Datadog, Zendesk)

## CLI
```bash
aws events put-events --entries '[{"Source":"my-app","DetailType":"OrderCreated","Detail":"{\"orderId\":\"123\"}","EventBusName":"default"}]'
aws events put-rule --name "EC2-State-Change" --event-pattern '{"source":["aws.ec2"],"detail-type":["EC2 Instance State-change Notification"]}'
aws events put-targets --rule "EC2-State-Change" --targets Id=1,Arn=arn:aws:lambda:us-east-1:xxx:function:my-function
aws events put-rule --name "Daily-Report" --schedule-expression "cron(0 8 * * ? *)"
```

## Q&A
**Q1: What is EventBridge?** A: Event bus for service integration. **Q2: Difference from CloudWatch Events?** A: EventBridge evolved (SaaS, schema registry). **Q3: Targets?** A: Lambda, SQS, SNS, Step Functions, API Gateway. **Q4: Event pattern?** A: JSON filter for events. **Q5: Scheduled events?** A: Yes, cron syntax.
