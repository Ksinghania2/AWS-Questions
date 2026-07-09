# IAM Password Policy

An IAM password policy defines the password requirements for your AWS account's IAM users.

## What is an IAM Password Policy?

A set of rules that enforce password complexity, rotation, and reuse restrictions for IAM users. This applies only to users with a console password (not access keys).

## Policy Settings

| Setting | Description | Example |
|---------|-------------|---------|
| **Minimum length** | Minimum characters required | `8` |
| **Require uppercase** | At least one uppercase letter | `true` |
| **Require lowercase** | At least one lowercase letter | `true` |
| **Require numbers** | At least one numeric character | `true` |
| **Require symbols** | At least one non-alphanumeric | `true` |
| **Allow change own** | Users can change their password | `true` |
| **Expiration** | Days until password expires | `90` |
| **Prevent reuse** | Number of previous passwords blocked | `3` |
| **Max age** | Maximum password age in days | `90` |

## CLI Examples

### Set Password Policy
```bash
# Set a strict password policy
aws iam update-account-password-policy \
    --minimum-password-length 12 \
    --require-uppercase-characters \
    --require-lowercase-characters \
    --require-numbers \
    --require-symbols \
    --allow-users-to-change-password \
    --max-password-age 90 \
    --password-reuse-prevention 5 \
    --hard-expiry
```

### View Current Policy
```bash
# Get current password policy
aws iam get-account-password-policy

# Output example:
# {
#     "PasswordPolicy": {
#         "MinimumPasswordLength": 12,
#         "RequireSymbols": true,
#         "RequireNumbers": true,
#         "RequireUppercaseCharacters": true,
#         "RequireLowercaseCharacters": true,
#         "AllowUsersToChangePassword": true,
#         "ExpirePasswords": true,
#         "MaxPasswordAge": 90,
#         "PasswordReusePrevention": 5,
#         "HardExpiry": true
#     }
# }
```

### Delete Password Policy
```bash
# Remove password policy (use defaults)
aws iam delete-account-password-policy
```

### Set Policy for Specific Users (SCPs)

For AWS Organizations, you can enforce password policies via SCPs:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "iam:UpdateAccountPasswordPolicy",
            "Resource": "*",
            "Condition": {
                "NumericLessThan": {
                    "iam:PasswordPolicyMinimumLength": "14"
                }
            }
        }
    ]
}
```

## Bash Script for Policy Setup

```bash
#!/bin/bash
# setup-password-policy.sh

apply_policy() {
    local ENVIRONMENT=$1
    
    case $ENVIRONMENT in
        "production")
            aws iam update-account-password-policy \
                --minimum-password-length 16 \
                --require-uppercase-characters \
                --require-lowercase-characters \
                --require-numbers \
                --require-symbols \
                --max-password-age 30 \
                --password-reuse-prevention 10
            ;;
        "development")
            aws iam update-account-password-policy \
                --minimum-password-length 8 \
                --require-uppercase-characters \
                --require-lowercase-characters \
                --max-password-age 180 \
                --password-reuse-prevention 3
            ;;
    esac
}

apply_policy "production"
```

## Exam Tips

- ✅ **Password policies** apply to ALL IAM users in the account
- ✅ **Root user** is NOT affected by password policy
- ✅ **Access keys** are NOT affected by password policy
- ✅ **Hard expiry** forces password change at next login
- ✅ **Password reuse prevention** stores previous password hashes
- ✅ **Cannot enforce** password policy for federated users
- ✅ **Maximum password age** can be up to 1095 days (3 years)
- ✅ **Minimum password length** ranges from 6 to 128 characters

## Q&A

**Q1: What does an IAM password policy control?**
A: Password complexity, rotation, reuse, and expiration for IAM users.

**Q2: Does the password policy apply to the root user?**
A: No, only to IAM users with console passwords.

**Q3: Does password policy affect access keys?**
A: No, access keys are independent of password policies.

**Q4: What is the minimum password length range?**
A: 6 to 128 characters.

**Q5: What is hard expiry?**
A: Forces users to change their password at next login when expired.

**Q6: How many previous passwords can be blocked?**
A: Up to 24 previous passwords.

**Q7: Can you enforce password policies for federated users?**
A: No, password policies only apply to IAM users in the account.

**Q8: How do you view the current password policy?**
A: `aws iam get-account-password-policy`.

**Q9: How do you remove a custom password policy?**
A: `aws iam delete-account-password-policy`.

**Q10: What is the maximum password age setting?**
A: Up to 1095 days (3 years).