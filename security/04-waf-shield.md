# AWS WAF & Shield

## WAF (Layer 7)
Protects against SQL injection, XSS, DDoS.

## Shield
| Feature | Standard | Advanced |
|---------|----------|----------|
| Protection | L3/4 DDoS | L3/4/7 DDoS |
| Cost | Free | $3,000/month |
| DRT | No | Yes 24/7 |

## CLI
```bash
aws wafv2 create-web-acl --name my-acl --scope REGIONAL --default-action Allow={} --rules '[]' --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl
aws wafv2 associate-web-acl --web-acl-arn arn:aws:wafv2:us-east-1:xxx:regional/webacl/my-acl/xxx --resource-arn arn:aws:elasticloadbalancing:us-east-1:xxx:loadbalancer/app/my-alb/xxx
aws shield create-protection --name my-protection --resource-arn arn:aws:elasticloadbalancing:us-east-1:xxx:loadbalancer/app/my-alb/xxx
```

## Q&A
**Q1: WAF layer?** A: Layer 7. **Q2: Standard vs Advanced?** A: Standard free (L3/4); Advanced $3k/mo (L3/4/7 + DRT). **Q3: WAF integrations?** A: ALB, CloudFront, API Gateway. **Q4: What is rate-based rule?** A: Blocks IPs exceeding rate. **Q5: Managed rule groups?** A: Pre-built from AWS/Marketplace.
