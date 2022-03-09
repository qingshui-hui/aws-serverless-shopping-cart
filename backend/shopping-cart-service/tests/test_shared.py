import os

import pytest
import shared  # noqa: E402  # import from layer
from mock import patch


class Tests:

    def test_get_cart_id_from_cookie(self):
        headers = {
            "cookie": "cartId=example-cart-id"
        }
        cartId, _ = shared.get_cart_id(headers)
        print(cartId)
        assert cartId == "example-cart-id"

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
