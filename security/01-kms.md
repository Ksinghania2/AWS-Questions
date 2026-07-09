# AWS KMS

Key management and encryption.

## Key Types
| Type | Control |
|------|---------|
| AWS Managed | By AWS service |
| Customer Managed | Full control (rotation, policy) |
| Custom Key Store | CloudHSM-backed (FIPS 140-2 L3) |

## CLI
```bash
aws kms create-key --description "My key"
aws kms create-alias --alias-name alias/my-key --target-key-id xxx
aws kms encrypt --key-id alias/my-key --plaintext fileb://plaintext.txt --output text --query CiphertextBlob > encrypted.txt
aws kms decrypt --ciphertext-blob fileb://encrypted.txt --output text --query Plaintext | base64 --decode > decrypted.txt
aws kms generate-data-key --key-id alias/my-key --key-spec AES_256
aws kms enable-key-rotation --key-id xxx
```

## Q&A
**Q1: AWS Managed vs Customer Managed?** A: Customer = full control. **Q2: What is envelope encryption?** A: Encrypt data key with KMS key. **Q3: Max encrypt size?** A: 1MB. **Q4: Key rotation?** A: Yearly for customer managed. **Q5: Custom Key Store?** A: CloudHSM-backed. **Q6: IAM vs Key Policy?** A: Both needed; key policy must trust IAM.
