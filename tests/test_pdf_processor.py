import pytest
import os
from app.utils.pdf_processor import PDFProcessor
from reportlab.pdfgen import canvas
from io import BytesIO

@pytest.fixture
def test_pdf_path(tmp_path):
    """Crée un PDF de test temporaire"""
    pdf_path = tmp_path / "test.pdf"
    
    # Création d'un PDF simple
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 100, "Page 1")
    c.showPage()
    c.drawString(100, 100, "Page 2")
    c.save()
    
    return str(pdf_path)

@pytest.fixture
def processor(app):
    """Crée une instance du processeur PDF"""
    return PDFProcessor(app.config)

def test_pdf_processing(processor, test_pdf_path):
    """Teste le traitement complet d'un PDF"""
    result = processor.process_pdf(test_pdf_path)
    
    assert result['status'] == 'success'
    assert result['image_count'] == 2
    assert len(result['images']) == 2
    
    # Vérifie que les fichiers images existent
    for image_path in result['images']:
        assert os.path.exists(image_path)

def test_invalid_pdf_processing(processor, tmp_path):
    """Teste le traitement d'un fichier invalide"""
    invalid_pdf = tmp_path / "invalid.pdf"
    with open(invalid_pdf, 'w') as f:
        f.write("Not a PDF")
    
    with pytest.raises(Exception):
        processor.process_pdf(str(invalid_pdf))