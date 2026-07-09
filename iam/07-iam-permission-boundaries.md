# IAM Permission Boundaries & Session Policies

Permission boundaries and session policies are advanced IAM features that further restrict the maximum permissions an IAM entity can have.

## What are Permission Boundaries?

A permission boundary is a managed policy that sets the **maximum permissions** an IAM entity (user or role) can have. The effective permissions are the intersection of the boundary and the entity's identity-based policies.

## Permission Boundary Evaluation

```
IAM Policy (Allow: ec2:*, s3:*)
        ∩
Permission Boundary (Allow: ec2:*, s3:GetObject)
        =
Effective Permissions (Allow: ec2:*, s3:GetObject)
```

## Architecture

```
Permission Boundary (Maximum Ceiling)
        │
        ├── IAM User/Role
        │   └── Identity-based Policies (What they want to do)
        │
        └── Intersection = Effective Permissions
```

## CLI Examples

### Create Permission Boundary Policy
```bash
# Create a permission boundary policy
aws iam create-policy \
    --policy-name "EC2-S3-Boundary" \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:Describe*",
                    "ec2:RunInstances",
                    "s3:Get*",
                    "s3:List*"
                ],
                "Resource": "*"
            }
        ]
    }'
```

### Create User with Permission Boundary
```bash
# Create user with permission boundary
aws iam create-user \
    --user-name "developer" \
    --permissions-boundary "arn:aws:iam::123456789012:policy/EC2-S3-Boundary"

# Attach additional policy
aws iam attach-user-policy \
    --user-name "developer" \
    --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"

# Even with Admin policy, user is limited by the boundary
```

### Create Role with Permission Boundary
```bash
# Create role with permission boundary
aws iam create-role \
    --role-name "EC2-S3-Role" \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }' \
    --permissions-boundary "arn:aws:iam::123456789012:policy/EC2-S3-Boundary"
```

### List Users with Permission Boundaries
```bash
# List users with permission boundaries
aws iam list-users \
    --query 'Users[?PermissionsBoundary!=null]'

# Get specific user's boundary
aws iam get-user \
    --user-name "developer" \
    --query 'User.PermissionsBoundary'
```

### Update Permission Boundary
```bash
# Update user's permission boundary
aws iam put-user-permissions-boundary \
    --user-name "developer" \
    --permissions-boundary "arn:aws:iam::123456789012:policy/New-Boundary"

# Remove permission boundary
aws iam delete-user-permissions-boundary \
    --user-name "developer"
```

## Session Policies

Session policies are passed when assuming a role or getting federated credentials via STS. They further restrict the role's permissions for that specific session.

### Session Policy with AssumeRole
```bash
# Assume role with session policy (further restricts)
aws sts assume-role \
    --role-arn "arn:aws:iam::123456789012:role/Admin" \
    --role-session-name "RestrictedSession" \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::my-bucket/*"
            }
        ]
    }'
```

### Session Policy with GetFederationToken
```bash
# Get federation token with session policy
aws sts get-federation-token \
    --name "MobileAppUser" \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::my-app-bucket/*"
            }
        ]
    }'
```

## Effective Permission Calculation

```
Effective = Identity-Based ∩ Permission Boundary ∩ Session Policy

Example:
Identity Policy: Allow ec2:*, s3:*, iam:*
Permission Boundary: Allow ec2:*, s3:GetObject
Session Policy: Allow s3:GetObject

Result: Only s3:GetObject (most restrictive)
```

## Use Cases

### 1. Delegating Admin with Boundaries
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:CreateUser",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:PermissionsBoundary": "arn:aws:iam::123456789012:policy/EC2Only"
                }
            }
        }
    ]
}
```

### 2. Preventing Privilege Escalation
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "iam:PutUserPermissionsBoundary",
                "iam:PutRolePermissionsBoundary",
                "iam:DeleteUserPermissionsBoundary",
                "iam:DeleteRolePermissionsBoundary"
            ],
            "Resource": "*"
        }
    ]
}
```

### 3. Developer Sandbox Boundary
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "ec2:RunInstances",
                "ec2:TerminateInstances",
                "s3:Get*",
                "s3:Put*",
                "s3:List*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "Action": [
                "iam:*",
                "organizations:*",
                "account:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## Exam Tips

- ✅ **Permission boundaries** set the maximum permissions for users/roles
- ✅ **Session policies** further restrict STS sessions
- ✅ **Effective permissions** = intersection of all applicable policies
- ✅ **Boundaries cannot grant permissions** - only restrict
- ✅ **Boundaries are IAM policies** (managed or custom)
- ✅ **Session policies** are passed inline during STS calls
- ✅ **Use boundaries** to delegate user/role creation safely
- ✅ **Deny always wins** - even over boundaries
- ✅ **Boundaries do NOT affect service-linked roles**
- ✅ **Maximum 1 boundary** per user/role

## Q&A

**Q1: What is an IAM permission boundary?**
A: A managed policy that sets the maximum permissions an IAM entity can have.

**Q2: How do effective permissions work with boundaries?**
A: Effective = Identity Policy ∩ Permission Boundary ∩ Session Policy.

**Q3: Can a permission boundary grant permissions?**
A: No, it only sets the maximum ceiling for permissions.

**Q4: What is a session policy?**
A: A policy passed during STS AssumeRole that further restricts the session.

**Q5: How many permission boundaries can a user have?**
A: One per user or role.

**Q6: Do permission boundaries affect service-linked roles?**
A: No, service-linked roles are not affected.

**Q7: How do you create a user with a permission boundary?**
A: `aws iam create-user --user-name dev --permissions-boundary arn:aws:iam::xxx:policy/Boundary`

**Q8: What is the use case for permission boundaries?**
A: Delegating admin access safely, preventing privilege escalation.

**Q9: Can you remove a permission boundary?**
A: Yes, using `aws iam delete-user-permissions-boundary`.

**Q10: What happens if a boundary denies an action that IAM allows?**
A: The action is denied (deny always wins).

**Q11: How do you pass a session policy?**
A: Using the `--policy` parameter in `aws sts assume-role`.

**Q12: Can permission boundaries be used with SCPs?**
A: Yes, they work together (SCP at org level, boundary at entity level).

**Q13: What is the difference between SCP and permission boundary?**
A: SCP applies to all accounts in an OU; boundary applies to specific users/roles.

**Q14: Can you attach a permission boundary to a group?**
A: No, only to users and roles.

**Q15: What is the key exam scenario for permission boundaries?**
A: Allowing junior admins to create users but restricting them to only create users with specific boundaries.