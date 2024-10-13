# firebase_config.py

import firebase_admin
from firebase_admin import firestore
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde .env
load_dotenv()

# Leer el ID del proyecto desde las variables de entorno
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

def iniciar_firebase():
    # Inicializar Firebase solo si no está ya inicializado
    if not firebase_admin._apps:
        firebase_admin.initialize_app(options={"projectId": project_id})
    return firestore.client()

