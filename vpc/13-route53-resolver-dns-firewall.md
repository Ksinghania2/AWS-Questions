# Route53 Resolver DNS Firewall

Route53 Resolver DNS Firewall provides DNS-level filtering to protect your VPCs from DNS-based threats.

## What is DNS Firewall?

DNS Firewall filters DNS queries originating from your VPC. It allows you to control which domains your resources can resolve, blocking access to known malicious domains.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Domain List** | Collection of domains to allow or block |
| **Rule Group** | Set of rules with domain lists and actions |
| **Rule** | Association between domain list and action (ALLOW, BLOCK, ALERT) |
| **Firewall Association** | Links rule group to a VPC |
| **Query Logs** | Logs of DNS queries for analysis |

## Architecture

```
VPC
├── EC2 Instance ──> DNS Query ──> Route53 Resolver
│                                      │
│                                      ├── DNS Firewall
│                                      │   ├── Rule Group
│                                      │   │   ├── Block malicious domains
│                                      │   │   ├── Allow trusted domains
│                                      │   │   └── Alert on suspicious
│                                      │   │
│                                      │   └── Query Logs → S3/CloudWatch
│                                      │
│                                      └── Resolved DNS → EC2 Instance
```

## CLI Examples

### Create Domain List
```bash
# Create a domain list for blocking malicious domains
aws route53resolver create-firewall-domain-list \
    --name "Malicious-Domains" \
    --domains "malware.example.com" "phishing.example.com" "c2.example.com"

# Create a domain list for allowing trusted domains
aws route53resolver create-firewall-domain-list \
    --name "Corporate-Whitelist" \
    --domains "mycompany.com" "partner.com" "sso.example.com"
```

### Import Domains from File
```bash
# Create domain list from file
aws route53resolver import-firewall-domains \
    --firewall-domain-list-arn arn:aws:route53resolver:us-east-1:123456789012:firewall-domain-list/rdl-abc123 \
    --operation REPLACE \
    --file-url "s3://my-dns-lists/malicious-domains.txt"
```

### Create Rule Group
```bash
# Create a rule group
aws route53resolver create-firewall-rule-group \
    --name "Production-DNS-Filter" \
    --rules '[
        {
            "Name": "Block-Malicious",
            "Action": "BLOCK",
            "BlockResponse": "NXDOMAIN",
            "FirewallDomainListId": "rdl-abc123",
            "Priority": 10
        },
        {
            "Name": "Alert-Suspicious",
            "Action": "ALERT",
            "FirewallDomainListId": "rdl-def456",
            "Priority": 20
        }
    ]'
```

### Add Rules to Rule Group
```bash
# Add a block rule
aws route53resolver create-firewall-rule \
    --firewall-rule-group-id rfg-abc123 \
    --firewall-domain-list-id rdl-abc123 \
    --name "Block-Malware" \
    --priority 10 \
    --action BLOCK \
    --block-response NXDOMAIN

# Add an allow rule
aws route53resolver create-firewall-rule \
    --firewall-rule-group-id rfg-abc123 \
    --firewall-domain-list-id rdl-def456 \
    --name "Allow-Corporate" \
    --priority 100 \
    --action ALLOW

# Add an alert rule
aws route53resolver create-firewall-rule \
    --firewall-rule-group-id rfg-abc123 \
    --firewall-domain-list-id rdl-ghi789 \
    --name "Alert-Suspicious" \
    --priority 200 \
    --action ALERT
```

### Associate Rule Group with VPC
```bash
# Associate rule group with a VPC
aws route53resolver associate-firewall-rule-group \
    --firewall-rule-group-id rfg-abc123 \
    --vpc-id vpc-12345678 \
    --name "Production-VPC-Association" \
    --priority 100
```

### Configure Query Logging
```bash
# Enable DNS query logging
aws route53resolver create-firewall-rule-group-association \
    --firewall-rule-group-id rfg-abc123 \
    --vpc-id vpc-12345678 \
    --name "Production-Logging" \
    --priority 100

# Create query log config
aws route53resolver create-resolver-query-log-config \
    --name "DNS-Query-Logs" \
    --destination-arn arn:aws:s3:::my-dns-logs \
    --creator-request-id "unique-id-123"
```

