from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

from psycopg2.extensions import cursor

from app.backend.env import APP_CONFIG
from app.schemas import Slug, Url


def get_url(slug_data: Slug, db_cursor: cursor) -> str | None:
    """Get the original URL from the slug.

    Parameters
    ----------
    slug_data : Slug
        The slug.
    db_cursor : cursor
        The database cursor.

    Returns
    -------
    str | None
        The original URL or None if the slug is not found.
    """
    db_cursor.execute(
        """
        SELECT original_url FROM urls WHERE slug = %s
        AND expires_at > CURRENT_TIMESTAMP
    """,
        (slug_data.slug,),
    )
    result = db_cursor.fetchone()
    if result:
        return result[0]
    return None


def update_url_click_count(slug_data: Slug, db_cursor: cursor) -> None:
    """Update the click count of the URL by adding 1.

    Parameters
    ----------
    slug_data : Slug
        The slug.
    db_cursor : cursor
        The database cursor.
    """
    db_cursor.execute(
        """
        UPDATE urls SET click_count = click_count + 1 WHERE slug = %s
        """,
        (slug_data.slug,),
    )


def slug_exists(slug_data: Slug, db_cursor: cursor) -> bool:
    """Check if the slug exists in the database.

    Parameters
    ----------
    slug_data : Slug
        The slug.
    db_cursor : cursor
        The database cursor.

    Returns
    -------
    bool
        True if the slug exists, False otherwise.
    """
    db_cursor.execute(
        """SELECT slug FROM urls WHERE slug = %s""",
        (slug_data.slug,),
    )
    result = db_cursor.fetchone()
    return True if result else False


def get_slug_from_original_url(
    url_data: Url, db_cursor: cursor
) -> Slug | None:
    """Get the slug from the original URL.

    Parameters
    ----------
    url_data : Url
        The URL.
    db_cursor : cursor
        The database cursor.

    Returns
    -------
    Slug | None
        The slug or None if the URL is not found.
    """
    db_cursor.execute(
        """
        SELECT slug FROM urls WHERE original_url = %s
        AND expires_at > CURRENT_TIMESTAMP
        """,
        (str(url_data.url),),
    )
    result = db_cursor.fetchone()
    if result:
        return Slug(slug=result[0])
    return None


def generate_slug(db_cursor: cursor) -> Slug:
    """Generate a random slug that does not exist in the database.

    Parameters
    ----------
    db_cursor : cursor
        The database cursor.

    Returns
    -------
    Slug
        The generated slug.
    """
    while True:
        slug = "".join(
            choice(ascii_uppercase + ascii_lowercase + digits)
            for _ in range(APP_CONFIG.MAX_SLUG_LENGTH)
        )
        slug_data = Slug(slug=slug)
        if not slug_exists(slug_data, db_cursor):
            break
    return slug_data


def create_url(original_url: Url, slug_data: Slug, db_cursor: cursor) -> None:
    """Create a URL in the database.

    Parameters
    ----------
    original_url : Url
        The original URL.
    slug_data : Slug
        The slug.
    db_cursor : cursor
        The database cursor.
    """
    db_cursor.execute(
        """
        INSERT INTO urls (slug, original_url)
        VALUES (%s, %s)
        """,
        (slug_data.slug, str(original_url.url)),
    )


def get_url_click_count(slug_data: Slug, db_cursor: cursor) -> int:
    """Get the click count of the URL.

    Parameters
    ----------
    slug_data : Slug
        The slug.
    db_cursor : cursor
        The database cursor.

    Returns
    -------
    int
        The click count of the URL.
    """
    db_cursor.execute(
        """
        SELECT click_count FROM urls WHERE slug = %s
        """,
        (slug_data.slug,),
    )
    result = db_cursor.fetchone()
    return result[0] if result else 0
