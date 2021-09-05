import os

AUTH_HOST = os.getenv("AUTH_HOST", "localhost")
AUTH_PORT = os.getenv("AUTH_PORT", "5000")
UGC_API_HOST = os.getenv("UGC_API_HOST", "localhost")
UGC_API_PORT = os.getenv("UGC_API_PORT", "8000")

API_SERVICE_URL = f"{UGC_API_HOST}:{UGC_API_PORT}"
AUTH_SERVICE_URL = f"{AUTH_HOST}:{AUTH_PORT}"
API = "v1"
