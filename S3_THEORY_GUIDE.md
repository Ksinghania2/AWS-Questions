# AWS S3 Theory Guide

This file is a revision-style guide for AWS S3. It is written so that even a beginner can understand the main theory clearly after reading it once. It covers the most important concepts, rules, features, limits, and common exam points.

## 1. What is S3?
Amazon S3 stands for Simple Storage Service. It is an AWS service used to store objects such as files, images, videos, documents, logs, backups, and application data.

S3 is one of the most important AWS services because it is:
- simple to use
- highly scalable
- durable and reliable
- available globally
- suitable for backup, archive, static websites, and content storage

Important point: S3 is object storage, not block storage and not a traditional filesystem.

Example:
```bash
aws s3 ls
```

## 2. Core S3 Concepts
### Bucket
A bucket is a container that stores objects. Every object must live inside a bucket.

Think of a bucket as a top-level folder in cloud storage.

Example:
```bash
aws s3api create-bucket --bucket my-demo-bucket --region us-east-1
```

### Object
An object is the actual file stored in S3. Each object has:
- data (the file content)
- metadata (extra information about the file)
- a key (the name/path inside the bucket)

Example:
```bash
aws s3 cp hello.txt s3://my-demo-bucket/hello.txt
```

### Key
The key is the full name of the object inside the bucket. It works like a file path.

Examples:
- `hello.txt`
- `images/logo.png`
- `backup/2024/file.zip`

### Prefix
A prefix is the part of the object key before the last slash. It helps group files logically.

Example:
- `images/` is a prefix
- `images/logo.png` is an object key

## 3. How S3 Organizes Data
S3 is different from a normal hard drive or file server because it does not use folders in the traditional sense. Instead, it uses object keys that look like paths.

So even if you see names like:
- `docs/report.pdf`
- `images/photo.jpg`

S3 still stores them as object keys inside a bucket.

This is why S3 is often described as a flat storage system with logical grouping through prefixes.

## 4. Bucket Naming Rules
A bucket name must follow strict rules:
- 3 to 63 characters long
- only lowercase letters, numbers, and hyphens
- must start and end with a letter or number
- must be globally unique across all AWS accounts
- cannot be an IP address

Good examples:
- `my-bucket-2024`
- `project-data-123`

Bad examples:
- `MyBucket`
- `my_bucket`
- `mybucket-`

Important exam point: bucket names are unique globally, not just within your account.

## 5. Bucket Restrictions and Limitations
There are some important restrictions in S3:
- bucket names must be unique globally
- bucket names cannot contain uppercase letters
- bucket names cannot contain underscores
- bucket names cannot contain spaces
- a bucket cannot be nested inside another bucket
- S3 does not support true folder hierarchy the way a local file system does

These restrictions matter because bucket naming and structure affect how you design storage.

## 6. Bucket Types and Common Use Cases
S3 is commonly used for different purposes:

### General-purpose bucket
Used for storing files, backups, logs, and application data.

### Static website bucket
Used to host web pages.

### Data lake bucket
Used to store large amounts of structured or unstructured data.

### Backup bucket
Used for archive and disaster recovery.

### Log bucket
Used for storing application logs and system logs.

## 7. S3 Storage Classes
S3 offers different storage classes depending on access frequency and cost.

### Standard
Best for frequently accessed data.
- low latency
- high throughput
- good for active files

### Standard-IA
Best for infrequently accessed data.
- cheaper than Standard
- retrieval is more expensive

### One Zone-IA
Lower-cost storage stored in one Availability Zone.
- less resilient than Standard-IA

### Intelligent-Tiering
Automatically moves objects between access tiers based on usage.
- good when access patterns are uncertain

### Glacier
Used for archives and long-term storage.
- very low cost
- retrieval takes time

### Glacier Deep Archive
Used for rarely accessed archival data.
- lowest cost
- retrieval is very slow

Example:
```bash
aws s3 cp file.txt s3://my-bucket/file.txt --storage-class STANDARD_IA
```

## 8. Versioning
Versioning keeps multiple versions of the same object.

This is useful when:
- a file is overwritten by mistake
- a file is deleted accidentally
- you need to restore an older copy

Important points:
- versioning is enabled at the bucket level
- each version is stored separately
- old versions can be recovered later
- versioning increases storage cost

Example:
```bash
aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled
```

