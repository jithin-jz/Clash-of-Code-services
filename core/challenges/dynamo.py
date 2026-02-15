import os
import boto3
from datetime import datetime

DYNAMODB_URL = os.getenv("DYNAMODB_URL", "http://dynamodb:8000")
REGION_NAME = os.getenv("AWS_REGION", "us-west-2")
TABLE_NAME = "ChallengeProgress"

class DynamoChallengeClient:
    def __init__(self):
        self.resource = boto3.resource(
            "dynamodb",
            endpoint_url=DYNAMODB_URL,
            region_name=REGION_NAME,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy"
        )

    def create_table_if_not_exists(self):
        try:
            tables = [table.name for table in self.resource.tables.all()]
            if TABLE_NAME not in tables:
                self.resource.create_table(
                    TableName=TABLE_NAME,
                    KeySchema=[
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition Key
                        {'AttributeName': 'challenge_slug', 'KeyType': 'RANGE'} # Sort Key
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'user_id', 'AttributeType': 'S'},
                        {'AttributeName': 'challenge_slug', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                )
                print(f"Table {TABLE_NAME} created.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def update_progress(self, user_id: str, challenge_slug: str, status: str, stars: int = 0):
        try:
            table = self.resource.Table(TABLE_NAME)
            table.put_item(
                Item={
                    'user_id': str(user_id),
                    'challenge_slug': challenge_slug,
                    'status': status,
                    'stars': stars,
                    'last_updated': datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            print(f"Error updating challenge progress in DynamoDB: {e}")

    def get_user_progress(self, user_id: str):
        try:
            table = self.resource.Table(TABLE_NAME)
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(str(user_id))
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error fetching challenge progress from DynamoDB: {e}")
            return []

dynamo_challenge_client = DynamoChallengeClient()
