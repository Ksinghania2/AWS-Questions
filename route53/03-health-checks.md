# Route53 Health Checks

## Types
| Type | Monitors | Use Case |
|------|----------|----------|
| Endpoint | Specific IP/domain | Direct endpoint monitoring |
| CloudWatch | CloudWatch alarm | Custom metrics |
| Calculated | Other health checks | Composite status |

## CLI
```bash
# Create endpoint health check
aws route53 create-health-check     --caller-reference "hc-$(date +%s)"     --health-check-config '{
        "IPAddress": "1.2.3.4",
        "Port": 443,
        "Type": "HTTPS",
        "ResourcePath": "/health",
        "FailureThreshold": 3,
        "RequestInterval": 30,
        "EnableSNI": true
    }'

# Create calculated health check
aws route53 create-health-check     --caller-reference "calc-$(date +%s)"     --health-check-config '{
        "Type": "CALCULATED",
        "ChildHealthChecks": ["xxx", "yyy"],
        "HealthThreshold": 2
    }'

# Associate health check with Route53 record
# (Use --health-check-id in the failover routing policy)
```

## Health Check States
- **Healthy**: Passed threshold checks
- **Unhealthy**: Failed threshold checks
- **Insufficient Data**: Not enough data

## Q&A
**Q1: What is a calculated health check?** A: Combines multiple health checks into one.
**Q2: What are the request intervals?** A: 10 seconds (fast) or 30 seconds (standard).
**Q3: What is the failure threshold?** A: Number of consecutive failures before marking unhealthy (default 3).
**Q4: Can health checks monitor on-premises endpoints?** A: Yes, if the endpoint is accessible from the internet.
**Q5: What is the difference between endpoint and CloudWatch health checks?** A: Endpoint checks the resource directly; CloudWatch checks a metric alarm.
