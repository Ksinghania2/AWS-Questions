# DSSE-KMS (Dual-Layer Server-Side Encryption with KMS)

DSSE-KMS applies **two layers of encryption**: one layer managed by S3 and a second layer managed by KMS. This provides defense-in-depth for the most sensitive data.

## How It Works

```
Two layers of encryption:
Layer 1: S3-managed encryption (AES-256)
Layer 2: KMS-managed encryption (AES-256 via KMS key)
```

- **Key management**: Combined — S3 manages one key, you manage the KMS key
- **Encryption algorithm**: AES-256 × 2 (dual layer)
- **Additional cost**: Higher (extra KMS calls + compute)
- **Use case**: Maximum security, regulatory compliance, defense-in-depth

## CLI Commands

```bash
# Upload with DSSE-KMS
aws s3api put-object \
  --bucket my-bucket \
  --key top-secret.pdf \
  --body top-secret.pdf \
  --server-side-encryption aws:kms:dsse \
  --ssekms-key-id arn:aws:kms:us-east-1:123456789012:key/abc123-...

# Check if object uses DSSE-KMS
aws s3api head-object --bucket my-bucket --key top-secret.pdf \
  --query "ServerSideEncryption" --output text
```

## When to Use DSSE-KMS

| Scenario | Recommendation |
|---|---|
| **Defense-in-depth required** | ✅ DSSE-KMS |
| **Highest security classification** | ✅ DSSE-KMS |
| **Regulatory double-encryption requirement** | ✅ DSSE-KMS |
| **General encryption needs** | ❌ Use SSE-S3 or SSE-KMS (simpler, cheaper) |

## Exam Quick Reference
- ✅ **Two layers** of encryption
- ✅ **S3-managed + KMS-managed** keys
- ✅ **Higher cost** than SSE-S3 or SSE-KMS
- ✅ Best for **maximum security, defense-in-depth**
- ✅ **Newer feature** — may appear in recent exam questions