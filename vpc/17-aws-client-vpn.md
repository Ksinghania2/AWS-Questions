# AWS Client VPN

AWS Client VPN is a managed VPN service that allows users to securely connect to AWS or on-premises networks using a VPN client.

## What is Client VPN?

A managed OpenVPN-based service that lets users connect to AWS resources from anywhere using a VPN client application.

## Key Components

| Component | Description |
|-----------|-------------|
| **Client VPN Endpoint** | VPN server in the cloud |
| **Target Network** | Subnets to associate with the endpoint |
| **Authorization Rules** | Controls which users/groups can access which networks |
| **Client Certificate** | Certificate for client authentication |
| **Server Certificate** | Server certificate from ACM for the endpoint |
| **Route** | Networks accessible via the VPN |

## Architecture

```
User's Device (Anywhere)
    │
    ├── AWS Client VPN Application
    │   │
    │   ├── OpenVPN Tunnel (Encrypted)
    │   │       │
    │   │       ▼
    │   │   Internet
    │   │       │
    │   │       ▼
    │   │   Client VPN Endpoint
    │   │       │
    │   │       ├── Associated Subnet (ENI)
    │   │       │       │
    │   │       │       ├── VPC Resources (EC2, RDS, etc.)
    │   │       │       └── On-premises via VPC Peering/VPN/DX
    │   │       │
    │   │       └── Authentication
    │   │           ├── Certificate-based
    │   │           ├── SAML-based (AD, Okta)
    │   │           └── Mutual authentication
```

## Authentication Methods

| Method | Description |
|--------|-------------|
| **Certificate-based** | Client and server certificates |
| **SAML-based** | Federated auth (Active Directory, Okta, Azure AD) |
| **Mutual Authentication** | Both certificate and SAML/Active Directory |

## CLI Examples

### Create Server Certificate (ACM)
```bash
# Request or import server certificate in ACM
aws acm import-certificate \
    --certificate fileb://server.crt \
    --private-key fileb://server.key \
    --certificate-chain fileb://ca-chain.crt
```

### Create Client VPN Endpoint
```bash
# Create a Client VPN endpoint
aws ec2 create-client-vpn-endpoint \
    --client-cidr-range "10.200.0.0/16" \
    --server-certificate-arn arn:aws:acm:us-east-1:123456789012:certificate/abc123 \
    --authentication-options '[
        {
            "Type": "certificate-authentication",
            "MutualAuthentication": {
                "ClientRootCertificateChainArn": "arn:aws:acm:us-east-1:123456789012:certificate/def456"
            }
        }
    ]' \
    --connection-log-options '{
        "Enabled": true,
        "CloudwatchLogGroup": "client-vpn-logs",
        "CloudwatchLogStream": "connection-events"
    }' \
    --tag-specifications ResourceType=client-vpn-endpoint,Tags=[{Key=Name,Value=Production-VPN}]
```

### Associate Target Network
```bash
# Associate subnet with VPN endpoint
aws ec2 associate-client-vpn-target-network \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --subnet-id subnet-12345678
```

### Add Authorization Rule
```bash
# Allow full access to VPC
aws ec2 authorize-client-vpn-ingress \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --target-network-cidr 10.0.0.0/16 \
    --authorize-all-groups

# Allow specific group access to specific network
aws ec2 authorize-client-vpn-ingress \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --target-network-cidr 10.0.1.0/24 \
    --access-group-id "sg-12345678" \
    --description "Developers access to app subnet"
```

### Add Route
```bash
# Add route to VPC
aws ec2 create-client-vpn-route \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --destination-cidr 10.0.0.0/16 \
    --target-vpc-subnet-id subnet-12345678

# Add route to internet
aws ec2 create-client-vpn-route \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --destination-cidr 0.0.0.0/0 \
    --target-vpc-subnet-id subnet-12345678 \
    --description "Internet access via NAT"
```

### Export Client Configuration
```bash
# Download client configuration
aws ec2 export-client-vpn-client-configuration \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --output text > client-config.ovpn
```

### Manage Client Certificates
```bash
# Revoke a client certificate
aws ec2 revoke-client-vpn-ingress \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --target-network-cidr 10.0.0.0/16 \
    --revoke-all-groups
```

