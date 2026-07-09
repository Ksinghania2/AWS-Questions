# Route53 DNSSEC & Zonal Shift

## DNSSEC (DNS Security Extensions)
Cryptographically signs DNS records to prevent spoofing and cache poisoning.

```bash
# Enable DNSSEC signing
aws route53 enable-hosted-zone-dnssec --hosted-zone-id ZONEID

# Create key signing key (KSK)
aws route53 create-key-signing-key     --hosted-zone-id ZONEID     --key-management-service-arn arn:aws:kms:us-east-1:xxx:key/xxx     --name "my-ksk"     --status ACTIVE

# Get DNSSEC status
aws route53 get-dnssec --hosted-zone-id ZONEID
```

## Zonal Shift
Puts a resource in a specific AZ out of service for disaster recovery testing.

```bash
# Start zonal shift
aws route53-recovery-cluster start-zonal-shift     --resource-identifier "arn:aws:elasticloadbalancing:us-east-1:xxx:loadbalancer/app/my-alb/xxx"     --away-from "us-east-1a"     --comment "DR testing"     --expires-in 7200
```

## Q&A
**Q1: What does DNSSEC protect against?** A: DNS spoofing and cache poisoning.
**Q2: What two keys are used in DNSSEC?** A: KSK (Key Signing Key) and ZSK (Zone Signing Key).
**Q3: What is Zonal Shift?** A: Moves traffic away from a specific AZ for DR testing.
**Q4: How long can a zonal shift last?** A: Up to 7200 seconds (2 hours).
**Q5: What services support Zonal Shift?** A: ALB, NLB, and other zonal resources.
