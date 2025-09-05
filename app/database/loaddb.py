from app.backend.env import APP_CONFIG
from app.constants import Environment
from app.database.pg import ConnectionManager


def load_db(connection_manager: ConnectionManager):
    """Initialize the database schema and load the initial data.
    If the database is in development environment, load the initial data.

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
            )
        """,
            (
                APP_CONFIG.MAX_SLUG_LENGTH,
                APP_CONFIG.MAX_URL_LENGTH,
                APP_CONFIG.DEFAULT_EXPIRATION_DAYS,
            ),
        )

        if APP_CONFIG.ENV == Environment.DEV.value:
            values = [
                ("aY2Pv8", "https://www.google.com/"),
                ("Lt1fov", "https://www.youtube.com/"),
            ]
            for slug, url in values:
                cursor.execute(
                    """
                    INSERT INTO urls (slug, original_url)
                    VALUES (%s, %s)
                    ON CONFLICT (slug) DO NOTHING
                    """,
                    (slug, url),
                )
