from app.database.pg import connection_manager


def load_db():
    with connection_manager.get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                slug VARCHAR(6) NOT NULL PRIMARY KEY,
                original_url VARCHAR(2048) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP + INTERVAL '1 day',
                click_count INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_urls_slug ON urls (slug);
        """)
        # check if primary = index


def populate_db():
    with connection_manager.get_cursor() as cursor:
        # insert two rows
        cursor.execute("""
            INSERT INTO urls (slug, original_url, created_at, expires_at, click_count)
            VALUES ('aY2Pv8', 'https://www.google.com/', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 day', 0)
        """)
        cursor.execute("""
            INSERT INTO urls (slug, original_url, created_at, expires_at, click_count)
            VALUES ('Lt1fov', 'https://www.youtube.com/', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 day', 0)
        """)
