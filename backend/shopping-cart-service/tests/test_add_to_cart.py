
import json
import os
from unittest import mock
from unittest.mock import patch

from moto import mock_dynamodb2, mock_lambda

from tests.mock_table import get_mock_table, sample_data
from tests.utils import mock_shared, product_data
from tests.utils.logger import lambda_context


@patch("shared.get_user_sub", mock_shared.get_user_sub)
@patch("utils.get_product_from_external_service", product_data.get_product_mock)
class TestGetCartTotal:

    @classmethod
    def setup_method(cls):
        cls.env_patcher = mock.patch.dict(os.environ, {
                                          'TABLE_NAME': 'sample_table', 'PRODUCT_SERVICE_URL': 'http://example.com/test'})
        cls.env_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.env_patcher.stop()

    @mock_dynamodb2
    @mock_lambda
    def test_add_to_cart_handler(self, lambda_context):
        import add_to_cart

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
        res = add_to_cart.lambda_handler(event, lambda_context)
        res_body = json.loads(res['body'])
        assert res["statusCode"] == 200
        assert res_body["message"] == "product added to cart"


    @mock_dynamodb2
    @mock_lambda
    def test_add_to_user_cart(self, lambda_context):
        import add_to_cart

        # prepare table
        mock_table = get_mock_table()
        event = {
            "body": json.dumps({
                "productId": "d2580eff-d105-45a5-9b21-ba61995bc6da",
                "quantity": 1,
            }),
            "headers": {
                "Authorization" : "dummy-jwt",
            },
        }
        # test lambda_handler
        res = add_to_cart.lambda_handler(event, lambda_context)
        res_body = json.loads(res['body'])
        assert res["statusCode"] == 200
        assert res_body["message"] == "product added to cart"

        # test product is added to a user cart
        res_after = mock_table.get_item(
            Key={"pk": "user#dummy-jwt", "sk": "product#d2580eff-d105-45a5-9b21-ba61995bc6da"}
        )
        assert res_after['Item']['pk'] == "user#dummy-jwt"


    @mock_dynamodb2
    @mock_lambda
    def test_no_request_payload(self, lambda_context):
        import add_to_cart

        # prepare table
        mock_table = get_mock_table()
        event = {}
        # test lambda_handler
        res = add_to_cart.lambda_handler(event, lambda_context)
        res_body = json.loads(res['body'])
        assert res["statusCode"] == 400
        assert res_body["message"] == "No Request payload"

    @mock_dynamodb2
    @mock_lambda
    def test_product_not_found(self, lambda_context):
        import add_to_cart

        # prepare table
        mock_table = get_mock_table()
        event = {
            "body": json.dumps({
                "productId": "",
                "quantity": 1,
            }),
            "headers": {
                "cookie": "cartId=c94eee3d-475d-4753-8a99-7e24a9781ca1"
            },}
        # test lambda_handler
        res = add_to_cart.lambda_handler(event, lambda_context)
        res_body = json.loads(res['body'])
        assert res["statusCode"] == 404
        assert res_body["message"] == "product not found"

    @mock_dynamodb2
    @mock_lambda
    def test_decrement_quantity(self, lambda_context):
        import add_to_cart

        # prepare table
        mock_table = get_mock_table()
        for row in sample_data():
            mock_table.put_item(Item=row)
        event = {
            "body": json.dumps({
                "productId": "d2580eff-d105-45a5-9b21-ba61995bc6da",
                "quantity": -1,
            }),
            "headers": {
                "cookie": "cartId=c94eee3d-475d-4753-8a99-7e24a9781ca1"
            },
        }
        # before
        res_before = mock_table.get_item(
            Key={"pk": "cart#c94eee3d-475d-4753-8a99-7e24a9781ca1", "sk": "product#d2580eff-d105-45a5-9b21-ba61995bc6da"}
        )
        # test lambda_handler
        res = add_to_cart.lambda_handler(event, lambda_context)
        res_body = json.loads(res['body'])
        assert res["statusCode"] == 200
        assert res_body["message"] == "product added to cart"
        # after
        res_after = mock_table.get_item(
            Key={"pk": "cart#c94eee3d-475d-4753-8a99-7e24a9781ca1", "sk": "product#d2580eff-d105-45a5-9b21-ba61995bc6da"}
        )
        assert res_before['Item']['quantity'] == 1
        assert res_after['Item']['quantity'] == 0
