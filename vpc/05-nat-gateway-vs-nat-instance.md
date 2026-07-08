# NAT Gateway vs NAT Instance

**SAA-C03 Core Focus**: Understand when to use NAT Gateway vs NAT Instance for outbound internet access from private subnets.

## Comparison

| Feature | NAT Gateway | NAT Instance |
|---|---|---|
| **Type** | Managed AWS service | EC2 instance (AMI) |
| **Availability** | Highly available (per AZ) | Need to configure HA yourself |
| **Bandwidth** | Up to 45 Gbps | Depends on instance type |
| **Management** | Fully managed by AWS | You manage (patches, etc.) |
| **Cost** | Per hour + data processing | Per hour (instance cost) |
| **Security Groups** | Not supported | Supported |
| **NACLs** | Supported | Supported |
| **Elastic IP** | Auto-assigned (or choose) | Need to attach EIP |
| **Port forwarding** | Not supported | Supported |
| **Bastion host** | Not supported | Can be used as bastion |
| **Traffic metrics** | CloudWatch metrics | CloudWatch + instance metrics |

## NAT Gateway (Recommended)

```bash
# Create NAT Gateway (requires Elastic IP)
aws ec2 allocate-address --domain vpc
# Output: AllocationId: eipalloc-12345

aws ec2 create-nat-gateway \
  --subnet-id subnet-public \
  --allocation-id eipalloc-12345

# Add route from private subnet to NAT Gateway
aws ec2 create-route \
  --route-table-id rtb-private \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id nat-12345

# Describe NAT Gateways
aws ec2 describe-nat-gateways

# Delete NAT Gateway
aws ec2 delete-nat-gateway --nat-gateway-id nat-12345
# Release Elastic IP
aws ec2 release-address --allocation-id eipalloc-12345
```

## NAT Instance (Legacy)

```bash
# Launch NAT instance (using Amazon NAT AMI)
aws ec2 run-instances \
  --image-id ami-0cff7528ff583bf9a \  # Amazon Linux NAT AMI
  --instance-type t3.micro \
  --subnet-id subnet-public \
  --associate-public-ip-address

# Disable source/destination check (required for NAT)
aws ec2 modify-instance-attribute \
  --instance-id i-12345 \
  --source-dest-check "{\"Value\": false}"

# Add route from private subnet to NAT instance
aws ec2 create-route \
  --route-table-id rtb-private \
  --destination-cidr-block 0.0.0.0/0 \
  --instance-id i-12345
```

## Python (boto3)

```python
import boto3

ec2 = boto3.client('ec2')

def create_nat_gateway_setup(vpc_id, public_subnet_id, private_rt_id):
    """Create NAT Gateway and configure routing"""
    # Allocate Elastic IP
    eip = ec2.allocate_address(Domain='vpc')
    eip_id = eip['AllocationId']
    
    # Create NAT Gateway
    nat = ec2.create_nat_gateway(
        SubnetId=public_subnet_id,
        AllocationId=eip_id
    )
    nat_id = nat['NatGateway']['NatGatewayId']
    print(f"NAT Gateway created: {nat_id}")
    
    # Add route from private subnet to NAT
    ec2.create_route(
        RouteTableId=private_rt_id,
        DestinationCidrBlock='0.0.0.0/0',
        NatGatewayId=nat_id
    )
    print(f"Route added to private RT: 0.0.0.0/0 → NAT Gateway")
    
    return {'NatGatewayId': nat_id, 'AllocationId': eip_id}
```

## Exam Scenarios

| Scenario | Solution |
|---|---|
| **Private subnet needs internet access** | NAT Gateway in public subnet |
| **High availability required** | NAT Gateway in each AZ |
| **Need to use as bastion host** | NAT Instance (NAT Gateway doesn't support SSH) |
| **Low cost, small workload** | NAT Instance (cheaper for low traffic) |
| **Managed solution, no maintenance** | NAT Gateway |
| **Port forwarding needed** | NAT Instance |

## Exam Quick Reference
- ✅ **NAT Gateway**: Managed, HA, up to 45 Gbps, per-AZ
- ✅ **NAT Instance**: Self-managed, can be bastion, supports port forwarding
- ✅ **NAT Gateway** is the recommended solution
- ✅ **NAT Instance** requires disabling source/destination check
- ✅ **NAT Gateway** is AZ-specific (create one per AZ for HA)
- ✅ **NAT Gateway** cannot be used as a bastion host
- ✅ **NAT Instance** can be used as a bastion host
- ✅ Both provide outbound internet to private subnets