from collections.abc import Sequence

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Row


class DatabaseConnection:
    def __init__(self, str_conn: str) -> None:
        self.str_conn: str = str_conn
        self._engine: Engine | None = None
        self._SessionLocal: sessionmaker[Session] | None = None

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(self.str_conn, future=True, echo=False)
        return self._engine

    @property
    def SessionLocal(self) -> sessionmaker[Session]:
        if self._SessionLocal is None:
            self._SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False, class_=Session)
        return self._SessionLocal

    def execute_query(self, query: str) -> Sequence[Row] | None:
        try:
            with self.SessionLocal() as session:
                result = session.execute(text(query))
                return result.fetchall()
        except Exception:
            return None

    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            return True
        except Exception:
            return False
