# Route53 Routing Policies

## Policy Types
| Policy | Description | Use Case |
|--------|-------------|----------|
| Simple | Single record, random selection | Basic DNS |
| Weighted | Distribute traffic by weight | A/B testing, canary |
| Latency | Route to lowest latency | Global apps |
| Failover | Active-passive | DR, disaster recovery |
| Geolocation | Route by user location | Regional content |
| Geoproximity | Route by location + bias | Traffic shifting |
| Multi-Value | Return multiple healthy IPs | Simple HA |

## CLI
```bash
# Simple
aws route53 change-resource-record-sets --hosted-zone-id ZONEID --change-batch '{"Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"example.com","Type":"A","TTL":300,"ResourceRecords":[{"Value":"1.2.3.4"}]}}]}'

# Weighted
aws route53 change-resource-record-sets --hosted-zone-id ZONEID --change-batch '{"Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"app.example.com","Type":"A","SetIdentifier":"prod-v1","Weight":90,"TTL":60,"ResourceRecords":[{"Value":"1.2.3.4"}]}}]}'

# Failover (primary)
aws route53 change-resource-record-sets --hosted-zone-id ZONEID --change-batch '{"Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"app.example.com","Type":"A","SetIdentifier":"primary","Failover":"PRIMARY","HealthCheckId":"xxx","TTL":60,"ResourceRecords":[{"Value":"1.2.3.4"}]}}]}'

# Latency
aws route53 change-resource-record-sets --hosted-zone-id ZONEID --change-batch '{"Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"app.example.com","Type":"A","SetIdentifier":"us-east","Region":"us-east-1","TTL":60,"ResourceRecords":[{"Value":"1.2.3.4"}]}}]}'
```

## Q&A
**Q1: Which policy for A/B testing?** A: Weighted routing policy.
**Q2: Which policy for DR (active-passive)?** A: Failover routing policy.
**Q3: Which policy routes based on user location?** A: Geolocation routing policy.
**Q4: Which policy routes to lowest latency?** A: Latency routing policy.
**Q5: What is geoproximity bias?** A: Shifts traffic from one region to another (+/- bias).
