# IAM Identity Federation

Identity federation allows users to access AWS resources using existing identities from external identity providers (IdPs) without creating IAM users.

## What is Identity Federation?

A mechanism that lets users authenticate using their existing corporate credentials (Active Directory, Okta, Azure AD, Google, Facebook) and receive temporary AWS credentials via STS.

## Federation Types

| Type | Description | Use Case |
|------|-------------|----------|
| **SAML 2.0** | Enterprise SSO with SAML-compatible IdP | Corporate AD, Okta, Azure AD |
| **Web Identity** | OIDC/OAuth2 with social IdPs | Mobile apps, web apps |
| **OIDC** | OpenID Connect for custom IdPs | Custom identity solutions |
| **Custom Federation** | Custom broker service | Legacy systems |
| **Cognito Identity Pools** | AWS-managed identity federation | Mobile/Web apps with AWS |

## SAML 2.0 Federation

### Architecture
```
User → Corporate AD → SAML IdP → AWS Console/API
                                    │
                                    ├── SAML Assertion
                                    ├── STS: AssumeRoleWithSAML
                                    └── Temporary Credentials
```

### Create SAML Provider
```bash
# Create SAML identity provider
aws iam create-saml-provider \
    --saml-metadata-document file://metadata.xml \
    --name "CorporateAD"

# List SAML providers
aws iam list-saml-providers

# Get SAML provider details
aws iam get-saml-provider \
    --saml-provider-arn arn:aws:iam::123456789012:saml-provider/CorporateAD
```

### Create Role for SAML Federation
```bash
# Create role that trusts SAML provider
aws iam create-role \
    --role-name "SAML-Admin" \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Federated": "arn:aws:iam::123456789012:saml-provider/CorporateAD"
                },
                "Action": "sts:AssumeRoleWithSAML",
                "Condition": {
                    "StringEquals": {
                        "SAML:aud": "https://signin.aws.amazon.com/saml"
                    }
                }
            }
        ]
    }'
```

### Assume Role with SAML
```bash
# This is done by the SAML IdP, not directly by users
# The IdP generates a SAML assertion and calls:
aws sts assume-role-with-saml \
    --role-arn "arn:aws:iam::123456789012:role/SAML-Admin" \
    --principal-arn "arn:aws:iam::123456789012:saml-provider/CorporateAD" \
    --saml-assertion "base64-encoded-saml-assertion"
```

## Web Identity Federation

### Architecture
```
User → Social IdP (Google, FB, Amazon) → ID Token
                                            │
                                            ├── Cognito Identity Pool
                                            ├── STS: AssumeRoleWithWebIdentity
                                            └── Temporary Credentials
```

### Create Role for Web Identity
```bash
# Create role for web identity federation
aws iam create-role \
    --role-name "WebApp-Role" \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Federated": "accounts.google.com"
                },
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Condition": {
                    "StringEquals": {
                        "accounts.google.com:aud": "123456789012.apps.googleusercontent.com"
                    }
                }
            }
        ]
    }'
```

### Assume Role with Web Identity
```bash
# Mobile/web app calls this with ID token from social IdP
aws sts assume-role-with-web-identity \
    --role-arn "arn:aws:iam::123456789012:role/WebApp-Role" \
    --role-session-name "MobileUser123" \
    --web-identity-token "google-id-token" \
    --provider-id "accounts.google.com"
```

## Cognito Identity Pools

### Create Identity Pool
```bash
# Create Cognito identity pool
aws cognito-identity create-identity-pool \
    --identity-pool-name "MyAppPool" \
    --allow-unauthenticated-identities \
    --supported-login-providers '{
        "accounts.google.com": "123456789012.apps.googleusercontent.com",
        "graph.facebook.com": "fb-app-id"
    }'
```

### Set IAM Roles for Identity Pool
```bash
# Set authenticated and unauthenticated roles
aws cognito-identity set-identity-pool-roles \
    --identity-pool-id "us-east-1:abc123" \
    --roles '{
        "authenticated": "arn:aws:iam::123456789012:role/AuthenticatedRole",
        "unauthenticated": "arn:aws:iam::123456789012:role/UnauthenticatedRole"
    }'
```

