from loguru import logger
import os

from core.settings.base import *

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv('DEBUG', 0))


MEDIA_URL = "/media/"
STATIC_URL = '/static/'
MEDIA_ROOT = Path(BASE_DIR).joinpath('media')
STATIC_ROOT = Path(BASE_DIR).joinpath('static')

logger.add(f'{BASE_DIR}/logs/project/info.log', level='INFO', rotation='00:00', compression='zip')
