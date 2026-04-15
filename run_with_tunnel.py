#!/usr/bin/env python
"""
Run Flask app with ngrok tunnel for public URL access
"""
import os
import sys
from pyngrok import ngrok
from app import app

def main():
    # Set ngrok auth token (optional, for better features)
    # ngrok.set_auth_token("YOUR_TOKEN_HERE")
    
    print("=" * 60)
    print("🚀 Library Management System - Public Tunnel")
    print("=" * 60)
    
    # Start ngrok tunnel
    print("\n⏳ Starting ngrok tunnel...")
    try:
        # Create tunnel to localhost:5000
        tunnel = ngrok.connect(5000, "http")
        public_url = tunnel.public_url
        
        print(f"\n✅ PUBLIC URL ACTIVE:")
        print(f"   {public_url}")
        print(f"\n📱 Share this URL with others to access your app!")
        print("\n" + "=" * 60)
        print("LOGIN CREDENTIALS:")
        print("=" * 60)
        print("\n👤 Admin Login:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👥 Demo Members (use email as username):")
        print("   📧 selvamagal@library.edu")
        print("   📧 sandhiya@library.edu")
        print("   📧 janikaa.sri@library.edu")
        print("   Password: member123 (for all)")
        print("\n" + "=" * 60)
        print("Press CTRL+C to stop the server")
        print("=" * 60 + "\n")
        
        # Run Flask app
        app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"\n❌ Error starting tunnel: {e}")
        print("\nFailing over to localhost only...")
        print("Running at: http://127.0.0.1:5000")
        app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()
