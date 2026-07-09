# CloudFront Functions vs Lambda@Edge

## Comparison
| Feature | CloudFront Functions | Lambda@Edge |
|---------|---------------------|-------------|
| **Runtime** | JavaScript | Node.js, Python |
| **Execution time** | < 1ms | 5s (viewer), 30s (origin) |
| **Memory** | 2MB | 128MB - 10GB |
| **Network access** | No | Yes (can call AWS services) |
| **File system** | No | Yes |
| **Use case** | Lightweight transforms | Complex logic |
| **Cost** | Very low | Higher |
| **Max size** | 10KB | 1MB (viewer), 50MB (origin) |

## When to Use
- **CloudFront Functions**: URL redirects, header manipulation, cache key normalization
- **Lambda@Edge**: A/B testing, user authentication, content personalization, origin fetch

## CLI
```bash
# Create CloudFront Function
aws cloudfront create-function     --name redirect-function     --function-config Comment="URL redirect",Runtime=cloudfront-js-2.0     --function-code 'function handler(event) {
        var request = event.request;
        if (request.uri.endsWith("/")) {
            request.uri += "index.html";
        }
        return request;
    }'

# Publish function
aws cloudfront publish-function --name redirect-function --if-match xxx

# Associate with distribution
aws cloudfront update-distribution     --id E1ABC123DEF     --distribution-config file://config.json
```

## Q&A
**Q1: What is the max execution time for CloudFront Functions?** A: < 1ms.
**Q2: What is the max execution time for Lambda@Edge (viewer)?** A: 5 seconds.
**Q3: Can CloudFront Functions access the network?** A: No.
**Q4: Which is cheaper?** A: CloudFront Functions (very low cost).
**Q5: What are the four event triggers?** A: Viewer Request, Viewer Response, Origin Request, Origin Response.
