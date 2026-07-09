# Traffic Mirroring

Traffic Mirroring copies network traffic from Elastic Network Interfaces (ENIs) for advanced monitoring and security analysis.

## What is Traffic Mirroring?

Traffic Mirroring captures and inspects network traffic at scale without introducing agents or modifying the source instances. It copies traffic from source ENIs to target destinations for analysis.

## Use Cases

- **Security monitoring**: Detect anomalies, intrusions, malware
- **Content inspection**: Verify data in transit
- **Troubleshooting**: Debug network issues
- **Compliance**: Audit traffic for regulatory requirements
- **Performance monitoring**: Analyze application traffic patterns

## Architecture

```
Source (ENI) ────> Traffic Mirror Session ────> Target
                                                    │
                                                    ├── NLB (Network Load Balancer)
                                                    ├── ENI (Monitoring appliance)
                                                    └── GWLB (Gateway Load Balancer)
```

## Components

| Component | Description |
|-----------|-------------|
| **Source** | ENI(s) whose traffic is mirrored |
| **Target** | Destination for mirrored traffic (NLB, ENI, GWLB) |
| **Filter** | Rules defining which traffic to mirror |
| **Session** | Association between source, target, and filter |

## CLI Examples

### Create Traffic Mirror Filter
```bash
# Create filter for traffic mirroring
aws ec2 create-traffic-mirror-filter \
    --description "Capture all TCP traffic" \
    --tag-specifications ResourceType=traffic-mirror-filter,Tags=[{Key=Environment,Value=Production}]
```

### Add Filter Rules
```bash
# Add ingress rule (inbound traffic)
aws ec2 create-traffic-mirror-filter-rule \
    --traffic-mirror-filter-id tmf-12345678 \
    --traffic-direction ingress \
    --rule-number 10 \
    --rule-action accept \
    --protocol 6 \
    --destination-cidr-block 0.0.0.0/0 \
    --source-cidr-block 10.0.0.0/8 \
    --destination-port-range From=443,To=443

# Add egress rule (outbound traffic)
aws ec2 create-traffic-mirror-filter-rule \
    --traffic-mirror-filter-id tmf-12345678 \
    --traffic-direction egress \
    --rule-number 20 \
    --rule-action accept \
    --protocol 6 \
    --destination-cidr-block 0.0.0.0/0 \
    --source-cidr-block 0.0.0.0/0 \
    --source-port-range From=1024,To=65535

# Capture all traffic (no port restrictions)
aws ec2 create-traffic-mirror-filter-rule \
    --traffic-mirror-filter-id tmf-12345678 \
    --traffic-direction ingress \
    --rule-number 30 \
    --rule-action accept \
    --protocol 6 \
    --destination-cidr-block 0.0.0.0/0 \
    --source-cidr-block 0.0.0.0/0

# Remove a rule
aws ec2 delete-traffic-mirror-filter-rule \
    --traffic-mirror-filter-rule-id tfr-12345678
```

### Create Traffic Mirror Session
```bash
# Create a traffic mirror session
aws ec2 create-traffic-mirror-session \
    --description "Production monitoring" \
    --network-interface-id eni-12345678 \
    --traffic-mirror-target-id tmt-12345678 \
    --traffic-mirror-filter-id tmf-12345678 \
    --session-number 1 \
    --virtual-network-id 12345 \
    --packet-length 1500
```

### Create Traffic Mirror Target

#### Target Type: Network Load Balancer
```bash
# Create traffic mirror target for NLB
aws ec2 create-traffic-mirror-target \
    --description "NLB Target" \
    --network-load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/net/my-nlb/abc123 \
    --tag-specifications ResourceType=traffic-mirror-target,Tags=[{Key=Name,Value=NLB-Target}]
```

#### Target Type: ENI
```bash
# Create traffic mirror target for ENI
aws ec2 create-traffic-mirror-target \
    --description "Monitoring ENI" \
    --network-interface-id eni-98765432
```

#### Target Type: Gateway Load Balancer Endpoint
```bash
# Create traffic mirror target for GWLB endpoint
aws ec2 create-traffic-mirror-target \
    --description "GWLB Endpoint" \
    --gateway-load-balancer-endpoint-id gwlbe-12345678
```

### Describe and List
```bash
# List traffic mirror sessions
aws ec2 describe-traffic-mirror-sessions

# List traffic mirror targets
aws ec2 describe-traffic-mirror-targets

# List traffic mirror filters
aws ec2 describe-traffic-mirror-filters

# Describe specific session
aws ec2 describe-traffic-mirror-sessions \
    --traffic-mirror-session-ids tms-12345678
```

