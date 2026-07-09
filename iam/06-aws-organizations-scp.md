# AWS Organizations & Service Control Policies (SCPs)

AWS Organizations centrally manages multiple AWS accounts, and SCPs set permission boundaries across those accounts.

## What is AWS Organizations?

A service that allows you to centrally manage multiple AWS accounts as a group, applying policies and controlling access across accounts.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Management Account** | The master account that creates the organization |
| **Member Account** | Standard account within the organization |
| **Organizational Unit (OU)** | Group of accounts for policy application |
| **Service Control Policy (SCP)** | Policy that sets maximum permissions for accounts/OUs |
| **Feature Set** | Consolidated Billing or All Features |

## Organization Structure

```
Management Account (Root)
│
├── OU: Security
│   ├── Log Archive Account
│   └── Security Audit Account
│
├── OU: Workloads
│   ├── OU: Production
│   │   ├── Prod-App Account
│   │   ├── Prod-DB Account
│   │   └── Prod-Web Account
│   │
│   └── OU: Development
│       ├── Dev-App Account
│       └── Dev-Test Account
│
└── OU: Infrastructure
    ├── Networking Account
    ├── Shared Services Account
    └── DNS Account
```

## CLI Examples

### Create Organization
```bash
# Create an organization (use 'ALL' or 'CONSOLIDATED_BILLING')
aws organizations create-organization \
    --feature-set ALL

# Describe organization
aws organizations describe-organization
```

### Create Organizational Unit
```bash
# Create OUs
aws organizations create-organizational-unit \
    --parent-id r-abc123 \
    --name "Security"

aws organizations create-organizational-unit \
    --parent-id r-abc123 \
    --name "Workloads"

aws organizations create-organizational-unit \
    --parent-id ou-abc123-def456 \
    --name "Production"
```

### Invite Account
```bash
# Invite an existing account to join
aws organizations invite-account-to-organization \
    --target Id=123456789012,Type=ACCOUNT \
    --notes "Please join our AWS Organization"

# Create a new account
aws organizations create-account \
    --email "admin@mycompany.com" \
    --account-name "Production-App"
```

### Move Account to OU
```bash
# Move account to an OU
aws organizations move-account \
    --account-id 123456789012 \
    --source-parent-id r-abc123 \
    --destination-parent-id ou-abc123-def456
```

### List Accounts and OUs
```bash
# List all accounts
aws organizations list-accounts

# List accounts in an OU
aws organizations list-accounts-for-parent \
    --parent-id ou-abc123-def456

# List OUs
aws organizations list-organizational-units-for-parent \
    --parent-id r-abc123

# List parents of an account
aws organizations list-parents \
    --child-id 123456789012
```

## Service Control Policies (SCPs)

### What are SCPs?

SCPs define the **maximum permissions** for accounts in an OU. They cannot grant permissions—only deny or allow within boundaries.

### Important: SCP Inheritance

```
Root (Full Access)
├── SCP: "Deny Root User Actions"
│
├── OU: Production (Inherits Root SCP)
│   ├── SCP: "Allow Only EC2, S3, RDS"
│   │
│   ├── Prod-App Account
│   ├── Prod-DB Account
│   └── Prod-Web Account
│
└── OU: Development (Inherits Root SCP)
    └── SCP: "Allow All AWS Services" (No additional restrictions)
        ├── Dev-App Account
        └── Dev-Test Account
```

### Create SCP
```bash
# Create a service control policy
aws organizations create-policy \
    --name "DenyRootUserActions" \
    --description "Prevents usage of root user" \
    --type SERVICE_CONTROL_POLICY \
    --content '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Deny",
                "Action": "*",
                "Resource": "*",
                "Condition": {
                    "StringLike": {
                        "aws:PrincipalArn": "arn:aws:iam::*:root"
                    }
                }
            }
        ]
    }'
```

