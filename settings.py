import os
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

# GENERAL
DEBUG = True if os.getenv('DEBUG', default='FALSE') == 'TRUE' else False

# MAPILLARY
API_ROOT_ENDPOINT = os.getenv(
    'API_ROOT_ENDPOINT',
    default='127.0.0.1:60010/api/v1'
)

LOG_FILE_NAME = os.getenv(
    'LOG_FILE_NAME',
    default='glw.log'
)

LOG_SERVER_HOST = os.getenv(
    'LOG_SERVER_HOST',
    default='127.0.0.1'
)

LOG_SERVER_PORT = os.getenv(
    'LOG_SERVER_PORT',
    default='60000'
)


UI_URL = os.getenv(
    'UI_URL',
    default='http://127.0.0.1:60030'
)
