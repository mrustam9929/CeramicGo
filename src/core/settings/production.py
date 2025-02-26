from loguru import logger
import os

from core.settings.base import *

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = ["ceramicgo.mdev.uz", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://ceramicgo.mdev.uz",
    "http://localhost",
    "http://127.0.0.1"
]
MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR).joinpath('media')
STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR).joinpath('static')

logger.add(f'{BASE_DIR}/logs/project/info.log', level='INFO', rotation='00:00', compression='zip')
