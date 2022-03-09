import json
import os

import boto3
import pytest
from moto import mock_dynamodb2, mock_lambda

from mock import patch


from tests.utils.logger import lambda_context

from .mock_table import get_mock_table, sample_data


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
    def test_handler(self, lambda_context):
        with patch.dict(os.environ, {'TABLE_NAME': 'sample_table', 'PRODUCT_SERVICE_URL': 'http://example.com/test'}):
            from get_cart_total import lambda_handler
        # prepare table
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
        # test lambda_handler
        res = lambda_handler(event, lambda_context)
        parsedBody = json.loads(res['body'])
        assert parsedBody["product"] == "d2580eff-d105-45a5-9b21-ba61995bc6da"

