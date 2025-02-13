@echo off
setlocal EnableDelayedExpansion

:: Ajout d'un log pour le débogage
set "LOG_FILE=%~dp0deploy_log.txt"
echo Démarrage du déploiement: %date% %time% > "%LOG_FILE%"

:: Définition de l'arborescence
set "BASE_DIR=%~dp0"
set "BASE_DIR=%BASE_DIR:~0,-1%"
set "FLIPBOOK_DIR=%BASE_DIR%\Flipbook"
set "CONFIG_FILE=%FLIPBOOK_DIR%\config\settings.ini"
set "PY_SCRIPT=%FLIPBOOK_DIR%\flipbook_generator.py"
set "LOG_DIR=%FLIPBOOK_DIR%\logs"
set "VENV_DIR=%FLIPBOOK_DIR%\venv"

:: ********************************************
:: 1. Environnement virtuel
:: ********************************************
echo [1/9] Configuration du venv...
if not exist "%VENV_DIR%\" (
    echo Création de l'environnement virtuel...
    python -m venv "%VENV_DIR%" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo ERREUR: Échec de création du venv >> "%LOG_FILE%"
        echo ERREUR: Échec de création du venv
        echo Consultez le fichier %LOG_FILE% pour plus de détails
        pause
        exit /b 1
    ) else (
        echo Environnement virtuel créé.
    )
) else (
    echo Environnement virtuel déjà présent.
)
pause

:: ********************************************
:: 2. Installation des dépendances
:: ********************************************
echo [2/9] Installation des dépendances...
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat" >> "%LOG_FILE%" 2>&1
    "%VENV_DIR%\Scripts\pip" list | findstr "pymupdf pillow" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        "%VENV_DIR%\Scripts\pip" install --no-cache-dir pymupdf pillow >> "%LOG_FILE%" 2>&1
        if errorlevel 1 (
            echo ERREUR: Installation des packages >> "%LOG_FILE%"
            echo ERREUR: Installation des packages
            echo Consultez le fichier %LOG_FILE% pour plus de détails
            pause
            exit /b 1
        ) else (
            echo Dépendances installées.
        )
    ) else (
        echo Dépendances déjà installées.
    )
) else (
    echo ERREUR: L'environnement virtuel n'existe pas >> "%LOG_FILE%"
    echo ERREUR: L'environnement virtuel n'existe pas
    pause
    exit /b 1
)
pause

:: Vérification de Python avec log
echo [3/9] Vérification de Python 3.8+...
python --version >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ATTENTION: Python non trouvé dans le PATH. Le script va continuer mais des erreurs peuvent survenir.
    echo ATTENTION: Python non trouvé dans le PATH. >> "%LOG_FILE%"
) else (
    echo Python trouvé.
)
pause

:: Vérification de la version de Python
for /f "tokens=1,2 delims=." %%A in ('python -V 2^>^&1') do (
    set PYTHON_MAJOR=%%A
    set PYTHON_MINOR=%%B
)

:: Convertir les versions en nombres entiers pour comparaison
set /a PYTHON_MAJOR_INT=%PYTHON_MAJOR:~2%
set /a PYTHON_MINOR_INT=%PYTHON_MINOR%

:: Comparaison de la version de Python
if %PYTHON_MAJOR_INT% LSS 3 (
    echo ATTENTION: Version Python trop ancienne ^(3.8+ requis^). Le script va continuer mais des erreurs peuvent survenir.
    python --version
) else if %PYTHON_MAJOR_INT% EQU 3 (
    if %PYTHON_MINOR_INT% LSS 8 (
        echo ATTENTION: Version Python trop ancienne ^(3.8+ requis^). Le script va continuer mais des erreurs peuvent survenir.
        python --version
    ) else (
        echo Version Python correcte.
    )
)
pause

:: Vérification de curl
echo [4/9] Vérification de curl...
curl --version >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERREUR: curl non trouvé dans le PATH.
    echo Veuillez télécharger curl depuis https://curl.se/windows/ et ajouter le chemin d'accès au répertoire bin de curl à la variable PATH.
    echo Cette erreur a été enregistrée dans %LOG_FILE%
    echo ERREUR: curl non trouvé dans le PATH. >> "%LOG_FILE%"
    pause
    exit /b 1
) else (
    echo curl trouvé.
)
pause

