# Amazon Route 53

Route 53 is a **DNS (Domain Name System) web service** that routes end users to AWS resources.

## Core Concepts

| Concept | Description |
|---|---|
| **Hosted Zone** | Container for DNS records (public or private) |
| **Record Set** | DNS record (A, AAAA, CNAME, Alias, MX, TXT, NS, SOA) |
| **Alias Record** | AWS-specific DNS record (maps to AWS resources) |
| **Routing Policy** | How Route 53 responds to queries |
| **Health Check** | Monitors endpoint health for DNS failover |
| **Traffic Flow** | Visual policy editor for complex routing |

## Record Types

| Type | Use Case |
|---|---|
| **A** | Maps domain to IPv4 address |
| **AAAA** | Maps domain to IPv6 address |
| **CNAME** | Maps domain to another domain (not for root domain) |
| **Alias** | Maps domain to AWS resource (ELB, CloudFront, S3) |
| **MX** | Mail exchange records |
| **TXT** | Text data (SPF, DKIM, verification) |
| **NS** | Name server records |

## Alias vs CNAME

| Feature | Alias | CNAME |
|---|---|---|
| **Root domain** | ✅ Yes (`example.com`) | ❌ No (only `www.example.com`) |
| **AWS resources** | ✅ Yes (ELB, CloudFront, S3, etc.) | ❌ No |
| **Free** | ✅ Yes (no charge) | ✅ Yes |
| **TTL** | Configurable | Configurable |

## CLI Commands

```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name example.com \
  --caller-reference $(date +%s)

# Create A record (simple routing)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456789 \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "www.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "203.0.113.10"}]
      }
    }]
  }'

# Create Alias record to ELB
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456789 \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "my-alb-12345.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'

# List hosted zones
aws route53 list-hosted-zones

# Get DNS records
aws route53 list-resource-record-sets --hosted-zone-id Z123456789
```

## Python (boto3)

```python
import boto3

route53 = boto3.client('route53')

def create_simple_record(domain, record_name, ip_address):
    """Create an A record pointing to an IP address"""
    # Get hosted zone by domain
    zones = route53.list_hosted_zones_by_name(DNSName=domain)
    zone_id = zones['HostedZones'][0]['Id']
    
    # Create record
    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',  # Create or update
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': ip_address}]
                }
            }]
        }
    )
    print(f"Created record {record_name} → {ip_address}")
    return response

def create_alias_record(domain, record_name, alias_target):
    """Create an alias record to an AWS resource"""
    zones = route53.list_hosted_zones_by_name(DNSName=domain)
    zone_id = zones['HostedZones'][0]['Id']
    
    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'A',
                    'AliasTarget': {
                        'HostedZoneId': alias_target['zone_id'],
                        'DNSName': alias_target['dns_name'],
                        'EvaluateTargetHealth': True
                    }
                }
            }]
        }
    )
    print(f"Created alias record {record_name}")
    return response
```

## Routing Policies

| Policy | Description | Use Case |
|---|---|---|
| **Simple** | Single record, random if multiple | Simple resolution |
| **Weighted** | % of traffic to each resource | A/B testing, canary |
| **Latency** | Route to lowest latency region | Global apps |
| **Failover** | Primary → Secondary on failure | Active-passive DR |
| **Geolocation** | Route based on user location | Regional content |
| **Geoproximity** | Route based on geographic distance | Traffic flow |
| **Multi-Value** | Return multiple healthy records | Simple load balancing |

## Exam Quick Reference
- ✅ **Route 53** = AWS DNS service
- ✅ **Alias records** = Free, for AWS resources, works with root domain
- ✅ **CNAME** = Cannot be used for root domain
- ✅ **Routing policies**: Simple, Weighted, Latency, Failover, Geolocation, Geoproximity, Multi-Value
- ✅ **Health checks** = Monitor endpoint health
- ✅ **DNS failover** = Route traffic away from unhealthy endpoints
- ✅ **53** = Traditional DNS port number