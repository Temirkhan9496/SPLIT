import pytest
from app import app

#тесты для всех методов нашего API и для методов класса работы с БД. Мы будем использовать pytest для этого:
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_pereval(client):
    rv = client.get('/submitData/1')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert 'id' in json_data

def test_update_pereval(client):
    rv = client.patch('/submitData/1', json={'name': 'Updated Again'})
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['state'] == 1

def test_get_perevals_by_email(client):
    rv = client.get('/submitData/?user__email=test@example.com')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data) > 0
    assert 'id' in json_data[0]