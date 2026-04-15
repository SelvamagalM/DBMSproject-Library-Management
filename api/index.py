import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

# Export the Flask app for Vercel
# Vercel looks for 'app' or a WSGI callable
__all__ = ['app']
