# S3 Object Lock (WORM)

WORM (Write Once, Read Many) storage protects data from being overwritten or deleted. See the detailed guide at [s3 object overview/locking.md](../s3%20object%20overview/locking.md).

## Quick Reference

| Mode | Override Possible? | Use Case |
|---|---|---|
| **GOVERNANCE** | Yes (with `s3:BypassGovernanceRetention`) | Internal policies |
| **COMPLIANCE** | **No** (not even root) | Regulatory compliance |
| **Legal Hold** | Remove hold manually | eDiscovery, legal cases |

## Requirements
- ✅ Must be enabled at **bucket creation** (cannot be added later)
- ✅ **Versioning must be enabled**
- ✅ Default retention can be set at bucket level

```bash
# Create bucket with Object Lock
aws s3api create-bucket --bucket my-locked-bucket \
  --object-lock-enabled-for-bucket --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning --bucket my-locked-bucket \
  --versioning-configuration Status=Enabled

# Set default retention
aws s3api put-object-lock-configuration --bucket my-locked-bucket \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {"DefaultRetention": {"Mode": "GOVERNANCE", "Days": 365}}
  }'

# Upload with compliance lock
aws s3api put-object --bucket my-locked-bucket --key report.pdf \
  --body report.pdf \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date 2030-12-31
```

## Exam Scenarios
- **"Financial records must not be deleted for 7 years"** → Object Lock COMPLIANCE mode
- **"Legal hold on documents during lawsuit"** → Legal Hold
- **"Internal policy prevents deletion for 90 days"** → Object Lock GOVERNANCE mode