import pytest
from flask import url_for, current_app

def test_index_route(client):
    """Test la route index."""
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
    # Ajoutez d'autres assertions selon ce que votre route index doit retourner

def test_config_route(client):
    response = client.get(url_for('main.config_page'))
    assert response.status_code == 200
    # Vérifier que les configurations sont bien affichées
    assert b'PDF Source' in response.data
    assert b'Output Folder' in response.data
    assert b'Quality' in response.data
    assert b'Dossier de destination' in response.data
    assert b'URL SharePoint' in response.data
    assert b'Username SharePoint' in response.data
    assert b'Password SharePoint' in response.data
    assert b'Dossier SharePoint' in response.data

def test_convert_route(client):
    response = client.get(url_for('main.convert'))
    assert response.status_code == 200

def test_history_route(client):
    response = client.get(url_for('main.history_page'))
    assert response.status_code == 200

def test_logs_route(client):
    """Test la route des logs."""
    response = client.get(url_for('main.logs_page'))
    assert response.status_code == 200
