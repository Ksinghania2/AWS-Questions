# ASG Lifecycle Hooks & Cooldown Periods

## Lifecycle Hooks
Pause instance state transitions to run custom actions before instances launch or terminate.

## States
```
Pending -> Pending:Wait -> Pending:Proceed -> InService
InService -> Terminating:Wait -> Terminating:Proceed -> Terminated
```

## CLI
```bash
# Create lifecycle hook
aws autoscaling put-lifecycle-hook     --lifecycle-hook-name my-hook     --auto-scaling-group-name my-asg     --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING     --heartbeat-timeout 300     --default-result CONTINUE     --notification-target-arn arn:aws:sns:us-east-1:xxx:my-topic     --role-arn arn:aws:iam::xxx:role/ASG-Lifecycle-Role

# Complete lifecycle action
aws autoscaling complete-lifecycle-action     --lifecycle-hook-name my-hook     --auto-scaling-group-name my-asg     --lifecycle-action-result CONTINUE     --instance-id i-xxx
```

## Cooldown Period
- Default: 300 seconds (5 minutes)
- Prevents rapid scaling thrashing
- Can be overridden per policy

## Q&A
**Q1: What is a lifecycle hook?** A: Pauses instance transitions to run custom actions.
**Q2: What are the two lifecycle transitions?** A: Pending (launch) and Terminating (shutdown).
**Q3: What is the default cooldown period?** A: 300 seconds (5 minutes).
**Q4: What happens if heartbeat timeout expires?** A: Default result (CONTINUE or ABANDON) is applied.
**Q5: Use case for lifecycle hooks?** A: Run teardown scripts, extract logs before termination.
