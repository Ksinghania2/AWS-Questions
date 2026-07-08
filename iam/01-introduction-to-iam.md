# Introduction to AWS IAM

AWS Identity and Access Management (IAM) lets you **manage access** to AWS services and resources securely.

## Core Concepts

| Concept | Description |
|---|---|
| **User** | Identity with long-term credentials (password, access keys) |
| **Group** | Collection of users (policies attached to group apply to all members) |
| **Role** | Identity with temporary credentials (assumed by users, services, apps) |
| **Policy** | JSON document defining permissions (what actions are allowed/denied) |

## Types of Policies

| Type | Description |
|---|---|
| **AWS Managed** | Pre-built by AWS (e.g., AdministratorAccess, ReadOnlyAccess) |
| **Customer Managed** | Created by you in your account |
| **Inline** | Embedded directly in a user, group, or role |
| **Resource-based** | Attached to a resource (e.g., S3 bucket policy) |
| **Service Control Policy (SCP)** | Organization-level policy (AWS Organizations) |

## CLI Commands

```bash
# Create IAM user
aws iam create-user --user-name alice

# Create IAM group
aws iam create-group --group-name Developers

# Add user to group
aws iam add-user-to-group --user-name alice --group-name Developers

# Create customer managed policy
aws iam create-policy \
  --policy-name S3ReadOnly \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
    }]
  }'

# Attach policy to group
aws iam attach-group-policy \
  --group-name Developers \
  --policy-arn arn:aws:iam::123456789012:policy/S3ReadOnly

# List users
aws iam list-users

# List groups
aws iam list-groups
```

## Python (boto3)

```python
import boto3
import json

iam = boto3.client('iam')

# Create user with policy
def create_developer_user(username):
    """Create an IAM user and attach S3 read-only policy"""
    # Create user
    iam.create_user(UserName=username)
    print(f"Created user: {username}")
    
    # Create access key
    keys = iam.create_access_key(UserName=username)
    print(f"Access Key: {keys['AccessKey']['AccessKeyId']}")
    
    # Create policy
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": ["arn:aws:s3:::*", "arn:aws:s3:::*/*"]
        }]
    }
    
    policy = iam.create_policy(
        PolicyName=f'{username}-s3-readonly',
        PolicyDocument=json.dumps(policy_doc)
    )
    
    # Attach policy
    iam.attach_user_policy(
        UserName=username,
        PolicyArn=policy['Policy']['Arn']
    )
    print(f"Attached S3 read-only policy to {username}")

# create_developer_user('developer-1')
```

## Exam Quick Reference
- ✅ **Users**: Long-term credentials for humans/applications
- ✅ **Groups**: Organize users, attach policies to group
- ✅ **Roles**: Temporary credentials for services/apps
- ✅ **Policies**: JSON document with Allow/Deny statements
- ✅ **Managed policies**: Reusable, versioned
- ✅ **Inline policies**: Embedded in user/group/role
- ✅ **Least privilege**: Grant only necessary permissions
- ✅ **IAM is global** (not region-specific)