# Amazon API Gateway

API Gateway is a fully managed service for creating, publishing, and securing APIs.

## API Types
| Type | Description | Use Case |
|------|-------------|----------|
| **REST** | RESTful APIs with advanced features | Full control over API |
| **HTTP** | Low-latency HTTP APIs | Simpler, cheaper, faster |
| **WebSocket** | Two-way communication | Real-time apps |

## Key Features
- **Throttling**: Rate limiting (10,000 rps default)
- **Caching**: Response caching to reduce backend load
- **Custom Authorizers**: Lambda or Cognito for auth
- **API Keys**: Usage plans for monetization
- **Stage variables**: Environment-specific config

## CLI
```bash
# Create REST API
aws apigateway create-rest-api --name MyAPI --region us-east-1

# Get root resource ID
ROOT_ID=$(aws apigateway get-resources --rest-api-id abc123 --query 'items[0].id' --output text)

# Create resource
RESOURCE_ID=$(aws apigateway create-resource     --rest-api-id abc123     --parent-id $ROOT_ID     --path-part "orders"     --query 'id' --output text)

# Create method (POST)
aws apigateway put-method     --rest-api-id abc123     --resource-id $RESOURCE_ID     --http-method POST     --authorization-type NONE     --api-key-required

# Create HTTP API (simpler)
aws apigatewayv2 create-api     --name MyHTTPAPI     --protocol-type HTTP     --target arn:aws:lambda:us-east-1:xxx:function:my-function

# Create WebSocket API
aws apigatewayv2 create-api     --name MyWSAPI     --protocol-type WEBSOCKET     --route-selection-expression '$request.body.action'

# Deploy API
aws apigateway create-deployment     --rest-api-id abc123     --stage-name prod

# Create usage plan
aws apigateway create-usage-plan     --name BasicPlan     --api-stages apiId=abc123,stage=prod     --throttle burstLimit=20,rateLimit=10
```

## Q&A
**Q1: What are the three API types?** A: REST, HTTP, WebSocket.
**Q2: What is the difference between REST and HTTP APIs?** A: HTTP APIs are simpler, cheaper, and faster (but less feature-rich).
**Q3: How do you throttle API requests?** A: Via usage plans with rate/burst limits.
**Q4: What are custom authorizers?** A: Lambda functions that validate auth tokens.
**Q5: Can API Gateway cache responses?** A: Yes, to reduce backend load.
