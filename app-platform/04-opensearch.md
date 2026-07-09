# Amazon OpenSearch Service

Managed search and analytics.

## CLI
```bash
aws opensearch create-domain --domain-name my-domain --engine-version OpenSearch_2.11 --cluster-config InstanceType=r5.large.search,InstanceCount=3 --ebs-options EBSEnabled=true,VolumeSize=100
aws opensearch describe-domain --domain-name my-domain
aws opensearch delete-domain --domain-name my-domain
```

## Q&A
**Q1: What is OpenSearch?** A: Search and analytics. **Q2: Use cases?** A: Log analytics, app search, observability. **Q3: Can it be in a VPC?** A: Yes. **Q4: What is Dashboards?** A: Visualization tool. **Q5: OpenSearch vs Elasticsearch?** A: OpenSearch is the AWS successor.