:: Demande de l'URL SharePoint spécifique
set "SHAREPOINT_URL="
setlocal EnableDelayedExpansion
if not exist "%CONFIG_FILE%" (
    :ask_url
    set /p "SHAREPOINT_URL=Veuillez entrer l'URL SharePoint spécifique (ex: https://capgemini.sharepoint.com/...): "
    if "!SHAREPOINT_URL!" == "" (
        echo URL ne peut pas être vide.
        goto :ask_url
    )
    set "SHAREPOINT_URL=!SHAREPOINT_URL:"=!"
    set "SHAREPOINT_URL=!SHAREPOINT_URL:http://=https://!"
    if "!SHAREPOINT_URL:~0,8!" neq "https://" set "SHAREPOINT_URL=https://!SHAREPOINT_URL!"
    echo URL SharePoint définie sur !SHAREPOINT_URL!
    pause
) else (
    for /f "tokens=1,2 delims==" %%A in ('type "%CONFIG_FILE%" ^| find "sharepoint_base_url"') do (
        set "SHAREPOINT_URL=%%B"
    )
    set "SHAREPOINT_URL=!SHAREPOINT_URL:"=!"
    echo URL SharePoint définie sur !SHAREPOINT_URL!
    pause
)

:: Vérification des droits d'écriture
echo [5/9] Test des droits d'écriture... >> "%LOG_FILE%" 2>&1
mkdir "%FLIPBOOK_DIR%\_test" 2>nul
if errorlevel 1 (
    echo ERREUR: Pas de droits d'écriture dans le dossier >> "%LOG_FILE%"
    echo ERREUR: Pas de droits d'écriture dans le dossier
    pause
    exit /b 1
) else (
    echo Droits d'écriture confirmés.
)

:: Vérification de la suppression du dossier _test
if exist "%FLIPBOOK_DIR%\_test" (
    rd "%FLIPBOOK_DIR%\_test"
    if errorlevel 1 (
        echo ERREUR: Impossible de supprimer le dossier _test >> "%LOG_FILE%"
        echo ERREUR: Impossible de supprimer le dossier _test
        pause
        exit /b 1
    ) else (
        echo Dossier _test supprimé.
    )
) else (
    echo Dossier _test déjà supprimé.
)
pause

:: ********************************************
:: 6. Création de l'arborescence
:: ********************************************
echo [6/9] Création de l'arborescence...
if not exist "%FLIPBOOK_DIR%" mkdir "%FLIPBOOK_DIR%"
for %%d in (pdf_source pdf_cible html_cible fait logs config) do (
    if not exist "%FLIPBOOK_DIR%\%%d" mkdir "%FLIPBOOK_DIR%\%%d"
)
if errorlevel 1 (
    echo ERREUR: Création des dossiers échouée >> "%LOG_FILE%"
    echo ERREUR: Création des dossiers échouée
    pause
    exit /b 1
) else (
    echo Arborescence créée.
)
pause

