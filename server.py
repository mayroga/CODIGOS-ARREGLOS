import os
from flask import Flask, request, jsonify, send_from_directory, Response
from google import genai

app = Flask(__name__, static_folder='public', static_url_path='')

# Inicialización obligatoria para tu clave 'AIza'
api_key_env = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key_env)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# MÓDULO 1: CREAR APLICACIONES DESDE CERO
@app.route('/crear_app', methods=['POST'])
def crear_app():
    data = request.get_json()
    descripcion = data.get('descripcion', '')
    
    prompt = f"""
    Eres un Ingeniero de Software Senior. Crea una aplicación completa desde cero basada en esta descripción: "{descripcion}".
    Genera una arquitectura limpia, moderna y funcional dividida en 3 archivos independientes.
    
    Devuelve los códigos estructurados EXACTAMENTE con este formato divisor:
    ===ARCHIVO1===
    (Código del Servidor/Backend completo)
    ===ARCHIVO2===
    (Código de la Interfaz/HTML completo)
    ===ARCHIVO3===
    (Código de la Lógica/JS o Estilos/CSS completo)
    ===SUGERENCIAS===
    (Explicación paso a paso de cómo guardarlo, qué librerías instalar y cómo desplegarlo)
    """
    return Response(generar_stream(prompt), mimetype='text/plain')

# MÓDULO 2: REVISIÓN DE APLICACIONES Y CÓDIGOS (ANÁLISIS)
@app.route('/revisar_app', methods=['POST'])
def revisar_app():
    data = request.get_json()
    desc = data.get('descripcion', '')
    c1 = data.get('codigo1', '')
    c2 = data.get('codigo2', '')
    c3 = data.get('codigo3', '')
    
    prompt = f"""
    Eres un Arquitecto de Software. Realiza una auditoría y revisión profunda de estos códigos basados en el objetivo: "{desc}".
    Analiza la lógica, la seguridad, la eficiencia de memoria y cómo se relacionan entre sí.
    
    Deja los paneles de código intactos, pero genera un reporte exhaustivo en la sección de sugerencias.
    
    Devuelve la respuesta con este formato estricto:
    ===ARCHIVO1===
    {c1}
    ===ARCHIVO2===
    {c2}
    ===ARCHIVO3===
    {c3}
    ===SUGERENCIAS===
    ### REPORTE DE REVISIÓN TÉCNICA
    - Errores de lógica encontrados:
    - Cuellos de botella o consumo excesivo de memoria:
    - Fallas de conexión detectadas entre archivos:
    - Recomendaciones de mejora:
    """
    return Response(generar_stream(prompt), mimetype='text/plain')

# MÓDULO 3: CORRECCIÓN DE CÓDIGOS (SINTAXIS, COMAS, CORCHETES)
@app.route('/corregir_app', methods=['POST'])
def corregir_app():
    data = request.get_json()
    desc = data.get('descripcion', '')
    c1 = data.get('codigo1', '')
    c2 = data.get('codigo2', '')
    c3 = data.get('codigo3', '')
    
    prompt = f"""
    Eres un Compilador Automatizado de Alta Precisión. Tu única tarea es reparar errores mecánicos: sintaxis rota, comas mal puestas, corchetes o llaves faltantes, y mala sangría en los 3 códigos provistos, asegurando que queden vinculados correctamente según la descripción: "{desc}".
    PRESERVA TODA LA LÓGICA FUNCIONAL QUE YA SIRVE. No elimines código útil.
    
    Devuelve los códigos completamente corregidos y limpios con este formato divisor:
    ===ARCHIVO1===
    (Código 1 corregido sin errores)
    ===ARCHIVO2===
    (Código 2 corregido sin errores)
    ===ARCHIVO3===
    (Código 3 corregido sin errores)
    ===SUGERENCIAS===
    ✓ Todos los errores de sintaxis, comas y corchetes han sido rectificados con éxito. Los archivos están limpios y listos.
    """
    return Response(generar_stream(prompt), mimetype='text/plain')

def generar_stream(prompt):
    try:
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt
        )
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"===SUGERENCIAS===\nError de conexión con la IA: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
