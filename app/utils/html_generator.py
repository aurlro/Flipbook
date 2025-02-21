"""Module de génération de pages HTML pour le FlipBook."""

import logging
from pathlib import Path
from typing import List, Optional

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


logger = logging.getLogger(__name__)


class HTMLGenerator:
    """Générateur de HTML pour le FlipBook."""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialise le générateur HTML.

        Args:
            template_dir (Path, optional): Répertoire des templates
        """
        if not JINJA2_AVAILABLE:
            raise ImportError(
                "Le package jinja2 est requis. "
                "Installez-le avec 'pip install jinja2'"
            )

        self.template_dir = template_dir or Path("app/templates")
        self.template_dir.mkdir(parents=True, exist_ok=True)

        # Création du template par défaut
        self._ensure_default_template()

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def _ensure_default_template(self) -> None:
        """Crée le template HTML par défaut s'il n'existe pas."""
        template_path = self.template_dir / "flipbook.html"
        if not template_path.exists():
            default_template = self._get_default_template()
            template_path.write_text(default_template, encoding="utf-8")
            logger.info(f"Template par défaut créé : {template_path}")

    def _get_default_template(self) -> str:
        """
        Retourne le contenu du template HTML par défaut.

        Returns:
            str: Le contenu du template HTML
        """
        return (
            "<!DOCTYPE html>\n"
            '<html lang="fr">\n'
            "<head>\n"
            '    <meta charset="UTF-8">\n'
            '    <meta name="viewport" content="width=device-width, '
            'initial-scale=1.0">\n'
            "    <title>{{ title }}</title>\n"
            "    <style>\n"
            "        body {\n"
            "            margin: 0;\n"
            "            padding: 0;\n"
            "            background: #333;\n"
            "            display: flex;\n"
            "            flex-direction: column;\n"
            "            align-items: center;\n"
            "            min-height: 100vh;\n"
            "        }\n"
            "        .flipbook-container {\n"
            "            width: 100%;\n"
            "            max-width: {{ page_width }}px;\n"
            "            margin: 20px auto;\n"
            "            text-align: center;\n"
            "        }\n"
            "        .page {\n"
            "            max-width: 100%;\n"
            "            height: auto;\n"
            "            display: none;\n"
            "            margin: auto;\n"
            "        }\n"
            "        .page.active {\n"
            "            display: block;\n"
            "        }\n"
            "        .controls {\n"
            "            position: fixed;\n"
            "            bottom: 20px;\n"
            "            left: 50%;\n"
            "            transform: translateX(-50%);\n"
            "            background: rgba(0, 0, 0, 0.7);\n"
            "            padding: 10px;\n"
            "            border-radius: 5px;\n"
            "            z-index: 1000;\n"
            "            color: white;\n"
            "        }\n"
            "        button {\n"
            "            padding: 8px 15px;\n"
            "            margin: 0 5px;\n"
            "            cursor: pointer;\n"
            "            background: #444;\n"
            "            color: white;\n"
            "            border: 1px solid #666;\n"
            "            border-radius: 3px;\n"
            "        }\n"
            "        button:disabled {\n"
            "            opacity: 0.5;\n"
            "            cursor: not-allowed;\n"
            "        }\n"
            "        #page-num {\n"
            "            margin: 0 10px;\n"
            "        }\n"
            "    </style>\n"
            "</head>\n"
            "<body>\n"
            '    <div class="flipbook-container">\n'
            "        {% for image in images %}\n"
            '        <img src="{{ image }}" class="page" '
            'alt="Page {{ loop.index }}" data-page="{{ loop.index }}">\n'
            "        {% endfor %}\n"
            "    </div>\n"
            '    <div class="controls">\n'
            '        <button id="prev">Précédent</button>\n'
            '        <span id="page-num">Page 1/{{ images|length }}</span>\n'
            '        <button id="next">Suivant</button>\n'
            "    </div>\n"
            "    <script>\n"
            "        document.addEventListener('DOMContentLoaded', function() {\n"
            "            const pages = document.querySelectorAll('.page');\n"
            "            const pageNum = document.getElementById('page-num');\n"
            "            const prevBtn = document.getElementById('prev');\n"
            "            const nextBtn = document.getElementById('next');\n"
            "            let currentPage = 0;\n"
            "\n"
            "            function showPage(index) {\n"
            "                pages.forEach(page => "
            "page.classList.remove('active'));\n"
            "                pages[index].classList.add('active');\n"
            "                pageNum.textContent = `Page ${index + 1}/"
            "${pages.length}`;\n"
            "                prevBtn.disabled = index === 0;\n"
            "                nextBtn.disabled = index === pages.length - 1;\n"
            "            }\n"
            "\n"
            "            prevBtn.addEventListener('click', () => {\n"
            "                if (currentPage > 0) {\n"
            "                    currentPage--;\n"
            "                    showPage(currentPage);\n"
            "                }\n"
            "            });\n"
            "\n"
            "            nextBtn.addEventListener('click', () => {\n"
            "                if (currentPage < pages.length - 1) {\n"
            "                    currentPage++;\n"
            "                    showPage(currentPage);\n"
            "                }\n"
            "            });\n"
            "\n"
            "            document.addEventListener('keydown', (e) => {\n"
            "                if (e.key === 'ArrowLeft') prevBtn.click();\n"
            "                if (e.key === 'ArrowRight') nextBtn.click();\n"
            "            });\n"
            "\n"
            "            showPage(0);\n"
            "        });\n"
            "    </script>\n"
            "</body>\n"
            "</html>"
        )

    def generate_flipbook(
        self,
        image_paths: List[Path],
        output_path: Path,
        title: str = "FlipBook",
        page_width: int = 800,
    ) -> Path:
        """
        Génère le HTML du FlipBook.

        Args:
            image_paths: Liste des chemins des images
            output_path: Chemin de sortie pour le fichier HTML
            title: Titre du FlipBook
            page_width: Largeur maximale des pages en pixels

        Returns:
            Path: Chemin du fichier HTML généré
        """
        try:
            template = self.env.get_template("flipbook.html")

            # Conversion des chemins d'images en URLs relatives
            image_urls = [
                str(path.absolute().relative_to(output_path.parent.absolute()))
                for path in image_paths
            ]

            # Génération du HTML
            html_content = template.render(
                title=title,
                images=image_urls,
                page_width=page_width,
            )

            # Création du dossier de sortie si nécessaire
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Sauvegarde du fichier HTML
            output_path.write_text(html_content, encoding="utf-8")

            logger.info(f"FlipBook généré avec succès : {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur lors de la génération du HTML : {e}")
            raise

    def get_template_list(self) -> List[str]:
        """
        Retourne la liste des templates disponibles.

        Returns:
            List[str]: Liste des noms de templates
        """
        try:
            return [t for t in self.env.list_templates() if t.endswith(".html")]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des templates : {e}")
            return []
