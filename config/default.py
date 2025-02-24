import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    PDF_SOURCE_FOLDER = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "src/PDF_SOURCE"
    )
    OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    ALLOWED_EXTENSIONS = {"pdf"}
