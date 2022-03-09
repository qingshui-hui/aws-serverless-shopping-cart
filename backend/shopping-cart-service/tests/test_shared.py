import os

import pytest
import layers.shared as shared # noqa: E402  # import from layer
from unittest.mock import patch


class Tests:

    def test_get_cart_id_from_cookie(self):
        headers = {
            "cookie": "cartId=example-cart-id"
        }
        cartId, generated = shared.get_cart_id(headers)
        assert generated == False
        assert cartId == "example-cart-id"

    def test_get_generated_cart_id(self):
        headers = {
            "cookie": ""
        }
        cartId, generated = shared.get_cart_id(headers)
        assert generated == True

    @patch.dict(os.environ, {
        "AWS_REGION": "ap-northeast-1", "USERPOOL_ID": "aaa"
    })
    def test_get_user_sub_by_jwt(self):
        no_user_sub = shared.get_user_sub("aaa")
        assert no_user_sub == None

        import cognitojwt
        from jose.exceptions import JWTError

        # https://docs.pytest.org/en/6.2.x/assert.html#assertions-about-expected-exceptions
        with pytest.raises(JWTError) as excinfo:
            verified_claims = cognitojwt.decode(
                "1111.2222", os.environ["AWS_REGION"], os.environ["USERPOOL_ID"]
            )
        print(excinfo.value)
        assert "Error decoding token headers." in str(excinfo.value)
