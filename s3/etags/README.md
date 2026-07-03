# ETag Notes

# ETag is a short value that S3 gives to an object.
# It helps you check whether the file changed.

## Simple idea
- Upload a file
- Get its ETag
- Compare it later

## Beginner example
```bash
# Create a small test file
printf 'hello\n' > hello.txt

# Upload it to S3
aws s3 cp hello.txt s3://my-bucket/hello.txt

# Get the ETag
aws s3api head-object --bucket my-bucket --key hello.txt --query ETag --output text
```

## What to remember
- If the file changes, the ETag usually changes too.
- ETag is useful for checking if an object is the same or different.
