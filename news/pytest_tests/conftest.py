import pytest

from django.test.client import Client

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
