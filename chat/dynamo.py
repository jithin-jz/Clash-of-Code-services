import os
import aioboto3
from datetime import datetime

DYNAMODB_URL = os.getenv("DYNAMODB_URL", "http://dynamodb:8000")
REGION_NAME = os.getenv("AWS_REGION", "us-west-2")
TABLE_NAME = "ChatMessages"

class DynamoClient:
    def __init__(self):
        self.session = aioboto3.Session()
        self.endpoint_url = DYNAMODB_URL

    async def create_table_if_not_exists(self):
        async with self.session.resource("dynamodb", endpoint_url=self.endpoint_url, region_name=REGION_NAME) as dynamo:
            try:
                tables = [table.name async for table in dynamo.tables.all()]
                if TABLE_NAME not in tables:
                    await dynamo.create_table(
                        TableName=TABLE_NAME,
                        KeySchema=[
                            {'AttributeName': 'room_id', 'KeyType': 'HASH'},  # Partition Key
                            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'} # Sort Key
                        ],
                        AttributeDefinitions=[
                            {'AttributeName': 'room_id', 'AttributeType': 'S'},
                            {'AttributeName': 'timestamp', 'AttributeType': 'S'}
                        ],
                        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    )
                    print(f"Table {TABLE_NAME} created.")
            except Exception as e:
                print(f"Error creating table: {e}")

    async def save_message(self, room_id: str, sender: str, message: str):
        async with self.session.resource("dynamodb", endpoint_url=self.endpoint_url, region_name=REGION_NAME) as dynamo:
            table = await dynamo.Table(TABLE_NAME)
            await table.put_item(
                Item={
                    'room_id': room_id,
                    'timestamp': datetime.utcnow().isoformat(),
                    'sender': sender,
                    'content': message
                }
            )

    async def get_messages(self, room_id: str, limit: int = 50):
        async with self.session.resource("dynamodb", endpoint_url=self.endpoint_url, region_name=REGION_NAME) as dynamo:
            table = await dynamo.Table(TABLE_NAME)
            response = await table.query(
                KeyConditionExpression=aioboto3.dynamodb.conditions.Key('room_id').eq(room_id),
                ScanIndexForward=False, # Get latest first
                Limit=limit
            )
            return response.get('Items', [])

dynamo_client = DynamoClient()
