: '

    This script should run on the first deployment. Thereby, allowing creation of pre-required resources to be created.

    Tags (Case Sensitive):
    -s      SAM/CloudFormation Stack Name
    -b      S3 Bucket Name
    -r      Backend Repository Name (CodeCommit)
    -f      Frontend Repository Name (CodeCommit)
    
    Example of Command:
    bash sam-deploy.sh -s saas-test-stack -b saas-test-bucket -r saas-test-backend -f saas-test-frontend

'

#!/bin/bash
set -eo pipefail

while getopts s:b:r:f: option
    do
    case ${option}
        in
        s) STACK_NAME=${OPTARG};;
        b) BUCKET_NAME=${OPTARG};;
        r) BACKEND_REPO=${OPTARG};;
        f) FRONTEND_REPO=${OPTARG};;
    esac
done

[ -z ${STACK_NAME}  ] && echo "Error: STACK_NAME (-s) argument is missing." && exit 1;
[ -z ${BUCKET_NAME} ] && echo "Error: BUCKET_NAME (-b) argument is missing." && exit 1;
[ -z ${BACKEND_REPO} ] && echo "Error: BACKEND_REPO (-r) argument is missing." && exit 1;
[ -z ${FRONTEND_REPO} ] && echo "Error: FRONTEND_REPO (-f) argument is missing." && exit 1;

# check and create s3 bucket if not exists
if aws s3api head-bucket --bucket $BUCKET_NAME 2>/dev/null; 
then
    echo $BUCKET_NAME
else
    aws s3 mb s3://$BUCKET_NAME
fi

# check and create backend codecommit repo if not exists
if aws codecommit get-repository --repository-name $BACKEND_REPO | grep -w $BACKEND_REPO
then
    echo $BACKEND_REPO
else
    aws codecommit create-repository --repository-name $BACKEND_REPO
fi

# check and create backend codecommit repo if not exists
if aws codecommit get-repository --repository-name $FRONTEND_REPO | grep -w $FRONTEND_REPO
then
    echo $FRONTEND_REPO
else
    aws codecommit create-repository --repository-name $FRONTEND_REPO
fi

# build dependencies (if any)
sam build

# put openapi file into s3 bucket
aws s3api put-object --bucket $BUCKET_NAME --key $STACK_NAME/openapi-spec.yaml --body ./openapi-spec.yaml

# package sam template (to be compatible with cloudformation template) 
# then upload required files (e.g. dependencies) to specified bucket
sam package --output-template-file packaged.yaml --s3-bucket $BUCKET_NAME --s3-prefix ${STACK_NAME}

# put packaged.yaml file to specified bucket 
aws s3api put-object --bucket $BUCKET_NAME --key $STACK_NAME/packaged.yaml --body ./packaged.yaml

# deploy packaged.yaml file and upload to specified bucket
sam deploy --template-file packaged.yaml --s3-bucket $BUCKET_NAME --s3-prefix ${STACK_NAME} --stack-name $STACK_NAME --capabilities CAPABILITY_IAM --parameter-overrides SaaSEnrolmentS3BucketName=${BUCKET_NAME} BackendRepository=${BACKEND_REPO} FrontendRepository=${FRONTEND_REPO}
