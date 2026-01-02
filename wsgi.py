import sys
import os

# Add the project directory to the Python path
path = '/home/yourusername/pro'  # Change 'yourusername' to your PythonAnywhere username
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application

if __name__ == "__main__":
    application.run()

