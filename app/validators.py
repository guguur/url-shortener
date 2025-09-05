from urllib.parse import urlparse

from app.backend.env import APP_CONFIG


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_valid_domain(url: str) -> bool:
    return url.startswith(f"{APP_CONFIG.HOST}")
