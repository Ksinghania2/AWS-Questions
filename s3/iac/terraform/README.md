# Terraform Example

Terraform uses simple config files to create AWS resources.

## Simple example
```hcl
# Create a simple S3 bucket with Terraform.
resource "aws_s3_bucket" "example" {
  bucket = "my-terraform-bucket"
}
```

## Basic steps
```bash
# Download providers and modules
terraform init

# See what will change
terraform plan

# Apply the change
terraform apply
```
