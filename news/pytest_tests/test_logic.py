from http import HTTPStatus

import pytest
from news.models import Comment
from pytest_django.asserts import assertRedirects, assertFormError
from news.pytest_tests.conftest import Constants
from news.forms import BAD_WORDS, WARNING

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
        client, get_news_detail, form_data):
    """Проверка возможности создания комментария анонимом"""
    client.post(get_news_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author_client, get_news_detail, form_data, news, author):
    """Проверка POST-запросов на добавление комментариев"""
    response = author_client.post(get_news_detail, data=form_data)
    assertRedirects(response, f'{get_news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == Constants.COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, get_news_detail):
    """Проверка блокировки стоп-слов"""
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(get_news_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url, url_to_comments):
    """Проверка на удаление комментрия автором"""
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, delete_url):
    """Проврекана удаление комментрия от пользователя-читателя"""
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client, new_comment_data, edit_url, url_to_comments, comment):
    """Проверкана редактирование от имени автора комментария"""
    response = author_client.post(edit_url, data=new_comment_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == Constants.NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
        not_author_client, new_comment_data, edit_url, comment):
    """Проверка на редактирование комментрия от имени другого пользователя"""
    response = not_author_client.post(edit_url, data=new_comment_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == Constants.COMMENT_TEXT
