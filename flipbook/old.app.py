from pathlib import Path

from flask import Flask, jsonify, render_template, request

from .core import FlipbookRenderer

# Créez l'application Flask avec le bon template_folder
template_dir = Path(__file__).resolve().parent / "templates"
static_dir = Path(__file__).resolve().parent / "static"
app = Flask(
    __name__, template_folder=str(template_dir), static_folder=str(static_dir)
)

renderer = FlipbookRenderer()

# Configuration
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    UPLOAD_FOLDER=Path("upload"),
    ALLOWED_EXTENSIONS={"png", "jpg", "jpeg", "gif"},
)


def allowed_file(filename: str) -> bool:
    """Vérifie si l'extension du fichier est autorisée."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/")
def index():
    """Route pour la page d'accueil."""
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Gère l'upload des fichiers."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = Path(file.filename)
        save_path = app.config["UPLOAD_FOLDER"] / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)
        file.save(str(save_path))

        result = renderer.load_page(str(save_path))
        if result.success:
            return jsonify(
                {
                    "success": True,
                    "filename": filename.name,
                    "path": str(save_path),
                }
            )
        return jsonify({"error": result.error}), 400

    return jsonify({"error": "File type not allowed"}), 400


@app.route("/api/pages/list")
def list_available_pages():
    """Renvoie la liste des pages disponibles"""
    static_dir = Path(app.static_folder) / "images"
    images = []

    if static_dir.exists():
        images = [
            url_for("static", filename=f"images/{f.name}")
            for f in static_dir.iterdir()
            if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif"}
        ]

    return jsonify({"pages": images})


if __name__ == "__main__":
    app.run(debug=True)
