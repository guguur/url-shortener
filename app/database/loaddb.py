from app.backend.env import APP_CONFIG
from app.constants import Environment
from app.database.pg import ConnectionManager


def load_db(connection_manager: ConnectionManager):
    """Load the database.

    Parameters
    ----------
    connection_manager : ConnectionManager
        The connection manager.
    """
    connection_manager.init_pool()
    with connection_manager.get_cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                slug VARCHAR(%s) NOT NULL PRIMARY KEY,
                original_url VARCHAR(%s) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP + INTERVAL '%s day',
                click_count INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_urls_slug ON urls (slug);
        """,
            (
                APP_CONFIG.MAX_SLUG_LENGTH,
                APP_CONFIG.MAX_URL_LENGTH,
                APP_CONFIG.DEFAULT_EXPIRATION_DAYS,
            ),
        )
        # check if primary = index

        if APP_CONFIG.ENV == Environment.DEV:
            # insert two rows
            cursor.execute("""
                INSERT INTO urls (slug, original_url, created_at, expires_at, click_count)
                VALUES ('aY2Pv8', 'https://www.google.com/', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 day', 0)
                ON CONFLICT (slug) DO NOTHING
            """)
            cursor.execute("""
                INSERT INTO urls (slug, original_url, created_at, expires_at, click_count)
                VALUES ('Lt1fov', 'https://www.youtube.com/', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 day', 0)
                ON CONFLICT (slug) DO NOTHING
            """)
