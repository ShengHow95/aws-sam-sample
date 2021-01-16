import boto3
import json
import re
import os
REGION = os.environ['AWS_REGION']


class RdsDataHelper(object):

    def __init__(self, *, tags=['admin']):
        session = boto3.Session(region_name=REGION)
        self._s3Client = session.resource(service_name='s3')
        self._smClient = session.client(service_name='secretsmanager')
        self._rdsDataClient = session.client(service_name='rds-data')
        self.getSecretsDetails(tags)

    def getSecretsDetails(self, tags=[]):
        self._secrets = self._smClient.list_secrets(
            Filters=[{ 'Key': 'tag-value', 'Values': [tag] } for tag in tags ]
        )['SecretList'][0]

        self._secretsArn = self._secrets['ARN']
        self._secretsName = self._secrets['Name']
        self._secretsValues = json.loads(self._smClient.get_secret_value(SecretId=self._secretsName)['SecretString'])
        
        accountId = self._secrets['ARN'].split(":")[4]
        dbClusterIdentifier = self._secretsValues['dbClusterIdentifier']
        self._rdsArn = self._secretsValues.get('dbClusterArn', 'arn:aws:rds:{}:{}:cluster:{}'.format(REGION, accountId, dbClusterIdentifier))
        self._s3Bucket = self._secretsValues['s3Bucket']

    def createDatabase(self, *, database):
        createDbSql = 'CREATE DATABASE {};'.format(database)
        self.executeSql(sql_statement=createDbSql)

    def createDatabaseUser(self, *, username, password, database):
        createUserSql = 'CREATE USER "{}"@"%" IDENTIFIED BY "{}"'.format(username, password)
        grantPrivSql = 'GRANT SELECT,INSERT,UPDATE ON {}.* TO "{}"@"%" WITH GRANT OPTION'.format(database,username)
        flushPrivSql = 'FLUSH PRIVILEGES'
        self.executeSql(sql_statement=createUserSql)
        self.executeSql(sql_statement=grantPrivSql)
        self.executeSql(sql_statement=flushPrivSql)

    def importTables(self, *, database):
        bucket = self._s3Client.Bucket(self._s3Bucket)
        for obj in bucket.objects.filter(Prefix='sqldump/'):
            objContent = bucket.Object(key=obj.key).get()
            objBody = objContent['Body'].read()
            for sqlLine in objBody.decode("utf-8").strip().split(';'):
                sqlLine = re.sub('^\\s*--.*\n?', '', sqlLine, flags=re.MULTILINE)
                if sqlLine == '' :
                    continue
                self.executeSql(sql_statement=sqlLine, database=database)

    def executeSql(self, *, sql_statement, database=None):
        if database is None:
            return self._rdsDataClient.execute_statement(
                secretArn=self._secretsArn,
                resourceArn=self._rdsArn,
                sql=sql_statement
            )
        else:
            return self._rdsDataClient.execute_statement(
                secretArn=self._secretsArn,
                resourceArn=self._rdsArn,
                database=database,
                sql=sql_statement
            )