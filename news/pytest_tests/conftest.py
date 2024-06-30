from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    """Фикстура автора"""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Фикстура не автора"""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    """Фикстура автора"""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Фикстура логина обычного пользователя"""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    """Фикстура объекта новости"""
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def comment(author, news):
    """Объект комментария"""
    comment = Comment.objects.create(
        news=news,
        text='Текст заметки',
        author=author,

    )
    return comment


@pytest.fixture
def pk_for_news(news):
    """Получение pk новости"""
    return (news.id,)


@pytest.fixture
def pk_for_comment(comment):
    """Получение pk комментария"""
    return (comment.pk,)


@pytest.fixture
def get_news_detail(news):
    """Получение url новости"""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def news_list(news):
    """Создание списка новостей"""
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News.objects.create(
            title='Заголовок',
            text='Текст',
            date=today - timedelta(days=index)
        )
        all_news.append(news)
    return


@pytest.fixture
def comments_list(news, comment, not_author_client):
    """Создание списка комментариев"""
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=not_author_client,
            text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return


@pytest.fixture
def get_homepage_objects(news_list, author_client):
    """Получение объектов главной страницы"""
    url = reverse('news:home')
    response = author_client.get(url)
    return response.context['object_list']
