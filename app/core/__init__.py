import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from .config import Settings

settings = Settings()


log_filename = './logs/save_my_wallet.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

# Handler que rota el archivo de log diariamente
handler = TimedRotatingFileHandler(
    log_filename,
    when='midnight',
    interval=1,
    backupCount=0,
)
handler.suffix = '%Y%m%d'  # Añade la fecha al final del archivo

# Formato del log
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# Añadir el handler al logger
logger.addHandler(handler)
