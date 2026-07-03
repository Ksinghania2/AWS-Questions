# CDK Example

AWS CDK lets you write AWS infrastructure in Python.

## Simple example
```python
from aws_cdk import App, Stack
from aws_cdk.aws_s3 import Bucket

class DemoStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        # Create an S3 bucket in this stack.
        Bucket(self, 'DemoBucket')

app = App()
DemoStack(app, 'DemoStack')
app.synth()
```

## Basic steps
```bash
# Set up CDK for the first time
cdk bootstrap

# Deploy the stack
cdk deploy
```
