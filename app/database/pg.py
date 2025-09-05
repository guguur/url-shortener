from contextlib import contextmanager
from typing import Generator

from psycopg2.extensions import connection, cursor
from psycopg2.pool import SimpleConnectionPool

from app.backend.env import DatabaseConfig


class ConnectionManager:
    def __init__(self):
        self.connection_pool: SimpleConnectionPool = None

    def init_pool(self):
        if self.connection_pool:
            return
        self.connection_pool = SimpleConnectionPool(
            host=DatabaseConfig.HOST,
            port=DatabaseConfig.PORT,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.NAME,
            minconn=DatabaseConfig.POOL_MIN_CONNECTIONS,
            maxconn=DatabaseConfig.POOL_MAX_CONNECTIONS,
            timeout=DatabaseConfig.POOL_TIMEOUT,
            reconnect=DatabaseConfig.POOL_RECONNECT,
        )

    def close_pool(self):
        if self.connection_pool:
            self.connection_pool.closeall()
            self.connection_pool = None

    @contextmanager
    def get_connection(self) -> Generator[connection, None, None]:
        try:
            conn = self.connection_pool.getconn()
            yield conn
        finally:
            self.connection_pool.putconn(conn)

    def get_cursor(self) -> cursor:
        with self.get_connection() as conn:
            return conn.cursor()


connection_manager = ConnectionManager()
