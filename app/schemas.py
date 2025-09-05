from pydantic import BaseModel, HttpUrl


class ShortenUrlResponse(BaseModel):
    slug: str
    shorten_url: HttpUrl
