# S3 Object Lock

See detailed guide at [s3/s3 object overview/locking.md](../s3%20object%20overview/locking.md).

## Quick Reference

- **GOVERNANCE**: Can be bypassed with `s3:BypassGovernanceRetention`
- **COMPLIANCE**: Absolute lock — no one can override
- **Legal Hold**: Indefinite hold — removed manually
- **Prerequisites**: Versioning enabled, enabled at bucket creation
- **Default retention**: Set at bucket level, applied automatically to new objects

```bash
aws s3api create-bucket --bucket my-bucket --object-lock-enabled-for-bucket
aws s3api put-object --bucket my-bucket --key file.txt --body file.txt \
  --object-lock-mode COMPLIANCE --object-lock-retain-until-date 2030-12-31
```

## Exam Tips
- **Cannot be added** to an existing bucket — must be created with it
- **Versioning is required**
- **COMPLIANCE mode** = no one can delete (not even root)
- **GOVERNANCE mode** = admins with proper permissions can override
- **Legal hold** = indefinite, good for lawsuits/eDiscovery