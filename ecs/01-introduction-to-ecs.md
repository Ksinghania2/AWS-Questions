# Amazon ECS (Elastic Container Service)

ECS is a fully managed container orchestration service.

## Launch Types
| Type | Description | Use Case |
|------|-------------|----------|
| **Fargate** | Serverless (no EC2 management) | Most workloads |
| **EC2** | Manage underlying instances | Large workloads, cost optimization |

## Key Concepts
| Concept | Description |
|---------|-------------|
| **Cluster** | Group of container resources |
| **Task Definition** | JSON blueprint for containers |
| **Task** | Single running instance of a task definition |
| **Service** | Maintains desired count of tasks |
| **Container Agent** | Runs on each EC2 instance |

## CLI
```bash
# Register task definition
aws ecs register-task-definition     --family my-app     --network-mode awsvpc     --requires-compatibilities FARGATE     --cpu "256"     --memory "512"     --container-definitions '[
        {"name":"my-container","image":"nginx:latest","essential":true,"portMappings":[{"containerPort":80,"protocol":"tcp"}]}
    ]'

# Create service
aws ecs create-service     --cluster my-cluster     --service-name my-service     --task-definition my-app     --desired-count 2     --launch-type FARGATE     --network-configuration 'awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}'

# Run task (one-off)
aws ecs run-task     --cluster my-cluster     --task-definition my-app     --launch-type FARGATE     --count 1

# List tasks
aws ecs list-tasks --cluster my-cluster --service-name my-service

# Update service
aws ecs update-service --cluster my-cluster --service my-service --desired-count 5

# Execute command in running task
aws ecs execute-command --cluster my-cluster --task task-xxx --container my-container --interactive --command "/bin/sh"
```

## Task Role vs Task Execution Role
| Role | Purpose |
|------|---------|
| **Task Execution Role** | Pulls images from ECR, sends logs to CloudWatch |
| **Task Role** | Grants permissions to the application code |

## Q&A
**Q1: What is the difference between Fargate and EC2 launch types?** A: Fargate is serverless; EC2 gives you control over instances.
**Q2: What is a task definition?** A: JSON blueprint defining containers, resources, and networking.
**Q3: What is a service?** A: Maintains desired count of running tasks.
**Q4: What is the difference between task role and task execution role?** A: Execution role pulls images/logs; task role is for app permissions.
**Q5: What is ECS Exec?** A: SSH-like access into running containers.
