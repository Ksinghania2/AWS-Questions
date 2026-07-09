# Amazon EKS (Elastic Kubernetes Service)

EKS provides managed Kubernetes clusters.

## Key Features
- Managed control plane (multi-AZ)
- Worker nodes (self-managed or managed node groups)
- Fargate for serverless pods
- Integrated with IAM, VPC, CloudWatch

## CLI
```bash
# Create EKS cluster
aws eks create-cluster     --name my-cluster     --role-arn arn:aws:iam::xxx:role/eks-cluster-role     --resources-vpc-config subnetIds=subnet-xxx,subnet-yyy,securityGroupIds=sg-xxx

# Create node group
aws eks create-nodegroup     --cluster-name my-cluster     --nodegroup-name my-nodes     --node-role arn:aws:iam::xxx:role/eks-node-role     --subnets subnet-xxx subnet-yyy     --instance-types t3.medium     --scaling-config minSize=2,maxSize=10,desiredSize=3

# Update kubeconfig
aws eks update-kubeconfig --name my-cluster --region us-east-1

# Run kubectl commands
kubectl get nodes
kubectl get pods -n kube-system

# Delete cluster
aws eks delete-cluster --name my-cluster
```

## Q&A
**Q1: What is EKS?** A: Managed Kubernetes service.
**Q2: Does EKS manage the control plane?** A: Yes, it's multi-AZ and managed by AWS.
**Q3: What are the worker node options?** A: Managed node groups, self-managed, or Fargate.
**Q4: How do you connect to an EKS cluster?** A: `aws eks update-kubeconfig --name cluster-name`.
**Q5: What is EKS Distro?** A: Open-source Kubernetes distribution used by EKS.