## AWS IAM Identity Center (SSO)

### Enable Identity Center
```bash
# Create Identity Center instance
aws sso-admin create-instance \
    --name "CompanySSO"

# List instances
aws sso-admin list-instances
```

### Create Permission Set
```bash
# Create permission set
aws sso-admin create-permission-set \
    --instance-arn "arn:aws:sso:::instance/ssoins-abc123" \
    --name "AdministratorAccess" \
    --session-duration "PT8H"

# Attach managed policy
aws sso-admin attach-managed-policy-to-permission-set \
    --instance-arn "arn:aws:sso:::instance/ssoins-abc123" \
    --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-abc123/ps-def456" \
    --managed-policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"
```

### Assign Access
```bash
# Assign user/group to permission set for account
aws sso-admin create-account-assignment \
    --instance-arn "arn:aws:sso:::instance/ssoins-abc123" \
    --target-id "123456789012" \
    --target-type AWS_ACCOUNT \
    --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-abc123/ps-def456" \
    --principal-type GROUP \
    --principal-id "g-abc123"
```

## Federation Comparison

| Feature | SAML 2.0 | Web Identity | Cognito | Identity Center |
|---------|----------|--------------|---------|-----------------|
| **IdP** | Enterprise AD, Okta | Google, FB, Amazon | Any OIDC provider | AWS managed |
| **Protocol** | SAML | OIDC/OAuth2 | OIDC/OAuth2 | SAML/SCIM |
| **Use case** | Enterprise SSO | Mobile/Web apps | Mobile/Web apps | Multi-account SSO |
| **User management** | External | External | Cognito User Pools | Built-in or external |
| **Temporary creds** | STS | STS | STS | AWS SSO tokens |

## Exam Tips

- ✅ **SAML 2.0** for enterprise SSO with Active Directory
- ✅ **Web Identity Federation** for social logins (Google, FB, Amazon)
- ✅ **Cognito Identity Pools** provide AWS credentials to federated users
- ✅ **IAM Identity Center** is the modern SSO service (replaces AWS SSO)
- ✅ **Federation does NOT create IAM users** - uses temporary credentials
- ✅ **AssumeRoleWithSAML** is the STS API for SAML federation
- ✅ **AssumeRoleWithWebIdentity** is the STS API for web identity
- ✅ **SCIM** can sync users/groups from IdP to Identity Center
- ✅ **Attribute-based access control (ABAC)** works with federation
- ✅ **Session duration** can be configured for federated roles

## Q&A

**Q1: What is identity federation?**
A: Using existing identities from external providers to access AWS without creating IAM users.

**Q2: What are the main federation types?**
A: SAML 2.0, Web Identity Federation, Cognito Identity Pools, IAM Identity Center.

**Q3: What STS API is used for SAML federation?**
A: `AssumeRoleWithSAML`.

**Q4: What STS API is used for web identity federation?**
A: `AssumeRoleWithWebIdentity`.

**Q5: What is the difference between Cognito User Pools and Identity Pools?**
A: User Pools are for authentication (sign-in); Identity Pools provide AWS credentials.

**Q6: What is IAM Identity Center?**
A: AWS's managed SSO service (formerly AWS SSO) for multi-account access.

**Q7: Can federation work without IAM users?**
A: Yes, federation uses temporary credentials via STS.

**Q8: What protocol does enterprise federation typically use?**
A: SAML 2.0.

**Q9: How do you create a SAML identity provider?**
A: `aws iam create-saml-provider --saml-metadata-document file://metadata.xml`.

**Q10: What is SCIM in Identity Center?**
A: System for Cross-domain Identity Management - syncs users from IdP.

**Q11: Can you use Google or Facebook to access AWS?**
A: Yes, via Web Identity Federation or Cognito Identity Pools.

**Q12: What is a permission set in Identity Center?**
A: A collection of IAM policies assigned to users/groups for specific accounts.

**Q13: How long can federated sessions last?**
A: Configurable, typically 1-12 hours.

**Q14: What is ABAC in federation?**
A: Attribute-based access control using user attributes from the IdP.

**Q15: What is the benefit of federation over IAM users?**
A: Centralized user management, no credential rotation, SSO experience.