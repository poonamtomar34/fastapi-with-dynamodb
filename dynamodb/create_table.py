import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
try:
    table = dynamodb.create_table(
        TableName='TodoApi',
        KeySchema=[
            {
                'AttributeName': 'itemId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'itemId',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table status:", table.table_status)
except Exception as e:
    print('error', e)