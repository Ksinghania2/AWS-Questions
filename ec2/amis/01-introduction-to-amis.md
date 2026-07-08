# Amazon Machine Images (AMIs)

An AMI is a **template** that contains the OS, software, and configuration for launching EC2 instances.

## Types of AMIs

| Type | Source | Use Case |
|---|---|---|
| **Public AMIs** | AWS, community | Quick launch, generic workloads |
| **Custom AMIs** | Your own (created from instances) | Pre-configured, optimized |
| **AWS Marketplace** | Vendors | Licensed software (Windows, SQL, etc.) |

## Creating Custom AMIs

```bash
# Create AMI from existing EC2 instance
aws ec2 create-image \
  --instance-id i-12345 \
  --name "web-server-v1" \
  --description "Web server with nginx installed" \
  --no-reboot

# List AMIs
aws ec2 describe-images --image-ids ami-12345

# Find AMI by name
aws ec2 describe-images --filters "Name=name,Values=amzn2-ami-hvm*" --query 'Images[*].[ImageId,Name,Description]'

# Copy AMI to another region
aws ec2 copy-image \
  --source-image-id ami-12345 \
  --source-region us-east-1 \
  --region eu-west-1 \
  --name "web-server-eu"

# Deregister AMI
aws ec2 deregister-image --image-id ami-12345

# Share AMI with another account
aws ec2 modify-image-attribute \
  --image-id ami-12345 \
  --launch-permission "Add=[{UserId=123456789012}]"

# Make AMI public
aws ec2 modify-image-attribute \
  --image-id ami-12345 \
  --launch-permission "Add=[{Group=all}]"
```

## Exam Quick Reference
- ✅ **AMI** = OS + software template for EC2
- ✅ **Create AMI** from running/stopped instances
- ✅ **Copy AMI** across regions
- ✅ **Share AMI** with other accounts
- ✅ **Deregister AMI** when no longer needed
- ✅ **AMI = EBS snapshots** (each AMI includes EBS snapshots)
- ✅ **Permissions**: Private (default), Public, Shared
- ✅ **Cross-region**: Must copy AMI to use in another region