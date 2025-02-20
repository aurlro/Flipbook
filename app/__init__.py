from flask import Flask, render_template
from config.default import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialisation des blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
        
    return app