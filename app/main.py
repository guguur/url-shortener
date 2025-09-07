from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from psycopg2.extensions import cursor
from pydantic import ValidationError

from app.backend.env import APP_CONFIG
from app.database.loaddb import load_db
from app.database.pg import connection_manager, get_db_cursor
from app.schemas import ShortenUrlResponse, Slug, Url
from app.services.urls import (
    create_url,
    generate_slug,
    get_slug_from_original_url,
    get_url,
    get_url_click_count,
    update_url_click_count,
)

DB_Cursor = Annotated[cursor, Depends(get_db_cursor)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_db(connection_manager)
    yield
    connection_manager.close_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/{slug}")
def redirect_to_url(slug: str, db_cursor: DB_Cursor):
    """Redirect to the original URL and update the click count.

    Parameters
    ----------
    slug : str
        The slug.

    Raises
    ------
    HTTPException
        404: If the URL is not found.

    Returns
    -------
    RedirectResponse
        The redirect response.
    """
    try:
        slug_data = Slug(slug=slug)
    except ValidationError:
        raise HTTPException(status_code=404, detail="Invalid URL") from None
    redirect_url = get_url(slug_data, db_cursor)

    if redirect_url:
        update_url_click_count(slug_data, db_cursor)
        return RedirectResponse(redirect_url)
    raise HTTPException(status_code=404, detail="Invalid URL")


@app.get("/stats/{slug}", response_model=int)
def get_url_stats(slug: str, db_cursor: DB_Cursor):
    """Get the click count of the URL.

    Parameters
    ----------
    slug : str
        The slug.

    Raises
    ------
    HTTPException
        404: If the slug is not found.

    Returns
    -------
    int
        The click count of the URL.
    """
    try:
        slug_data = Slug(slug=slug)
    except ValidationError:
        raise HTTPException(status_code=404, detail="Invalid URL") from None
    if not get_url(slug_data, db_cursor):
        raise HTTPException(status_code=404, detail="Invalid URL")
    return get_url_click_count(slug_data, db_cursor)


@app.post("/shorten", response_model=ShortenUrlResponse)
def shorten_url(url: Url, db_cursor: DB_Cursor):
    """Shorten the URL.

    Parameters
    ----------
    url : Url
        The URL to shorten.

    Raises
    ------
    HTTPException
        404: If the URL is not found.

    Returns
    -------
    ShortenUrlResponse
        The shortened URL.
    """
    slug_data = get_slug_from_original_url(url, db_cursor)
    if not slug_data:
        slug_data = generate_slug(db_cursor)
        create_url(url, slug_data, db_cursor)
    return ShortenUrlResponse(
        shorten_url=f"{APP_CONFIG.HOST}:{APP_CONFIG.PORT}/{slug_data.slug}",
    )
