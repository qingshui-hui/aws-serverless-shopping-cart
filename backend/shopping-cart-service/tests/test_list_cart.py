
import json
import os

import boto3

import pytest
from unittest.mock import patch
from moto import mock_dynamodb2, mock_lambda

from tests.utils.logger import lambda_context

from .mock_table import get_mock_table, sample_data
from boto3.dynamodb.conditions import Key

with patch.dict(os.environ, {'TABLE_NAME': 'sample_table', 'PRODUCT_SERVICE_URL': 'http://example.com/test'}):
    import list_cart

class TestGetCartTotal:

    @mock_dynamodb2
    @mock_lambda
    def test_create_empty_cart(self, lambda_context):
        event = {
            "headers": {
                "cookie": ""
            },
        }
        # test lambda_handler
        res = list_cart.lambda_handler(event, lambda_context)
        resBody = json.loads(res['body'])
        assert res["statusCode"] == 200
        assert resBody["products"] == []

    @mock_dynamodb2
    @mock_lambda
    @patch.dict(os.environ, {'TABLE_NAME': 'sample_table', 'PRODUCT_SERVICE_URL': 'http://example.com/test'})
    def test_list_cart_items(self, lambda_context):
        # クラス変数にmock_tableを設定するとうまくいかなかった。
        mock_table = get_mock_table()
        for row in sample_data():
            mock_table.put_item(Item=row)

        event = {
            "headers": {
                "cookie": "cartId=c94eee3d-475d-4753-8a99-7e24a9781ca1"
            },
        }
        # test lambda_handler
        res = list_cart.lambda_handler(event, lambda_context)
        res_body = json.loads(res['body'])

        assert res["statusCode"] == 200
        assert len(res_body["products"]) > 0

    @mock_dynamodb2
    def test_list_cart_query(self):
        mock_table = get_mock_table()
        for row in sample_data():
            mock_table.put_item(Item=row)

        key_string = "cart#c94eee3d-475d-4753-8a99-7e24a9781ca1"
        response = mock_table.query(
            KeyConditionExpression=Key("pk").eq(key_string)
            & Key("sk").begins_with("product#"),
            ProjectionExpression="sk,quantity,productDetail",
            FilterExpression="quantity > :val",  # Only return items with more than 0 quantity
            ExpressionAttributeValues={":val": 0},
        )
        product_list = response.get("Items", [])
        assert len(product_list) > 0
