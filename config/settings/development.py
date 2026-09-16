from .base import *
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ".onrender.com", "ecotech-nsou.onrender.com"]
#ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://ecotech-nsou.onrender.com",
]
