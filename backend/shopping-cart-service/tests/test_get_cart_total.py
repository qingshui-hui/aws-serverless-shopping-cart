import json
import os
import sys

import boto3
import pytest
from moto import mock_dynamodb2, mock_lambda

from mock import patch

sys.path.append("..")

from .mock import get_mock_table, sample_data


class TestGetCartTotal:

    @mock_dynamodb2
    def test_headers(self):
        mock_table = get_mock_table()
        for row in sample_data():
            mock_table.put_item(Item=row)

        dynamodb = boto3.resource("dynamodb")
        table = mock_table
        product_id = "d2580eff-d105-45a5-9b21-ba61995bc6da"
        response = table.get_item(
            Key={"pk": f"product#{product_id}", "sk": "totalquantity"}
        )
        # print(response)
        # 1件も見つからなかったらItemがセットされない
        assert "Item" in response
        assert response["Item"]["pk"] == "product#d2580eff-d105-45a5-9b21-ba61995bc6da"

    @mock_dynamodb2
    @mock_lambda
    def test_handler(self):
        with patch.dict(os.environ, {'TABLE_NAME': 'sample_table'}):
            from get_cart_total import lambda_handler
        mock_table = get_mock_table()
        mock_table.put_item(Item={
            "pk": "product#d2580eff-d105-45a5-9b21-ba61995bc6da",
            "sk": "totalquantity",
            "quantity": 1,
        })
        event = {
            "pathParameters": {
                "product_id": "d2580eff-d105-45a5-9b21-ba61995bc6da"
            }
        }
        res = lambda_handler(event, Context())
        print(res['body'])
        parsedBody = json.loads(res['body'])
        assert parsedBody["product"] == "d2580eff-d105-45a5-9b21-ba61995bc6da"

class Context:
    pass
