"""Tests pour les utilitaires du FlipBook."""

import pytest
from pathlib import Path
from app.utils import PDFProcessor, HTMLGenerator, DependencyManager


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Crée un dossier temporaire pour les tests."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def temp_template_dir(tmp_path: Path) -> Path:
    """Crée un dossier temporaire pour les templates."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir(parents=True)
    return template_dir


@pytest.fixture
def html_generator(temp_template_dir: Path) -> HTMLGenerator:
    """Instance de HTMLGenerator pour les tests."""
    generator = HTMLGenerator(template_dir=temp_template_dir)
    generator._ensure_default_template()
    return generator


def test_html_generator_initialization(temp_template_dir: Path) -> None:
    """Test d'initialisation du HTMLGenerator."""
    generator = HTMLGenerator(template_dir=temp_template_dir)
    generator._ensure_default_template()
    assert generator is not None
    assert generator.template_dir == temp_template_dir
    template_path = temp_template_dir / "flipbook.html"
    assert template_path.exists(), f"Le template n'existe pas à {template_path}"


def test_html_generator_template_creation(
    html_generator: HTMLGenerator, temp_template_dir: Path
) -> None:
    """Test de la création du template par défaut."""
    templates = html_generator.get_template_list()
    assert "flipbook.html" in templates, f"Templates disponibles : {templates}"
    template_path = temp_template_dir / "flipbook.html"
    assert template_path.exists(), f"Le template n'existe pas à {template_path}"


def test_pdf_processor_initialization() -> None:
    """Test d'initialisation du PDFProcessor."""
    processor = PDFProcessor()
    assert processor is not None
    assert processor.quality == 75
    assert isinstance(processor.output_folder, Path)


def test_dependency_manager_exists() -> None:
    """Vérifie que DependencyManager existe."""
    assert DependencyManager is not None


def test_dependency_manager_can_check_dependencies() -> None:
    """Vérifie que DependencyManager peut vérifier les dépendances."""
    status = DependencyManager.get_dependency_status()
    assert isinstance(status, dict)
    assert "total" in status
    assert "installed" in status
