# AWS Site-to-Site VPN

AWS Site-to-Site VPN creates encrypted tunnels between your on-premises network and your VPC over the internet.

## What is Site-to-Site VPN?

A secure, encrypted connection between your on-premises network (or remote office) and your AWS VPC using IPsec tunnels.

## Key Components

| Component | Description |
|-----------|-------------|
| **Virtual Private Gateway (VGW)** | VPN concentrator on the AWS side |
| **Customer Gateway (CGW)** | Represents your on-premises router |
| **VPN Connection** | Logical connection between VGW and CGW |
| **VPN Tunnel** | Two encrypted IPsec tunnels (active/active or active/passive) |
| **Route Propagation** | Propagates VPN routes to VPC route tables |

## Architecture

```
On-Premises Data Center
    │
    ├── Customer Gateway (CGW)
    │   ├── Router/Firewall IP: 203.0.113.1
    │   │
    │   ├── IPSec Tunnel 1 (Active)
    │   │       │
    │   │       ▼
    │   │   Internet
    │   │       │
    │   │       ▼
    │   │   Virtual Private Gateway (VGW)
    │   │       │
    │   │       └── VPC Route Table (Propagated routes)
    │   │
    │   └── IPSec Tunnel 2 (Standby)
    │           │
    │           ▼
    │       Internet
    │           │
    │           ▼
    │       Virtual Private Gateway (VGW)
    │           │
    │           └── VPC Route Table (Propagated routes)
```

## CLI Examples

### Create Customer Gateway
```bash
# Create a customer gateway for on-premises router
aws ec2 create-customer-gateway \
    --type ipsec.1 \
    --public-ip 203.0.113.1 \
    --bgp-asn 65000 \
    --tag-specifications ResourceType=customer-gateway,Tags=[{Key=Name,Value=OnPrem-Router}]
```

### Create Virtual Private Gateway
```bash
# Create VPG with custom BGP ASN
aws ec2 create-vpn-gateway \
    --type ipsec.1 \
    --amazon-side-asn 64512 \
    --tag-specifications ResourceType=vpn-gateway,Tags=[{Key=Name,Value=Production-VPG}]

# Attach VPG to VPC
aws ec2 attach-vpn-gateway \
    --vpn-gateway-id vgw-12345678 \
    --vpc-id vpc-12345678
```

### Create VPN Connection
```bash
# Create VPN connection between VGW and CGW
aws ec2 create-vpn-connection \
    --type ipsec.1 \
    --customer-gateway-id cgw-12345678 \
    --vpn-gateway-id vgw-12345678 \
    --options '{
        "StaticRoutesOnly": false,
        "TunnelOptions": [
            {
                "TunnelInsideCidr": "169.254.10.0/30",
                "PreSharedKey": "MyPSKKey123!"
            },
            {
                "TunnelInsideCidr": "169.254.10.4/30",
                "PreSharedKey": "MyPSKKey456!"
            }
        ]
    }'
```

### Enable Route Propagation
```bash
# Propagate VPN routes to VPC route table
aws ec2 enable-vgw-route-propagation \
    --route-table-id rtb-12345678 \
    --gateway-id vgw-12345678
```

### Add Static Routes (for non-BGP)
```bash
# Create static route for VPN
aws ec2 create-vpn-connection-route \
    --vpn-connection-id vpn-12345678 \
    --destination-cidr-block 10.0.0.0/16
```

### Download VPN Configuration
```bash
# Download configuration for your router
aws ec2 describe-vpn-connections \
    --vpn-connection-ids vpn-12345678 \
    --query 'VpnConnections[0].CustomerGatewayConfiguration' \
    --output text > router-config.xml
```

### Monitor VPN Status
```bash
# Describe VPN connections
aws ec2 describe-vpn-connections \
    --vpn-connection-ids vpn-12345678

# Check tunnel status
aws ec2 describe-vpn-connections \
    --vpn-connection-ids vpn-12345678 \
    --query 'VpnConnections[0].VgwTelemetry'

# View CloudWatch metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/VPN \
    --metric-name TunnelState \
    --dimensions Name=VpnId,Value=vpn-12345678 \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 300 \
    --statistics Average
```

### Modify VPN Connection
```bash
# Modify VPN connection options
aws ec2 modify-vpn-connection \
    --vpn-connection-id vpn-12345678 \
    --options '{
        "TunnelOptions": [
            {"DPDTimeoutAction": "clear"}
        ]
    }'
```

### Delete VPN Connection
```bash
# Disable route propagation first
aws ec2 disable-vgw-route-propagation \
    --route-table-id rtb-12345678 \
    --gateway-id vgw-12345678

# Delete VPN connection
aws ec2 delete-vpn-connection \
    --vpn-connection-id vpn-12345678
```

