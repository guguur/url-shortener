from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

from psycopg2.extensions import cursor

from app.constants import LEN_SLUG


def get_url(slug: str, db_cursor: cursor) -> str | None:
    db_cursor.execute(
        """
        SELECT original_url FROM urls WHERE slug = %s
        AND expires_at > CURRENT_TIMESTAMP
    """,
        (slug,),
    )
    result = db_cursor.fetchone()
    if result:
        db_cursor.execute(
            """
            UPDATE urls SET click_count = click_count + 1 WHERE slug = %s
            """,
            (slug,),
        )
        return result[0]
    return None


def slug_exists(slug: str, db_cursor: cursor) -> bool:
    db_cursor.execute(
        """
        SELECT slug FROM urls WHERE slug = %s
        """,
        (slug,),
    )
    result = db_cursor.fetchone()
    return True if result else False


def get_slug_from_original_url(url: str, db_cursor: cursor) -> str:
    db_cursor.execute(
        """
        SELECT slug FROM urls WHERE original_url = %s
        AND expires_at > CURRENT_TIMESTAMP
        """,
        (url,),
    )
    result = db_cursor.fetchone()
    if result:
        return result[0]
    return None


def generate_slug(db_cursor: cursor) -> str:
    while True:
        slug = "".join(
            choice(ascii_uppercase + ascii_lowercase + digits)
            for _ in range(LEN_SLUG)
        )
        if not slug_exists(slug, db_cursor):
            break
    return slug


def create_url(original_url: str, slug: str, db_cursor: cursor) -> str:
    db_cursor.execute(
        """
        INSERT INTO urls (slug, original_url)
        VALUES (%s, %s)
        """,
        (slug, original_url),
    )
    return slug


def get_url_click_count(slug: str, db_cursor: cursor) -> int:
    db_cursor.execute(
        """
        SELECT click_count FROM urls WHERE slug = %s
        """,
        (slug,),
    )
    result = db_cursor.fetchone()
    return result[0] if result else 0