### List and Describe
```bash
# List firewall rule groups
aws route53resolver list-firewall-rule-groups

# List firewall domain lists
aws route53resolver list-firewall-domain-lists

# List firewall rules in a group
aws route53resolver list-firewall-rules \
    --firewall-rule-group-id rfg-abc123

# List associations
aws route53resolver list-firewall-rule-group-associations

# Get domain list details
aws route53resolver get-firewall-domain-list \
    --firewall-domain-list-id rdl-abc123
```

### Update and Delete
```bash
# Update rule group
aws route53resolver update-firewall-rule \
    --firewall-rule-group-id rfg-abc123 \
    --firewall-domain-list-id rdl-abc123 \
    --name "Block-Malware" \
    --priority 10 \
    --action BLOCK \
    --block-response NXDOMAIN

# Delete firewall rule
aws route53resolver delete-firewall-rule \
    --firewall-rule-group-id rfg-abc123 \
    --firewall-domain-list-id rdl-abc123

# Disassociate rule group from VPC
aws route53resolver disassociate-firewall-rule-group \
    --firewall-rule-group-association-id frga-abc123
```

## Block Responses

| Response | Description | Example |
|----------|-------------|---------|
| **NXDOMAIN** | Domain doesn't exist | DNS returns "domain not found" |
| **NODATA** | No records for domain | DNS returns empty response |
| **OVERRIDE** | Custom response | Returns a safe IP address |

```bash
# Block with custom override
aws route53resolver create-firewall-rule \
    --firewall-rule-group-id rfg-abc123 \
    --firewall-domain-list-id rdl-abc123 \
    --name "Block-With-Override" \
    --priority 10 \
    --action BLOCK \
    --block-response OVERRIDE \
    --block-override-dns-type CNAME \
    --block-override-domain "safepage.mycompany.com"
```

## Exam Tips

- ✅ **DNS Firewall** filters DNS queries at the Route53 Resolver level
- ✅ **Actions**: ALLOW, BLOCK, ALERT
- ✅ **Block responses**: NXDOMAIN, NODATA, OVERRIDE
- ✅ **Domain lists** can be imported from S3
- ✅ **Query logs** can be sent to S3, CloudWatch, or Firehose
- ✅ **Rule priority** determines evaluation order (lower number = higher priority)
- ✅ **ALERT action** logs but does not block
- ✅ **BLOCK action** prevents DNS resolution for specified domains
- ✅ **No additional cost** for DNS Firewall beyond standard Route53 Resolver
- ✅ **Regional service** - configure per-region

## Q&A

**Q1: What is Route53 Resolver DNS Firewall?**
A: A DNS-level filtering service that controls which domains can be resolved from your VPC.

**Q2: What are the three actions available in DNS Firewall rules?**
A: ALLOW, BLOCK, and ALERT.

**Q3: What block responses are available?**
A: NXDOMAIN (domain doesn't exist), NODATA (no records), OVERRIDE (custom response).

**Q4: How do you import a large domain list?**
A: Upload to S3 and use `import-firewall-domains` with the S3 URL.

**Q5: Can DNS Firewall be used across multiple VPCs?**
A: Yes, a rule group can be associated with multiple VPCs.

**Q6: What is the difference between ALERT and BLOCK actions?**
A: ALERT logs the query but allows it; BLOCK prevents DNS resolution.

**Q7: Where can DNS query logs be sent?**
A: S3, CloudWatch Logs, or Kinesis Data Firehose.

**Q8: How does rule priority work?**
A: Lower priority numbers are evaluated first (higher priority).

**Q9: Can you override blocked domains with a safe page?**
A: Yes, using the OVERRIDE block response with a custom domain.

**Q10: Is DNS Firewall a global or regional service?**
A: Regional - must be configured per-region.