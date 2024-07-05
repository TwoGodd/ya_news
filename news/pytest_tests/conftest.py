from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.models import Comment, News


class Constants:
    COMMENT_TEXT = 'Текст комментария'
    NEW_COMMENT_TEXT = 'Обновлённый комментарий'


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
    """Фикстура создания новости"""
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def comment(author, news):
    """Фикстура создания комментария"""
    comment = Comment.objects.create(
        news=news,
        text=Constants.COMMENT_TEXT,
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
    return (comment.id,)


@pytest.fixture
def url_news_home():
    """URL на домашнюю страницу"""
    return reverse('news:home')


@pytest.fixture
def url_news_detail(pk_for_news):
    """URL на страницу с деталями новости"""
    return reverse('news:detail', args=pk_for_news)


@pytest.fixture
def url_news_edit(pk_for_comment):
    """URL на страницу редактирования новости"""
    return reverse('news:edit', args=pk_for_comment)


@pytest.fixture
def url_news_delete(pk_for_comment):
    """URL на страницу удаления новости"""
    return reverse('news:delete', args=pk_for_comment)


@pytest.fixture
def url_users_login():
    """URL на страницу входа в профиль"""
    return reverse('users:login')


@pytest.fixture
def url_users_logout():
    """URL на страницу выхода из профиля"""
    return reverse('users:logout')


@pytest.fixture
def url_users_signup():
    """URL на страницу выхода авторизации"""
    return reverse('users:signup')


@pytest.fixture
def url_to_comments(url_news_detail):
    """Адрес блока с комментариями"""
    return url_news_detail + '#comments'


@pytest.fixture
def news_list(news):
    """Создание списка новостей"""
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title='Заголовок',
            text='Текст',
            date=today - timedelta(days=index)
        )
        all_news.append(news)
    News.objects.bulk_create(all_news)
    return


@pytest.fixture
def comments_list(news, comment, not_author_client):
    """Создание списка комментариев"""
    now = timezone.now()
    all_comments = []
    for index in range(10):
        comment = Comment(
            news=news,
            author=not_author_client,
            text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        all_comments.append(comment)
    Comment.objects.bulk_create()
    return


@pytest.fixture
def get_homepage_objects(news_list, author_client):
    """Получение объектов главной страницы"""
    url = reverse('news:home')
    response = author_client.get(url)
    return response.context['object_list']


@pytest.fixture
def form_data():
    """Данные для POST-запроса по обновлению комментария"""
    return {'text': Constants.COMMENT_TEXT}


@pytest.fixture
def new_comment_data():
    """Данные для POST-запроса по обновлению комментария"""
    return {'text': Constants.NEW_COMMENT_TEXT}