### Attach SCP to OU
```bash
# Attach SCP to an OU
aws organizations attach-policy \
    --policy-id p-scpabc123 \
    --target-id ou-abc123-def456

# Attach SCP to root
aws organizations attach-policy \
    --policy-id p-scpabc123 \
    --target-id r-abc123

# List attached policies
aws organizations list-policies-for-target \
    --target-id ou-abc123-def456 \
    --filter SERVICE_CONTROL_POLICY
```

### Detach and Delete SCP
```bash
# Detach SCP
aws organizations detach-policy \
    --policy-id p-scpabc123 \
    --target-id ou-abc123-def456

# Delete policy (must be detached from all targets first)
aws organizations delete-policy \
    --policy-id p-scpabc123
```

### Update SCP
```bash
# Update policy
aws organizations update-policy \
    --policy-id p-scpabc123 \
    --name "Updated-DenyRoot" \
    --description "Updated root user restrictions"
```

## Common SCP Examples

### 1. Deny Root User Actions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "aws:PrincipalArn": "arn:aws:iam::*:root"
                }
            }
        }
    ]
}
```

### 2. Restrict to Allowed Regions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "NotAction": [
                "aws:RequestedRegion"
            ],
            "Resource": "*",
            "Condition": {
                "StringNotEquals": {
                    "aws:RequestedRegion": [
                        "us-east-1",
                        "us-west-2",
                        "eu-west-1"
                    ]
                }
            }
        }
    ]
}
```

### 3. Deny Untagged Resources
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "ec2:RunInstances",
                "ec2:CreateVolume"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:RequestTag/Environment": "true"
                }
            }
        }
    ]
}
```

### 4. Prevent IAM Policy Changes
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
                "iam:CreatePolicy",
                "iam:DeletePolicy"
            ],
            "Resource": "*"
        }
    ]
}
```

## SCP Evaluation Logic

```
1. Full AWS Access (default)
2. Apply Deny SCPs (Deny wins)
3. Apply Allow SCPs (Allow only if there's an Allow)
4. Intersection with IAM policies
```

## Exam Tips

- ✅ **SCPs cannot grant permissions** - they only set boundaries
- ✅ **SCPs affect ALL principals** (including root) in member accounts
- ✅ **SCPs do NOT affect the management account**
- ✅ **Default is FullAccess** (Allow everything) unless you attach a deny
- ✅ **Inheritance** flows from root → OU → account
- ✅ **SCPs + IAM policies** = effective permissions (intersection)
- ✅ **Maximum 5 SCPs** per account per target
- ✅ **Maximum 1000 policies** per organization
- ✅ **SCPs are JSON** documents similar to IAM policies
- ✅ **Use SCPs** for guardrails, not granular permissions

## Q&A

**Q1: What is the purpose of AWS Organizations?**
A: Centrally manage multiple AWS accounts with consolidated billing and policy control.

**Q2: What is a Service Control Policy?**
A: A policy that sets the maximum permissions for accounts in an OU.

**Q3: Can SCPs grant permissions?**
A: No, they only define boundaries (allow or deny).

**Q4: Does the management account get affected by SCPs?**
A: No, SCPs only affect member accounts.

**Q5: What is the default SCP behavior?**
A: Full AWS Access (Allow everything).

**Q6: How does SCP inheritance work?**
A: SCPs flow from root → OU → account; more restrictive always wins.

**Q7: What is the difference between SCP and IAM policy?**
A: SCP sets max boundaries; IAM policy grants specific permissions within those boundaries.

**Q8: How many SCPs can be attached to a target?**
A: Up to 5 SCPs per target (OU or account).

**Q9: Can you use SCPs to require MFA?**
A: Yes, SCPs can enforce MFA for all accounts in an organization.

**Q10: What happens if an SCP denies an action but IAM allows it?**
A: The action is denied (deny always wins).

**Q11: What is an Organizational Unit?**
A: A group of accounts used for hierarchical policy management.

**Q12: Can you move accounts between OUs?**
A: Yes, using `aws organizations move-account`.

**Q13: What is the feature set for full SCP support?**
A: "All features" must be enabled.

**Q14: How do you create a new account in an organization?**
A: `aws organizations create-account`.

**Q15: What is the maximum number of policies per organization?**
A: 1000 policies.