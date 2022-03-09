import json

from moto import mock_dynamodb2, mock_lambda

from tests.mock_table import get_mock_table
from tests.utils.logger import lambda_context


class TestDeleteFromCart:

    @mock_dynamodb2
    @mock_lambda
    def test_delete_from_cart(self, lambda_context):
        import delete_from_cart
        item = {
            "pk": "product#d2580eff-d105-45a5-9b21-ba61995bc6da",
            "sk": "totalquantity",
            "quantity": 1,
        }
        # prepare table
        mock_table = get_mock_table()
        mock_table.put_item(Item=item)
        res_before = mock_table.get_item(
            Key={"pk": item["pk"], "sk": item["sk"]}
        )
        assert "Item" in res_before
        event = {
            "Records": [
                {"body": json.dumps(item)}
            ]
        }
        # test lambda_handler
        delete_res = delete_from_cart.lambda_handler(event, lambda_context)
        assert delete_res["statusCode"] == 200
        res_after = mock_table.get_item(
            Key={"pk": item["pk"], "sk": item["sk"]}
        )
        assert not "Item" in res_after
