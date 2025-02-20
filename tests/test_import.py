import sys
import os
import unittest

class TestEnvironment(unittest.TestCase):

    def test_current_working_directory(self):
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        self.assertTrue(os.path.isdir(cwd), "Current working directory does not exist")

    def test_python_path(self):
        python_path = sys.path
        print(f"Python path: {python_path}")
        self.assertIsInstance(python_path, list, "Python path is not a list")
        self.assertGreater(len(python_path), 0, "Python path is empty")

    def test_list_directory_contents(self):
        contents = os.listdir('.')
        print("\nTrying to list directory contents:")
        print(contents)
        self.assertIsInstance(contents, list, "Directory contents is not a list")
        self.assertGreater(len(contents), 0, "Directory contents is empty")

    def test_list_app_directory_contents(self):
        app_dir = './app'
        self.assertTrue(os.path.isdir(app_dir), "App directory does not exist")
        contents = os.listdir(app_dir)
        print("\nTrying to list app directory contents:")
        print(contents)
        self.assertIsInstance(contents, list, "App directory contents is not a list")
        self.assertGreater(len(contents), 0, "App directory contents is empty")

if __name__ == '__main__':
    unittest.main()
