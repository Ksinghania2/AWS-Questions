# Amazon ECR (Elastic Container Registry)

ECR is a fully managed Docker container registry.

## Key Features
- Store, manage, and deploy container images
- Integrated with ECS and EKS
- Vulnerability scanning
- Cross-region replication
- Lifecycle policies

## CLI
```bash
# Create repository
aws ecr create-repository     --repository-name my-app     --image-scanning-configuration scanOnPush=true     --encryption-type AES256

# Login (get token)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Push image
docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# Pull image
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# List images
aws ecr list-images --repository-name my-app

# Lifecycle policy
aws ecr put-lifecycle-policy     --repository-name my-app     --lifecycle-policy-text '{
        "rules": [{
            "rulePriority": 1,
            "description": "Expire old images",
            "selection": {"tagStatus":"any","countType":"imageCountMoreThan","countNumber":100},
            "action": {"type":"expire"}
        }]
    }'
```

## Q&A
**Q1: What is ECR?** A: Container image registry for Docker images.
**Q2: How do you authenticate to ECR?** A: `aws ecr get-login-password | docker login`.
**Q3: Does ECR support vulnerability scanning?** A: Yes, on push.
**Q4: Can ECR replicate across regions?** A: Yes.
**Q5: What are lifecycle policies?** A: Rules to auto-expire old images.
