import pytest
from io import BytesIO
from app import create_app
from app.utils.validators import FileValidator

@pytest.fixture
def app():
    app = create_app('config.TestConfig')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Convertisseur PDF en Flipbook' in response.data

def test_upload_invalid_file(client):
    data = {
        'pdf_file': (BytesIO(b'not a pdf'), 'test.txt'),
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'Format de fichier non autoris' in response.data

def test_file_validator():
    assert FileValidator.allowed_file('test.pdf') == True
    assert FileValidator.allowed_file('test.txt') == False