# VPC Endpoints & PrivateLink

**SAA-C03 Core Focus**: VPC Endpoints allow private access to AWS services without internet gateway, NAT, or VPN.

## Types of VPC Endpoints

| Type | Service | How it Works | Cost |
|---|---|---|---|
| **Gateway Endpoint** | S3, DynamoDB | Prefix-list in route table | **Free** |
| **Interface Endpoint** | Most AWS services | ENI with private IP | Per hour + per GB |
| **Gateway Load Balancer Endpoint** | 3rd-party appliances | Traffic to GWLB | Per hour |

## Gateway Endpoints (S3 & DynamoDB)

```
Private Subnet → Gateway Endpoint → S3/DynamoDB
(No internet required, no NAT needed)
```

```bash
# Create Gateway Endpoint for S3
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-12345

# Create Gateway Endpoint for DynamoDB
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.dynamodb \
  --route-table-ids rtb-12345

# Describe endpoints
aws ec2 describe-vpc-endpoints

# Delete endpoint
aws ec2 delete-vpc-endpoints --vpc-endpoint-ids vpce-12345
```

## Interface Endpoints (AWS PrivateLink)

```
Private Subnet → ENI (Private IP) → AWS Service
```

```bash
# Create Interface Endpoint for SSM
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.ssm \
  --subnet-ids subnet-12345 subnet-67890 \
  --security-group-ids sg-12345

# Create Interface Endpoint for CloudWatch Logs
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.logs \
  --subnet-ids subnet-12345 \
  --security-group-ids sg-12345
```

## Gateway Endpoint vs Interface Endpoint

| Feature | Gateway Endpoint | Interface Endpoint |
|---|---|---|
| **Services** | S3, DynamoDB only | 100+ AWS services |
| **How it works** | Route table prefix list | ENI + Private IP |
| **Cost** | **Free** | Per hour + data processing |
| **Security** | Bucket policy + IAM | Security Groups |
| **Cross-region** | ❌ No | ✅ Yes |
| **On-premises** | ❌ No (VPN/DX needed) | ✅ Yes (via VPN/DX) |
| **Private DNS** | ❌ Not needed | ✅ Auto-enabled |

## Exam Quick Reference
- ✅ **Gateway Endpoint**: Free, S3 & DynamoDB only, uses route table
- ✅ **Interface Endpoint**: Paid, 100+ services, uses ENI
- ✅ **Gateway Endpoint**: No internet/NAT needed for S3/DynamoDB access
- ✅ **Interface Endpoint**: Uses PrivateLink technology
- ✅ **Gateway Load Balancer Endpoint**: For 3rd-party appliances
- ✅ **Gateway Endpoint**: Accessible from on-premises via VPN/Direct Connect
- ✅ **Interface Endpoint**: Accessible from on-premises