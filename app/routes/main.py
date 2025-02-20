from flask import Blueprint, render_template, current_app
from app.services.pdf_processor import process_pdf
from app.services.html_generator import generate_html

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/process', methods=['POST'])
def process_document():
    # Logique de traitement du PDF
    pass