## 9. Encryption
S3 can protect stored data with encryption.

### SSE-S3
Server-side encryption with S3-managed keys.
- easy to use
- AWS manages the keys

### SSE-KMS
Server-side encryption with AWS KMS keys.
- better control and auditability
- good for regulated workloads

### Client-Side Encryption
The client encrypts the data before uploading it.
- application-managed security

Example:
```bash
aws s3 cp secret.txt s3://my-bucket/secret.txt --sse aws:kms
```

## 10. Access Control in S3
Access to S3 is controlled using several methods.

### IAM Policies
These are attached to users, groups, or roles.

### Bucket Policies
These are attached to the bucket itself.

### Access Control Lists (ACLs)
An older access control method. It is less commonly used now.

### Block Public Access
A setting that prevents public access by mistake.

Important point:
- S3 buckets are private by default
- public access must be enabled intentionally

Example policy idea:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

## 11. Bucket Policies vs IAM Policies
- Bucket policies are attached to buckets.
- IAM policies are attached to identities.

Use bucket policy when access should be controlled at bucket level.
Use IAM policy when you want to control what a specific user or role can do.

## 12. Lifecycle Rules
Lifecycle rules automatically move or delete objects based on age.

Common examples:
- move old files to Standard-IA after 30 days
- move old files to Glacier after 90 days
- delete files after 365 days

Lifecycle rules help reduce cost and keep storage organized.

## 13. Static Website Hosting
S3 can host a static website using HTML, CSS, and JavaScript files.

Use cases:
- personal websites
- documentation sites
- landing pages

Important requirements:
- enable static website hosting on the bucket
- upload an index document
- make the files public if the site should be accessible publicly

Example:
- upload `index.html`
- enable static website hosting

## 14. Multipart Upload
Multipart upload is used for large files.

It helps because:
- large files can be uploaded in parts
- uploads are more reliable
- uploads can be resumed
- performance is better for big files

This is commonly used for videos, backups, and large archives.

Example:
```bash
aws s3 cp largefile.zip s3://my-bucket/largefile.zip
```

## 15. ETag
An ETag is a hash-like value that identifies an object version.

It helps check whether data changed.

Example:
```bash
aws s3api head-object --bucket my-bucket --key hello.txt --query ETag --output text
```

If the object content changes, the ETag usually changes too.

## 16. Consistency Model
S3 provides strong read-after-write consistency for new object PUTs and DELETEs.

That means:
- after uploading a file, you can read it immediately
- after deleting a file, the delete result is visible immediately

This makes S3 predictable and reliable.

## 17. Event Notifications
S3 can trigger events when objects are created, deleted, or modified.

Common examples:
- trigger a Lambda function after upload
- send an email or notification
- start processing on new files

## 18. Cross-Region Replication
Cross-Region Replication (CRR) copies objects from one bucket to another bucket in a different region.

Why it is used:
- disaster recovery
- compliance
- lower latency for users in another region

## 19. Transfer Acceleration
Transfer Acceleration speeds up uploads to S3 using AWS edge locations.

Useful when:
- users are far away from the bucket region
- large uploads need better performance

## 20. Object Lock
Object Lock prevents objects from being deleted or overwritten for a defined period.

It is used for:
- legal holds
- compliance requirements
- retention policies

## 21. Inventory and Analytics
S3 can provide storage inventory and analytics reports.

Useful for:
- auditing objects
- tracking storage usage
- monitoring cost

## 22. Common S3 Commands
```bash
# create bucket
aws s3api create-bucket --bucket my-bucket --region us-east-1

# upload file
aws s3 cp hello.txt s3://my-bucket/hello.txt

# list files
aws s3 ls s3://my-bucket/

# delete file
aws s3 rm s3://my-bucket/hello.txt
```

## 23. Important Exam Points
- S3 is object storage, not block storage
- Data is stored in buckets as objects
- Every object has a key
- Bucket names must be unique globally
- Bucket names cannot contain uppercase letters or underscores
- Buckets are private by default
- Use versioning for protection
- Use encryption for security
- Use lifecycle rules to manage cost
- Use policies and IAM to control access
- S3 is commonly used for backups, archives, static websites, and file storage

## 24. Short Summary
S3 is a highly scalable object storage service used for storing files in buckets. The most important principles to remember are bucket naming, object keys, storage classes, versioning, encryption, access control, lifecycle rules, and consistency.
