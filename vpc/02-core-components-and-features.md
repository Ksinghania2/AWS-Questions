# VPC Core Components and Key Features

## Core Components

| Component | Description |
|---|---|
| **VPC** | Virtual network (CIDR block, region-scoped) |
| **Subnet** | AZ-specific IP range (public or private) |
| **Route Table** | Rules for traffic routing |
| **Internet Gateway** | Public internet access for VPC |
| **NAT Gateway/Instance** | Outbound internet for private subnets |
| **Security Group** | Instance-level firewall (stateful) |
| **NACL** | Subnet-level firewall (stateless) |
| **VPC Endpoint** | Private access to AWS services |
| **VPN Gateway** | Connect on-premises to VPC |

## Key Features

### CIDR Blocks
- Min: /28 (16 IPs)
- Max: /16 (65,536 IPs)
- Primary CIDR only (no changing after creation)
- Can add secondary CIDR blocks
- Cannot overlap with peered VPC CIDRs

### Tenancy
- **Default**: Shared hardware (multi-tenant)
- **Dedicated**: Your own hardware (single-tenant)

### DNS Settings
- `enableDnsSupport`: DNS resolution enabled
- `enableDnsHostnames`: Instances get public DNS hostnames

## CLI Commands

```bash
# Create VPC with DNS support
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 modify-vpc-attribute --vpc-id vpc-12345 --enable-dns-support "{\"Value\":true}"
aws ec2 modify-vpc-attribute --vpc-id vpc-12345 --enable-dns-hostnames "{\"Value\":true}"

# Create subnet (public)
aws ec2 create-subnet --vpc-id vpc-12345 --cidr-block 10.0.1.0/24
aws ec2 modify-subnet-attribute --subnet-id subnet-12345 --map-public-ip-on-launch

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id vpc-12345 --internet-gateway-id igw-12345

# Create route to IGW
aws ec2 create-route --route-table-id rtb-12345 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-12345

# Create default VPC
aws ec2 create-default-vpc

# Describe VPC attributes
aws ec2 describe-vpc-attribute --vpc-id vpc-12345 --attribute enableDnsSupport
```

## Python (boto3)

```python
import boto3

ec2 = boto3.client('ec2')

def create_complete_vpc(name, cidr_block='10.0.0.0/16'):
    """Create a VPC with all core components"""
    # Create VPC
    vpc = ec2.create_vpc(CidrBlock=cidr_block)
    vpc_id = vpc['Vpc']['VpcId']
    ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': name}])
    
    # Enable DNS
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    
    # Create Internet Gateway
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
    
    # Create public subnet
    subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24')
    subnet_id = subnet['Subnet']['SubnetId']
    ec2.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={'Value': True})
    
    # Create route table and add route to IGW
    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt['RouteTable']['RouteTableId']
    ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_id)
    
    print(f"VPC '{name}' created: {vpc_id}")
    return {'VpcId': vpc_id, 'SubnetId': subnet_id, 'IgwId': igw_id}

# Create VPC
vpc = create_complete_vpc('my-demo-vpc')
```

## Exam Quick Reference
- ✅ VPC has primary + optional secondary CIDR blocks
- ✅ Subnets are AZ-specific (one subnet = one AZ)
- ✅ Internet Gateway enables public internet access
- ✅ Security Groups = stateful instance firewall
- ✅ NACLs = stateless subnet firewall
- ✅ Default VPC simplifies quick starts
- ✅ Tenancy: Default vs Dedicated
- ✅ DNS attributes: enableDnsSupport, enableDnsHostnames