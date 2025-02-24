import io

import pytest

from flipbook.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test de la page d'accueil"""
    rv = client.get("/")
    assert rv.status_code == 200
    html_content = rv.data.decode("utf-8")
    assert "Mon Flipbook" in html_content
    assert '<div class="flipbook-container">' in html_content


def test_upload_no_file(client):
    """Test de l'upload sans fichier"""
    rv = client.post("/api/upload")
    assert rv.status_code == 400
    assert b"No file part" in rv.data


def test_upload_empty_file(client):
    """Test de l'upload avec un fichier vide"""
    rv = client.post("/api/upload", data={"file": (io.BytesIO(b""), "")})
    assert rv.status_code == 400
    assert b"No selected file" in rv.data


def test_upload_valid_file(client):
    """Test de l'upload avec un fichier valide"""
    data = io.BytesIO()
    data.write(b"fake image data")
    data.seek(0)

    rv = client.post("/api/upload", data={"file": (data, "test.jpg")})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["success"] is True
    assert "filename" in json_data


def test_list_pages(client):
    """Test de la liste des pages"""
    rv = client.get("/api/pages")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "pages" in json_data
    assert "current_page" in json_data
