# Amazon CloudWatch

Monitoring and observability.

## Components
| Component | Purpose |
|-----------|---------|
| Logs | Centralized logging |
| Metrics | Performance data |
| Alarms | Threshold alerts |
| Dashboards | Visualization |
| Unified Agent | System metrics (RAM, disk) |

## Host Metrics (Free)
- CPU, Network, Disk, Status Checks
- NOT memory or disk space (require Unified Agent)

## CLI
```bash
aws cloudwatch put-metric-data --namespace "MyApp" --metric-name "PageLoadTime" --value 250 --unit Milliseconds
aws cloudwatch put-metric-alarm --alarm-name "HighCPU" --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --evaluation-periods 2 --threshold 80 --comparison-operator GreaterThanThreshold --dimensions Name=InstanceId,Value=i-xxx
aws cloudwatch put-composite-alarm --alarm-name "Multi" --alarm-rule "ALARM(HighCPU) OR ALARM(HighMemory)" --alarm-actions arn:aws:sns:us-east-1:xxx:my-topic
aws logs create-log-group --log-group-name my-app-logs
```

## Q&A
**Q1: Default EC2 metrics?** A: CPU, Network, Disk, Status Checks. **Q2: How to get memory metrics?** A: Install Unified Agent. **Q3: Composite alarm?** A: Combines alarms with AND/OR. **Q4: What is Logs Insights?** A: SQL-like query for logs. **Q5: Custom metrics?** A: Yes, via PutMetricData.
