# VPC Lattice

VPC Lattice is a fully managed service for service-to-service networking, discovery, and monitoring across VPCs and accounts.

## What is VPC Lattice?

VPC Lattice enables you to connect, monitor, and secure connections between services across multiple VPCs and accounts without requiring VPC peering, Transit Gateway, or complex routing.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Service Network** | Logical grouping of services with shared access policies |
| **Service** | Individual application or microservice |
| **Target Group** | Group of compute resources (EC2, ECS, Lambda, IP) |
| **Listener** | Process that checks for connection requests |
| **Rule** | Routes requests based on path, method, header |
| **Auth Policy** | IAM-based authorization for service access |

## Architecture

```
Service Network (shared across VPCs)
├── Service: Order-Service
│   ├── Listener: HTTP:80
│   ├── Target Group: EC2 Instances
│   └── Auth Policy: Allow from Payment-Service
│
├── Service: Payment-Service  
│   ├── Listener: gRPC:50051
│   ├── Target Group: ECS Tasks
│   └── Auth Policy: Allow from API-Gateway
│
└── Service: Inventory-Service
    ├── Listener: HTTP:8080
    ├── Target Group: Lambda Functions
    └── Auth Policy: Allow from Order-Service
```

## CLI Examples

### Create Service Network
```bash
# Create a service network
aws vpc-lattice create-service-network \
    --name "MyServiceNetwork" \
    --auth-type AWS_IAM \
    --tags Key=Environment,Value=Production
```

### Create Service
```bash
# Create a service
aws vpc-lattice create-service \
    --name "OrderService" \
    --auth-type AWS_IAM \
    --certificate-arn arn:aws:acm:us-east-1:123456789012:certificate/abc123

# List services
aws vpc-lattice list-services
```

### Create Target Group
```bash
# Create target group for EC2 instances
aws vpc-lattice create-target-group \
    --name "Order-Targets" \
    --type INSTANCE \
    --config Port=8080,Protocol=HTTP,VpcIdentifier=vpc-12345678

# For Lambda targets
aws vpc-lattice create-target-group \
    --name "Lambda-Targets" \
    --type LAMBDA

# For IP targets
aws vpc-lattice create-target-group \
    --name "IP-Targets" \
    --type IP \
    --config Port=443,Protocol=HTTPS,VpcIdentifier=vpc-12345678
```

### Register Targets
```bash
# Register EC2 instances
aws vpc-lattice register-targets \
    --target-group-arn arn:aws:vpc-lattice:us-east-1:123456789012:targetgroup/tg-abc123 \
    --targets Id=i-1234567890abcdef0,Port=8080 \
              Id=i-0987654321fedcba0,Port=8080

# Register Lambda function
aws vpc-lattice register-targets \
    --target-group-arn arn:aws:vpc-lattice:us-east-1:123456789012:targetgroup/tg-lambda123 \
    --targets Id=arn:aws:lambda:us-east-1:123456789012:function:MyFunction
```

### Create Listener and Rules
```bash
# Create HTTP listener
aws vpc-lattice create-listener \
    --name "http-listener" \
    --service-arn arn:aws:vpc-lattice:us-east-1:123456789012:service/svc-abc123 \
    --protocol HTTP \
    --port 80 \
    --default-action Forward={TargetGroups=[{TargetGroupIdentifier=tg-abc123,Weight=100}]}

# Create rule for path-based routing
aws vpc-lattice create-rule \
    --name "order-rule" \
    --service-arn arn:aws:vpc-lattice:us-east-1:123456789012:service/svc-abc123 \
    --listener-arn arn:aws:vpc-lattice:us-east-1:123456789012:listener/listener-abc123 \
    --match HttpMatch={PathMatch={CaseSensitive=false,Match={Prefix=/api/orders}}} \
    --action Forward={TargetGroups=[{TargetGroupIdentifier=tg-abc123,Weight=100}]}
```

### Associate Service Network
```bash
# Associate VPC with service network
aws vpc-lattice create-service-network-vpc-association \
    --service-network-identifier sn-abc123 \
    --vpc-identifier vpc-12345678

# Associate service with service network
aws vpc-lattice create-service-network-service-association \
    --service-network-identifier sn-abc123 \
    --service-identifier svc-abc123
```

### Auth Policies
```bash
# Create auth policy for service
aws vpc-lattice put-auth-policy \
    --resource-identifier arn:aws:vpc-lattice:us-east-1:123456789012:service/svc-abc123 \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "vpc-lattice:Invoke",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:SourceOrgID": "o-abc123def"
                }
            }
        }]
    }'
```

## Monitoring

```bash
# List access logs for service
aws vpc-lattice get-access-log-subscription \
    --access-log-subscription-identifier als-abc123

# Create access log subscription
aws vpc-lattice create-access-log-subscription \
    --resource-identifier arn:aws:vpc-lattice:us-east-1:123456789012:service/svc-abc123 \
    --destination-arn arn:aws:s3:::my-lattice-logs
```

## Comparison: VPC Lattice vs Service Mesh

| Feature | VPC Lattice | App Mesh |
|---------|-------------|----------|
| **Scope** | Cross-VPC, Cross-account | Within ECS/EKS |
| **Protocols** | HTTP, HTTPS, gRPC | HTTP, gRPC, TCP |
| **Auth** | IAM-based | mTLS, IAM |
| **Discovery** | Built-in | Requires additional config |
| **Management** | Fully managed | Sidecar proxy (Envoy) |

## Exam Tips

- ✅ **VPC Lattice** is for service-to-service networking across VPCs
- ✅ Uses **IAM auth policies** for access control
- ✅ **No VPC peering or Transit Gateway required**
- ✅ Supports **EC2, ECS, EKS, Lambda, and IP targets**
- ✅ **Access logs** can be sent to S3, CloudWatch, Firehose
- ✅ **Auth type**: NONE (open) or AWS_IAM
- ✅ **Health checks** are automatic for registered targets
- ✅ **Weighted routing** supported across target groups

## Q&A

**Q1: What problem does VPC Lattice solve?**
A: Service-to-service connectivity across VPCs without requiring VPC peering or Transit Gateway.

**Q2: What are the target types supported by VPC Lattice?**
A: INSTANCE, IP, LAMBDA.

**Q3: How is access control managed in VPC Lattice?**
A: Via IAM-based auth policies attached to services or service networks.

**Q4: Can VPC Lattice connect services across AWS accounts?**
A: Yes, via service network associations.

**Q5: What protocols does VPC Lattice support?**
A: HTTP, HTTPS, and gRPC.

**Q6: How does VPC Lattice differ from VPC Peering?**
A: VPC Lattice is for service-level connectivity with built-in auth; VPC Peering is for network-level connectivity.

**Q7: Can VPC Lattice route to Lambda functions?**
A: Yes, Lambda is a supported target type.

**Q8: Where can VPC Lattice access logs be delivered?**
A: S3, CloudWatch Logs, or Kinesis Data Firehose.

**Q9: What is a Service Network in VPC Lattice?**
A: A logical grouping of services with shared access policies.

**Q10: Does VPC Lattice support weighted routing?**
A: Yes, for distributing traffic across target groups.