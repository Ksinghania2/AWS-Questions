# AWS AppSync

Managed GraphQL service.

## CLI
```bash
aws appsync create-graphql-api --name my-api --authentication-type API_KEY
aws appsync create-data-source --api-id abc123 --name UserTable --type AMAZON_DYNAMODB --dynamodb-config tableName=Users,awsRegion=us-east-1
```

## Q&A
**Q1: What is AppSync?** A: Managed GraphQL. **Q2: Difference from API Gateway?** A: AppSync = GraphQL + subscriptions; API Gateway = REST/HTTP. **Q3: Data sources?** A: DynamoDB, Lambda, RDS, HTTP. **Q4: Real-time?** A: Yes, via WebSocket subscriptions. **Q5: Offline support?** A: Yes.
