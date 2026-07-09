# Amazon SQS

Message queuing service.

## Standard vs FIFO
| Feature | Standard | FIFO |
|---------|----------|------|
| Throughput | Unlimited | 3000/s |
| Ordering | Best-effort | Strict FIFO |
| Duplicates | At-least-once | Exactly-once |

## CLI
```bash
aws sqs create-queue --queue-name my-queue
aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/xxx/my-queue --message-body "Hello"
aws sqs receive-message --queue-url https://sqs.us-east-1.amazonaws.com/xxx/my-queue --max-number-of-messages 10 --visibility-timeout 30 --wait-time-seconds 20
aws sqs delete-message --queue-url https://sqs.us-east-1.amazonaws.com/xxx/my-queue --receipt-handle RECEIPT
```

## Q&A
**Q1: Standard vs FIFO?** A: Standard = unlimited/no ordering; FIFO = 3000/s/strict ordering. **Q2: What is DLQ?** A: Queue for failed messages. **Q3: Visibility timeout?** A: 30s default, max 12h. **Q4: Long polling?** A: Waits up to 20s for messages. **Q5: Max message size?** A: 256KB (use S3 Extended Client for larger).
