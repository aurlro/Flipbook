def test_imports():
    imports = {
        'Flask': 'flask',
        'Flask-WTF': 'flask_wtf',
        'Pillow': 'PIL',
        'PyPDF2': 'PyPDF2',
        'python-dotenv': 'dotenv',
        'pytest': 'pytest'
    }

<<<<<<< HEAD

class TestEnvironment(unittest.TestCase):
=======
    results = []
    for name, module in imports.items():
        try:
            __import__(module)
            results.append(f"✅ {name} importé avec succès")
        except ImportError as e:
            results.append(f"❌ {name} NON importé : {str(e)}")
>>>>>>> ba066e810d1d85ad7cf37c29561aa5b4baee6d02

    return results

<<<<<<< HEAD
    def test_python_path(self):
        python_path = sys.path
        print(f"Python path: {python_path}")
        self.assertIsInstance(python_path, list, "Python path is not a list")
        self.assertGreater(len(python_path), 0, "Python path is empty")

    def test_list_directory_contents(self):
        contents = os.listdir(".")
        print("\nTrying to list directory contents:")
        print(contents)
        self.assertIsInstance(contents, list, "Directory contents is not a list")
        self.assertGreater(len(contents), 0, "Directory contents is empty")

    def test_list_app_directory_contents(self):
        app_dir = "./app"
        self.assertTrue(os.path.isdir(app_dir), "App directory does not exist")
        contents = os.listdir(app_dir)
        print("\nTrying to list app directory contents:")
        print(contents)
        self.assertIsInstance(contents, list, "App directory contents is not a list")
        self.assertGreater(len(contents), 0, "App directory contents is empty")


if __name__ == "__main__":
    unittest.main()
=======
if __name__ == "__main__":
    print("Test des imports:")
    for result in test_imports():
        print(result)
>>>>>>> ba066e810d1d85ad7cf37c29561aa5b4baee6d02
