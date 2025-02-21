import os
import pytest
from app import create_app
from urllib.parse import quote as url_quote


@pytest.fixture
def app():
    """Créé une instance de l'application pour les tests."""
    app = create_app("testing")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Créé un client de test."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Créé un runner de test pour les commandes CLI."""
    return app.test_cli_runner()
