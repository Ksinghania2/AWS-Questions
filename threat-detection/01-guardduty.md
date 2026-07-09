# Amazon GuardDuty

Intelligent threat detection.

## Data Sources
- VPC Flow Logs
- CloudTrail
- DNS Logs

## CLI
```bash
aws guardduty create-detector --enable
aws guardduty list-findings --detector-id DETECTORID
aws guardduty get-findings --detector-id DETECTORID --finding-ids FINDINGID
aws guardduty create-filter --detector-id DETECTORID --name Critical --finding-criteria '{"Criterion":{"severity":{"Gte":7}}}'
```

## Q&A
**Q1: What is GuardDuty?** A: Threat detection. **Q2: Data sources?** A: VPC Flow Logs, CloudTrail, DNS. **Q3: Finding?** A: Potential security issue. **Q4: Regional?** A: Yes, per region. **Q5: Severity levels?** A: Low(1-3), Medium(4-6), High(7-8.9), Critical(9-10).
