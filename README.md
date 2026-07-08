# AWS S3 Solutions Architect — Complete Study Repository

Comprehensive S3 study notes, CLI/Python scripts, and exam revision material for the **AWS Solutions Architect** certification.

## 📚 Quick Navigation

| Section | Description |
|---|---|
| **[S3 Theory Guide](S3_THEORY.md)** | **Start here** — complete exam revision with cheat sheet |
| **[AWS Setup](AWS_SETUP.md)** | Installation and configuration guide |
| **[API Docs](API/)** | AWS API, CLI, STS, Smithy documentation |
| | |

### S3 Documentation

| Category | Topics |
|---|---|
| **[Buckets](s3/buckets/)** | Naming rules, restrictions, types, URL formats, folder structure |
| **[Storage Classes](s3/s3%20storage%20classes/)** | Standard, IA, One Zone-IA, Intelligent-Tiering, Glacier (3 types), Express One Zone |
| **[Object Overview](s3/s3%20object%20overview/)** | Versioning, consistency, metadata, tags, prefixes, checksums, locking, ETags |
| **[Encryption](s3/encryption/)** | SSE-S3, SSE-KMS, SSE-C, DSSE-KMS, Client-Side Encryption, in-transit |
| **[Features](s3/features/)** | Presigned URLs, lifecycle, static web hosting, multipart upload, replication, event notifications, Transfer Acceleration, WORM, S3 Select, Inventory |
| **[Security](s3/s3%20security%20overview/)** | Access points, bucket policies, IAM, ACLs, Block Public Access, CORS, PrivateLink, MFA Delete |

### Hands-On Examples

| Resource | What You'll Learn |
|---|---|
| **[Bash Scripts](s3/bash-scripts/)** | Create/delete buckets, upload/list/delete objects, sync |
| **[PowerShell](s3/powershell-scripts/)** | PowerShell S3 operations module |
| **[CloudFormation](s3/iac/cfn/)** | IaC template for S3 bucket |
| **[CDK](s3/iac/cdk/)** | AWS CDK (TypeScript) example |
| **[Terraform](s3/iac/terraform/)** | Terraform HCL for S3 |
| **[Pulumi](s3/iac/pulumi/)** | Pulumi (Python) for S3 |
| **[Java SDK](s3/sdk/java/)** | Java SDK starter |
| **[Ruby SDK](s3/sdk/ruby/)** | Ruby SDK starter |

## 🚀 Quick Start

```bash
# 1. Install AWS CLI (see AWS_SETUP.md)
aws configure

# 2. Create a test bucket
aws s3api create-bucket --bucket my-unique-bucket-$(date +%s) --region us-east-1

# 3. Upload a file
echo "Hello S3" > hello.txt
aws s3 cp hello.txt s3://my-unique-bucket/

# 4. List objects
aws s3 ls s3://my-unique-bucket/

# 5. Generate presigned URL
aws s3 presign s3://my-unique-bucket/hello.txt --expires-in 3600

# 6. Clean up
aws s3 rm s3://my-unique-bucket/hello.txt
aws s3 rb s3://my-unique-bucket/
```

## 📖 How to Use This Repo for Exam Preparation

### Week Before Exam — Final Review
1. Read **[S3_THEORY.md](S3_THEORY.md)** — comprehensive theory + cheat sheet
2. Practice CLI commands from each section
3. Review **"Common Exam Scenarios"** in S3_THEORY.md
4. Memorize **"Must-Know Numbers"**

### Study Path
```
Week 1: Buckets Naming + Storage Classes
Week 2: Versioning + Encryption + Access Control
Week 3: Features (lifecycle, replication, notifications, presigned URLs)
Week 4: Security + Object Lock + Performance
Week 5: Review S3_THEORY.md + practice CLI commands
```

### Each File Contains:
- ✅ **Theory** — Clear, concise explanations
- ✅ **CLI Commands** — Real AWS CLI commands with examples
- ✅ **Python (boto3)** — Code examples with documentation
- ✅ **Exam Tips** — Common exam scenarios and pitfalls
- ✅ **Quick Reference** — Bullet points for last-minute revision