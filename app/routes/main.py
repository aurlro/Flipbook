import os
from flask import render_template, current_app, request, flash, jsonify
from app.services.pdf_processor import process_pdf
from app.services.html_generator import generate_html
from app.routes import main  # Importez l'instance 'main'

@main.route('/')
def index():
    """
    Route principale affichant le flipbook.
    Charge les images depuis le dossier `output_folder` et les affiche dans un template HTML.
    """
    output_folder = current_app.config['OUTPUT_FOLDER']
    pages = []

    try:
        # Récupérer les chemins des images dans l'ordre
        for file in sorted(os.listdir(output_folder)):
            if file.endswith(('.jpg', '.png', '.jpeg')):
                page_path = f'/output/{file}'  # Chemin relatif pour l'URL
                pages.append(page_path)
    except FileNotFoundError:
        flash("Le dossier de sortie n'existe pas.", "error")
    except Exception as e:
        flash(f"Erreur lors du chargement des images: {e}", "error")

    return render_template('flipbook_template.html', pages=pages)

@main.route('/config')
def config_page():
    """
    Route affichant la page de configuration.
    Récupère les configurations actuelles de l'application et les affiche dans un template HTML.
    """
    config = {
        'pdf_source': current_app.config.get('PDF_SOURCE', ''),
        'output_folder': current_app.config.get('OUTPUT_FOLDER', ''),
        'quality': current_app.config.get('QUALITY', 100)
    }
    return render_template('config.html', config=config)

@main.route('/convert')
def convert():
    """
    Route affichant la page de conversion.
    """
    return render_template('convert.html')

@main.route('/history')
def history_page():
    """
    Route affichant l'historique des conversions.
    **TODO:** Implémenter la logique pour récupérer l'historique des conversions.
    """
    conversions = []  # À remplacer par la vraie récupération des données
    return render_template('history.html', conversions=conversions)

@main.route('/logs')
def logs_page():
    """
    Route affichant les logs.
    **TODO:** Implémenter la logique pour récupérer les logs.
    """
    logs = []  # À remplacer par la vraie récupération des logs
    return render_template('logs.html', logs=logs)

@main.route('/process-pdf', methods=['POST'])
def process_pdf_route():
    """
    Route pour traiter le PDF et générer le flipbook.
    Reçoit le chemin du PDF, le dossier de sortie et la qualité en entrée.
    Appelle les fonctions `process_pdf` et `generate_html` pour effectuer le traitement.
    Retourne une réponse JSON indiquant le succès ou l'échec de l'opération.
    """
    try:
        pdf_path = current_app.config['PDF_SOURCE']
        output_folder = current_app.config['OUTPUT_FOLDER']
        quality = current_app.config['QUALITY']

        # Vérifier si le fichier PDF existe
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("Le fichier PDF source n'existe pas.")

        image_files = process_pdf(pdf_path, output_folder, quality)
        # generate_html(image_files)  # Vous n'utilisez pas le résultat de cette fonction ici

        # Vous pourriez ajouter ici l'enregistrement dans l'historique

        flash('PDF traité avec succès', 'success')
        return jsonify({
            'status': 'success',
            'message': 'PDF processed successfully',
            'files': image_files  # Retourner les noms des fichiers image
        })
    except FileNotFoundError as e:
        flash(str(e), "error")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    except Exception as e:
        flash(f"Erreur lors du traitement du PDF: {e}", "error")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/update-config', methods=['POST'])
def update_config():
    """
    Route pour mettre à jour la configuration de l'application.
    Reçoit les nouvelles valeurs de configuration via un formulaire HTML.
    Met à jour les variables de configuration de l'application.
    Retourne une réponse JSON indiquant le succès ou l'échec de l'opération.
    """
    try:
        # Mettre à jour la configuration
        current_app.config['PDF_SOURCE'] = request.form.get('pdf_source')
        current_app.config['OUTPUT_FOLDER'] = request.form.get('output_folder')
        current_app.config['QUALITY'] = int(request.form.get('quality', 100))

        # Validation des données du formulaire (à implémenter)
        #...

        flash('Configuration mise à jour avec succès', 'success')
        return jsonify({'status': 'success'})
    except ValueError:
        flash("La qualité doit être un nombre entier.", "error")
        return jsonify({'status': 'error', 'message': "La qualité doit être un nombre entier."}), 500
    except Exception as e:
        flash(f"Erreur lors de la mise à jour de la configuration: {e}", "error")
        return jsonify({'status': 'error', 'message': str(e)}), 500