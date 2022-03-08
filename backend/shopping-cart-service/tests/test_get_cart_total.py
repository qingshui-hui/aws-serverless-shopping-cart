import boto3
import pytest
from moto import mock_dynamodb2

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