## Dynamic Routing (BGP)

```bash
# Enable BGP route propagation
aws ec2 modify-vpn-connection \
    --vpn-connection-id vpn-12345678 \
    --options '{
        "StaticRoutesOnly": false
    }'

# View BGP status
# BGP exchanges routes automatically via the two tunnels
```

## Complete Setup Script

```bash
#!/bin/bash
# setup-vpn.sh
# Complete VPN setup script

VPC_ID="vpc-12345678"
ONPREM_IP="203.0.113.1"
BGP_ASN="65000"

# 1. Create Customer Gateway
CGW_ID=$(aws ec2 create-customer-gateway \
    --type ipsec.1 \
    --public-ip $ONPREM_IP \
    --bgp-asn $BGP_ASN \
    --query 'CustomerGateway.CustomerGatewayId' \
    --output text)

echo "Customer Gateway: $CGW_ID"

# 2. Create Virtual Private Gateway
VGW_ID=$(aws ec2 create-vpn-gateway \
    --type ipsec.1 \
    --query 'VpnGateway.VpnGatewayId' \
    --output text)

aws ec2 attach-vpn-gateway --vpn-gateway-id $VGW_ID --vpc-id $VPC_ID
echo "VPG: $VGW_ID attached to $VPC_ID"

# 3. Create VPN Connection
VPN_ID=$(aws ec2 create-vpn-connection \
    --type ipsec.1 \
    --customer-gateway-id $CGW_ID \
    --vpn-gateway-id $VGW_ID \
    --query 'VpnConnection.VpnConnectionId' \
    --output text)

echo "VPN Connection: $VPN_ID"

# 4. Download config
aws ec2 describe-vpn-connections \
    --vpn-connection-ids $VPN_ID \
    --query 'VpnConnections[0].CustomerGatewayConfiguration' \
    --output text > "${VPN_ID}-config.xml"

echo "Configuration saved to ${VPN_ID}-config.xml"
```

## Exam Tips

- ✅ **Two tunnels** per VPN connection for redundancy
- ✅ **BGP** enables dynamic route exchange (automatic)
- ✅ **Static routes** require manual configuration
- ✅ **Route propagation** must be enabled in VPC route tables
- ✅ **VPN supports** up to 1.25 Gbps per tunnel
- ✅ **ECMP** (Equal Cost Multi-Path) with two tunnels = 2.5 Gbps
- ✅ **Accelerated VPN** option for better performance via AWS Global Accelerator
- ✅ **CloudWatch metrics** available for monitoring
- ✅ **VPN cannot** directly access on-premises via Direct Connect (separate)
- ✅ **Maximum** 50 VPN connections per region (soft limit)

## Q&A

**Q1: How many tunnels does each VPN connection have?**
A: Two tunnels (IPsec) for redundancy.

**Q2: What is the difference between static routes and BGP?**
A: Static routes require manual configuration; BGP exchanges routes automatically.

**Q3: What is a Customer Gateway?**
A: Represents your on-premises router or firewall in AWS.

**Q4: What is a Virtual Private Gateway?**
A: The VPN concentrator on the AWS side of the VPN connection.

**Q5: How do you enable automatic route propagation from VPN?**
A: `aws ec2 enable-vgw-route-propagation --route-table-id rtb-xxx --gateway-id vgw-xxx`

**Q6: What is the bandwidth limit per VPN tunnel?**
A: Up to 1.25 Gbps (2.5 Gbps with ECMP across two tunnels).

**Q7: Can you download the VPN configuration for your router?**
A: Yes, using `aws ec2 describe-vpn-connections`.

**Q8: What monitoring metrics are available for VPN?**
A: TunnelState (0=DOWN, 1=UP) via CloudWatch.

**Q9: What is Accelerated VPN?**
A: Uses AWS Global Accelerator to improve VPN performance by optimizing the AWS-side path.

**Q10: How many VPN connections can you have per region?**
A: 50 (soft limit, can be increased).

**Q11: Can VPN and Direct Connect be used together?**
A: Yes, Direct Connect for primary, VPN as backup.

**Q12: What encryption does Site-to-Site VPN use?**
A: IPsec with AES 128-bit or 256-bit encryption.

**Q13: What is the default DPD timeout action?**
A: Clear (terminates the tunnel if peer is unreachable).

**Q14: Can you modify VPN tunnel options after creation?**
A: Yes, using `modify-vpn-connection`.

**Q15: What is ECMP in VPN context?**
A: Equal Cost Multi-Path - using both tunnels simultaneously for double bandwidth.