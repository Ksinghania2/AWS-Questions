# EC2 Instance Metadata & User Data

Instance metadata is data about your EC2 instance that can be used to configure or manage the running instance.

## What is Instance Metadata?

Metadata is data about your EC2 instance that can be accessed from within the instance itself at the link-local address 169.254.169.254.

## IMDSv2 (Recommended)

```bash
# Get session token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Use token for requests
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/
```

## Common Metadata Endpoints

```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Instance identity
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/instance-id)
INSTANCE_TYPE=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/instance-type)
AZ=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/placement/availability-zone)
REGION=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/placement/region)

# Networking
LOCAL_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/local-ipv4)
PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/public-ipv4)
MAC=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/mac)
SUBNET_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/subnet-id)
VPC_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/vpc-id)

# IAM Role
ROLE_NAME=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/iam/security-credentials/ | head -1)
# Get temporary credentials
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE_NAME

# Security groups
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/security-groups
```

## User Data (Bootstrap Scripts)

```bash
# Get user data
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/user-data
```

## IMDSv1 vs IMDSv2

| Feature | IMDSv1 | IMDSv2 |
|---------|--------|--------|
| **Access** | Direct GET | PUT token + GET |
| **Security** | No protection | Session token required |
| **SSRF Protection** | Basic | Strong |
| **Token TTL** | N/A | 1s-6h configurable |

## Exam Tips

- ✅ **IMDSv2** is more secure (session token required)
- ✅ **169.254.169.254** is the metadata endpoint
- ✅ **User data** max 16KB (64KB base64)
- ✅ **Instance identity document** is cryptographically signed
- ✅ **IAM credentials** from metadata auto-rotate
- ✅ **Enforce IMDSv2**: `MetadataOptions.HttpTokens=required`

## Q&A

**Q1: What is the metadata endpoint IP?** A: 169.254.169.254

**Q2: What is the difference between IMDSv1 and IMDSv2?** A: IMDSv2 requires a session token.

**Q3: How do you get the instance ID from within an instance?** A: `curl http://169.254.169.254/latest/meta-data/instance-id`

**Q4: What is user data used for?** A: Bootstrap scripts at instance launch.

**Q5: What is the max size of user data?** A: 16KB raw (64KB base64).

**Q6: How do you get IAM credentials from within an instance?** A: From /latest/meta-data/iam/security-credentials/.

**Q7: How long can an IMDSv2 token last?** A: 1 second to 6 hours.

**Q8: How do you enforce IMDSv2?** A: Set `HttpTokens=required` on the instance.

**Q9: What is the instance identity document?** A: A cryptographically signed document with instance attributes.

**Q10: Is metadata encrypted?** A: No, but only accessible from within the instance.