import sys
import os

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    print("Attempting to import app as module...")
    import app

    print("Successfully imported app")
    print(f"app.__file__: {app.__file__}")
except Exception as e:
    print(f"Failed to import app: {e}")
