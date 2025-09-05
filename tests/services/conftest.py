import logging
from datetime import datetime, timedelta, timezone

import psycopg2
import pytest

from app.backend.env import APP_CONFIG, DB_CONFIG
from app.constants import Environment

logger = logging.getLogger(__name__)


def populate_db(connector: psycopg2.extensions.connection):
    with connector.cursor() as cursor:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS urls (
                    slug VARCHAR(%s) NOT NULL PRIMARY KEY,
                    original_url VARCHAR(%s) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP + 
                    INTERVAL '%s day',
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
                (
                    "aY2Pv8",
                    "https://www.google.com/",
                    datetime.now() + timedelta(days=1),
                ),
                (
                    "Lt1fov",
                    "https://www.youtube.com/",
                    datetime.now(timezone.utc),
                ),
            ]
            for slug, url, expires_at in values:
                cursor.execute(
                    """
                        INSERT INTO urls (slug, original_url, expires_at)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (slug) DO NOTHING
                        """,
                    (slug, url, expires_at),
                )
        connector.commit()


@pytest.fixture(name="internal_db_session")
def internal_db_session_fixture():
    """
    Fixture to provide a database session for internal tests.
    This session is used for operations that do not require an external
    database.
    """
    connector = psycopg2.connect(
        host=DB_CONFIG.HOST,
        port=DB_CONFIG.PORT,
        user=DB_CONFIG.USER,
        password=DB_CONFIG.PASSWORD.get_secret_value(),
        database=DB_CONFIG.NAME,
    )
    try:
        populate_db(connector)
        yield connector
    except Exception as e:
        logger.exception("Error during database session setup; %s", e)
        raise
    finally:
        # clean database drop table urls
        with connector.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS urls")
            connector.commit()
        connector.close()