:: ********************************************
:: 7. Génération du script Python
:: ********************************************
echo [7/9] Génération du script flipbook_generator.py...
if not exist "%PY_SCRIPT%" (
    (
        echo import os
        echo import sys
        echo import fitz
        echo import configparser
        echo from PIL import Image
        echo from urllib.parse import urlparse
        echo.
        echo # Lecture de la configuration
        echo config = configparser.ConfigParser()
        echo config.read(os.path.join(os.path.dirname(__file__), 'config', 'settings.ini'))
        echo.
        echo # Validation de l'URL SharePoint
        echo parsed_url = urlparse(config['DEFAULT']['sharepoint_base_url'])
        echo if not (parsed_url.scheme == 'https' and parsed_url.netloc and len(parsed_url.netloc.split('.')) >= 2):
        echo     raise ValueError(f"URL SharePoint INVALIDE: {config['DEFAULT']['sharepoint_base_url']} - HTTPS requis et domaine valide")
        echo.
        echo # Définition des chemins
        echo PATHS = {
        echo     'source_dir': os.path.join(os.path.dirname(__file__), 'pdf_source'),
        echo     'output_img': os.path.join(os.path.dirname(__file__), 'pdf_cible'),
        echo     'output_html': os.path.join(os.path.dirname(__file__), 'html_cible'),
        echo     'done_dir': os.path.join(os.path.dirname(__file__), 'fait')
        echo }
        echo.
        echo # Paramètres
        echo SETTINGS = {
        echo     'dpi': 200,
        echo     'quality': config['DEFAULT'].getint('image_quality')
        echo }
        echo.
        echo # Fonction pour générer le flipbook HTML
        echo def generate_html(pdf_name, page_count):
        echo     return f'''<!DOCTYPE html>
        echo <html>
        echo <head>
        echo     <meta charset="UTF-8"/>
        echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        echo     <title>{pdf_name}</title>
        echo     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lettura@2.1.0/dist/lettura.min.css"/>
        echo </head>
        echo <body>
        echo     <div
        echo         data-flipbook
        echo         data-source="../pdf_cible/{pdf_name}/"
        echo         data-format="jpg"
        echo         style="width: 100%; height: 100vh;">
        echo     </div>
        echo     <script src="https://cdn.jsdelivr.net/npm/lettura@2.1.0/dist/lettura.min.js"></script>
        echo </body>
        echo </html>
        echo '''
        echo.
        echo # Traitement d'un fichier PDF
        echo def process_pdf(pdf_path):
        echo     try:
        echo         pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        echo         output_dir = os.path.join(PATHS['output_img'], pdf_name)
        echo         os.makedirs(output_dir, exist_ok=True)
        echo         doc = fitz.open(pdf_path)
        echo         for i in range(len(doc)):
        echo             page = doc.load_page(i)
        echo             pix = page.get_pixmap(dpi=SETTINGS['dpi'])
        echo             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        echo             img.save(os.path.join(output_dir, f"page_{i+1}.jpg"), quality=SETTINGS['quality'])
        echo         with open(os.path.join(PATHS['output_html'], f"{pdf_name}.html"), 'w', encoding='utf-8') as f:
        echo             f.write(generate_html(pdf_name, len(doc)))
        echo         os.rename(pdf_path, os.path.join(PATHS['done_dir'], os.path.basename(pdf_path)))
        echo         return True
        echo     except Exception as e:
        echo         print(f"ERREUR: {str(e)}")
        echo         return False
        echo.
        echo if __name__ == '__main__':
        echo     for filename in os.listdir(PATHS['source_dir']):
        echo         if filename.lower().endswith('.pdf'):
        echo             process_pdf(os.path.join(PATHS['source_dir'], filename))
    ) > "%PY_SCRIPT%"
    if errorlevel 1 (
        echo ERREUR: Génération du script Python >> "%LOG_FILE%"
        echo ERREUR: Génération du script Python
        pause
        exit /b 1
    ) else (
        echo Script Python généré.
    )
) else (
    echo Script Python déjà présent.
)
pause

:: ********************************************
:: 8. Configuration (settings.ini)
:: ********************************************
echo [8/9] Configuration...
if not exist "%CONFIG_FILE%" (
    set "IMG_QUALITY=85"
    setlocal EnableDelayedExpansion
    set /p "IMG_QUALITY=Qualité images [85]: "
    if "!IMG_QUALITY!" == "" set "IMG_QUALITY=85"
    if !IMG_QUALITY! lss 0 set "IMG_QUALITY=85"
    (
        echo [DEFAULT]
        echo sharepoint_base_url = "!SHAREPOINT_URL!"
        echo image_quality = !IMG_QUALITY!
    ) > "%CONFIG_FILE%"
    endlocal
) else (
    echo Fichier de configuration déjà présent.
)
pause

:: ********************************************
:: 9. Démarrage du script
:: ********************************************
echo [9/9] Démarrage du script Flipbook...
if exist "%PY_SCRIPT%" (
    "%VENV_DIR%\Scripts\python" "%PY_SCRIPT%" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
        echo ERREUR: Exécution du script Python >> "%LOG_FILE%"
        echo ERREUR: Exécution du script Python
        echo Consultez le fichier %LOG_FILE% pour plus de détails
        pause
        exit /b 1
    ) else (
        echo Script Flipbook démarré.
    )
) else (
    echo ERREUR: Le script Python n'existe pas >> "%LOG_FILE%"
    echo ERREUR: Le script Python n'existe pas
    pause
    exit /b 1
)

echo.
echo Processus terminé. Vérifiez le fichier log pour plus de détails.
echo Log disponible dans: %LOG_FILE%
pause
