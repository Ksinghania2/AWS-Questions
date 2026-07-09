# AWS Network Firewall

AWS Network Firewall is a managed firewall service that provides network traffic filtering for VPCs, including stateful inspection, intrusion prevention, and web filtering.

## What is AWS Network Firewall?

A managed service that filters traffic at the VPC perimeter with stateful and stateless rules, supporting thousands of rules with automatic scaling.

## Key Features

- **Stateful inspection**: Track connection state (like security groups)
- **Stateless rules**: Fast, simple allow/deny (like NACLs)
- **Intrusion Prevention System (IPS)**: Detect and block exploits
- **Web filtering**: Filter by URL, domain, HTTP headers
- **TLS inspection**: Decrypt and inspect encrypted traffic
- **Centralized management**: Across multiple VPCs and accounts

## Architecture

```
Internet
    │
    ▼
Internet Gateway
    │
    ▼
AWS Network Firewall (Firewall Endpoint)
    │
    ├── Stateless Rules (fast path)
    │   ├── Allow trusted IPs
    │   ├── Block known bad IPs
    │   └── Forward to stateful
    │
    ├── Stateful Rules (deep inspection)
    │   ├── Suricata-compatible IPS rules
    │   ├── Domain/URL filtering
    │   └── Protocol detection
    │
    ▼
Protected VPC Subnets
```

## Components

| Component | Description |
|-----------|-------------|
| **Firewall** | Top-level resource associating policy with VPC |
| **Firewall Policy** | Set of stateless + stateful rule groups |
| **Stateless Rule Group** | Fast, simple allow/deny rules (priority-based) |
| **Stateful Rule Group** | Deep packet inspection rules |
| **Rule Group** | Collection of firewall rules |
| **Firewall Endpoint** | ENI in a subnet for traffic inspection |

## CLI Examples

### Create Stateless Rule Group
```bash
# Create stateless rule group
aws network-firewall create-rule-group \
    --rule-group-name "Block-Bad-IPs" \
    --type STATELESS \
    --capacity 100 \
    --rule-group '{
        "RulesSource": {
            "StatelessRulesAndCustomActions": {
                "StatelessRules": [{
                    "RuleDefinition": {
                        "MatchAttributes": {
                            "Sources": [{"AddressDefinition": "10.0.0.0/8"}],
                            "Destinations": [{"AddressDefinition": "0.0.0.0/0"}],
                            "Protocols": [6],
                            "DestinationPorts": [{"FromPort": 443, "ToPort": 443}]
                        },
                        "Actions": ["aws:pass"]
                    },
                    "Priority": 1
                }]
            }
        }
    }'
```

### Create Stateful Rule Group (Domain Filter)
```bash
# Create stateful rule group for domain filtering
aws network-firewall create-rule-group \
    --rule-group-name "Domain-Filter" \
    --type STATEFUL \
    --capacity 100 \
    --rule-group '{
        "RulesSource": {
            "RulesString": "pass tcp $HOME_NET any -> $EXTERNAL_NET 443 (msg:\"Allow trusted domains\"; content:\".mycompany.com\"; nocase; sid:1;)"
        }
    }'
```

### Create Stateful Rule Group (IPS)
```bash
# Create stateful rule group with Suricata rules
aws network-firewall create-rule-group \
    --rule-group-name "IPS-Rules" \
    --type STATEFUL \
    --capacity 1000 \
    --rule-group '{
        "RulesSource": {
            "RulesString": "drop tcp $HOME_NET any -> $EXTERNAL_NET 80 (msg:\"Block HTTP\"; sid:100;)"
        }
    }'
```

### Create Firewall Policy
```bash
# Create firewall policy
aws network-firewall create-firewall-policy \
    --firewall-policy-name "Production-Policy" \
    --firewall-policy '{
        "StatelessDefaultActions": ["aws:forward_to_sfe"],
        "StatelessFragmentDefaultActions": ["aws:forward_to_sfe"],
        "StatelessRuleGroupReferences": [{
            "ResourceArn": "arn:aws:network-firewall:us-east-1:123456789012:stateless-rulegroup/Block-Bad-IPs",
            "Priority": 10
        }],
        "StatefulRuleGroupReferences": [{
            "ResourceArn": "arn:aws:network-firewall:us-east-1:123456789012:stateful-rulegroup/Domain-Filter"
        }]
    }'
```

