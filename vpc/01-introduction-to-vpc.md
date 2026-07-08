# Introduction to Amazon VPC

Amazon Virtual Private Cloud (VPC) lets you provision a logically isolated section of AWS where you can launch resources in a virtual network you define.

## What is a VPC?

A VPC is a **virtual network** dedicated to your AWS account. It's logically isolated from other AWS virtual networks.

| Feature | Description |
|---|---|
| **Region-scoped** | A VPC exists within a single AWS region |
| **CIDR block** | You define the IP address range (e.g., 10.0.0.0/16) |
| **Subnets** | Divide VPC into subnets (AZ-specific) |
| **Route tables** | Control traffic routing between subnets and gateways |
| **Default VPC** | Automatically created in each region (unless deleted) |

## CLI Commands

```bash
# Create a VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16
# Output: VpcId: vpc-12345678

# Create a subnet
aws ec2 create-subnet --vpc-id vpc-12345678 --cidr-block 10.0.1.0/24

# List VPCs
aws ec2 describe-vpcs

# List subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-12345678"

# Delete VPC
aws ec2 delete-vpc --vpc-id vpc-12345678
```

## Python (boto3)

```python
import boto3

ec2 = boto3.client('ec2')

# Create VPC
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']
print(f"Created VPC: {vpc_id}")

# Create subnet
subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.1.0/24'
)
print(f"Created subnet: {subnet['Subnet']['SubnetId']}")

# List VPCs
vpcs = ec2.describe_vpcs()
print(f"Found {len(vpcs['Vpcs'])} VPCs:")
for v in vpcs['Vpcs']:
    print(f"  {v['VpcId']} - {v['CidrBlock']} - {'Default' if v.get('IsDefault') else 'Custom'}")
```

## Exam Quick Reference
- ✅ VPC = logically isolated virtual network
- ✅ Region-scoped (not global)
- ✅ CIDR block defines IP range (e.g., 10.0.0.0/16)
- ✅ Subnets are AZ-specific
- ✅ Default VPC exists in each region (can be deleted/recreated)
- ✅ Max 5 VPCs per region (soft limit, can be increased)