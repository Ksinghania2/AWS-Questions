# IAM Multi-Factor Authentication (MFA)

MFA adds an extra layer of security by requiring a second authentication factor beyond a password or access key.

## What is MFA?

A security mechanism that requires two or more authentication factors:
1. **Something you know** (password, access key)
2. **Something you have** (MFA device, phone, hardware token)

## MFA Device Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Virtual MFA** | App on phone (Google Authenticator, Authy, Microsoft Authenticator) | Most common, free |
| **U2F Security Key** | Physical USB key (YubiKey) | High security, phishing resistant |
| **Hardware TOTP Token** | Physical token (Gemalto) | Compliance requirements |
| **SMS MFA** | Text message code | Legacy, less secure |
| **FIDO2 Security Key** | Passwordless authentication | Modern, biometric support |

## CLI Examples

### Enable MFA for IAM User
```bash
# List virtual MFA devices
aws iam list-virtual-mfa-devices

# Create virtual MFA device
aws iam create-virtual-mfa-device \
    --virtual-mfa-device-name "alice-phone" \
    --outfile "QRCode.png" \
    --bootstrap-method QRCodePNG

# Enable MFA device for user
aws iam enable-mfa-device \
    --user-name alice \
    --serial-number arn:aws:iam::123456789012:mfa/alice-phone \
    --authentication-code1 123456 \
    --authentication-code2 789012
```

### List MFA Devices
```bash
# List MFA devices for a user
aws iam list-mfa-devices \
    --user-name alice

# List all virtual MFA devices
aws iam list-virtual-mfa-devices

# Check if MFA is enabled
aws iam get-user \
    --user-name alice \
    --query 'User.{MFA:MFADevices}'
```

### Deactivate/Remove MFA
```bash
# Deactivate MFA device
aws iam deactivate-mfa-device \
    --user-name alice \
    --serial-number arn:aws:iam::123456789012:mfa/alice-phone

# Delete virtual MFA device
aws iam delete-virtual-mfa-device \
    --serial-number arn:aws:iam::123456789012:mfa/alice-phone
```

### Resync MFA Device
```bash
# Resync if device is out of sync
aws iam resync-mfa-device \
    --user-name alice \
    --serial-number arn:aws:iam::123456789012:mfa/alice-phone \
    --authentication-code1 123456 \
    --authentication-code2 789012
```

## MFA in IAM Policies

### Require MFA for API Calls
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```

### Require MFA for Console Access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                },
                "Null": {
                    "aws:MultiFactorAuthAge": "true"
                }
            }
        }
    ]
}
```

### Allow Specific Actions Without MFA
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:ChangePassword",
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "NotAction": "iam:ChangePassword",
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```

## MFA with STS AssumeRole

```bash
# Assume role with MFA
aws sts assume-role \
    --role-arn "arn:aws:iam::123456789012:role/Admin" \
    --role-session-name "MFASession" \
    --serial-number "arn:aws:iam::987654321098:mfa/admin-user" \
    --token-code 123456
```

## MFA in Named Profiles

```bash
# ~/.aws/config
[profile admin]
role_arn = arn:aws:iam::123456789012:role/Admin
source_profile = default
mfa_serial = arn:aws:iam::987654321098:mfa/admin-user

# Usage - CLI will prompt for MFA code
aws s3 ls --profile admin
# Enter MFA code: 123456
```

## Bash Script: Enforce MFA

```bash
#!/bin/bash
# enforce-mfa.sh
# Apply MFA enforcement policy to all users

POLICY_ARN=$(aws iam create-policy \
    --policy-name "EnforceMFA" \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }]
    }' \
    --query 'Policy.Arn' \
    --output text)

# Attach to all users
for user in $(aws iam list-users --query 'Users[].UserName' --output text); do
    aws iam attach-user-policy \
        --user-name "$user" \
        --policy-arn "$POLICY_ARN"
    echo "MFA enforced for $user"
done
```

## Exam Tips

- ✅ **MFA** adds a second factor of authentication
- ✅ **Virtual MFA** is the most common and cost-effective
- ✅ **U2F/FIDO2** provides phishing-resistant authentication
- ✅ **Condition key**: `aws:MultiFactorAuthPresent` checks if MFA was used
- ✅ **Condition key**: `aws:MultiFactorAuthAge` checks how long since MFA
- ✅ **MFA is required** for API calls to delete MFA devices
- ✅ **Root user** should always have MFA enabled
- ✅ **MFA can be required** via IAM policies or SCPs
- ✅ **STS AssumeRole** supports MFA with `--serial-number` and `--token-code`
- ✅ **Hardware MFA** is required for compliance (FIPS 140-2 Level 3)

## Q&A

**Q1: What is MFA?**
A: Multi-Factor Authentication - requires two or more authentication factors.

**Q2: What types of MFA devices does AWS support?**
A: Virtual MFA (app), U2F security key, Hardware TOTP token, SMS, FIDO2.

**Q3: How do you require MFA for all API calls?**
A: Use an IAM policy with `"aws:MultiFactorAuthPresent": "false"` condition.

**Q4: What is the difference between `aws:MultiFactorAuthPresent` and `aws:MultiFactorAuthAge`?**
A: Present checks if MFA was used; Age checks how long since MFA authentication.

**Q5: How do you assume a role with MFA?**
A: Use `aws sts assume-role` with `--serial-number` and `--token-code`.

**Q6: Can MFA be enforced via SCPs?**
A: Yes, SCPs can require MFA for all accounts in an organization.

**Q7: What happens if you lose your MFA device?**
A: You need to contact AWS Support or use a backup method (if configured).

**Q8: How many virtual MFA devices can you have per user?**
A: Up to 8 MFA devices per user.

**Q9: Can you use the same MFA device for multiple AWS accounts?**
A: Yes, a virtual MFA app can hold tokens for multiple accounts.

**Q10: What is the most secure MFA option?**
A: U2F/FIDO2 security keys (phishing-resistant).

**Q11: How do you enable MFA for the root user?**
A: Via the AWS Console > Security Credentials > Activate MFA.

**Q12: What is the MFA serial number format?**
A: `arn:aws:iam::ACCOUNT-ID:mfa/DEVICE-NAME`.

**Q13: Can MFA be used with access keys?**
A: Yes, via STS AssumeRole with MFA or session policies.

**Q14: What is the bootstrap method for virtual MFA?**
A: QRCodePNG or Base32StringSeed.

**Q15: How do you resync an MFA device?**
A: `aws iam resync-mfa-device` with two consecutive authentication codes.