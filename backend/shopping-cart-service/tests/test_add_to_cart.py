
import json
import os

import boto3
import pytest
from unittest.mock import patch
from moto import mock_dynamodb2, mock_lambda

from tests.utils.logger import lambda_context

from .mock_table import get_mock_table, sample_data


def get_product_mock(product_id):
    product = json.loads("""{
        "category": "fruit",
        "createdDate": "2017-04-17T01:14:03 -02:00",
        "description": "Culpa non veniam deserunt dolor irure elit cupidatat culpa consequat nulla irure aliqua.",
        "modifiedDate": "2019-03-13T12:18:27 -01:00",
        "name": "packaged strawberries",
        "package": {
            "height": 948,
            "length": 455,
            "weight": 54,
            "width": 905
        },
        "pictures": [
            "http://placehold.it/32x32"
        ],
        "price": 716,
        "productId": "4c1fadaa-213a-4ea8-aa32-58c217604e3c",
        "tags": [
            "mollit",
            "ad",
            "eiusmod",
            "irure",
            "tempor"
        ]
    }""")
    product["productId"] = product_id
    return product

if __name__ == "__main__":
    product = get_product_mock("aaa")
    print(product)

class TestGetCartTotal:

    @mock_dynamodb2
    @mock_lambda
    @patch("utils.get_product_from_external_service", get_product_mock)
    @patch.dict(os.environ, {'TABLE_NAME': 'sample_table', 'PRODUCT_SERVICE_URL': 'http://example.com/test'})
    def test_add_to_cart_handler(self, lambda_context):
        from add_to_cart import lambda_handler

        # prepare table
        mock_table = get_mock_table()
        event = {
            "body": json.dumps({
                "productId": "d2580eff-d105-45a5-9b21-ba61995bc6da",
                "quantity": 1,
            }),
            "headers": {
                "cookie": "cartId=c94eee3d-475d-4753-8a99-7e24a9781ca1"
            },
        }
        # test lambda_handler
        res = lambda_handler(event, lambda_context)
        resBody = json.loads(res['body'])
        assert res["statusCode"] == 200
        assert resBody["message"] == "product added to cart"

