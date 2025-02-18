import os

def generate_html(image_files, title="Flipbook"):
    """
    Génère une page HTML intégrant le flipbook.
    Utilise un template simple qui intègre le script Turn.js.
    """
    image_elements = "\n".join(
        [f'<img src="{os.path.basename(img)}" alt="Page {idx+1}">' for idx, img in enumerate(image_files)]
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
        <script src="js/turn.min.js"></script>
        <script>
            // Initialisation du flipbook
            $("#flipbook").turn({{
                width: 800,
                height: 600,
                autoCenter: true
            }});
        </script>
    </body>
    </html>
    """
    return html_template
