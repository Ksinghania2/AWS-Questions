# Elastic Load Balancing (ELB)

ELB automatically distributes incoming traffic across multiple targets (EC2, Lambda, IPs, containers).

## Types of Load Balancers

| Type | Layer | Protocol | Use Case |
|---|---|---|---|
| **ALB** (Application LB) | Layer 7 | HTTP, HTTPS, WebSocket | Web apps, microservices |
| **NLB** (Network LB) | Layer 4 | TCP, UDP, TLS | High-performance, static IP |
| **CLB** (Classic LB) | Layer 4/7 | HTTP, HTTPS, TCP, SSL | Legacy (not recommended) |
| **GWLB** (Gateway LB) | Layer 3 | IP | 3rd-party appliances (firewalls) |

## ALB (Application Load Balancer)

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name my-alb \
  --subnets subnet-12345 subnet-67890 \
  --security-groups sg-12345 \
  --scheme internet-facing

# Create target group
aws elbv2 create-target-group \
  --name my-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-12345 \
  --health-check-path /health

# Register targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:...:targetgroup/my-targets/abc \
  --targets Id=i-12345 Id=i-67890

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:...:loadbalancer/app/my-alb/abc \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...:targetgroup/my-targets/abc
```

## NLB (Network Load Balancer)

```bash
# Create NLB
aws elbv2 create-load-balancer \
  --name my-nlb \
  --type network \
  --subnets subnet-12345 subnet-67890 \
  --scheme internet-facing

# Create target group (IP type for static IP)
aws elbv2 create-target-group \
  --name my-nlb-targets \
  --protocol TCP \
  --port 80 \
  --target-type ip \
  --vpc-id vpc-12345
```

## Exam Quick Reference
- ✅ **ALB**: Layer 7, HTTP/HTTPS, path-based routing, host-based routing
- ✅ **NLB**: Layer 4, TCP/UDP, static IP, ultra-high performance
- ✅ **CLB**: Legacy, not recommended for new apps
- ✅ **GWLB**: Layer 3, for 3rd-party appliances
- ✅ **Target Groups**: EC2, Lambda, IP addresses, ECS tasks
- ✅ **Health Checks**: Monitor target health
- ✅ **Sticky Sessions**: Session affinity (ALB uses cookies)
- ✅ **Cross-zone LB**: Distribute traffic across all AZs
- ✅ **Connection Draining**: Complete in-flight requests before deregistering