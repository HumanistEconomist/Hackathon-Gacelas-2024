# chatgpt_service.py

import os
import openai
import textwrap
import pdfplumber
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

if not openai_api_key:
    raise ValueError("La API key de OpenAI no se encuentra en las variables de entorno.")

TOKEN_LIMIT = 2048

def extraer_texto_pdf(filepath: str) -> str:
    texto_completo = ""
    with pdfplumber.open(filepath) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo

def dividir_texto(texto: str, limite_tokens: int = TOKEN_LIMIT) -> list:
    return textwrap.wrap(texto, width=limite_tokens//2)

def cargar_libro(pdf_path: str) -> list:
    texto_libro = extraer_texto_pdf(pdf_path)
    texto_fragmentado = dividir_texto(texto_libro)
    return texto_fragmentado

def generar_programa_estudios(csv_path: str, user_data: Dict) -> List[str]:
    # Leer los datos del CSV
    dataC = pd.read_csv(csv_path).to_dict(orient="records")

    # Crear el prompt dinámico para OpenAI
    cursos = [
        "Introducción a las finanzas personales", "Inversión básica",
        "Ahorro e impuestos", "Deuda y crédito", "Planificación financiera",
        "Fondos de inversión", "Seguros", "Inversión avanzada",
        "Criptomonedas", "Pensiones", "Mercados financieros"
    ]
    
    prompt = (
        f"Eres un profesor experto en finanzas personales. Tienes una lista de 11 cursos prehechos "
        f"que puedes utilizar: {', '.join(cursos)}. Además, puedes determinar si se debe hacer contenido extra. "
        f"Con base en las respuestas de usuario guardadas en este CSV: {dataC} y el registro de la base de datos del cliente: {user_data}, "
        f"genera una lista del orden en el que debería estar el programa de estudios para satisfacer las necesidades del cliente. "
        f"Tu respuesta debe ser una lista fácilmente diferenciable."
    )

    # Llamar a la API de OpenAI para obtener el programa de estudios
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=500
    )

    # Extraer la lista generada por OpenAI
    contenido = response['choices'][0]['message']['content']
    lista_estudios = [line.strip() for line in contenido.split('\n') if line.strip()]

    return lista_estudios


def generar_material_educativo(respuestas: list, user_id: str) -> tuple:
    # Generar el prompt basado en las respuestas del usuario
    prompt = "Genera una lista de artículos clave basados en estas respuestas del usuario: " + ", ".join(respuestas)

    # Crear el historial de conversación
    historial_conversacion = [
        {"role": "system", "content": "Eres un experto en finanzas personales y análisis financiero. Tu trabajo es generar artículos que permitan a los lectores aprender sobre finanzas personales. Al ser un profesor experto, sabes estructurar temas y planes de estudio. Los artículos que generes deben tener un resumen ejecutivo, descripciones claras y fórmulas cuando sea necesario. Deben estar adaptados para que una persona promedio pueda entenderlos, pero que abarquen los temas completamente. Intenta que tus respuestas sean claras y directas."},
        {"role": "user", "content": prompt}
    ]

    # Incluir contexto del libro en el mensaje del sistema
    pdf_path = "Investment_Banking_Valuation_LBOs_MA_and_IPOs_by_Joshua_Rosenbaum_Joshua_Pearl.pdf"  # Asegúrate de que esta ruta es correcta
    try:
        fragmentos_libro = cargar_libro(pdf_path)
        if fragmentos_libro:
            contexto_libro = "Utiliza el siguiente contenido como referencia:\n" + fragmentos_libro[0][:2000]
            historial_conversacion.insert(0, {"role": "system", "content": contexto_libro})
    except Exception as e:
        # Manejo de errores al cargar el libro
        print(f"Error al cargar el libro PDF: {e}")
        fragmentos_libro = []
        # Puedes optar por continuar sin el contexto del libro o manejarlo de otra manera

    # Llamar a la API de ChatGPT para generar la lista de artículos
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=historial_conversacion,
            max_tokens=600
        )

        # Extraer el contenido de la respuesta de ChatGPT
        contenido_chatgpt = respuesta['choices'][0]['message']['content']

        # Parsear la lista de artículos
        lista_articulos = parsear_lista_articulos(contenido_chatgpt)

        # Generar contenido para cada artículo
        articulos_generados = []
        for titulo in lista_articulos:
            contenido_articulo = generar_contenido_articulo(titulo, fragmentos_libro)
            articulos_generados.append({
                "titulo": titulo,
                "contenido": contenido_articulo
            })

        # Retornar los artículos generados y el historial de conversación
        return articulos_generados, historial_conversacion

    except Exception as e:
        raise Exception(f"Error al generar el material educativo: {str(e)}")

def parsear_lista_articulos(texto: str) -> list:
    # Convierte el texto recibido en una lista de títulos
    lineas = texto.strip().split('\n')
    titulos = []
    for linea in lineas:
        if linea.strip():
            if '.' in linea:
                titulo = linea.split('.', 1)[1].strip()
            else:
                titulo = linea.strip()
            titulos.append(titulo)
    return titulos

def generar_contenido_articulo(titulo: str, fragmentos_libro: list) -> str:
    # Generar el prompt para el artículo individual
    prompt = f"Escribe un artículo detallado sobre el siguiente tema: '{titulo}'. Utiliza el siguiente contenido como referencia cuando sea relevante:\n\n"
    if fragmentos_libro:
        prompt += fragmentos_libro[0][:2000]  # Usar el primer fragmento del libro como referencia

    # Llamar a la API de ChatGPT para generar el artículo
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto en finanzas personales y análisis financiero. Genera artículos educativos detallados y claros."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        contenido_articulo = respuesta['choices'][0]['message']['content']
        return contenido_articulo

    except Exception as e:
        raise Exception(f"Error al generar el artículo '{titulo}': {str(e)}")

def generar_contenido_curso(nombre: str) -> dict:
    prompt = (
        f"Eres un experto en finanzas personales. Genera un curso completo sobre el tema '{nombre}'. "
        f"Incluye una breve descripción, un nivel de dificultad (Básico, Intermedio, Avanzado), "
        f"y una lista de 3-5 temas con sus explicaciones."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        contenido = response['choices'][0]['message']['content']

        # Simular estructura JSON del contenido generado
        return {
            "nombre": nombre,
            "descripcion": contenido[:100],  # Breve descripción del curso
            "nivel": "Intermedio",  # Asumimos un nivel por defecto
            "temas": [
                {"titulo": "Tema 1", "explicacion": contenido[:100]},
                {"titulo": "Tema 2", "explicacion": contenido[100:200]},
                {"titulo": "Tema 3", "explicacion": contenido[200:300]},
            ]
        }
    except Exception as e:
        raise Exception(f"Error al generar contenido del curso: {str(e)}")