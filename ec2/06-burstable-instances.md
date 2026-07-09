# Burstable Instances (T Family)

T instances provide baseline CPU with ability to burst above baseline using CPU credits.

## How CPU Credits Work
- Earn credits when below baseline CPU
- Spend credits when above baseline
- Unlimited mode: Can burst beyond credit balance (charged extra)

## T Instance Types
| Type | Baseline | Credits/hr | Use Case |
|------|----------|------------|----------|
| t4g.nano | 5% | 6 | Microservices |
| t4g.micro | 10% | 12 | Low-traffic web |
| t4g.small | 20% | 24 | Dev/test |
| t4g.medium | 20% | 24 | Small DBs |
| t4g.large | 30% | 36 | Web servers |

## CLI
```bash
# Launch with unlimited
aws ec2 run-instances --image-id ami-xxx --instance-type t3.micro --credit-specification CpuCredits=unlimited

# Check credits
aws ec2 describe-instance-credit-specifications --instance-ids i-xxx

# Monitor via CloudWatch
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUCreditBalance --dimensions Name=InstanceId,Value=i-xxx --start-time 2024-01-01T00:00:00Z --end-time 2024-01-02T00:00:00Z --period 300 --statistics Average
```

## Standard vs Unlimited
| Mode | Cost | Best For |
|------|------|----------|
| Standard | Included | Steady workloads |
| Unlimited | Extra cost for burst > credits | Spiky workloads |

## Q&A
**Q1: What is a CPU credit?** A: One vCPU at 100% for 1 minute.
**Q2: Baseline for t4g.micro?** A: 10% CPU.
**Q3: What happens when credits run out in standard mode?** A: CPU drops to baseline.
**Q4: What is unlimited mode?** A: Can burst beyond credits (charged extra).
**Q5: Best use case for T instances?** A: Low-to-moderate CPU with occasional spikes.
