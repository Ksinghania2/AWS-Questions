# EC2 Pricing Models

## Pricing Options

| Model | Discount | Commitment | Use Case |
|-------|----------|------------|----------|
| **On-Demand** | None | None | Short-term, unpredictable |
| **Reserved (Standard)** | Up to 72% | 1 or 3 years | Steady-state workloads |
| **Reserved (Convertible)** | Up to 54% | 1 or 3 years | Need flexibility (family/OS/tenancy) |
| **Spot** | Up to 90% | None | Fault-tolerant, stateless, batch |
| **Dedicated Host** | N/A | 1 or 3 years | BYOL, compliance, sockets/cores |
| **Savings Plans** | Up to 72% | 1 or 3 years | Flexible across EC2/Fargate/Lambda |

## CLI Examples

```bash
# Purchase Reserved Instance
aws ec2 purchase-reserved-instances-offering \
    --reserved-instances-offering-id rif-abc123 \
    --instance-count 3

# Request Spot Instances
aws ec2 request-spot-instances \
    --spot-price "0.05" \
    --instance-count 5 \
    --launch-specification ImageId=ami-xxx,InstanceType=t3.micro

# Describe Spot price history
aws ec2 describe-spot-price-history \
    --instance-types t3.micro \
    --product-description "Linux/UNIX" \
    --start-time 2024-01-01T00:00:00Z

# Create Capacity Reservation
aws ec2 create-capacity-reservation \
    --instance-type p3dn.24xlarge \
    --instance-platform "Linux/UNIX" \
    --availability-zone us-east-1a \
    --instance-count 5

# Describe Reserved Instances
aws ec2 describe-reserved-instances

# Describe Spot Instance requests
aws ec2 describe-spot-instance-requests
```

## Key Exam Points

- ✅ **On-Demand**: No commitment, highest cost, best for short-term
- ✅ **Standard RI**: Fixed attributes (instance family, region), biggest discount
- ✅ **Convertible RI**: Can change family, OS, tenancy (less discount)
- ✅ **Spot**: Up to 90% off, 2-minute termination notice, can't be terminated manually
- ✅ **Dedicated Host**: Physical server visibility, for compliance/BYOL
- ✅ **Dedicated Instance**: Hardware isolated at host level but no server visibility
- ✅ **Savings Plans**: Hourly spend commitment, most flexible (EC2 Instance, Compute, SageMaker)
- ✅ **Capacity Reservation**: Reserve compute capacity in specific AZ, no discount
- ✅ **Regional vs Zonal RIs**: Zonal provides capacity reservation; Regional provides discount flexibility

## Q&A

**Q1: Best pricing model for steady-state production workload?** A: Reserved Instance or Savings Plan.
**Q2: Best for stateless batch processing?** A: Spot Instances (up to 90% off).
**Q3: What is the Spot termination notice time?** A: 2 minutes.
**Q4: What pricing model gives full physical server control?** A: Dedicated Host.
**Q5: What is the most flexible discount model?** A: Compute Savings Plans (covers EC2, Fargate, Lambda).
**Q6: What is the difference between Dedicated Host and Dedicated Instance?** A: Host gives sockets/cores visibility for BYOL; Instance is hardware isolated but no visibility.
**Q7: Can Convertible RIs be exchanged?** A: Yes, can change instance family, OS, tenancy during term.
**Q8: What is a Capacity Reservation?** A: Reserve compute capacity in a specific AZ for any duration (no discount).
**Q9: Which RI type provides capacity reservation benefit?** A: Zonal Reserved Instances (Regional RIs do not reserve capacity).
**Q10: What is the benefit of Compute Savings Plans over RIs?** A: More flexible - applies to any EC2 instance regardless of family/region.