# Amazon CloudFront

CloudFront is a global Content Delivery Network (CDN) that delivers content with low latency.

## Key Concepts
| Concept | Description |
|---------|-------------|
| **Origin** | Source of content (S3, ALB, EC2, HTTP server) |
| **Distribution** | CloudFront configuration |
| **Edge Location** | Local cache point (450+ locations) |
| **Regional Edge Cache** | Larger cache between origin and edge |
| **Origin Shield** | Centralized cache layer to reduce origin load |
| **Behavior** | Path-based routing rules |

## CLI
```bash
# Create distribution
aws cloudfront create-distribution     --origin-domain-name my-bucket.s3.amazonaws.com     --default-root-object index.html     --enabled

# Create distribution with S3 OAI
aws cloudfront create-distribution-with-origin-access-control     --origin-domain-name my-bucket.s3.amazonaws.com     --default-root-object index.html     --enabled

# Invalidate cache
aws cloudfront create-invalidation     --distribution-id E1ABC123DEF     --paths "/*" "/images/*"

# List distributions
aws cloudfront list-distributions

# Get distribution config
aws cloudfront get-distribution --id E1ABC123DEF
```

## Origin Shield
- Additional caching layer before origin
- Reduces origin load
- Increases cache hit ratio
- Additional cost

## Q&A
**Q1: What is CloudFront?** A: Global CDN for low-latency content delivery.
**Q2: What is Origin Shield?** A: Centralized cache layer that reduces origin load.
**Q3: How do you clear CloudFront cache?** A: Create an invalidation (/* for all objects).
**Q4: What is OAI?** A: Origin Access Identity - restricts S3 access to only CloudFront.
**Q5: What is the difference between Edge Location and Regional Edge Cache?** A: Edge is local cache; Regional Edge Cache is larger, between edge and origin.
