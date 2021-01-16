# AWS SAM/CloudFormation Template Sample

### Services Covered in this templates:
1. VPC
2. Subnets
3. Gateway (Internet/NAT)
4. Security Group
5. S3 Bucket
6. Aurora RDS
7. DynamoDB
8. Lambdas
9. API Gateway
10. CodeCommit
11. CodeBuild
12. CodeDeploy
13. Amplify


### Something to be aware of:
This template is to be deployed to Singapore Region (ap-southeast-1). If your region is different, please kindly change the necessary especially in the VPC and Subnets resources.

### Instructions:
1. On the first time, run the `first-deploy.sh` to create the required S3 Bucket, Frontend CodeCommit Repository and Backend CodeCommit Repository. The following line shows an example of command to be run:

`bash first-deploy.sh -s saas-test-stack -b saas-test-bucket -r saas-test-backend -f saas-test-frontend`

2. Push your template with codes (if necessary) to the created repo and go to CodePipeline. You should see your pipeline is being created and rerun whenever you update or push any code to `master branch`.
