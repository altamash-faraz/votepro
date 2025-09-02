#!/usr/bin/env python3
"""
Generate a secure secret key for Flask application
Run this and copy the output to your Render environment variables
"""
import secrets

print("🔐 Secure Secret Key for Flask:")
print("Copy this to your Render Environment Variables as SECRET_KEY:")
print()
print(secrets.token_urlsafe(32))
print()
print("📝 This key is cryptographically secure and should be kept secret!")
