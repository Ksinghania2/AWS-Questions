# AWS Direct Connect

AWS Direct Connect provides a dedicated private network connection from your on-premises data center to AWS, bypassing the public internet.

## What is Direct Connect?

A dedicated physical connection between your network and AWS, providing consistent network performance, lower latency, and higher security compared to internet-based connections.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **DX Location** | Physical facility where connection is established |
| **Virtual Interface (VIF)** | Logical interface over the physical connection |
| **Private VIF** | Connects to a VPC via Virtual Private Gateway |
| **Public VIF** | Connects to AWS public services (S3, DynamoDB) |
| **Transit VIF** | Connects to Transit Gateway for multi-VPC access |
| **Virtual Private Gateway** | VPN concentrator on the VPC side |
| **Direct Connect Gateway** | Global gateway for multiple VPCs/regions |
| **BFD** | Bidirectional Forwarding Detection for fast failover |

## Architecture

```
On-Premises Data Center
    │
    ├── Router
    │   │
    │   ├── Physical Connection (1Gbps/10Gbps/100Gbps)
    │   │       │
    │   │       ▼
    │   │   AWS Direct Connect Location
    │   │       │
    │   │       ├── Private VIF ──> Virtual Private Gateway ──> VPC
    │   │       ├── Public VIF  ──> AWS Public Services (S3, DynamoDB)
    │   │       └── Transit VIF ──> Direct Connect Gateway ──> Transit Gateway ──> Multiple VPCs
    │   │
    │   └── VPN Connection (Backup/Encrypted)
    │           │
    │           ▼
    │       Internet (Backup path)
```

## Connection Types

| Type | Bandwidth | Use Case |
|------|-----------|----------|
| **Dedicated** | 1 Gbps, 10 Gbps, 100 Gbps | High-volume, predictable workloads |
| **Hosted** | 50 Mbps - 10 Gbps | Lower bandwidth, flexible scaling |
| **MACsec** | 10 Gbps+ | Encryption at Layer 2 |

## CLI Examples

### Create Virtual Private Gateway
```bash
# Create VPG for VPC attachment
aws ec2 create-vpn-gateway \
    --type ipsec.1 \
    --amazon-side-asn 64512 \
    --tag-specifications ResourceType=vpn-gateway,Tags=[{Key=Name,Value=MyVPG}]

# Attach VPG to VPC
aws ec2 attach-vpn-gateway \
    --vpn-gateway-id vgw-12345678 \
    --vpc-id vpc-12345678
```

### Create Direct Connect Gateway
```bash
# Create Direct Connect Gateway
aws directconnect create-direct-connect-gateway \
    --direct-connect-gateway-name "MyDXGateway" \
    --amazon-side-asn 64512
```

### Create Virtual Interface (Private VIF)
```bash
# Create private VIF for VPC connection
aws directconnect create-private-virtual-interface \
    --connection-id dxcon-abc123 \
    --new-private-virtual-interface '{
        "virtualInterfaceName": "Private-VIF-Prod",
        "vlan": 100,
        "asn": 65000,
        "authKey": "bgp-password-123",
        "amazonAddress": "169.254.10.1/30",
        "customerAddress": "169.254.10.2/30",
        "virtualGatewayId": "vgw-12345678"
    }'
```

### Create Virtual Interface (Public VIF)
```bash
# Create public VIF for AWS public services
aws directconnect create-public-virtual-interface \
    --connection-id dxcon-abc123 \
    --new-public-virtual-interface '{
        "virtualInterfaceName": "Public-VIF",
        "vlan": 200,
        "asn": 65000,
        "authKey": "bgp-password-456",
        "amazonAddress": "169.254.20.1/30",
        "customerAddress": "169.254.20.2/30",
        "routeFilterPrefixes": [
            {"cidr": "203.0.113.0/24"},
            {"cidr": "198.51.100.0/24"}
        ]
    }'
```

### Create Transit VIF
```bash
# Create transit VIF for Transit Gateway
aws directconnect create-transit-virtual-interface \
    --connection-id dxcon-abc123 \
    --new-transit-virtual-interface '{
        "virtualInterfaceName": "Transit-VIF",
        "vlan": 300,
        "asn": 65000,
        "authKey": "bgp-password-789",
        "amazonAddress": "169.254.30.1/30",
        "customerAddress": "169.254.30.2/30",
        "directConnectGatewayId": "dxgw-12345678"
    }'
```

