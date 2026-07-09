# AMI Types

## Categories
| Type | Source | Use Case |
|------|--------|----------|
| Public | AWS/community | Quick launch |
| Private | Your account | Custom configs |
| Marketplace | Third-party | Licensed software |
| Custom | Created by you | Golden images |

## CLI
```bash
# Find public AMIs
aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*"

# Your AMIs
aws ec2 describe-images --owners self

# Create AMI
aws ec2 create-image --instance-id i-xxx --name "MyApp-v1" --no-reboot

# Copy to another region
aws ec2 copy-image --source-image-id ami-xxx --source-region us-east-1 --region eu-west-1

# Share with account
aws ec2 modify-image-attribute --image-id ami-xxx --launch-permission "Add={UserId=123456789012}"

# Deregister
aws ec2 deregister-image --image-id ami-xxx
```

## Q&A
**Q1: How to create a custom AMI?** A: `aws ec2 create-image --instance-id i-xxx --name "MyAMI"`.
**Q2: Can you share AMIs across accounts?** A: Yes, via modify-image-attribute.
**Q3: How to copy AMI to another region?** A: `aws ec2 copy-image --source-region us-east-1 --region eu-west-1`.
**Q4: What does --no-reboot do?** A: Creates AMI without stopping instance (faster but may affect consistency).
**Q5: Are AMIs regional or global?** A: Regional - must copy to use in other regions.
