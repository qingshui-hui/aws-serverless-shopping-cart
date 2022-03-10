import json
from shared import NotFoundException

def get_product_mock(product_id):
    if product_id == None or product_id == "":
        raise NotFoundException
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