### Associate Direct Connect Gateway with VPG
```bash
# Associate DX Gateway with Virtual Private Gateway
aws directconnect create-direct-connect-gateway-association \
    --direct-connect-gateway-id dxgw-12345678 \
    --virtual-gateway-id vgw-12345678

# For Transit Gateway
aws directconnect create-direct-connect-gateway-association \
    --direct-connect-gateway-id dxgw-12345678 \
    --gateway-id tgw-12345678
```

### Describe Connections
```bash
# List Direct Connect connections
aws directconnect describe-connections

# Describe virtual interfaces
aws directconnect describe-virtual-interfaces

# Describe Direct Connect Gateways
aws directconnect describe-direct-connect-gateways

# Describe LAGs (Link Aggregation Groups)
aws directconnect describe-lags
```

### Create LAG (Link Aggregation Group)
```bash
# Create LAG to aggregate multiple connections
aws directconnect create-lag \
    --number-of-connections 2 \
    --connections-bandwidth "10Gbps" \
    --lag-name "Production-LAG" \
    --location "EqDC2"
```

### Enable MACsec
```bash
# Enable MACsec on a dedicated connection
aws directconnect update-connection \
    --connection-id dxcon-abc123 \
    --encryption-mode "should_encrypt"
```

## Direct Connect vs VPN

| Feature | Direct Connect | Site-to-Site VPN |
|---------|---------------|------------------|
| **Connection** | Dedicated physical line | Internet-based |
| **Bandwidth** | 50 Mbps - 100 Gbps | Up to 1.25 Gbps per tunnel |
| **Latency** | Consistent, low | Variable |
| **SLA** | 99.99% (with redundant connections) | 99.95% |
| **Encryption** | Optional (MACsec) | Always encrypted (IPsec) |
| **Setup time** | Weeks (physical installation) | Minutes |
| **Cost** | Higher (monthly port + data transfer) | Lower (hourly + data transfer) |
| **Use case** | Production, high-volume, latency-sensitive | Dev/test, backup, low-volume |

## Exam Tips

- ✅ **Direct Connect** provides dedicated, private connection to AWS
- ✅ **Private VIF** connects to a single VPC via Virtual Private Gateway
- ✅ **Public VIF** connects to AWS public services (S3, DynamoDB, EC2)
- ✅ **Transit VIF** connects to Transit Gateway for multi-VPC access
- ✅ **Direct Connect Gateway** enables access to VPCs in any region
- ✅ **LAG** aggregates multiple connections for higher bandwidth
- ✅ **MACsec** provides Layer 2 encryption
- ✅ **BFD** enables fast failover detection
- ✅ **VPN backup** is recommended for redundancy
- ✅ **Setup requires** weeks for physical installation

## Q&A

**Q1: What is AWS Direct Connect?**
A: A dedicated private network connection from on-premises to AWS, bypassing the public internet.

**Q2: What are the three types of virtual interfaces?**
A: Private VIF (VPC), Public VIF (AWS services), Transit VIF (Transit Gateway).

**Q3: What is a Direct Connect Gateway?**
A: A global gateway that allows access to VPCs in any AWS region.

**Q4: What is the difference between dedicated and hosted connections?**
A: Dedicated is a physical line (1/10/100 Gbps); hosted is provisioned by a partner (50 Mbps-10 Gbps).

**Q5: How do you increase bandwidth beyond a single connection?**
A: Use LAG (Link Aggregation Group) to aggregate multiple connections.

**Q6: What encryption option is available for Direct Connect?**
A: MACsec (Media Access Control Security) at Layer 2.

**Q7: What is a good backup for Direct Connect?**
A: A Site-to-Site VPN connection over the internet.

**Q8: How long does it typically take to set up Direct Connect?**
A: Weeks, due to physical installation and cross-connect provisioning.

**Q9: What is BFD in Direct Connect?**
A: Bidirectional Forwarding Detection for fast failover detection.

**Q10: Can Direct Connect access VPCs in multiple regions?**
A: Yes, using Direct Connect Gateway with Transit VIF and Transit Gateway.

**Q11: What is the bandwidth range for Direct Connect?**
A: 50 Mbps to 100 Gbps (hosted and dedicated).

**Q12: What SLA does Direct Connect offer?**
A: 99.99% with redundant connections.

**Q13: Can you use Direct Connect without a VPN?**
A: Yes, but a VPN backup is recommended for redundancy.

**Q14: What is a LAG?**
A: Link Aggregation Group - combines multiple connections for higher bandwidth and redundancy.

**Q15: What is the purpose of a Virtual Private Gateway?**
A: The VPN concentrator on the VPC side that terminates Private VIFs and VPN connections.