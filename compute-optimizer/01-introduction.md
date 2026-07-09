# AWS Compute Optimizer

Recommends optimal AWS resource configurations.

## Supported Resources
- EC2 instances
- Auto Scaling groups
- EBS volumes
- Lambda functions

## CLI
```bash
aws compute-optimizer get-ec2-instance-recommendations --instance-arns arn:aws:ec2:us-east-1:xxx:instance/i-xxx
aws compute-optimizer get-enrollment-status
aws compute-optimizer get-recommendation-summaries
```

## Q&A
**Q1: What is Compute Optimizer?** A: Rightsizing recommendations. **Q2: What metrics does it use?** A: CloudWatch metrics (CPU, memory, I/O). **Q3: Supported resources?** A: EC2, ASG, EBS, Lambda. **Q4: Free?** A: Yes, basic recommendations; enhanced requires opt-in. **Q5: How often are recommendations generated?** A: Daily.
