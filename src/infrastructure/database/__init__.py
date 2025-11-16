from src.config import settings
from .database_connection import DatabaseConnection


db_conn = DatabaseConnection(settings.CONN_DB)
