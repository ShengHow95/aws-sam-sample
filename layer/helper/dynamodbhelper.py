import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr, And, Or


class DynamoDbHelper(object):

    _pkName = None
    _skName = None

    def __init__(self, *, table_name):
        self._table = boto3.resource('dynamodb').Table(table_name)
        keySchema = self._table.key_schema
        self._pkName = keySchema[0]['AttributeName']
        if len(keySchema) == 2:
            self._skName = keySchema[1]['AttributeName']

    def addSingleItem(self, *, item):
        item[self._pkName] = str(uuid.uuid1().hex)
        return self._table.put_item(Item=item)

    def getSingleItem(self, *, item):
        if self._skName == None:
            return self._table.query(
                KeyConditionExpression=Key(self._pkName).eq(item[self._pkName]),
                ConsistentRead=True,
            )['Items'][0]
        else:
            return self._table.query(
                KeyConditionExpression=Key(self._pkName).eq(item[self._pkName]) & Key(self._skName).eq(item[self._skName]),
                ConsistentRead=True,
            )['Items'][0]

    def updateSingleItem(self, *, item):
        responseItem = self.getSingleItem(item=item)
        responseItem.update(item)
        return self._table.put_item(Item=responseItem)

    def scanAllItems(self, *, attributes_returned_list=[], filter_expression_list=[]):
        if attributes_returned_list == [] and filter_expression_list == []:
            return self._table.scan()['Items']
        elif attributes_returned_list != [] and filter_expression_list == []:
            if len(attributes_returned_list) == 1:
                return self._table.scan(ProjectionExpression=attributes_returned_list[0])['Items']
            elif len(attributes_returned_list) > 1:
                return self._table.scan(ProjectionExpression=','.join(attributes_returned_list))['Items']
        elif attributes_returned_list == [] and filter_expression_list != []:
            if len(filter_expression_list) == 1:
                return self._table.scan(FilterExpression=filter_expression_list[0])['Items']
            elif len(filter_expression_list) > 1:
                return self._table.scan(FilterExpression=And(*filter_expression_list))['Items']
        elif attributes_returned_list != [] and filter_expression_list != []:
            if len(attributes_returned_list) == 1 and len(filter_expression_list) == 1:
                return self._table.scan(
                    ProjectionExpression=attributes_returned_list[0],
                    FilterExpression=filter_expression_list[0]
                )['Items']
            elif len(attributes_returned_list) == 1 and len(filter_expression_list) > 1:
                return self._table.scan(
                    ProjectionExpression=attributes_returned_list[0],
                    FilterExpression=And(*filter_expression_list)
                )['Items']
            elif len(attributes_returned_list) > 1 and len(filter_expression_list) == 1:
                return self._table.scan(
                    ProjectionExpression=','.join(attributes_returned_list),
                    FilterExpression=filter_expression_list[0]
                )['Items']
            elif len(attributes_returned_list) > 1 and len(filter_expression_list) > 1:
                return self._table.scan(
                    ProjectionExpression=','.join(attributes_returned_list),
                    FilterExpression=And(*filter_expression_list)
                )['Items']