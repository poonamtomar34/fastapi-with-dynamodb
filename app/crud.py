import uuid
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table('TodoApi')

def create_item(item):
    try:
        response = table.put_item(Item=item)
        return item  # Return the created item itself
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_items():
    response = table.scan()
    #print('response', response)
    return response.get('Items', [])

def get_item(item_id):
    response = table.get_item(Key={'itemId': item_id})
    return response.get('Item', None)

def update_item(item_id, new_attributes):
    try:
        response = table.update_item(
            Key={'itemId': item_id},  # Specify the primary key
            UpdateExpression='SET title = :title, description = :description, done = :done',
            ExpressionAttributeValues={
                ':title': new_attributes['title'],
                ':description': new_attributes['description'],
                ':done': new_attributes['done']
            },
            ReturnValues='ALL_NEW'  # Return the updated item
        )
        return response.get('Attributes', {})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_item(item_id):
    try:
        response = table.delete_item(Key={'itemId': item_id})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return response
