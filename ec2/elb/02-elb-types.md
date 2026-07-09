# ELB Types (ALB, NLB, CLB, GWLB)

## Load Balancer Types
| Type | Layer | Protocol | Use Case |
|------|-------|----------|----------|
| **ALB** | L7 | HTTP/HTTPS/gRPC/WebSocket | Microservices, path-based routing |
| **NLB** | L4 | TCP/UDP/TLS | High throughput, static IP |
| **CLB** | L4/L7 | HTTP/HTTPS/TCP/SSL | Legacy (not recommended) |
| **GWLB** | L3 | IP | Third-party appliances (firewalls, IDS/IPS) |

## CLI
```bash
# Create ALB
aws elbv2 create-load-balancer --name my-alb --subnets subnet-xxx subnet-yyy --security-groups sg-xxx

# Create NLB
aws elbv2 create-load-balancer --name my-nlb --type network --subnets subnet-xxx subnet-yyy

# Create GWLB
aws elbv2 create-load-balancer --name my-gwlb --type gateway --subnets subnet-xxx

# Create target group
aws elbv2 create-target-group --name my-tg --protocol HTTP --port 80 --vpc-id vpc-xxx

# Register targets
aws elbv2 register-targets --target-group-arn arn:xxx --targets Id=i-xxx Id=i-yyy

# Create listener
aws elbv2 create-listener --load-balancer-arn arn:xxx --protocol HTTP --port 80 --default-actions Type=Forward,TargetGroupArn=arn:xxx
```

## Key Differences
| Feature | ALB | NLB | GWLB |
|---------|-----|-----|------|
| Static IP | No | Yes (per AZ) | No |
| SSL Termination | Yes | Yes (TLS) | No |
| Path-based routing | Yes | No | No |
| Host-based routing | Yes | No | No |
| WebSocket | Yes | No | No |
| gRPC | Yes | No | No |
| Preservation of client IP | No (unless X-Forwarded-For) | Yes | Yes |

## Q&A
**Q1: Which LB is best for microservices with path-based routing?** A: ALB (Layer 7).
**Q2: Which LB provides static IP addresses?** A: NLB (Network Load Balancer).
**Q3: What is GWLB used for?** A: Deploying third-party appliances (firewalls, IDS/IPS).
**Q4: Which LB supports WebSocket and gRPC?** A: ALB.
**Q5: Which LB preserves client IP by default?** A: NLB and GWLB.
