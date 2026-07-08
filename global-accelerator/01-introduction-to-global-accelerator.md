# AWS Global Accelerator

AWS Global Accelerator improves the **availability and performance** of applications by using the AWS global network to route traffic.

## How It Works

```
User → Internet → AWS Edge Location (Anycast) → AWS Global Network → Application (ALB/NLB/EC2)
```

Instead of: `User → Internet → Application` (slower, less reliable)

## Key Features

| Feature | Description |
|---|---|
| **Anycast IP** | Two static IP addresses (or bring your own) |
| **Edge locations** | Traffic enters at the closest edge location |
| **AWS Global Network** | Traffic travels on AWS backbone (not public internet) |
| **Health checks** | Automatic failover to healthy endpoints |
| **Traffic dials** | Control traffic % per endpoint group |
| **Accelerator** | Improves performance for TCP/UDP traffic |

## Global Accelerator vs CloudFront

| Feature | Global Accelerator | CloudFront |
|---|---|---|
| **Protocol** | TCP/UDP (all traffic) | HTTP/HTTPS, WebSocket |
| **Use case** | Non-HTTP apps, gaming, VoIP | Static content, API caching |
| **Caching** | ❌ No caching | ✅ Edge caching |
| **Static IP** | ✅ 2 static IPs | ❌ No static IP (uses domain) |
| **DDoS protection** | ✅ AWS Shield | ✅ AWS Shield |
| **Best for** | Global TCP/UDP apps | Content delivery |

## CLI Commands

```bash
# Create accelerator
aws globalaccelerator create-accelerator \
  --name MyAccelerator \
  --ip-address-type IPV4

# Create listener (TCP port 80)
aws globalaccelerator create-listener \
  --accelerator-arn arn:aws:globalaccelerator::123456789012:accelerator/abc123 \
  --port-ranges FromPort=80,ToPort=80 \
  --protocol TCP

# Create endpoint group
aws globalaccelerator create-endpoint-group \
  --listener-arn arn:aws:globalaccelerator::...:listener/abc123 \
  --endpoint-group-region us-east-1 \
  --endpoint-configurations '[{
    "EndpointId": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/abc123",
    "Weight": 100
  }]'

# List accelerators
aws globalaccelerator list-accelerators

# Describe accelerator
aws globalaccelerator describe-accelerator \
  --accelerator-arn arn:aws:globalaccelerator::...:accelerator/abc123
```

## Exam Scenarios

| Scenario | Solution |
|---|---|
| **Global user base, need low latency** | Global Accelerator |
| **Non-HTTP protocol (gaming, VoIP)** | Global Accelerator (CloudFront is HTTP only) |
| **Need static IP for whitelisting** | Global Accelerator (2 static IPs) |
| **HTTP/HTTPS content delivery** | CloudFront (caching, edge compute) |
| **Disaster recovery failover** | Global Accelerator (health check failover) |

## Exam Quick Reference
- ✅ **Anycast IP** = 2 static IPs (or BYOIP)
- ✅ **TCP/UDP** support (not just HTTP)
- ✅ **AWS Global Network** = faster, more reliable
- ✅ **Health checks** = automatic failover
- ✅ **Traffic dials** = control traffic % per region
- ✅ **No caching** (unlike CloudFront)
- ✅ **DDoS protection** via AWS Shield
- ✅ **Best for**: Gaming, VoIP, IoT, non-HTTP apps