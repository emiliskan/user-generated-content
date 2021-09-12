import os


UGC_API_HOST = os.getenv("UGC_API_HOST", "localhost")
UGC_API_PORT = os.getenv("UGC_API_PORT", "8000")

API_SERVICE_URL = f"{UGC_API_HOST}:{UGC_API_PORT}"
API = "v1"

USER_ID = "cb17aa66-da6a-452c-8646-fd8d5e9488dc"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "strong_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
