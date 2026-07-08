# VPC Flow Logs

VPC Flow Logs capture information about IP traffic going to/from network interfaces in your VPC.

## Flow Logs Features

| Feature | Description |
|---|---|
| **Source** | VPC, subnet, or network interface level |
| **Destination** | CloudWatch Logs, S3, or Kinesis Firehose |
| **Format** | Custom format or default (version 2, 3, 4, 5) |
| **Logging** | Both accepted and rejected traffic |
| **Metadata** | Protocol, ports, packets, bytes, etc. |
| **Cost** | CloudWatch Logs ingestion + storage costs |

## CLI Commands

```bash
# Create flow logs to CloudWatch Logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-12345 \
  --log-group-name /aws/vpc/flow-logs \
  --deliver-logs-permission-arn arn:aws:iam::123456789012:role/FlowLogsRole \
  --traffic-type ALL

# Create flow logs to S3
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-12345 \
  --log-destination-type s3 \
  --log-destination arn:aws:s3:::my-flow-logs-bucket \
  --traffic-type ALL

# Create with custom format
aws ec2 create-flow-logs \
  --resource-type Subnet \
  --resource-ids subnet-12345 \
  --log-destination-type s3 \
  --log-destination arn:aws:s3:::my-flow-logs-bucket \
  --traffic-type REJECT \
  --log-format '${version} ${vpc-id} ${subnet-id} ${instance-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr}'

# Describe flow logs
aws ec2 describe-flow-logs

# Delete flow logs
aws ec2 delete-flow-logs --flow-log-ids fl-12345
```

## Exam Quick Reference
- ✅ Captures IP traffic metadata (not contents)
- ✅ Can be created at VPC, subnet, or ENI level
- ✅ Destinations: CloudWatch Logs, S3, Kinesis Firehose
- ✅ Traffic types: ALL, ACCEPT, REJECT
- ✅ Does NOT capture: DNS queries, DHCP, Amazon Time Sync, Windows license activation
- ✅ Useful for: security analysis, troubleshooting, compliance
- ✅ Can query with Athena (S3 destination) or CloudWatch Logs Insights