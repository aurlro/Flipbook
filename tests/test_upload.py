import pytest
import os
from io import BytesIO
from app import create_app
from app.utils.validators import FileValidator
from config.config import Config

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = 'tests/uploads'
    OUTPUT_FOLDER = 'tests/output'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    # Création des dossiers de test nécessaires
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    yield app
    
    # Nettoyage après les tests
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_upload_no_file(client):
    response = client.post('/')
    assert b'Aucun fichier' in response.data

def test_upload_empty_filename(client):
    data = {
        'pdf_file': (BytesIO(), '')
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'Aucun fichier' in response.data

def test_upload_invalid_extension(client):
    data = {
        'pdf_file': (BytesIO(b'not a pdf'), 'test.txt')
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'Type de fichier non autoris' in response.data

def test_file_validator():
    assert FileValidator.allowed_file('test.pdf') == True
    assert FileValidator.allowed_file('test.txt') == False

def create_test_pdf():
    """Crée un fichier PDF minimal pour les tests"""
    from reportlab.pdfgen import canvas
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 100, "Test PDF")
    c.save()
    buffer.seek(0)
    return buffer

def test_upload_valid_pdf(client):
    test_pdf = create_test_pdf()
    data = {
        'pdf_file': (test_pdf, 'test.pdf')
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 302  # Redirection après succès