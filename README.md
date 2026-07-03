# AWS S3 Practice Repo

This repo is a simple place to practice AWS S3 with the CLI, PowerShell, IaC tools, and SDKs.

## What you can try
- create an S3 bucket
- upload a file
- list bucket contents
- try basic CloudFormation, CDK, Terraform, and Pulumi examples
- explore Java and Ruby SDK starters

## Main folders
- [s3/bash-scripts](s3/bash-scripts) : simple AWS CLI examples
- [s3/powershell-scripts](s3/powershell-scripts) : PowerShell example
- [s3/iac/cfn](s3/iac/cfn) : CloudFormation example
- [s3/iac/cdk](s3/iac/cdk) : CDK example
- [s3/iac/terraform](s3/iac/terraform) : Terraform example
- [s3/iac/pulumi](s3/iac/pulumi) : Pulumi example
- [s3/sdk/java](s3/sdk/java) : Java SDK starter
- [s3/sdk/ruby](s3/sdk/ruby) : Ruby SDK starter
- [s3/etags](s3/etags) : short ETag notes

## Basic terminal commands
```bash
cd s3/bash-scripts
./create-bucket my-test-bucket
./put-object my-test-bucket hello.txt
./list-objects my-test-bucket
```

## Setup notes
- Run the installer scripts in [bin](bin) if you need AWS CLI, PowerShell, or Terraform.
- Make sure your AWS CLI is configured before running the examples.
