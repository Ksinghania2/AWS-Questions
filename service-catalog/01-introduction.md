# AWS Service Catalog

Create and manage IT service catalogs.

## Concepts
| Concept | Description |
|---------|-------------|
| Portfolio | Collection of products |
| Product | CloudFormation template |
| Constraint | Limits on product (launch, notification) |
| Provisioning Artifact | Version of product |

## CLI
```bash
aws servicecatalog create-product --name "EC2-Bastion" --owner "IT" --product-type CLOUD_FORMATION_TEMPLATE --provisioning-artifact-parameters '{"Name":"v1","Description":"Bastion host","Info":{"LoadTemplateFromURL":"https://s3.amazonaws.com/my-bucket/template.yaml"}}'
aws servicecatalog create-portfolio --display-name "Developer Tools" --provider-name "IT"
aws servicecatalog associate-product-with-portfolio --product-id prod-xxx --portfolio-id port-xxx
```

## Q&A
**Q1: What is Service Catalog?** A: IT service catalog for approved products. **Q2: What defines a product?** A: CloudFormation template. **Q3: What is a portfolio?** A: Collection of products. **Q4: What are constraints?** A: Limits (instance types, tags). **Q5: Can users self-provision?** A: Yes, from the catalog.
