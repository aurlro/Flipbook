"""Fournit les routes et la logique principale de l'application Flipbook."""

from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    url_for,
)

from .file_handler import FileHandler

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Affiche la page d'accueil."""
    return render_template("index.html")


@bp.route("/api/upload", methods=["POST"])
def upload_file():
    """
    Traiter les fichiers téléchargés.

    Gère l'upload des fichiers images et PDF, avec conversion si nécessaire.

    Returns:
        tuple: (JSON response, status code)
            - Pour les PDFs: URLs des pages converties
            - Pour les images: URL du fichier uploadé
    """
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    file_handler = FileHandler(current_app)
    result = file_handler.save_file(file)

    if not result["success"]:
        return jsonify({"error": result["error"]}), 400

    if result["type"] == "pdf":
        return handle_pdf_upload(result)
    return handle_image_upload(result)


def handle_pdf_upload(result):
    """
    Traiter l'upload d'un PDF.

    Args:
        result: Résultat de la sauvegarde du fichier

    Returns:
        Response: JSON avec les URLs des pages converties
    """
    page_urls = []
    for page_path in result["pages"]:
        rel_path = str(Path(page_path).relative_to(current_app.static_folder))
        page_urls.append(url_for("static", filename=rel_path))

    return jsonify(
        {
            "success": True,
            "type": "pdf",
            "pages": page_urls,
            "num_pages": result["num_pages"],
            "original_filename": result["original_filename"],
        }
    )


def handle_image_upload(result):
    """
    Traiter l'upload d'une image.

    Args:
        result: Résultat de la sauvegarde du fichier

    Returns:
        Response: JSON avec l'URL de l'image
    """
    file_path = Path(result["path"])
    rel_path = str(file_path.relative_to(current_app.static_folder))
    return jsonify(
        {
            "success": True,
            "type": "image",
            "path": url_for("static", filename=rel_path),
            "original_filename": result["original_filename"],
        }
    )


@bp.route("/api/pages")
def list_pages():
    """
    Lister toutes les pages disponibles.

    Returns:
        Response: Liste JSON des pages avec leurs URLs et types.
    """
    pdf_pages = Path(current_app.config["PDF_FOLDER"]).glob("*.jpg")
    uploads = Path(current_app.config["UPLOAD_FOLDER"]).glob("*.*")

    pages = []
    pages.extend(get_pdf_pages(pdf_pages))
    pages.extend(get_image_pages(uploads))

    return jsonify(
        {"success": True, "pages": sorted(pages, key=lambda x: x["filename"])}
    )


def get_pdf_pages(pdf_pages):
    """
    Obtenir la liste des pages PDF converties.

    Args:
        pdf_pages: Iterator des chemins de pages PDF

    Returns:
        list: Liste des informations des pages PDF
    """
    return [
        {
            "type": "pdf_page",
            "url": url_for("static", filename=f"pdf_pages/{page.name}"),
            "filename": page.name,
        }
        for page in pdf_pages
    ]


def get_image_pages(uploads):
    """
    Obtenir la liste des images uploadées.

    Args:
        uploads: Iterator des chemins d'images

    Returns:
        list: Liste des informations des images
    """
    img_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    return [
        {
            "type": "image",
            "url": url_for("static", filename=f"uploads/{upload.name}"),
            "filename": upload.name,
        }
        for upload in uploads
        if upload.suffix.lower() in img_extensions
    ]
