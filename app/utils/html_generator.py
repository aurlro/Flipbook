import os

def generate_html(image_files, title="Flipbook"):
    """
    Génère une page HTML intégrant le flipbook.
    Utilise un template simple.

    Parameters:
    image_files (list): Liste des chemins des fichiers image à inclure dans le flipbook.
    title (str): Le titre de la page HTML. Par défaut, "Flipbook".

    Returns:
    str: Le code HTML généré sous forme de chaîne de caractères.
    """
    image_basenames = [os.path.basename(img) for img in image_files]
    image_elements = "\n".join(
        [f'<img src="{img}" alt="Page {idx+1}">' for idx, img in enumerate(image_basenames)]
    )
    
    # Exemple de template très simple.
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link rel="stylesheet" href="css/flipbook.css">
    </head>
    <body>
        <div id="flipbook">
            {image_elements}
        </div>
    </body>
    </html>
    """
    return html_template
