# AWS Step Functions

Step Functions is a serverless orchestration service for building distributed applications as state machines.

## Key Concepts
| Concept | Description |
|---------|-------------|
| **State Machine** | Workflow definition in JSON (Amazon States Language) |
| **Task** | Single unit of work (Lambda, Activity, API call) |
| **Choice** | Conditional branching |
| **Parallel** | Execute branches concurrently |
| **Wait** | Delay execution |
| **Map** | Run steps for each item in a list |

## Workflow Types
| Type | Description |
|------|-------------|
| **Standard** | Long-running (up to 1 year), exactly-once |
| **Express** | Short-running (5 min), at-least-once or exactly-once |

## CLI
```bash
# Create state machine
aws stepfunctions create-state-machine     --name my-workflow     --definition '{
        "Comment": "A simple workflow",
        "StartAt": "ProcessOrder",
        "States": {
            "ProcessOrder": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:xxx:function:process-order",
                "Next": "CheckStatus"
            },
            "CheckStatus": {
                "Type": "Choice",
                "Choices": [
                    {"Variable": "$.status","StringEquals": "APPROVED","Next": "ShipOrder"},
                    {"Variable": "$.status","StringEquals": "REJECTED","Next": "NotifyRejection"}
                ]
            },
            "ShipOrder": {"Type":"Task","Resource":"arn:aws:lambda:us-east-1:xxx:function:ship-order","End":true},
            "NotifyRejection": {"Type":"Task","Resource":"arn:aws:lambda:us-east-1:xxx:function:notify-rejection","End":true}
        }
    }'     --role-arn arn:aws:iam::xxx:role/step-functions-role

# Start execution
aws stepfunctions start-execution     --state-machine-arn arn:aws:states:us-east-1:xxx:stateMachine:my-workflow     --input '{"orderId":"123","status":"APPROVED"}'

# List executions
aws stepfunctions list-executions --state-machine-arn arn:aws:states:us-east-1:xxx:stateMachine:my-workflow
```

## Q&A
**Q1: What is Step Functions used for?** A: Orchestrating multi-step serverless workflows.
**Q2: What is the difference between Standard and Express workflows?** A: Standard (up to 1 year, exactly-once); Express (5 min, at-least-once).
**Q3: What is the Amazon States Language?** A: JSON-based language for defining state machines.
**Q4: What state types are available?** A: Task, Choice, Parallel, Wait, Map, Fail, Succeed, Pass.
**Q5: Can Step Functions invoke Lambda, ECS, or API Gateway?** A: Yes, via Task states.
