# AWS Certificate Manager

SSL/TLS certificate management.

## CLI
```bash
aws acm request-certificate --domain-name example.com --validation-method DNS --subject-alternative-names www.example.com
aws acm import-certificate --certificate fileb://cert.pem --private-key fileb://key.pem --certificate-chain fileb://chain.pem
aws acm list-certificates
aws acm describe-certificate --certificate-arn arn:aws:acm:us-east-1:xxx:certificate/xxx
aws acm delete-certificate --certificate-arn arn:aws:acm:us-east-1:xxx:certificate/xxx
```

## Q&A
**Q1: Free?** A: Yes for AWS services. **Q2: Auto-renew?** A: Yes (DNS validation). **Q3: Integrations?** A: ALB, CloudFront, API Gateway, NLB. **Q4: What is ACM PCA?** A: Private CA for internal certs. **Q5: Validation methods?** A: DNS (recommended) and Email.
