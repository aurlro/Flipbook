from flask import Flask
from config.config import Config
import os

def create_app(config_name='default'):
    app = Flask(__name__, 
                static_folder='output',
                static_url_path='/output')
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
        
        # Configuration spécifique pour les tests
        app.config.update({
            'SERVER_NAME': 'localhost',
            'TESTING': True,
            'PDF_SOURCE': 'test_pdf_source',
            'OUTPUT_FOLDER': 'test_output_folder'
        })
    else:
        app.config.from_object('config.DevelopmentConfig')


        
    # Création sécurisée des dossiers
    for folder in [app.config['PDF_SOURCE'], app.config['OUTPUT_FOLDER']]:
        os.makedirs(folder, mode=0o750, exist_ok=True)
    
    # Création des dossiers seulement en mode non-test
    if not app.config.get('TESTING'):
        os.makedirs(app.config.get('PDF_SOURCE', 'default_pdf_source'), exist_ok=True)
        os.makedirs(app.config.get('OUTPUT_FOLDER', 'default_output_folder'), exist_ok=True)
        os.makedirs('output', exist_ok=True)
        os.makedirs('upload', exist_ok=True)
    
    # Enregistrement des blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    return app
