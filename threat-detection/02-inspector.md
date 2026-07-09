# Amazon Inspector

Vulnerability management.

## Scans
- EC2: OS vulnerabilities
- ECR: Container images
- Lambda: Code + dependencies

## CLI
```bash
aws inspector2 enable --resource-types EC2 ECR
aws inspector2 list-findings --filter-criteria '{"severity":[{"comparison":"EQUALS","value":"HIGH"}]}'
aws inspector2 list-coverage --resource-types EC2
```

## Q&A
**Q1: What is Inspector?** A: Vulnerability scanning. **Q2: What it scans for?** A: CVEs. **Q3: Container support?** A: Yes, ECR. **Q4: Network reachability?** A: Checks network exposure. **Q5: Agentless?** A: EC2 uses SSM; ECR agentless.
