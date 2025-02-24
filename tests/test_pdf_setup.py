import os
import sys
from pathlib import Path

from pdf2image import convert_from_path
from reportlab.pdfgen import canvas


def create_test_pdf(filename="test.pdf"):
    """Crée un PDF de test valide."""
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Test PDF")
    c.save()
    return Path(filename).absolute()


def test_pdf_setup():
    print("Python version:", sys.version)
    print("\nTesting PDF conversion setup...")

    try:
        from pdf2image.exceptions import PDFInfoNotInstalledError

        print("pdf2image imported successfully")
    except ImportError as e:
        print("Error importing pdf2image:", e)
        return

    # Vérifier Poppler
    try:
        from pdf2image import pdfinfo_from_path

        print("Poppler installation found")
    except Exception as e:
        print("Error: Poppler might not be installed or not in PATH")
        print("Error details:", str(e))
        return

    try:
        # Créer un PDF de test valide
        pdf_path = create_test_pdf()
        print(f"Created test PDF at: {pdf_path}")

        # Tester la conversion
        images = convert_from_path(str(pdf_path), dpi=200)
        print(f"PDF conversion successful! Converted {len(images)} page(s)")

        # Sauvegarder la première page pour vérification
        if images:
            test_image_path = "test_output.jpg"
            images[0].save(test_image_path)
            print(f"Saved test image to: {Path(test_image_path).absolute()}")

    except PDFInfoNotInstalledError:
        print("Error: poppler-utils not found. Please install poppler.")
        print(
            "Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/"
        )
        print("Linux: sudo apt-get install poppler-utils")
        print("macOS: brew install poppler")
    except Exception as e:
        print("Error during conversion test:", e)
    finally:
        # Nettoyage
        for file in ["test.pdf", "test_output.jpg"]:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"Cleaned up: {file}")
            except Exception as e:
                print(f"Error cleaning up {file}: {e}")

    # Vérifier le PATH pour Poppler sur Windows
    if sys.platform == "win32":
        print("\nChecking Windows PATH for Poppler:")
        path_dirs = os.environ["PATH"].split(";")
        poppler_found = False
        for directory in path_dirs:
            if "poppler" in directory.lower():
                print(f"Found Poppler in PATH: {directory}")
                poppler_found = True
                try:
                    bin_contents = os.listdir(directory)
                    print(f"Contents of Poppler bin directory: {bin_contents}")
                except Exception as e:
                    print(f"Could not list directory contents: {e}")

        if not poppler_found:
            print("No Poppler directory found in PATH!")
            print("Please add the Poppler 'bin' directory to your system PATH")


if __name__ == "__main__":
    test_pdf_setup()
