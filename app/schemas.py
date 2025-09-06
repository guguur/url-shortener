from urllib.parse import urlparse

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.backend.env import APP_CONFIG


class ShortenUrlResponse(BaseModel):
    shorten_url: HttpUrl


class Url(BaseModel):
    url: HttpUrl = Field(
        max_length=APP_CONFIG.MAX_URL_LENGTH,
        description="The URL to shorten",
        example="https://www.google.com",
    )

    @field_validator("url")
    @classmethod
    def validate_domain_not_self(cls, v: HttpUrl) -> HttpUrl:
        """Validate that the URL domain is not our own domain."""
        parsed_url = urlparse(str(v))
        input_domain = parsed_url.netloc.lower()

        # Get our domain from config
        our_parsed = urlparse(
            APP_CONFIG.HOST
            + (":" + str(APP_CONFIG.PORT) if APP_CONFIG.PORT else "")
        )
        our_domain = our_parsed.netloc.lower()

        if input_domain == our_domain:
            raise ValueError("Cannot shorten URLs from your own domain")

        return v


class Slug(BaseModel):
    slug: str = Field(
        max_length=APP_CONFIG.MAX_SLUG_LENGTH,
        description="The slug",
        example="aY2Pv8",
    )
