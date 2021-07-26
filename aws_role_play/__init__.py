import os
from os.path import expanduser

AWS_CONFIG_FILE = os.getenv(
    "AWS_CONFIG_FILE", os.path.join(expanduser("~"), ".aws", "config")
)
AWS_SHARED_CREDENTIALS_FILE = os.getenv(
    "AWS_SHARED_CREDENTIALS_FILE", os.path.join(expanduser("~"), ".aws", "credentials")
)
AWS_PROFILE = os.getenv("AWS_PROFILE")
