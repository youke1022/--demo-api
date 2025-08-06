import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert len(response.json['users']) == 1