import pytest

from django.test.client import Client
from pytest_django.asserts import assertRedirects

HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('url_news_home'), Client(), HTTP_STATUS_OK),
        (pytest.lazy_fixture('url_users_login'), Client(), HTTP_STATUS_OK),
        (pytest.lazy_fixture('url_users_logout'), Client(), HTTP_STATUS_OK),
        (pytest.lazy_fixture('url_users_signup'), Client(), HTTP_STATUS_OK),
        (pytest.lazy_fixture('url_news_detail'), Client(), HTTP_STATUS_OK),
        (
            pytest.lazy_fixture('url_news_edit'),
            pytest.lazy_fixture('author_client'),
            HTTP_STATUS_OK
        ),
        (
            pytest.lazy_fixture('url_news_edit'),
            pytest.lazy_fixture('not_author_client'),
            HTTP_STATUS_NOT_FOUND
        ),
        (
            pytest.lazy_fixture('url_news_delete'),
            pytest.lazy_fixture('author_client'),
            HTTP_STATUS_OK
        ),
        (
            pytest.lazy_fixture('url_news_delete'),
            pytest.lazy_fixture('not_author_client'),
            HTTP_STATUS_NOT_FOUND
        ),
    )
)
def test_pages_availability(reverse_url, parametrized_client, expected_status):
    """Тестирование доступности страниц"""
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'reverse_url',
    (
        (pytest.lazy_fixture('url_news_edit')),
        (pytest.lazy_fixture('url_news_delete'))
    ),
)
def test_redirects(client, reverse_url, url_users_login):
    """Тестирование редиректов"""
    expected_url = f'{url_users_login}?next={reverse_url}'
    response = client.get(reverse_url)
    assertRedirects(response, expected_url)
