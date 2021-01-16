import boto3
import json
import os
REGION = os.environ['AWS_REGION']


class SecretsManagerHelper(object):

    def __init__(self):
        session = boto3.Session(region_name=REGION)
        self._smClient = session.client(service_name='secretsmanager')

    def createSecret(self, *, unique_code, secrets, tags=[]):
        return self._smClient.create_secret(
            Name='{}.db'.format(unique_code),
            Description='Secrets for Tenant Database {}.db'.format(unique_code),
            SecretString=json.dumps(secrets),
            Tags=tags
        )

    def getSecret(self, *, secret_name):
        return json.loads(self._smClient.get_secret_value(SecretId=secret_name)['SecretString'])

    def listSecrets(self, *, tags=[]):
        return self._smClient.list_secrets(
            Filters=[{ 'Key': 'tag-value', 'Values': [tag] } for tag in tags ]
        )['SecretList']