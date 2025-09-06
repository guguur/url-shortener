from app.schemas import Slug, Url
from app.services import urls


def test_get_url_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        url = urls.get_url(Slug(slug="aY2Pv8"), cursor)
        assert url == "https://www.google.com/"


def test_get_url_not_found(internal_db_session):
    with internal_db_session.cursor() as cursor:
        url = urls.get_url(Slug(slug="abcdef"), cursor)
        assert url is None


def test_get_url_expired(internal_db_session):
    with internal_db_session.cursor() as cursor:
        url = urls.get_url(Slug(slug="Lt1fov"), cursor)
        assert url is None


def test_update_url_click_count_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        urls.update_url_click_count(Slug(slug="aY2Pv8"), cursor)
        cursor.execute("""select slug, original_url, click_count from urls""")
        result = cursor.fetchall()
        assert len(result) == 2
        assert ("aY2Pv8", "https://www.google.com/", 1) in result
        assert ("Lt1fov", "https://www.youtube.com/", 0) in result


def test_slug_exists_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert urls.slug_exists(Slug(slug="aY2Pv8"), cursor)


def test_slug_exists_not_found(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert not urls.slug_exists(Slug(slug="abcdef"), cursor)


def test_get_slug_from_original_url_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert urls.get_slug_from_original_url(
            Url(url="https://www.google.com/"), cursor
        ) == Slug(slug="aY2Pv8")


def test_get_slug_from_original_url_not_found(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert (
            urls.get_slug_from_original_url(
                Url(url="https://www.youtube.com/"), cursor
            )
            is None
        )


def test_get_slug_from_original_url_expired(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert (
            urls.get_slug_from_original_url(
                Url(url="https://www.youtube.com/"), cursor
            )
            is None
        )


def test_generate_slug_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert urls.generate_slug(cursor).slug != Slug(slug="aY2Pv8").slug


def test_create_url_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        urls.create_url(
            Url(url="https://www.test.com/"), Slug(slug="abcdef"), cursor
        )
        cursor.execute("""select slug, original_url from urls""")
        result = cursor.fetchall()
        assert len(result) == 3
        assert ("aY2Pv8", "https://www.google.com/") in result
        assert ("Lt1fov", "https://www.youtube.com/") in result
        assert ("abcdef", "https://www.test.com/") in result


def test_get_url_click_count_ok(internal_db_session):
    with internal_db_session.cursor() as cursor:
        assert urls.get_url_click_count(Slug(slug="aY2Pv8"), cursor) == 0


def test_get_url_click_count_more_than_zero(internal_db_session):
    with internal_db_session.cursor() as cursor:
        urls.update_url_click_count(Slug(slug="aY2Pv8"), cursor)
        assert urls.get_url_click_count(Slug(slug="aY2Pv8"), cursor) == 1
