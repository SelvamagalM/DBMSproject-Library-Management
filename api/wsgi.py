#!/usr/bin/env python
"""
This is the main entry point for Vercel.
It should be at the root or in api/ folder.
"""
import os
import sys
from pathlib import Path

# Set environment flag
os.environ['VERCEL'] = '1'

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from app import app
    
    # For Vercel serverless functions
    def handler(request):
        """Vercel serverless handler"""
        with app.test_client() as client:
            # Forward the request to Flask
            response = client.open(
                path=request.path,
                method=request.method,
                data=request.body,
                headers=dict(request.headers)
            )
            return response
    
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback - just return a working app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return '<h1>Welcome to Library Management</h1><a href="/login">Login</a>'
    
    def handler(request):
        with app.test_client() as client:
            response = client.open(
                path=request.path,
                method=request.method,
                data=request.body,
                headers=dict(request.headers)
            )
            return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
