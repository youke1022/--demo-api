import pytest
from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.mark.parametrize("input_data, expected_status", [
    ({"id": 2, "name": "New User"}, 201),
    ({}, 400),  # 无效数据测试
])
def test_add_user_parametrized(client, input_data, expected_status):
    response = client.post('/api/users', json=input_data)
    assert response.status_code == expected_status

