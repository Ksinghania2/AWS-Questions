# Introduction to Amazon EC2

Amazon Elastic Compute Cloud (EC2) provides **resizable compute capacity** in the cloud as virtual servers.

## Core Concepts

| Concept | Description |
|---|---|
| **Instance** | Virtual server (choice of CPU, RAM, storage, networking) |
| **AMI** | Amazon Machine Image (OS + software template) |
| **Instance Type** | Hardware specification (e.g., t3.micro, c5.xlarge) |
| **Key Pair** | SSH key for secure login (public/private) |
| **Security Group** | Virtual firewall (stateful, instance-level) |
| **EBS** | Block storage volumes (persistent) |
| **Instance Profile** | IAM role attached to the instance |

## Instance Types & Families

| Family | Type | Use Case |
|---|---|---|
| **General Purpose** | t3, t4g, m6i | Web servers, small DBs |
| **Compute Optimized** | c6i, c7g | Batch processing, gaming, HPC |
| **Memory Optimized** | r6i, x2iedn | In-memory caches, large DBs |
| **Storage Optimized** | i3, d2 | High I/O, data warehousing |
| **Accelerated Computing** | p4, g5 | ML training, video rendering |

## CLI Commands

```bash
# Run an EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-12345 \
  --subnet-id subnet-12345 \
  --associate-public-ip-address \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'

# List instances
aws ec2 describe-instances

# Stop instance
aws ec2 stop-instances --instance-ids i-12345

# Start instance
aws ec2 start-instances --instance-ids i-12345

# Terminate instance
aws ec2 terminate-instances --instance-ids i-12345

# Get console output
aws ec2 get-console-output --instance-id i-12345

# Get instance screenshot
aws ec2 get-console-screenshot --instance-id i-12345
```

## Python (boto3)

```python
import boto3

ec2 = boto3.client('ec2')

def launch_web_server(name, subnet_id, sg_id, key_name):
    """Launch a web server instance"""
    instances = ec2.run_instances(
        ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2
        InstanceType='t3.micro',
        KeyName=key_name,
        SecurityGroupIds=[sg_id],
        SubnetId=subnet_id,
        AssociatePublicIpAddress=True,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': name}]
        }]
    )
    
    instance_id = instances['Instances'][0]['InstanceId']
    print(f"Instance {instance_id} launching...")
    return instance_id

def list_instances_by_state(state='running'):
    """List EC2 instances by state"""
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': [state]}]
    )
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'Type': instance['InstanceType'],
                'State': instance['State']['Name'],
                'PrivateIP': instance.get('PrivateIpAddress', 'N/A'),
                'PublicIP': instance.get('PublicIpAddress', 'N/A')
            })
            print(f"{instance['InstanceId']} | {instance['InstanceType']} | {instance['State']['Name']}")
    
    return instances

# Launch instance
instance_id = launch_web_server('web-1', 'subnet-12345', 'sg-12345', 'my-key')

# List instances
list_instances_by_state()
```

## Exam Quick Reference
- ✅ **EC2** = virtual servers in the cloud
- ✅ **AMIs** = OS + software templates (Amazon Linux, Ubuntu, Windows)
- ✅ **Instance types** = CPU + RAM + Network (t3.micro, c5.xlarge, etc.)
- ✅ **Key Pairs** = SSH access (RSA, ED25519)
- ✅ **Security Groups** = Stateful firewalls (instance-level)
- ✅ **EBS** = Persistent block storage
- ✅ **Instance Profile** = IAM role for the instance
- ✅ **User Data** = Bootstrap scripts run at launch
- ✅ **Termination Protection** = Prevents accidental termination
- ✅ **Instance Metadata** = http://169.254.169.254/latest/meta-data/