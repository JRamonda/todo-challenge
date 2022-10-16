import pytest
from base.models import Task

@pytest.fixture
def task_creation():
  return Task(
    title = 'ordenar',
  )

@pytest.mark.django_db
def test_task_creation(task_creation):
  task_creation.complete = True
  task_creation.save()
  assert task_creation.complete

@pytest.mark.django_db
def test_task_creation_fail():
  with pytest.raises(Exception):
    Task.objects.create(
      title = 'ordenar',
      complete = 'prueba',
    )