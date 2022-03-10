import sys
import os

sys.path.append(".")
sys.path.append("..")
sys.path.append("./layers/")

# dyanmodbを正しくモックできていれば不要になる。
# os.environ.setdefault("AWS_ACCESS_KEY_ID", "akid")
# os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "sak")
# os.environ.setdefault("AWS_DEFAULT_REGION", "ap-northeast-1")

os.environ.setdefault("POWERTOOLS_SERVICE_NAME", "Example")
os.environ.setdefault("POWERTOOLS_METRICS_NAMESPACE", "Application")
os.environ.setdefault("TABLE_NAME", "sample_table")
os.environ.setdefault("PRODUCT_SERVICE_URL", "'http://example.com/test'")