### Monitor and Describe
```bash
# Describe VPN endpoint
aws ec2 describe-client-vpn-endpoints \
    --client-vpn-endpoint-ids cvpn-endpoint-12345678

# Describe connections
aws ec2 describe-client-vpn-connections \
    --client-vpn-endpoint-id cvpn-endpoint-12345678

# Describe target networks
aws ec2 describe-client-vpn-target-networks \
    --client-vpn-endpoint-id cvpn-endpoint-12345678

# Describe routes
aws ec2 describe-client-vpn-routes \
    --client-vpn-endpoint-id cvpn-endpoint-12345678

# Describe authorization rules
aws ec2 describe-client-vpn-authorization-rules \
    --client-vpn-endpoint-id cvpn-endpoint-12345678
```

### Modify Endpoint
```bash
# Update authentication options
aws ec2 modify-client-vpn-endpoint \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --connection-log-options '{
        "Enabled": true,
        "CloudwatchLogGroup": "client-vpn-logs-updated"
    }'
```

### Delete
```bash
# Disassociate target networks first
aws ec2 disassociate-client-vpn-target-network \
    --client-vpn-endpoint-id cvpn-endpoint-12345678 \
    --association-id cvpn-assoc-12345678

# Delete the endpoint
aws ec2 delete-client-vpn-endpoint \
    --client-vpn-endpoint-id cvpn-endpoint-12345678
```

## SAML Authentication Setup

```bash
# Create endpoint with SAML authentication
aws ec2 create-client-vpn-endpoint \
    --client-cidr-range "10.200.0.0/16" \
    --server-certificate-arn arn:aws:acm:us-east-1:123456789012:certificate/abc123 \
    --authentication-options '[
        {
            "Type": "federated-authentication",
            "FederatedAuthentication": {
                "SAMLProviderArn": "arn:aws:iam::123456789012:saml-provider/MySAMLProvider",
                "SelfServiceSAMLProviderArn": "arn:aws:iam::123456789012:saml-provider/MySelfServiceSAML"
            }
        }
    ]' \
    --client-connect-handler-options '{
        "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:vpn-post-auth",
        "Enabled": true
    }'
```

## Exam Tips

- ✅ **Client VPN** is a managed OpenVPN-based service for individual users
- ✅ **Authentication**: Certificate-based, SAML, or mutual
- ✅ **Client CIDR range** must not overlap with VPC or on-premises
- ✅ **Target network association** creates an ENI in the subnet
- ✅ **Authorization rules** control access to specific networks
- ✅ **Routes** define reachable networks
- ✅ **Connection logging** is optional but recommended
- ✅ **Split-tunnel** vs full-tunnel options for routing
- ✅ **Client Connect Handler** Lambda for post-authentication actions
- ✅ **Self-service portal** for users to download configurations

## Q&A

**Q1: What is AWS Client VPN?**
A: A managed OpenVPN-based service for individual users to securely connect to AWS.

**Q2: What authentication methods does Client VPN support?**
A: Certificate-based, SAML-based (federated), and mutual authentication.

**Q3: What is the client CIDR range?**
A: An IP address range assigned to VPN clients (e.g., 10.200.0.0/16).

**Q4: How do you provide internet access to VPN clients?**
A: Add a route to 0.0.0.0/0 pointing to a subnet with a NAT Gateway.

**Q5: What is split-tunnel vs full-tunnel?**
A: Split-tunnel only routes VPC traffic through VPN; full-tunnel routes all traffic.

**Q6: How do users connect to Client VPN?**
A: Using the AWS Client VPN application (desktop/mobile) or any OpenVPN client.

**Q7: What is a Client Connect Handler?**
A: A Lambda function that runs after authentication to apply post-connection policies.

**Q8: How do you provide access to specific users only?**
A: Using authorization rules with access group IDs and security group references.

**Q9: What logs are available for Client VPN?**
A: Connection logs (connections, disconnections, errors) to CloudWatch.

**Q10: Can Client VPN connect to on-premises networks?**
A: Yes, if the VPC has connectivity to on-premises via VPN or Direct Connect.

**Q11: What is the self-service portal?**
A: A web portal where users can download their VPN configuration.

**Q12: How many subnets can be associated with a Client VPN endpoint?**
A: Each endpoint can be associated with multiple subnets for high availability.

**Q13: Can you update the authentication method after creation?**
A: Yes, using `modify-client-vpn-endpoint`.

**Q14: What happens to active connections when you delete an endpoint?**
A: All connections are terminated immediately.

**Q15: Is Client VPN region-specific?**
A: Yes, endpoints are created per-region and users connect to that region's endpoint.