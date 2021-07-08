import os
from os.path import expanduser

AWS_CREDENTIALS_PATH = os.path.join(expanduser("~"), ".aws/credentials")
AWS_CONFIG_PATH = os.path.join(expanduser("~"), ".aws/config")
