import boto3
import pandas as pd
import os

def get_mock_table():
    mock_dynamodb = boto3.resource("dynamodb")
    mock_table = mock_dynamodb.create_table(
        TableName="sample_table",
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
        StreamSpecification={
            "StreamViewType": 'NEW_AND_OLD_IMAGES',
            "StreamEnabled": True,
        }
    )
    return mock_table

def sample_data():
    print(__file__)
    df = pd.read_csv(os.path.dirname(__file__) + '/sample.csv')
    items = []
    for index, row in df.iterrows():
        # if index == 0:
        #     continue
        items.append({
            "quantity": int(row[0]),
            "sk": row[1],
            "pk": row[2]
        })
    return items

if __name__ == '__main__':
    # mock_table()
    sample_data()
