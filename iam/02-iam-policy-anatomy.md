# Anatomy of an IAM Policy

## Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```

## Policy Elements

| Element | Required | Description |
|---|---|---|
| **Version** | Yes | Policy language version (2012-10-17) |
| **Statement** | Yes | One or more permission statements |
| **Effect** | Yes | Allow or Deny |
| **Action** | Yes | AWS actions (e.g., s3:GetObject) |
| **Resource** | Yes | ARN of the resource |
| **Condition** | No | When the policy applies |
| **Principal** | No | Who the policy applies to (resource-based policies only) |

## Policy Evaluation Logic

```
Request → Explicit Deny? → DENY ❌
        → Allow? → ALLOW ✅
        → Default → DENY ❌ (implicit)
```

**Order**: Explicit Deny > Allow > Implicit Deny (default)

## Condition Keys

| Condition Key | Description | Example |
|---|---|---|
| `aws:SourceIp` | Source IP address | `"IpAddress": {"aws:SourceIp": "203.0.113.0/24"}` |
| `aws:RequestedRegion` | AWS region | `"StringEquals": {"aws:RequestedRegion": "us-east-1"}` |
| `aws:MultiFactorAuthPresent` | MFA required | `"Bool": {"aws:MultiFactorAuthPresent": "true"}` |
| `aws:CurrentTime` | Time-based | `"DateGreaterThan": {"aws:CurrentTime": "2024-01-01T00:00:00Z"}` |
| `s3:ExistingObjectTag` | Object tag | `"StringEquals": {"s3:ExistingObjectTag/classification": "public"}` |

## CLI Commands

```bash
# Create policy from JSON file
aws iam create-policy \
  --policy-name MyPolicy \
  --policy-document file://policy.json

# Get policy version
aws iam get-policy --policy-arn arn:aws:iam::123456789012:policy/MyPolicy

# List policy versions
aws iam list-policy-versions --policy-arn arn:aws:iam::123456789012:policy/MyPolicy

# Create new policy version
aws iam create-policy-version \
  --policy-arn arn:aws:iam::123456789012:policy/MyPolicy \
  --policy-document file://policy-v2.json \
  --set-as-default

# Delete policy version
aws iam delete-policy-version \
  --policy-arn arn:aws:iam::123456789012:policy/MyPolicy \
  --version-id v2

# Simulate policy
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/alice \
  --action-names s3:GetObject s3:PutObject
```

## Exam Quick Reference
- ✅ **Version**: Always "2012-10-17"
- ✅ **Effect**: Allow or Deny
- ✅ **Action**: Service:Action (e.g., s3:GetObject)
- ✅ **Resource**: ARN of the resource
- ✅ **Condition**: Optional, when the policy applies
- ✅ **Principal**: Required for resource-based policies
- ✅ **Explicit Deny** always overrides Allow
- ✅ **Implicit Deny** is the default (no explicit Allow = denied)
- ✅ Use `iam simulate-principal-policy` to test policies