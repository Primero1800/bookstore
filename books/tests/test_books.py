import itertools
import json
from datetime import datetime, date

import pytest
from django.urls import reverse

from conftest import admin_api_client, models

URLS = [
    'http://football.kulichki.net',
    'https://www.primero1800.store',
    'https://www.sport-express.ru',
]
TESTS_COUNT = 10


@pytest.mark.django_db
def test_author_create(admin_api_client, models):
    Author = models['Author']
    author, _ = Author.objects.get_or_create(
        name='Test Author',
        surname='Ivanoff',
        slug='test_author_ivanoff',
        born=date(
            year=datetime.now().year-40,
            month=datetime.now().month,
            day=datetime.now().day,
        ),
    )
    author.save()
    authors = Author.objects.all()
    assert len(authors) == 1



@pytest.mark.parametrize(
    ('entered', 'expected'),
    list(
        zip(
            itertools.cycle(URLS), [201 for _ in range(TESTS_COUNT)]
        )
    )
)
@pytest.mark.django_db
def test_author_ads_settings(admin_api_client, models, author, entered, expected):
    Author = models['Author']
    authors = Author.objects.all()
    assert len(authors) == 1

    url = reverse('books:authoradssettings-list')
    Author = models['Author']

    data = {
        'author': Author.objects.last().id,
        'url': entered,
        'settings': json.dumps({
            "crontab": "* * * * *",
        }),
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == expected

    AuthorAdsSettings = models['AuthorAdsSettings']
    data = AuthorAdsSettings.objects.last().id
    url = reverse('books:authoradssettings-detail', args=(data,))
    response = admin_api_client.delete(url)
    assert response.status_code == 204

    aas = AuthorAdsSettings.objects.all()
    assert len(aas) == 0



# @pytest.mark.parametrize(
#     ('entered', 'expected'),
#     list(
#         zip(
#             itertools.cycle(URLS), [204 for _ in range(TESTS_COUNT)]
#         )
#     )
# )
# @pytest.mark.django_db
# def test_delete_author_ads_settings(admin_api_client, models, entered, expected):
#     AuthorAdsSettings = models['AuthorAdsSettings']
#     data = AuthorAdsSettings.objects.last().id
#     url = reverse('books:authoradssettings-detail', args=(data,))
#     response = admin_api_client.delete(url)
#     assert response.status_code == expected
#
#     aas = AuthorAdsSettings.objects.all()