from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RenderResult:
    """Résultat du rendu d'une page."""

    success: bool
    image: Optional[str] = None
    error: Optional[str] = None


class FlipbookRenderer:
    """Classe principale pour le rendu du flipbook."""

    def __init__(self):
        self.pages = []
        self.current_page = 0

    def load_page(self, image_path: str) -> RenderResult:
        """Charge une page d'image dans le flipbook.

        Args:
            image_path: Chemin vers l'image à charger.

        Returns:
            RenderResult: Résultat du chargement avec statut et données.
        """
        try:
            # Vérifier si le fichier existe
            if not Path(image_path).exists():
                return RenderResult(
                    success=False,
                    error=f"Le fichier {image_path} n'existe pas",
                )

            # TODO: Ajouter la logique de chargement d'image
            # Pour l'instant, on simule juste le succès
            self.pages.append(image_path)
            return RenderResult(success=True, image=image_path)

        except Exception as e:
            return RenderResult(success=False, error=str(e))

    def create_transition(
        self, from_page: int, to_page: int, duration: int = 800
    ) -> "TransitionEffect":
        """Crée un effet de transition entre deux pages.

        Args:
            from_page: Index de la page de départ.
            to_page: Index de la page d'arrivée.
            duration: Durée de la transition en ms (défaut: 800).

        Returns:
            TransitionEffect: Objet contenant les paramètres.
        """
        return TransitionEffect(
            from_page=from_page, to_page=to_page, duration=duration
        )


@dataclass
class TransitionEffect:
    """Classe représentant un effet de transition entre pages."""

    from_page: int
    to_page: int
    duration: int

    def is_valid(self) -> bool:
        """Vérifie si la transition est valide."""
        return (
            isinstance(self.from_page, int)
            and isinstance(self.to_page, int)
            and self.duration > 0
        )
