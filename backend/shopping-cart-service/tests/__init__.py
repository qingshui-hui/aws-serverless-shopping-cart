import sys
import os

sys.path.append(".")
sys.path.append("..")
sys.path.append("./layers/")

os.environ.setdefault("POWERTOOLS_SERVICE_NAME", "Example")
os.environ.setdefault("POWERTOOLS_METRICS_NAMESPACE", "Application")
