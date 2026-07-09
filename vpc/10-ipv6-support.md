# AWS IPv6 Support & Migrating from IPv4 to IPv6

AWS supports both IPv4 and IPv6 addressing. Understanding dual-stack networking is critical for the exam.

## IPv6 in VPC

### VPC IPv6 CIDR Blocks
```bash
# Associate an IPv6 CIDR block with a VPC
aws ec2 associate-vpc-cidr-block \
    --vpc-id vpc-12345678 \
    --amazon-provided-ipv6-cidr-block

# The IPv6 CIDR is auto-assigned (e.g., 2600:1f18:22a2:e300::/56)
```

### Subnet IPv6 CIDR
```bash
# Associate IPv6 CIDR with subnet
aws ec2 associate-subnet-cidr-block \
    --subnet-id subnet-12345678 \
    --ipv6-cidr-block 2600:1f18:22a2:e300::/64
```

## IPv6 Addressing Types

| Type | Description | Example |
|------|-------------|---------|
| **Global Unicast** | Internet-routable | `2600:1f18:22a2:e300::/64` |
| **Link-Local** | Local subnet only (FE80::/10) | `fe80::/10` |
| **EUI-64** | Auto-configured from MAC | `::abcd:12ff:fe34:5678` |

## Dual-Stack vs IPv6-Only

### Dual-Stack (Both IPv4 and IPv6)
```bash
# Create a dual-stack subnet
aws ec2 create-subnet \
    --vpc-id vpc-12345678 \
    --cidr-block 10.0.1.0/24 \
    --ipv6-cidr-block 2600:1f18:22a2:e300::/64

# Launch dual-stack EC2 instance
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.micro \
    --subnet-id subnet-12345678 \
    --associate-public-ip-address \
    --ipv6-address-count 1
```

### IPv6-Only Subnet
```bash
# Create IPv6-only subnet (no IPv4 CIDR)
aws ec2 create-subnet \
    --vpc-id vpc-12345678 \
    --ipv6-cidr-block 2600:1f18:22a2:e301::/64 \
    --ipv6-native

# Note: Not all services support IPv6-only
```

## Routing for IPv6

```bash
# Add IPv6 route to Internet Gateway
aws ec2 create-route \
    --route-table-id rtb-12345678 \
    --destination-ipv6-cidr-block ::/0 \
    --gateway-id igw-12345678

# Add IPv6 route to Egress-Only Internet Gateway
aws ec2 create-route \
    --route-table-id rtb-12345678 \
    --destination-ipv6-cidr-block ::/0 \
    --egress-only-internet-gateway-id eigw-12345678
```

## Egress-Only Internet Gateway (IPv6)

Unlike NAT Gateway (for IPv4), Egress-Only Internet Gateway allows outbound-only IPv6 traffic.

```bash
# Create Egress-Only Internet Gateway
aws ec2 create-egress-only-internet-gateway \
    --vpc-id vpc-12345678

# Attach to route table
aws ec2 create-route \
    --route-table-id rtb-12345678 \
    --destination-ipv6-cidr-block ::/0 \
    --egress-only-internet-gateway-id eigw-12345678
```

## Security Groups and NACLs for IPv6

```bash
# Security group rule for IPv6
aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,Ipv6Ranges=[{CidrIpv6=::/0}]

# NACL rule for IPv6
aws ec2 create-network-acl-entry \
    --network-acl-id acl-12345678 \
    --rule-number 100 \
    --protocol 6 \
    --rule-action allow \
    --egress \
    --cidr-block ::/0 \
    --port-range From=443,To=443
```

## DNS and IPv6

```bash
# Enable DNS resolution for IPv6 in VPC
aws ec2 modify-vpc-attribute \
    --vpc-id vpc-12345678 \
    --enable-dns-hostnames \
    --enable-dns-support

# Route53 AAAA record for IPv6
# aws route53 change-resource-record-sets --hosted-zone-id ZONEID --change-batch '{
#   "Changes": [{
#     "Action": "CREATE",
#     "ResourceRecordSet": {
#       "Name": "ipv6.example.com",
#       "Type": "AAAA",
#       "TTL": 300,
#       "ResourceRecords": [{"Value": "2600:1f18:22a2:e300::1"}]
#     }
#   }]
# }'
```

## Migration Strategies

### Strategy 1: Dual-Stack (Recommended)
```
1. Add IPv6 CIDR to existing VPC
2. Add IPv6 CIDR to existing subnets
3. Update route tables for IPv6
4. Update security groups/NACLs for IPv6
5. Update applications to support IPv6
```

### Strategy 2: New IPv6-Only VPC
```
1. Create new VPC with IPv6 CIDR
2. Create IPv6-only subnets
3. Migrate workloads
4. Decommission old IPv4 VPC
```

## Services Supporting IPv6

| Service | IPv6 Support |
|---------|-------------|
| EC2 | ✅ Dual-stack |
| VPC | ✅ Dual-stack, IPv6-only subnets |
| Internet Gateway | ✅ |
| Egress-Only IGW | ✅ (IPv6 only) |
| NAT Gateway | ❌ (IPv4 only) |
| ALB/NLB | ✅ Dual-stack |
| CloudFront | ✅ |
| Route53 | ✅ AAAA records |
| S3 | ✅ Dual-stack endpoints |
| Lambda | ✅ (VPC-enabled) |

## Exam Tips

- ✅ **IPv6 addresses are always public** (Global Unicast)
- ✅ **Egress-Only Internet Gateway** is the IPv6 equivalent of NAT Gateway
- ✅ **Dual-stack** means both IPv4 and IPv6 addresses
- ✅ **IPv6-only subnets** are possible but have service limitations
- ✅ **Security groups** support IPv6 CIDR notation
- ✅ **NAT Gateway does NOT support IPv6** - use Egress-Only IGW
- ✅ **IPv6 CIDR** is /56 for VPC, /64 for subnets
- ✅ **AWS provides** the IPv6 CIDR block automatically

## Q&A

**Q1: What is the IPv6 equivalent of a NAT Gateway?**
A: Egress-Only Internet Gateway.

**Q2: What is the default IPv6 CIDR size for a VPC?**
A: /56.

**Q3: What is the default IPv6 CIDR size for a subnet?**
A: /64.

**Q4: Can a NAT Gateway be used for IPv6 traffic?**
A: No, NAT Gateway only supports IPv4.

**Q5: What is a dual-stack subnet?**
A: A subnet that supports both IPv4 and IPv6 addressing.

**Q6: Are IPv6 addresses in AWS public or private?**
A: IPv6 Global Unicast addresses are public by default.

**Q7: How do you enable IPv6 for an existing VPC?**
A: Associate an IPv6 CIDR block using `aws ec2 associate-vpc-cidr-block --amazon-provided-ipv6-cidr-block`.

**Q8: What type of Route53 record is used for IPv6?**
A: AAAA record.

**Q9: Can security groups filter IPv6 traffic?**
A: Yes, using Ipv6Ranges in security group rules.

**Q10: What is the main limitation of IPv6-only subnets?**
A: Not all AWS services support IPv6-only; some require IPv4.