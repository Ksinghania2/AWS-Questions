# AWS Solutions Architect — Complete Study Repository

Comprehensive study notes, CLI commands, and exam revision material for the **AWS Solutions Architect (SAA-C03)** certification.

## 📚 Exam Topics Coverage

| Section | Topics Covered |
|---------|---------------|
| **[Setup & AWS CLI](setup-cli/)** | Configuration files, named profiles, env variables, autocompletion, autoprompt, configure commands |
| **[API & STS](API/)** | Access keys, retries, exponential backoff, Smithy, STS, AssumeRole, SigV4 |
| **[Amazon S3](s3/)** | Buckets, storage classes, objects, encryption, security, features (lifecycle, replication, event notifications, presigned URLs, Transfer Acceleration, WORM), IaC, SDKs |
| **[Amazon VPC](vpc/)** | Core components, NACLs vs SGs, NAT Gateway vs Instance, VPC Peering vs Transit Gateway, VPC Endpoints, Flow Logs, Shared VPCs, IPv6, VPC Lattice, Traffic Mirroring, DNS Firewall, Network Firewall, Direct Connect, Site-to-Site VPN, Client VPN |
| **[IAM](iam/)** | Users, groups, roles, policies, password policy, MFA, Organizations & SCPs, permission boundaries, identity federation (SAML, Web Identity, Cognito, Identity Center) |
| **[EC2](ec2/)** | Instance types & families, metadata (IMDSv1/v2), placement groups, pricing models (On-Demand, RI, Spot, Dedicated, Savings Plans), burstable instances |
| **[AMIs](ec2/amis/)** | Public, private, marketplace, custom images |
| **[Auto Scaling](ec2/asg/)** | Dynamic scaling policies (simple, step, target tracking, predictive), lifecycle hooks, cooldown periods |
| **[ELB](ec2/elb/)** | ALB, NLB, CLB, GWLB, cross-zone load balancing, session stickiness |
| **[Route53](route53/)** | Routing policies (simple, weighted, latency, failover, geolocation, geoproximity, multi-value), health checks, DNSSEC, zonal shift |
| **[CloudFront](cloudfront/)** | Distributions, origins, Origin Shield, CloudFront Functions vs Lambda@Edge |
| **[Global Accelerator](global-accelerator/)** | Anycast IP network proxying for TCP/UDP |
| **[EBS](ebs/)** | Volume types (gp3, io2, st1, sc1), multi-attach, RAID configurations |
| **[EFS](efs/)** | NFSv4, storage classes, lifecycle management, throughput modes |
| **[FSx](fsx/)** | Lustre, NetApp ONTAP, OpenZFS, Windows File Server |
| **[AWS Backup](backup/)** | Centralized backup plans, vaults, cross-region backup |
| **[Snow Family](snow/)** | Snowcone, Snowball Edge, Snowmobile |
| **[Data Migration](migration/)** | DMS, SCT, DataSync |
| **[Storage Gateway](storage-gateway/)** | File Gateway, Volume Gateway, Tape Gateway |
| **[RDS](rds/)** | Multi-AZ, Read Replicas, backups, snapshots |
| **[Aurora](aurora/)** | Cluster, serverless, global database, 15 replicas |
| **[DocumentDB](documentdb/)** | MongoDB-compatible document store |
| **[DynamoDB](dynamodb/)** | Tables, GSIs, LSIs, queries vs scans, DAX, Streams, TTL |
| **[Keyspaces](keyspaces/)** | Managed Apache Cassandra (CQL) |
| **[Neptune](neptune/)** | Graph database (Gremlin, SPARQL, openCypher) |
| **[ElastiCache](elasticache/)** | Redis vs Memcached, lazy loading, write-through |
| **[MemoryDB](memorydb/)** | Redis-compatible durable in-memory DB |
| **[ECR](ecr/)** | Container registry, vulnerability scanning, lifecycle policies |
| **[ECS](ecs/)** | Fargate vs EC2, task definitions, services, task roles |
| **[EKS](eks/)** | Managed Kubernetes, node groups, Fargate |
| **[Lambda](lambda/)** | Functions, versions, aliases, invocation types, concurrency, DLQs |
| **[Step Functions](step-functions/)** | State machines, standard vs express, Amazon States Language |
| **[API Gateway](api-gateway/)** | REST, HTTP, WebSocket APIs, throttling, caching, authorizers |
| **[Analytics](analytics/)** | Athena, Redshift, Glue, Lake Formation, Kinesis |
| **[App Platform](app-platform/)** | Elastic Beanstalk, Amplify, AppSync, OpenSearch |
| **[Messaging](messaging/)** | SNS (pub/sub, fan-out), SQS (standard vs FIFO, DLQs, long polling), Amazon MQ |
| **[Security](security/)** | KMS (envelope encryption), ACM (SSL/TLS), Secrets Manager, WAF & Shield |
| **[Threat Detection](threat-detection/)** | GuardDuty, Inspector, Macie, Security Hub |
| **[Monitoring](monitoring/)** | CloudWatch (metrics, alarms, logs, unified agent), EventBridge, CloudTrail |
| **[Service Catalog](service-catalog/)** | Portfolios, products, constraints |
| **[Compute Optimizer](compute-optimizer/)** | Rightsizing recommendations for EC2, ASG, EBS, Lambda |

## 📖 How to Use This Repo

### Structure
Each topic has its own directory with individual markdown files containing:
- **Theory**: Clear, concise explanations
- **CLI Commands**: Real AWS CLI commands with examples
- **Exam Tips**: Common exam scenarios and pitfalls
- **Q&A**: Practice questions for exam preparation

### Study Path
```
1. Start with IAM → VPC → EC2 (foundational)
2. Move to S3 → EBS → EFS → RDS → Aurora (storage/database)
3. Learn Route53 → CloudFront → ELB → ASG (networking/scaling)
4. Study Lambda → API Gateway → DynamoDB → SQS → SNS (serverless)
5. Security → Monitoring → Analytics → remaining topics
6. Review Q&A sections and practice questions
```

### Each File Contains
- ✅ **Theory** — Clear explanations
- ✅ **CLI Commands** — Real AWS CLI examples
- ✅ **Exam Tips** — Common scenarios and pitfalls
- ✅ **Q&A** — 3-20 practice questions per topic

## 🚀 Quick Start
```bash
# Verify AWS CLI is configured
aws sts get-caller-identity

# List available services
aws help

# Explore topics
open setup-cli/
open vpc/
open iam/
open ec2/