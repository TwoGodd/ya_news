from http import HTTPStatus

import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import Constants
from pytest_django.asserts import assertFormError, assertRedirects

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
        client, url_news_detail, form_data):
    """Проверка возможности создания комментария анонимом"""
    comments_count = Comment.objects.count()
    client.post(url_news_detail, data=form_data)
    comments_count_after_test = Comment.objects.count()
    assert comments_count_after_test == comments_count


def test_user_can_create_comment(
        author_client, url_news_detail, form_data, news, author):
    """Проверка POST-запросов на добавление комментариев"""
    response = author_client.post(url_news_detail, data=form_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == Constants.COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(
        author_client, url_news_detail):
    """Проверка блокировки стоп-слов"""
    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url_news_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count_after_test = Comment.objects.count()
    assert comments_count_after_test == comments_count


def test_author_can_delete_comment(
        author_client, url_news_delete, url_to_comments):
    """Проверка на удаление комментрия автором"""
    assert Comment.objects.count() == 1
    response = author_client.delete(url_news_delete)
    assertRedirects(response, url_to_comments)
    comments_count_after_test = Comment.objects.count()
    assert comments_count_after_test == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, url_news_delete, comment):
    """Проврекана удаление комментрия от пользователя-читателя"""
    comments_count_before_test = Comment.objects.count()
    comments_before_test = Comment.objects.get()
    response = not_author_client.delete(url_news_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count_after_test = Comment.objects.count()
    comments_after_test = Comment.objects.get()
    assert comments_count_before_test == comments_count_after_test
    assert comments_before_test == comments_after_test


def test_author_can_edit_comment(author_client, new_comment_data,
                                 url_news_edit, url_to_comments, comment):
    """Проверкана редактирование от имени автора комментария"""
    comments_before_test = Comment.objects.get()
    response = author_client.post(url_news_edit, data=new_comment_data)
    assertRedirects(response, url_to_comments)
    comments_after_test = Comment.objects.get()
    assert comments_before_test == comments_after_test


def test_user_cant_edit_comment_of_another_user(
        not_author_client, new_comment_data, url_news_edit, comment):
    """Проверка на редактирование комментрия от имени другого пользователя"""
    comments_before_test = Comment.objects.get()
    response = not_author_client.post(url_news_edit, data=new_comment_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_after_test = Comment.objects.get()
    assert comments_before_test == comments_after_test
