# AWS CloudTrail

API activity auditing.

## Event Types
| Type | Example | Cost |
|------|---------|------|
| Management | CreateVPC, TerminateInstances | Free (90 days) |
| Data | GetObject, PutItem | Paid |
| Insights | Anomalous activity | Paid |

## CLI
```bash
aws cloudtrail create-trail --name my-trail --s3-bucket-name my-logs --is-multi-region-trail --enable-log-file-validation
aws cloudtrail start-logging --name my-trail
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=CreateVpc --start-time 2024-01-01T00:00:00Z
aws cloudtrail describe-trails
aws cloudtrail stop-logging --name my-trail
```

## Q&A
**Q1: What is CloudTrail?** A: API activity auditing. **Q2: Management vs Data events?** A: Management = free control plane; Data = paid resource ops. **Q3: Event history retention?** A: 90 days free. **Q4: What is Insights?** A: ML-based anomaly detection. **Q5: Organization trail?** A: Logs all accounts in AWS Organizations.
