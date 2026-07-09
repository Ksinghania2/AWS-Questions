# AWS Elastic Beanstalk

PaaS for deploying web apps.

## Deployment Strategies
| Strategy | Downtime |
|----------|----------|
| All-at-Once | Yes |
| Rolling | No (reduced capacity) |
| Rolling with Batch | No |
| Immutable | No (best) |
| Blue/Green | No (swap CNAME) |

## CLI
```bash
aws elasticbeanstalk create-application --application-name my-app
aws elasticbeanstalk create-environment --application-name my-app --environment-name prod --solution-stack-name "64bit Amazon Linux 2 v5.8.0 running Node.js 18"
aws elasticbeanstalk update-environment --environment-name prod --version-label v2
aws elasticbeanstalk swap-environment-cnames --source-environment-name blue --destination-environment-name green
```

## Q&A
**Q1: What is Beanstalk?** A: PaaS for web apps. **Q2: Environment types?** A: Web Server (HTTP) and Worker (SQS). **Q3: Best deployment strategy?** A: Immutable or Blue/Green. **Q4: What is Blue/Green?** A: Separate environment, swap DNS. **Q5: Supported platforms?** A: Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker.
