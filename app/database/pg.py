import time
from contextlib import contextmanager
from typing import Generator, Optional

from psycopg2.extensions import connection, cursor
from psycopg2.pool import SimpleConnectionPool

from app.backend.env import DB_CONFIG


class ConnectionManager:
    def __init__(self):
        self.connection_pool: Optional[SimpleConnectionPool] = None

    def init_pool(self):
        """Initialize the connection pool with retry mechanism."""
        if self.connection_pool:
            return

        max_retries = 3  # number of retries
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                self.connection_pool = SimpleConnectionPool(
                    host=DB_CONFIG.HOST,
                    port=DB_CONFIG.PORT,
                    user=DB_CONFIG.USER,
                    password=DB_CONFIG.PASSWORD.get_secret_value(),
                    database=DB_CONFIG.NAME,
                    minconn=DB_CONFIG.POOL_MIN_CONNECTIONS,
                    maxconn=DB_CONFIG.POOL_MAX_CONNECTIONS,
                )
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise e

    def close_pool(self):
        """Close the connection pool safely."""
        if self.connection_pool:
            try:
                self.connection_pool.closeall()
                self.connection_pool = None
            except Exception as e:
                raise e

    @contextmanager
    def get_connection(self) -> Generator[connection, None, None]:
        """Get a connection from the pool with error handling."""
        if not self.connection_pool:
            raise Exception(
                "Connection pool not initialized. Call init_pool() first."
            )

        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        except Exception as e:
            raise e
        finally:
            if conn:
                try:
                    self.connection_pool.putconn(conn)
                except Exception as e:
                    raise e

    @contextmanager
    def get_cursor(self) -> Generator[cursor, None, None]:
        """Get a cursor with proper transaction management."""
        with self.get_connection() as conn:
            cursor_obj = conn.cursor()
            try:
                yield cursor_obj
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor_obj.close()


# Global instance
connection_manager = ConnectionManager()


# FastAPI dependency function
def get_db_cursor() -> Generator[cursor, None, None]:
    """
    Get a database cursor.

    Returns
    -------
    Generator[cursor, None, None]
        The database cursor.
    """
    with connection_manager.get_cursor() as cursor_obj:
        yield cursor_obj
