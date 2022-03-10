import sys
import pytest

sys.path.append("..")  # Add application to path
sys.path.append("./layers/")  # Add layer to path

import shared  # noqa: E402  # import from layer


class Tests:
    """
    Example included to demonstrate how to run unit tests when using lambda layers.
    """

    def test_headers(self):
        assert shared.HEADERS.get("Access-Control-Allow-Credentials") == True
