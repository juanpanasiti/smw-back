import logging
from datetime import datetime

from .config import Settings

settings = Settings()

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    filemode='a',
    filename='./logs/{}'.format(
        datetime.now().strftime('%Y%m%d_save_my_wallet.log')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)