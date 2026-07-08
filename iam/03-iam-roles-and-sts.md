# IAM Roles & STS

## IAM Roles

A **role** is an identity with permissions that can be assumed by trusted entities (users, services, or applications).

### When to Use Roles

| Use Case | Example |
|---|---|
| **EC2 instances** | Instance profile for S3 access |
| **Lambda functions** | Execution role for DynamoDB access |
| **Cross-account access** | Assume role in another account |
| **Federation** | SAML/SSO users assume a role |
| **Service-to-service** | CodePipeline → deploy to EC2 |

```bash
# Create role for EC2
aws iam create-role \
  --role-name EC2-S3-Access \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policy to role
aws iam attach-role-policy \
  --role-name EC2-S3-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile and add role
aws iam create-instance-profile --instance-profile-name EC2-S3-Profile
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-S3-Profile \
  --role-name EC2-S3-Access
```

## STS (Security Token Service)

STS provides **temporary credentials** for IAM roles and federated users.

### STS API Calls

| API | Description |
|---|---|
| `AssumeRole` | Get temp credentials for a role |
| `AssumeRoleWithWebIdentity` | Federated users (Cognito, OIDC) |
| `AssumeRoleWithSAML` | SAML 2.0 federation |
| `GetSessionToken` | MFA-protected session |
| `GetCallerIdentity` | Get current user/role details |
| `DecodeAuthorizationMessage` | Decode encoded error messages |

```bash
# Assume a role (get temporary credentials)
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/AdminRole \
  --role-session-name "my-session"

# Get session token with MFA
aws sts get-session-token \
  --serial-number arn:aws:iam::123456789012:mfa/user \
  --token-code 123456

# Get current caller identity
aws sts get-caller-identity

# Cross-account role assumption
# 1. Trust policy in Account A (allows Account B to assume role)
# 2. IAM policy in Account B (grants user permission to sts:AssumeRole)
aws sts assume-role \
  --role-arn arn:aws:iam::987654321012:role/CrossAccountRole \
  --role-session-name "cross-account-access"
```

## Cross-Account Roles

```
Account A (Prod)             Account B (Dev)
┌─────────────────┐          ┌──────────────────┐
│   S3 Bucket      │          │  IAM User (Bob)   │
│   (Resource)     │          │  Can assume role   │
│                  │ ←───←── │  in Account A      │
│ Trusts Account B │          │                    │
└─────────────────┘          └──────────────────┘
```

## Exam Quick Reference
- ✅ **Roles**: Temporary credentials via STS
- ✅ **Trust Policy**: Who can assume the role (Principal)
- ✅ **Permissions Policy**: What the role can do
- ✅ **STS**: Issues temporary credentials (valid up to 1 hour for AssumeRole)
- ✅ **Cross-account**: Role in Account A trusts Account B
- ✅ **EC2 Instance Profile**: IAM role for EC2 instances
- ✅ `get-caller-identity`: Debug current identity
- ✅ `DecodeAuthorizationMessage`: Decode access denied details