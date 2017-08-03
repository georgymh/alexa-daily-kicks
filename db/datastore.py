import json
import decimal
import datetime

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

from utils.utils import getTodaysDate
from utils.utils import DecimalEncoder
from utils.config import KICKS_TABLE_NAME
from utils.config import KICKS_METADATA_TABLE_NAME
from utils.config import KICKS_PROPERTY_TYPES_FOR_DYNAMO
from utils.config import KICKS_METADATA_PROPERTY_TYPES_FOR_DYNAMO


class DataStore(object):
    def __init__(self):
        self._table_name = KICKS_TABLE_NAME
        self._client = boto3.client('dynamodb')
        self._table = boto3.resource('dynamodb').Table(self._table_name)

    def retrieveKicks(self, date):
        response = self._client.scan(
            TableName=KICKS_TABLE_NAME,
            FilterExpression='ReleaseDate = :date',
            ExpressionAttributeValues={':date': {'S': date}}
        )
        #print('Response', json.dumps(response, indent=4, cls=DecimalEncoder))
        return response['Items']

    def retrieveNumberOfStoredKicks(self, date):
        response = self._client.scan(
            TableName=KICKS_METADATA_TABLE_NAME,
            FilterExpression='ReleaseDate = :date',
            ExpressionAttributeValues={':date': {'S': date}}
        )
        #print('Response\n',json.dumps(response, indent=4, cls=DecimalEncoder))
        if response["Count"] == 0:
            return 0
        return int(response["Items"][0]["Count"]["N"])

    def storeKicksMetadata(self, date, count):
        response = self._client.put_item(
            TableName=KICKS_METADATA_TABLE_NAME,
            Item={
                'ReleaseDate': {
                    'S': date
                },
                'Count': {
                    'N': str(count)
                }
            }
        )
        # print('Response', json.dumps(response, indent=4, cls=DecimalEncoder))

    def storeKicks(self, kicks):
        response = self._client.put_item(
            TableName=KICKS_TABLE_NAME,
            Item=self._convertToDataStoreObject(kicks)
        )
        # print('Response', json.dumps(response, indent=4, cls=DecimalEncoder))

    def storeBulkKicks(self, kicksList):
        with self._table.batch_writer() as batch:
            for kicks in kicksList:
                batch.put_item(Item=kicks.getInfo())

    def _convertToDataStoreObject(self, kicks):
        info = kicks.getInfo()
        returnObject = {}
        for key, val in info.items():
            propertyType = KICKS_PROPERTY_TYPES_FOR_DYNAMO[key]
            returnObject[key] = {
                propertyType: val
            }
        return returnObject
