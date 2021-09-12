import os

UGA_API_HOST = os.getenv("UGA_API_HOST", "localhost")
UGA_API_PORT = os.getenv("UGA_API_PORT", "8000")

API_SERVICE_URL = f"{UGA_API_HOST}:{UGA_API_PORT}"
API = "v1"

USER_ID = "cb17aa66-da6a-452c-8646-fd8d5e9488dc"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "strong_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
