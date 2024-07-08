import pytest
from db_handler import DatabaseHandler
import os

  #тесты для всех методов нашего API и для методов класса работы с БД. Мы будем использовать pytest для этого:
@pytest.fixture
def db():
    return DatabaseHandler()

def test_get_pereval_by_id(db):
    result = db.get_pereval_by_id(1)
    assert result is not None
    assert 'id' in result

def test_update_pereval(db):
    data = {'name': 'Updated Name'}
    status, message = db.update_pereval(1, data)
    assert status == 1
    assert message == "Update successful"
    result = db.get_pereval_by_id(1)
    assert result['name'] == 'Updated Name'

def test_get_perevals_by_email(db):
    email = 'test@example.com'
    results = db.get_perevals_by_email(email)
    assert len(results) > 0
    for result in results:
        assert result['user_email'] == email