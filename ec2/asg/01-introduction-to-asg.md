# Auto Scaling Groups (ASG)

ASG automatically adjusts the number of EC2 instances based on demand, ensuring you have the right amount of capacity.

## Core Concepts

| Concept | Description |
|---|---|
| **Launch Template** | Configuration template for new instances (AMI, instance type, key pair, SG) |
| **Desired Capacity** | Target number of instances |
| **Min Size** | Minimum number of instances (never goes below) |
| **Max Size** | Maximum number of instances (never goes above) |
| **Scaling Policies** | Rules for when to scale in/out |
| **Health Checks** | EC2 or ELB health checks |
| **ELB Integration** | Auto-register new instances with load balancer |

## CLI Commands

```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name web-template \
  --launch-template-data '{
    "ImageId": "ami-0c55b159cbfafe1f0",
    "InstanceType": "t3.micro",
    "KeyName": "my-key",
    "SecurityGroupIds": ["sg-12345"],
    "UserData": "IyEvYmluL2Jhc2gKeXVtIGluc3RhbGwgaHR0cGQgLXk="
  }'

# Create Auto Scaling Group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --launch-template LaunchTemplateName=web-template \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-12345,subnet-67890" \
  --target-group-arns arn:aws:elasticloadbalancing:...:targetgroup/web-targets/abc

# Update desired capacity
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name web-asg \
  --desired-capacity 5

# Create scaling policy (target tracking)
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name web-asg \
  --policy-name cpu-target \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {"PredefinedMetricType": "ASGAverageCPUUtilization"},
    "TargetValue": 60.0
  }'

# Describe ASG
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names web-asg

# Suspend processes
aws autoscaling suspend-processes \
  --auto-scaling-group-name web-asg \
  --scaling-processes AlarmNotification

# Resume processes
aws autoscaling resume-processes \
  --auto-scaling-group-name web-asg \
  --scaling-processes AlarmNotification
```

## Scaling Policies

| Policy | Description | Use Case |
|---|---|---|
| **Target Tracking** | Maintain a target metric (CPU, requests) | Most common, recommended |
| **Step Scaling** | Add/remove instances based on metric thresholds | When you need precise control |
| **Simple Scaling** | Add/remove based on CloudWatch alarms | Legacy, not recommended |
| **Scheduled Scaling** | Scale at specific times | Predictable patterns |
| **Predictive Scaling** | ML-based forecast | Cyclical patterns |

## Python (boto3)

```python
import boto3

autoscaling = boto3.client('autoscaling')
ec2 = boto3.client('ec2')

def create_asg_with_lb(asg_name, subnet_ids, target_group_arn):
    """Create Auto Scaling Group with a launch template"""
    # Create launch template
    ec2.create_launch_template(
        LaunchTemplateName=f'{asg_name}-template',
        LaunchTemplateData={
            'ImageId': 'ami-0c55b159cbfafe1f0',
            'InstanceType': 't3.micro',
            'SecurityGroupIds': ['sg-12345']
        }
    )
    
    # Create ASG
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={'LaunchTemplateName': f'{asg_name}-template'},
        MinSize=2,
        MaxSize=10,
        DesiredCapacity=2,
        VPCZoneIdentifier=subnet_ids,
        TargetGroupARNs=[target_group_arn],
        HealthCheckType='ELB',
        HealthCheckGracePeriod=300
    )
    
    # Add scaling policy
    autoscaling.put_scaling_policy(
        AutoScalingGroupName=asg_name,
        PolicyName='cpu-target-60',
        PolicyType='TargetTrackingScaling',
        TargetTrackingConfiguration={
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ASGAverageCPUUtilization'
            },
            'TargetValue': 60.0
        }
    )
    
    print(f"ASG '{asg_name}' created with 2-10 instances")
```

## Exam Quick Reference
- ✅ **Launch Template**: Instance configuration (modern, recommended)
- ✅ **Launch Configuration**: Legacy (use launch templates instead)
- ✅ **Min/Max/Desired**: Control instance count
- ✅ **Target Tracking**: Most common scaling policy
- ✅ **ELB Integration**: Auto-register/deregister instances
- ✅ **Health Checks**: EC2 status check or ELB health check
- ✅ **Cooldown Period**: Wait time between scaling activities
- ✅ **AZ Rebalancing**: Distribute instances across AZs
- ✅ **Termination Policy**: Which instance to terminate first (Oldest, Newest, Closest)
- ✅ **Lifecycle Hooks**: Pause instances for custom actions during launch/terminate