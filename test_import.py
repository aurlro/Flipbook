import sys
import os
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print("\nTrying to list directory contents:")
print(os.listdir('.'))
print("\nTrying to list app directory contents:")
print(os.listdir('./app'))
