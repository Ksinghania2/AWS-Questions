# Shared VPCs & AWS Resource Access Manager (RAM)

Shared VPCs allow multiple AWS accounts to centrally manage a VPC while sharing subnets with other accounts.

## What is a Shared VPC?

A shared VPC enables an account (owner) to share subnets with other accounts (participants) within the same AWS Organization. Participants can create resources in the shared subnets.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **VPC Owner** | Account that creates and manages the VPC |
| **Participant** | Account that uses shared subnets |
| **AWS RAM** | Resource Access Manager - service for sharing resources |
| **Organization** | AWS Organizations for multi-account management |

## Architecture

```
Account A (VPC Owner)
├── VPC (10.0.0.0/16)
│   ├── Public Subnet (shared via RAM)
│   ├── Private Subnet (shared via RAM)
│   └── Route Tables, NACLs, SGs (managed by owner)
│
Account B (Participant)
└── EC2 Instance (launched in shared subnet)
    └── Uses owner-managed routing, NACLs
```

## Sharing a VPC via AWS RAM

### Step 1: Create Resource Share
```bash
# Create a resource share in AWS RAM
aws ram create-resource-share \
    --name "Shared-VPC-Subnets" \
    --resource-arns arn:aws:ec2:us-east-1:123456789012:subnet/subnet-abc123 \
    --principals arn:aws:organizations::987654321098:organization/o-abc123def
```

### Step 2: Accept Invitation (if needed)
```bash
# Participant accepts the share
aws ram accept-resource-share-invitation \
    --resource-share-invitation-arn arn:aws:ram:us-east-1:987654321098:resource-share-invitation/abc123
```

### Step 3: Verify Shared Resources
```bash
# Owner: List resource shares
aws ram get-resource-shares \
    --resource-owner SELF \
    --name "Shared-VPC-Subnets"

# Participant: List shared resources
aws ram get-resource-share-invitations

# List resources in a share
aws ram list-resources \
    --resource-owner OTHER-ACCOUNTS \
    --resource-share-arn arn:aws:ram:us-east-1:123456789012:resource-share/abc123
```

## Participant Actions

### What Participants Can Do
```bash
# Launch EC2 in shared subnet
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.micro \
    --subnet-id subnet-abc123  # Shared subnet

# Create resources in shared subnets:
# - EC2 instances
# - RDS databases
# - ELB/ALB/NLB
# - Lambda functions
# - ECS tasks
# - Redshift clusters
```

### What Participants Cannot Do
```bash
# Cannot modify VPC-level resources
aws ec2 modify-vpc-attribute --vpc-id vpc-xxx  # DENIED
aws ec2 create-route-table --vpc-id vpc-xxx     # DENIED
aws ec2 create-subnet --vpc-id vpc-xxx          # DENIED
```

## Security Groups in Shared VPCs

```bash
# Participants can reference owner's security groups
aws ec2 authorize-security-group-ingress \
    --group-id sg-owner-managed \
    --protocol tcp \
    --port 443 \
    --source-group sg-participant-created
```

## CLI Examples

```bash
# List all shared subnets available to participant
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=vpc-abc123"

# Check if a subnet is shared
aws ec2 describe-subnets \
    --subnet-ids subnet-abc123 \
    --query 'Subnets[0].SubnetArn'

# List resource shares for a specific resource
aws ram list-resources \
    --resource-owner SELF \
    --resource-type "ec2:Subnet"
```

## Exam Tips

- ✅ **VPC Owner** manages routing, NACLs, security groups
- ✅ **Participants** launch resources but cannot modify VPC infrastructure
- ✅ **AWS RAM** is used to share subnets, not the entire VPC
- ✅ Participants must be in the **same AWS Organization**
- ✅ **Cross-account** security group references are supported
- ✅ **No charge** for sharing VPC subnets
- ✅ **Cannot share** default VPC subnets
- ✅ **100 subnets** max per VPC (shared or not)

## Q&A

**Q1: What service is used to share VPC subnets across accounts?**
A: AWS Resource Access Manager (RAM).

**Q2: Can a participant modify route tables in a shared VPC?**
A: No, only the VPC owner can modify VPC-level resources.

**Q3: What resources can participants launch in shared subnets?**
A: EC2, RDS, ELB, Lambda, ECS, Redshift, and other resources that require subnets.

**Q4: Do participants need to be in the same AWS Organization?**
A: Yes, VPC sharing requires AWS Organizations.

**Q5: Can you share a default VPC subnet?**
A: No, only custom VPC subnets can be shared.

**Q6: How does a participant accept a shared subnet invitation?**
A: Via `aws ram accept-resource-share-invitation`.

**Q7: Can participants reference the VPC owner's security groups?**
A: Yes, cross-account security group references are supported.

**Q8: What is the maximum number of subnets per VPC?**
A: 100 subnets per VPC (shared or not).

**Q9: Is there an additional cost for sharing VPC subnets?**
A: No, there is no charge for sharing VPC subnets.

**Q10: Can a participant delete the shared VPC?**
A: No, only the VPC owner can delete the VPC.