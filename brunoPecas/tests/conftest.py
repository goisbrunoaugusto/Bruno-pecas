import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from cars.models import CarModel
from parts.models import Part

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='testpass123',
        role='ADMIN'
    )

@pytest.fixture
def regular_user():
    return User.objects.create_user(
        username='regular',
        email='regular@test.com',
        password='testpass123',
        role='REGULAR'
    )

@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def authenticated_regular_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client

@pytest.fixture
def sample_part():
    return Part.objects.create(
        id=1,
        part_number=1,
        name="Test Part",
        price=99.99,
        quantity=10
    )

@pytest.fixture
def sample_car():
    return CarModel.objects.create(
        id=1,
        name="Test Car",
        manufacturer="Test Manufacturer",
        year=2024,
        details="Test Details"
    )
