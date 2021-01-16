import os
import json
import boto3


def lambda_handler(event, context):

    print("Success")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({"Message": "Success"})
    }