### Modify Session
```bash
# Update session (add description)
aws ec2 modify-traffic-mirror-session \
    --traffic-mirror-session-id tms-12345678 \
    --description "Updated monitoring session" \
    --session-number 2
```

### Clean Up
```bash
# Delete session first
aws ec2 delete-traffic-mirror-session \
    --traffic-mirror-session-id tms-12345678

# Delete target
aws ec2 delete-traffic-mirror-target \
    --traffic-mirror-target-id tmt-12345678

# Delete filter
aws ec2 delete-traffic-mirror-filter \
    --traffic-mirror-filter-id tmf-12345678
```

## Complete Example Script

```bash
#!/bin/bash
# setup-traffic-mirroring.sh
# Sets up traffic mirroring for an EC2 instance

INSTANCE_ID=$1
ENI_ID=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].NetworkInterfaces[0].NetworkInterfaceId' \
    --output text)

echo "Setting up traffic mirroring for instance $INSTANCE_ID"

# Create filter
FILTER_ID=$(aws ec2 create-traffic-mirror-filter \
    --description "Mirror all TCP traffic" \
    --query 'TrafficMirrorFilter.TrafficMirrorFilterId' \
    --output text)

# Add rules
aws ec2 create-traffic-mirror-filter-rule \
    --traffic-mirror-filter-id $FILTER_ID \
    --traffic-direction ingress \
    --rule-number 10 \
    --rule-action accept \
    --protocol 6 \
    --destination-cidr-block 0.0.0.0/0 \
    --source-cidr-block 0.0.0.0/0 > /dev/null

aws ec2 create-traffic-mirror-filter-rule \
    --traffic-mirror-filter-id $FILTER_ID \
    --traffic-direction egress \
    --rule-number 20 \
    --rule-action accept \
    --protocol 6 \
    --destination-cidr-block 0.0.0.0/0 \
    --source-cidr-block 0.0.0.0/0 > /dev/null

# Create target (NLB)
TARGET_ID=$(aws ec2 create-traffic-mirror-target \
    --description "Monitoring NLB" \
    --network-load-balancer-arn $NLB_ARN \
    --query 'TrafficMirrorTarget.TrafficMirrorTargetId' \
    --output text)

# Create session
SESSION_ID=$(aws ec2 create-traffic-mirror-session \
    --network-interface-id $ENI_ID \
    --traffic-mirror-target-id $TARGET_ID \
    --traffic-mirror-filter-id $FILTER_ID \
    --session-number 1 \
    --query 'TrafficMirrorSession.TrafficMirrorSessionId' \
    --output text)

echo "Traffic mirroring session $SESSION_ID created"
```

## Exam Tips

- ✅ **Traffic Mirroring copies traffic** from source ENIs to targets
- ✅ **Sources**: Any ENI in the VPC
- ✅ **Targets**: NLB, ENI, or GWLB Endpoint
- ✅ **Filters** define which traffic to capture (protocol, port, CIDR)
- ✅ **Session number** (1-32766) must be unique per source ENI
- ✅ **Packet length** can be specified (default is 1500 bytes)
- ✅ **VNI** (Virtual Network ID) helps identify mirrored traffic
- ✅ **No performance impact** on source instances (hardware-based)
- ✅ **Cannot mirror traffic** across VPC peering connections
- ✅ **Mirrored traffic** is not subject to security groups or NACLs

## Q&A

**Q1: What problem does Traffic Mirroring solve?**
A: It enables deep packet inspection and traffic analysis without installing agents on source instances.

**Q2: What are valid target types for traffic mirroring?**
A: NLB, ENI, or Gateway Load Balancer Endpoint.

**Q3: Can you filter which traffic is mirrored?**
A: Yes, using traffic mirror filters with rules for direction, protocol, ports, and CIDR ranges.

**Q4: What is the maximum session number?**
A: 32766 (1-32766 range).

**Q5: Does traffic mirroring impact source instance performance?**
A: No, it's hardware-based with no performance impact on source instances.

**Q6: Can you mirror traffic across VPC peering connections?**
A: No, traffic mirroring is limited to within a VPC.

**Q7: What is a Virtual Network ID (VNI)?**
A: An identifier to tag mirrored traffic for analysis purposes.

**Q8: Are mirrored packets subject to security groups?**
A: No, mirrored traffic bypasses security group and NACL evaluation.

**Q9: How do you specify which traffic to mirror?**
A: Through traffic mirror filter rules with direction, protocol, port range, and CIDR settings.

**Q10: What is the first step to configure traffic mirroring?**
A: Create a traffic mirror filter, then add filter rules.