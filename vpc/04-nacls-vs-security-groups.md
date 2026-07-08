# NACLs vs Security Groups

| Feature | Security Group | NACL (Network ACL) |
|---|---|---|
| **Level** | Instance-level | Subnet-level |
| **State** | **Stateful** (return traffic auto-allowed) | **Stateless** (return traffic must be explicitly allowed) |
| **Rules** | Allow rules only | Allow **and** Deny rules |
| **Rule evaluation** | All rules evaluated | Rules evaluated in order (lowest number first) |
| **Default** | Deny all inbound, Allow all outbound | Allow all inbound, Allow all outbound |
| **Applies to** | Attached to ENI/instance | Attached to subnet |
| **Max rules** | 60 inbound + 60 outbound | 20 inbound + 20 outbound (customizable) |
| **Use case** | Instance-level firewalling | Subnet-level additional protection |

## Security Groups (Stateful)

```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Web server security group" \
  --vpc-id vpc-12345

# Add inbound rule (HTTP)
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Add inbound rule (HTTPS)
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Add inbound SSH from specific IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.0/32

# Reference another SG (allow traffic from app-sg)
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 8080 \
  --source-group sg-app

# Remove rule
aws ec2 revoke-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

## NACLs (Stateless)

```bash
# Create NACL
aws ec2 create-network-acl --vpc-id vpc-12345

# Add inbound rule (allow HTTP)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-12345 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=80,To=80 \
  --cidr-block 0.0.0.0/0 \
  --rule-action allow \
  --ingress

# Add **outbound** rule for return traffic (required because stateless)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-12345 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=1024,To=65535 \
  --cidr-block 0.0.0.0/0 \
  --rule-action allow \
  --egress

# Add deny rule (lower number = higher priority, evaluated first)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-12345 \
  --rule-number 10 \
  --protocol tcp \
  --port-range From=22,To=22 \
  --cidr-block 0.0.0.0/0 \
  --rule-action deny \
  --ingress

# Associate NACL with subnet
aws ec2 associate-network-acl \
  --network-acl-id acl-12345 \
  --subnet-id subnet-12345

# Describe NACL entries
aws ec2 describe-network-acls --network-acl-ids acl-12345
```

## Key Exam Difference: Stateful vs Stateless

### Security Group (Stateful)
```
Request: Client → :80 → EC2 (allowed)
Response: EC2 → :random → Client (auto-allowed ✅)
```

### NACL (Stateless)
```
Request: Client → :80 → EC2 (allowed)
Response: EC2 → :random → Client (DENIED ❌)
Response: EC2 → :random → Client (allowed only if ephemeral port rule exists)
```

## Python (boto3)

```python
import boto3

ec2 = boto3.client('ec2')

# Create Security Group with rules
def create_web_sg(vpc_id):
    """Create web security group with common rules"""
    sg = ec2.create_security_group(
        GroupName='web-sg',
        Description='Web server SG',
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']
    
    # Inbound rules
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '10.0.0.0/8'}]},
        ]
    )
    print(f"Security Group {sg_id} created with rules")
    return sg_id

def create_nacl_with_http(vpc_id, subnet_id):
    """Create NACL with HTTP allow and ephemeral port return"""
    nacl = ec2.create_network_acl(VpcId=vpc_id)
    nacl_id = nacl['NetworkAcl']['NetworkAclId']
    
    # Inbound: Allow HTTP
    ec2.create_network_acl_entry(
        NetworkAclId=nacl_id, RuleNumber=100, Protocol='6',
        PortRange={'From': 80, 'To': 80}, CidrBlock='0.0.0.0/0',
        RuleAction='allow', Egress=False
    )
    
    # Outbound: Allow return traffic (ephemeral ports)
    ec2.create_network_acl_entry(
        NetworkAclId=nacl_id, RuleNumber=100, Protocol='6',
        PortRange={'From': 1024, 'To': 65535}, CidrBlock='0.0.0.0/0',
        RuleAction='allow', Egress=True
    )
    
    # Associate with subnet
    ec2.associate_network_acl(NetworkAclId=nacl_id, SubnetId=subnet_id)
    print(f"NACL {nacl_id} associated with {subnet_id}")
    return nacl_id
```

## Exam Quick Reference
- ✅ **Security Groups**: Stateful, allow rules only, instance-level
- ✅ **NACLs**: Stateless, allow+deny rules, subnet-level
- ✅ **SG**: Return traffic auto-allowed (stateful)
- ✅ **NACL**: Must explicitly allow return traffic (stateless)
- ✅ **SG Rules**: All evaluated (no order)
- ✅ **NACL Rules**: Evaluated in number order (lowest first)
- ✅ **SG**: Default deny all inbound
- ✅ **NACL**: Default allow all inbound
- ✅ Use both together for defense-in-depth