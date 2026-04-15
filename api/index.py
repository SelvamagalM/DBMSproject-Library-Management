import sys
import os

# Mark that we're running on Vercel serverless
os.environ['VERCEL'] = '1'

# Import the Flask app
from app import app

# Export the Flask app for Vercel
__all__ = ['app']
