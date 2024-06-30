import pytest
from django.conf import settings
from django.urls import reverse
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(get_homepage_objects):
    """Тестирование пагинатора: словарь контекста"""
    news_count = get_homepage_objects.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(get_homepage_objects):
    """Тестируем сортировку новостей"""
    all_dates = [news.date for news in get_homepage_objects]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(not_author_client, get_news_detail):
    """Тестируем сортировку комментариев на странице новости"""
    response = not_author_client.get(get_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, get_news_detail):
    """Тест наличия формы в словаре контекста анонимного клиента"""
    response = client.get(get_news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, get_news_detail):
    """Тест наличия формы в словаре контекста авторизованного пользователя"""
    response = author_client.get(get_news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
