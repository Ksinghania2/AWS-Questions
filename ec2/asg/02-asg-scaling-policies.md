# ASG Scaling Policies

## Dynamic Scaling Policies
| Policy | Description | Use Case |
|--------|-------------|----------|
| Simple | Set threshold, add/remove instances | Basic scaling |
| Step | Different adjustments based on breach size | Granular control |
| Target Tracking | Keep metric at target value (e.g., CPU 50%) | Most common |
| Predictive | ML-based forecast of traffic | Cyclical patterns |

## CLI
```bash
# Create ASG
aws autoscaling create-auto-scaling-group     --auto-scaling-group-name my-asg     --launch-configuration-name my-lc     --min-size 2 --max-size 10 --desired-capacity 2     --vpc-zone-identifier subnet-xxx,subnet-yyy

# Target tracking policy
aws autoscaling put-scaling-policy     --auto-scaling-group-name my-asg     --policy-name cpu-target     --policy-type TargetTrackingScaling     --target-tracking-configuration '{"TargetValue": 50.0,"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"}}'

# Step scaling
aws autoscaling put-scaling-policy     --auto-scaling-group-name my-asg     --policy-name step-policy     --policy-type StepScaling     --step-adjustments MetricIntervalLowerBound=0,MetricIntervalUpperBound=10,ScalingAdjustment=1 MetricIntervalLowerBound=10,ScalingAdjustment=2

# Predictive scaling
aws autoscaling put-scaling-policy     --auto-scaling-group-name my-asg     --policy-name predictive     --policy-type PredictiveScaling     --predictive-scaling-configuration '{"MetricSpecifications":[{"TargetValue":50,"PredefinedLoadMetricSpecification":{"PredefinedMetricType":"ASGTotalCPUUtilization"},"PredefinedScalingMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"}}]}'
```

## Q&A
**Q1: What is the most common scaling policy?** A: Target Tracking (e.g., keep CPU at 50%).
**Q2: What is Predictive Scaling?** A: ML-based forecasting for cyclical traffic patterns.
**Q3: What is the difference between Simple and Step scaling?** A: Step has different adjustments based on how much the metric breaches the threshold.
**Q4: What metrics can Target Tracking use?** A: Predefined (CPU, network, request count) or custom metrics.
**Q5: What is the cooldown period?** A: Time to wait before another scaling activity (default 300 seconds).
