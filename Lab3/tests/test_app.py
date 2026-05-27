import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_alive(client):
    rv = client.get('/health/alive')
    assert rv.status_code == 200
    assert b'OK' in rv.data

def test_root_html_only(client):
    rv = client.get('/', headers={'Accept': 'application/json'})
    assert rv.status_code == 406

def test_root_html_accept(client):
    rv = client.get('/', headers={'Accept': 'text/html'})
    assert rv.status_code == 200
    assert b'GET /tasks' in rv.data