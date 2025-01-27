import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient



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