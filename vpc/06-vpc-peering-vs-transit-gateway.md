# VPC Peering vs AWS Transit Gateway

**SAA-C03 Core Focus**: Understand when to use VPC Peering vs Transit Gateway for connecting VPCs.

## Comparison

| Feature | VPC Peering | Transit Gateway |
|---|---|---|
| **Connection type** | Direct 1:1 connection | Hub-and-spoke |
| **Scalability** | Full mesh (N² connections) | Star topology (N connections) |
| **Transitive routing** | ❌ Not supported | ✅ Supported |
| **Cross-region** | ✅ Yes | ✅ Yes |
| **Cross-account** | ✅ Yes | ✅ Yes |
| **Bandwidth** | Up to 10 Gbps | Up to 50 Gbps (per VPC attachment) |
| **Cost** | Per GB data transfer | Per hour + per GB |
| **Route tables** | Manual per VPC | Centralized |
| **VPN integration** | ❌ No | ✅ Yes (VPN attachment) |
| **Direct Connect** | ❌ No | ✅ Yes |
| **Best for** | Few VPCs (2-5) | Many VPCs (5-5000+) |

## VPC Peering

```bash
# Create peering connection (requester)
aws ec2 create-vpc-peering-connection \
  --vpc-id vpc-12345 \
  --peer-vpc-id vpc-67890 \
  --peer-region us-west-2

# Accept peering connection (accepter)
aws ec2 accept-vpc-peering-connection \
  --vpc-peering-connection-id pcx-12345

# Add routes in both VPC route tables
aws ec2 create-route \
  --route-table-id rtb-12345 \
  --destination-cidr-block 10.1.0.0/16 \
  --vpc-peering-connection-id pcx-12345

aws ec2 create-route \
  --route-table-id rtb-67890 \
  --destination-cidr-block 10.0.0.0/16 \
  --vpc-peering-connection-id pcx-12345

# Describe peering connections
aws ec2 describe-vpc-peering-connections

# Delete peering connection
aws ec2 delete-vpc-peering-connection --vpc-peering-connection-id pcx-12345
```

## Transit Gateway

```bash
# Create Transit Gateway
aws ec2 create-transit-gateway \
  --description "Main TGW" \
  --amazon-side-asn 64512 \
  --options AutoAcceptSharedAttachments=enable

# Create VPC attachment
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id tgw-12345 \
  --vpc-id vpc-12345 \
  --subnet-ids subnet-12345 subnet-67890

# Create Transit Gateway route table
aws ec2 create-transit-gateway-route-table \
  --transit-gateway-id tgw-12345

# Create static route
aws ec2 create-transit-gateway-route \
  --transit-gateway-route-table-id tgw-rtb-12345 \
  --destination-cidr-block 10.0.0.0/8 \
  --transit-gateway-attachment-id tgw-attach-12345

# Describe transit gateways
aws ec2 describe-transit-gateways
```

## Exam Scenarios

| Scenario | Solution |
|---|---|
| **Connect 2 VPCs** | VPC Peering (simpler, cheaper) |
| **Connect 50 VPCs** | Transit Gateway (avoids N² complexity) |
| **Connect to on-premises** | Transit Gateway + VPN |
| **Need transitive routing** | Transit Gateway (VPC Peering doesn't support) |
| **Same region, few VPCs** | VPC Peering |
| **Hub-and-spoke architecture** | Transit Gateway |

## Exam Quick Reference
- ✅ **VPC Peering**: Direct 1:1, no transitive routing
- ✅ **Transit Gateway**: Hub-and-spoke, transitive routing
- ✅ **VPC Peering**: Best for 2-5 VPCs
- ✅ **Transit Gateway**: Best for 5-5000+ VPCs
- ✅ **VPC Peering**: Full mesh = N² connections
- ✅ **Transit Gateway**: Star = N connections
- ✅ Both support cross-region and cross-account
- ✅ **Transit Gateway** integrates with VPN and Direct Connect