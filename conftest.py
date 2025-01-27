from datetime import date, datetime

import django
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from django.apps import apps


django.setup()



@pytest.fixture
def admin_api_client():
    user_model = get_user_model()

    admin, _ = user_model.objects.get_or_create(
        username='admin',
        password='adminpassword',
        is_staff=True,
        is_superuser=True
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    return client


@pytest.fixture
def models():
    return {model.__name__: model for model in apps.get_models()}

@pytest.fixture
def author(models):
    Author = models['Author']
    author = None
    if Author:
        author, _ = Author.objects.get_or_create(
            name='Test Author',
            surname='Ivanoff',
            slug='test_author_ivanoff',
            born=date(
                year=datetime.now().year - 40,
                month=datetime.now().month,
                day=datetime.now().day,
            ),
        )
        author.save()
    return author
