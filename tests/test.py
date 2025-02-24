import unittest
from pathlib import Path

from flipbook.core import FlipbookRenderer


class TestFlipbook(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.renderer = FlipbookRenderer()

        # Créer un fichier de test temporaire
        self.test_image_path = "test_image.jpg"
        Path(self.test_image_path).touch()

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Supprimer le fichier de test
        if Path(self.test_image_path).exists():
            Path(self.test_image_path).unlink()

    def test_page_loading(self):
        """Test du chargement d'une page"""
        result = self.renderer.load_page(self.test_image_path)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.image)

    def test_page_loading_nonexistent_file(self):
        """Test du chargement d'un fichier inexistant"""
        result = self.renderer.load_page("nonexistent.jpg")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_page_transition(self):
        """Test de la création d'une transition"""
        transition = self.renderer.create_transition(
            from_page=1, to_page=2, duration=800
        )
        self.assertEqual(transition.duration, 800)
        self.assertTrue(transition.is_valid())

    def test_invalid_transition_duration(self):
        """Test d'une transition avec durée invalide"""
        transition = self.renderer.create_transition(
            from_page=1, to_page=2, duration=-1
        )
        self.assertFalse(transition.is_valid())


if __name__ == "__main__":
    unittest.main()
