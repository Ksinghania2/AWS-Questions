# AWS Security Hub

Unified security dashboard.

## Aggregates
- GuardDuty findings
- Inspector findings
- Macie findings
- Firewall Manager

## CLI
```bash
aws securityhub enable-security-hub --enable-default-standards
aws securityhub get-findings --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}]}'
aws securityhub get-enabled-standards
aws securityhub disable-security-hub
```

## Q&A
**Q1: What is Security Hub?** A: Central security dashboard. **Q2: Sources?** A: GuardDuty, Inspector, Macie, Firewall Manager. **Q3: Standards?** A: CIS, PCI DSS, AWS Foundational. **Q4: Auto-remediation?** A: Yes via EventBridge. **Q5: Regional?** A: Yes.
