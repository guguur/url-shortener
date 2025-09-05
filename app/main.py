from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from psycopg2.extensions import cursor
from pydantic import HttpUrl

from app.backend.env import APP_CONFIG
from app.database.loaddb import load_db, populate_db
from app.database.pg import connection_manager
from app.schemas import ShortenUrlResponse
from app.services.urls import (
    create_url,
    generate_slug,
    get_slug_from_original_url,
    get_url,
    get_url_click_count,
)
from app.validators import is_valid_domain

DB_Cursor = Annotated[cursor, Depends(connection_manager.get_cursor)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection_manager.init_pool()
    load_db()
    populate_db()
    yield
    connection_manager.close_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/{slug}")
def redirect_to_url(slug: str, db_cursor: DB_Cursor):
    redirect_url = get_url(slug, db_cursor)
    if redirect_url:
        return RedirectResponse(redirect_url)
    else:
        return HTTPException(status_code=404, detail="Invalid URL")


@app.get("/{slug}/stats", response_model=int)
def get_url_stats(slug: str, db_cursor: DB_Cursor):
    return get_url_click_count(slug, db_cursor)


# use connection as parameter injection
@app.post("/shorten", response_model=ShortenUrlResponse)
def shorten_url(url: HttpUrl, db_cursor: DB_Cursor):
    if is_valid_domain(str(url)):
        return HTTPException(
            status_code=422, detail="Cannot shorten the same domain"
        )
    slug = get_slug_from_original_url(str(url), db_cursor)
    if not slug:
        slug = generate_slug()
        create_url(str(url), slug, db_cursor)
    return ShortenUrlResponse(
        slug=slug,
        shorten_url=f"{APP_CONFIG.HOST}:{APP_CONFIG.PORT}/{slug}",
    )
