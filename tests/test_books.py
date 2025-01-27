import pytest
from django.urls import reverse

from books.models import AuthorAdsSettings, Author


@pytest.mark.api
def test_create_authos_ads_settings(admin_api_client):
    url = reverse('books:api:ads-list')
    data = {
        'author': Author.objects.last(),
        'url': 'http://any-test.url',
        'settings': {
            "crontab": "* * * * *",
        },
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == 201