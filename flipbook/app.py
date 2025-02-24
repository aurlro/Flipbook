from pathlib import Path

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   url_for)

from .file_handler import FileHandler

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Route pour la page d'accueil."""
    return render_template("index.html")


@bp.route("/api/upload", methods=["POST"])
def upload_file():
    """Gère l'upload des fichiers."""
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    file_handler = FileHandler(current_app)
    result = file_handler.save_file(file)

    if not result["success"]:
        return jsonify({"error": result["error"]}), 400

    # Convertir les chemins en URLs
    if result["type"] == "pdf":
        page_urls = [
            url_for(
                "static", filename=str(Path(p).relative_to(current_app.static_folder))
            )
            for p in result["pages"]
        ]
        return jsonify(
            {
                "success": True,
                "type": "pdf",
                "pages": page_urls,
                "num_pages": result["num_pages"],
                "original_filename": result["original_filename"],
            }
        )
    else:
        return jsonify(
            {
                "success": True,
                "type": "image",
                "path": url_for(
                    "static",
                    filename=str(
                        Path(result["path"]).relative_to(current_app.static_folder)
                    ),
                ),
                "original_filename": result["original_filename"],
            }
        )


@bp.route("/api/pages")
def list_pages():
    """Liste toutes les pages disponibles."""
    pdf_pages = Path(current_app.config["PDF_FOLDER"]).glob("*.jpg")
    uploads = Path(current_app.config["UPLOAD_FOLDER"]).glob("*.*")

    pages = []

    # Ajouter les pages PDF converties
    for page in pdf_pages:
        pages.append(
            {
                "type": "pdf_page",
                "url": url_for("static", filename=f"pdf_pages/{page.name}"),
                "filename": page.name,
            }
        )

    # Ajouter les images uploadées
    for upload in uploads:
        if upload.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            pages.append(
                {
                    "type": "image",
                    "url": url_for("static", filename=f"uploads/{upload.name}"),
                    "filename": upload.name,
                }
            )

    return jsonify(
        {"success": True, "pages": sorted(pages, key=lambda x: x["filename"])}
    )
