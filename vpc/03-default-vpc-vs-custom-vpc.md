# Default VPC vs Custom VPC vs Shared VPCs

## Default VPC

Automatically created in each region when you create an AWS account.

| Feature | Default VPC |
|---|---|
| **CIDR** | Always 172.31.0.0/16 |
| **Subnets** | One /20 subnet per AZ |
| **Internet Gateway** | Pre-created and attached |
| **Route Table** | Pre-configured with IGW route |
| **Security Group** | Default SG (allows all outbound, no inbound) |
| **NACL** | Default (allows all traffic) |

```bash
# Check if default VPC exists
aws ec2 describe-account-attributes --attribute-names default-vpc

# Create default VPC (if deleted)
aws ec2 create-default-vpc

# Delete default VPC
aws ec2 delete-vpc --vpc-id vpc-xxxxx
```

## Custom VPC

You create and configure manually (more control).

| Feature | Custom VPC |
|---|---|
| **CIDR** | Choose your own (10.0.0.0/16, etc.) |
| **Subnets** | You create and configure |
| **Internet Gateway** | You create and attach |
| **Route Table** | You configure routes |
| **NAT Gateway** | You create for private subnets |
| **VPC Endpoints** | You create for private AWS access |

```bash
# Create custom VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16
```

## Shared VPCs (AWS RAM)

Share subnets across AWS accounts using AWS Resource Access Manager (RAM).

### Benefits
- Centralized control of VPC resources
- Separate accounts for workload isolation
- Shared subnets = shared route tables, NACLs, SGs

```bash
# Create a resource share for subnet
aws ram create-resource-share \
  --name "SharedVPCSubnet" \
  --resource-arns arn:aws:ec2:us-east-1:123456789012:subnet/subnet-12345 \
  --principals arn:aws:iam::987654321012:root
```

## Exam Quick Reference
- ✅ Default VPC = pre-created, 172.31.0.0/16, has IGW
- ✅ Custom VPC = manual creation, full control
- ✅ Share VPC subnets via AWS RAM
- ✅ Default VPC can be deleted and recreated
- ✅ Each region has its own default VPC
- ✅ Max 5 VPCs per region (custom)