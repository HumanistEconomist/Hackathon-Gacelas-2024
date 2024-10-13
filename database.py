# database.py

from firebase_config import iniciar_firebase

db = iniciar_firebase()

def guardar_usuario(user_id: str, nombre: str, apellido: str, edad: int):
    user_data = {
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad
    }
    db.collection("usuarios").document(user_id).set(user_data)

def obtener_usuario(user_id: str) -> dict:
    doc = db.collection("usuarios").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {}

def guardar_historial(user_id: str, historial: list):
    db.collection("historial_conversaciones").document(user_id).set({
        "historial": historial
    })

def obtener_historial(user_id: str) -> list:
    doc = db.collection("historial_conversaciones").document(user_id).get()
    if doc.exists:
        return doc.to_dict().get("historial", [])
    else:
        return []

def guardar_articulos(user_id: str, articulos: list):
    db.collection("articulos").document(user_id).set({
        "articulos": articulos
    })

def obtener_articulos(user_id: str) -> list:
    doc = db.collection("articulos").document(user_id).get()
    if doc.exists:
        return doc.to_dict().get("articulos", [])
    else:
        return []


