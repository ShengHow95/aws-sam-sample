import boto3


class CognitoHelper(object):

    def __init__(self, id):
        self._userPoolId = id
        self._client = boto3.client('cognito-idp')

    def getUsersList(self):
        return self._client.list_users(UserPoolId=self._userPoolId)

    def getUser(self, username):
        return self._client.admin_get_user(
            UserPoolId=self._userPoolId,
            Username=username
        )
    
    def createUser(self, username, email):
        return self._client.admin_create_user(
            UserPoolId=self._userPoolId,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
            DesiredDeliveryMediums=['EMAIL'],
            TemporaryPassword='Abcd1234'
        )

    def setUserPassword(self, username, password):
        return self._client.admin_set_user_password(
            UserPoolId=self._userPoolId,
            Username=username,
            Password=password,
            Permanent=True
        )
    
    def disableUser(self, username):
        return self._client.admin_disable_user(
            UserPoolId=self._userPoolId,
            Username=username
        )
    
    def enableUser(self, username):
        return self._client.admin_enable_user(
            UserPoolId=self._userPoolId,
            Username=username
        )