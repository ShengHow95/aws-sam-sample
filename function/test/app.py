import os
import json
import boto3
import string
import secrets
# from dynamodbhelper import DynamoDbHelper
# from secretsmanagerhelper import SecretsManagerHelper
# from lambdahelper import LambdaHelper

# Helper Objects Initialization
# dynamodbHelper = DynamoDbHelper(table_name=os.environ['DDBTable'])
# secretsManagerHelper = SecretsManagerHelper()
# lambdaHelper = LambdaHelper()

PASSWORD_FORMAT = string.ascii_letters + string.digits + '!#$%&()*+,-./:;<=>?[]^_{|}~'

def get_secure_random_string(length):
    secure_str = ''.join((secrets.choice(PASSWORD_FORMAT) for i in range(length)))
    return secure_str

def lambda_handler(event, context):

    # Event Variables
    # requestBody = json.loads(event['body'])
    
    try:
        # Actions
        # ddbResponse = dynamodbHelper.addSingleItem(item=requestBody)
        
        # secretsList = secretsManagerHelper.listSecrets(tags=['admin'])
        # secrets = secretsManagerHelper.getSecret(secret_name=secretsList[0]['Name'])
        # secrets['username'] = requestBody['UniqueCode']+'-user'
        # secrets['password'] = get_secure_random_string(16)
        # secrets['uniquecode'] = requestBody['UniqueCode']
        
        # lambdaResponse = lambdaHelper.invokeLambda(
        #     function_arn=os.environ['DatabaseAddFunctionArn'],
        #     payload= { "body": secrets }
        # )

        # if 'FunctionError' in lambdaResponse:
        #     raise Exception(json.loads(lambdaResponse['Payload'].read().decode('utf-8'))['errorMessage'])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"Message": "Successfully Executed Lambda Function"})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"Message": str(e)})
        }
