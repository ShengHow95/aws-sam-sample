import boto3
import json
import os
REGION = os.environ['AWS_REGION']


class LambdaHelper(object):

    def __init__(self):
        session = boto3.Session(region_name=REGION)
        self._lambdaClient = session.client(service_name='lambda')

    def invokeLambda(self, *, function_arn, payload):
        return self._lambdaClient.invoke(
            FunctionName=function_arn,
            LogType='Tail',
            Payload=json.dumps(payload)
        )