### Create Firewall
```bash
# Create firewall in a VPC
aws network-firewall create-firewall \
    --firewall-name "Production-Firewall" \
    --firewall-policy-arn arn:aws:network-firewall:us-east-1:123456789012:firewall-policy/Production-Policy \
    --vpc-id vpc-12345678 \
    --subnet-mappings SubnetId=subnet-abc123 \
    --description "Production VPC firewall"
```

### Update Firewall Policy
```bash
# Associate new policy with firewall
aws network-firewall associate-firewall-policy \
    --firewall-name "Production-Firewall" \
    --firewall-policy-arn arn:aws:network-firewall:us-east-1:123456789012:firewall-policy/Updated-Policy
```

### Logging Configuration
```bash
# Enable flow logs to S3
aws network-firewall update-logging-configuration \
    --firewall-name "Production-Firewall" \
    --logging-configuration '{
        "LogDestinationConfigs": [{
            "LogType": "FLOW",
            "LogDestinationType": "S3",
            "LogDestination": {"bucketName": "my-firewall-logs"}
        }]
    }'

# Enable alert logs to CloudWatch
aws network-firewall update-logging-configuration \
    --firewall-name "Production-Firewall" \
    --logging-configuration '{
        "LogDestinationConfigs": [{
            "LogType": "ALERT",
            "LogDestinationType": "CloudWatchLogs",
            "LogDestination": {"logGroup": "firewall-alerts"}
        }]
    }'
```

### List and Describe
```bash
# List firewalls
aws network-firewall list-firewalls

# Describe firewall
aws network-firewall describe-firewall \
    --firewall-name "Production-Firewall"

# List rule groups
aws network-firewall list-rule-groups

# Describe rule group
aws network-firewall describe-rule-group \
    --rule-group-name "Domain-Filter" \
    --type STATEFUL
```

## Stateless vs Stateful Rules

| Feature | Stateless | Stateful |
|---------|-----------|----------|
| **Performance** | Very fast | Deep inspection |
| **State tracking** | No | Yes (TCP/UDP/ICMP) |
| **Rule types** | Simple allow/deny | Suricata compatible |
| **Capacity** | Higher | Lower per rule group |
| **Use case** | Known bad IPs, high-volume | IPS, content filtering |
| **Default action** | Required | Optional |

## Exam Tips

- ✅ **AWS Network Firewall** is a managed firewall service for VPCs
- ✅ **Stateless rules** are evaluated first (priority order)
- ✅ **Stateful rules** use Suricata-compatible format
- ✅ **Default actions** required for stateless (forward to stateful, drop, pass)
- ✅ **Logging** supports FLOW and ALERT logs to S3, CloudWatch, Firehose
- ✅ **Capacity** determines max rules in a rule group
- ✅ **Firewall endpoint** is deployed in a VPC subnet
- ✅ **Automatic scaling** based on traffic volume
- ✅ **TLS inspection** requires importing certificates
- ✅ **Centralized management** via AWS Firewall Manager

## Q&A

**Q1: What is AWS Network Firewall?**
A: A managed firewall service providing stateful and stateless traffic filtering for VPCs.

**Q2: What rule format does stateful inspection use?**
A: Suricata-compatible rules format.

**Q3: What is the difference between stateless and stateful rules?**
A: Stateless is fast, simple allow/deny without state tracking; stateful provides deep packet inspection with connection tracking.

**Q4: What log types does AWS Network Firewall support?**
A: FLOW logs (all traffic) and ALERT logs (rule matches).

**Q5: Where can logs be sent?**
A: S3, CloudWatch Logs, or Kinesis Data Firehose.

**Q6: What is a firewall endpoint?**
A: An ENI deployed in a VPC subnet that processes traffic.

**Q7: Can AWS Network Firewall inspect TLS traffic?**
A: Yes, with TLS inspection configured using imported certificates.

**Q8: How does capacity work in rule groups?**
A: Capacity defines the maximum number of rules; more complex rules consume more capacity.

**Q9: What are the default actions for stateless rules?**
A: `aws:forward_to_sfe` (send to stateful), `aws:pass` (allow), `aws:drop` (deny).

**Q10: Can AWS Network Firewall be centrally managed?**
A: Yes, via AWS Firewall Manager across multiple accounts and VPCs.