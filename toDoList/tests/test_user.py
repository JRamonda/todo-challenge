import pytest
from django.contrib.auth.models import User

@pytest.fixture
def user_creation():
  return User(
    username='john',
    email='jlennon@beatles.com',
    password='glass onion'
  )

@pytest.mark.django_db
def test_common_user_creation(user_creation):
  user_creation.is_staff = False
  user_creation.save()
  assert user_creation.is_staff == False

@pytest.mark.django_db
def test_superuser_creation(user_creation):
  user_creation.is_superuser = True
  user_creation.is_staff = True
  user_creation.save()
  assert user_creation.is_superuser

@pytest.mark.django_db
def test_staff_user_creation(user_creation):
  user_creation.is_staff = True
  user_creation.save()
  assert user_creation.is_staff

@pytest.mark.django_db
def test_user_creation_fail():
  with pytest.raises(Exception):
    User.objects.create_user(
      password='glass onion',
      is_staff=False
    )