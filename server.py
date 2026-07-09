import os
from flask import Flask, request, jsonify, send_from_directory, Response
from google import genai

app = Flask(__name__, static_folder='public', static_url_path='')

# Inicialización segura para la API Key de formato 'AIza'
api_key_env = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key_env)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# HELPER: Une los archivos que envía el cliente para pasárselos como un bloque a la IA
def empaquetar_contexto(data):
    descripcion = data.get('descripcion', '')
    contexto = f"OBJETIVO / DESCRIPCIÓN DEL SISTEMA:\n{descripcion}\n\n"
    contexto += "=== ARCHIVOS ACTUALES ===\n"
    for i in range(1, 6):
        nombre = data.get(f'nombre{i}', f'Archivo_{i}').strip()
        contenido = data.get(f'codigo{i}', '').strip()
        if nombre or contenido:
            contexto += f"[{nombre if nombre else f'Archivo_{i}'}]\n{contenido}\n\n"
    return contexto

# MÓDULO 1: CREAR APLICACIONES (Generación Totalmente Relacionada)
@app.route('/crear_app', methods=['POST'])
def crear_app():
    contexto_usuario = empaquetar_contexto(request.get_json())
    prompt = f"""
    Eres un Arquitecto de Software Senior y Maestro de Codificación. Tu tarea es CREAR el sistema o los códigos solicitados.
    
    INSTRUCCIONES DE ALTA PRECISIÓN:
    1. Diseña un sistema donde todos los archivos estén milimétricamente ALINEADOS y RELACIONADOS entre sí (por ejemplo, que las rutas del backend coincidan con los fetch del frontend, y las clases CSS con el HTML).
    2. Genera los códigos completos, funcionales, optimizados para RAM y sin errores.
    
    Devuelve la respuesta estructurando CADA archivo de forma secuencial usando EXACTAMENTE este formato divisor de inicio y fin para que la interfaz los procese:
    
    :::INICIO_ARCHIVO:::Nombre_Del_Archivo.extension
    (Escribe aquí el código completo y real del archivo, sin usar marcadores markdown como ```)
    :::FIN_ARCHIVO:::
    
    Puedes generar hasta 5 archivos si el sistema lo requiere. Al final del flujo, añade obligatoriamente esta sección:
    :::INICIO_SUGERENCIAS:::
    (Escribe aquí la explicación paso a paso del proceso, dónde buscar errores, qué herramientas coger, qué evitar y cómo desplegar el sistema completo con éxito)
    :::FIN_SUGERENCIAS:::
    """ + contexto_usuario

    return Response(generar_stream(prompt), mimetype='text/plain')

# MÓDULO 2: REVISIÓN DE APLICACIONES (Auditoría Estructural)
@app.route('/revisar_app', methods=['POST'])
def revisar_app():
    contexto_usuario = empaquetar_contexto(request.get_json())
    prompt = f"""
    Eres un Auditor de Seguridad y Optimización de Código. Tu tarea es analizar de forma crítica los códigos provistos por el usuario.
    
    INSTRUCCIONES DE AUDITORÍA:
    1. Revisa cómo se relacionan los archivos entre sí y detecta fallas de conexión, llaves/corchetes rotos, código cortado o cuellos de botella en servidores como Render.
    2. Mantén los archivos del usuario intactos, pero genera una corrección y alineación optimizada de los mismos dentro del reporte si detectas fallas.
    
    Devuelve el resultado con este formato estricto:
    :::INICIO_SUGERENCIAS:::
    ### REPORTE DE INGENIERÍA DE ALTA PRECISIÓN
    
    1. ANÁLISIS DE ERRORES DETECTADOS:
    (Indica qué comas, corchetes, variables o conexiones estaban fallando)
    
    2. CÓDIGOS CORREGIDOS Y ALINEADOS:
    (Escribe aquí los bloques de código ya rectificados y acoplados perfectamente para que funcionen juntos)
    
    3. GUÍA MAESTRA DE DESPLIEGUE:
    (Explicación detallada de procesos, qué parámetros configurar y cómo operarlo sin sobrecargar memoria)
    :::FIN_SUGERENCIAS:::
    """ + contexto_usuario

    return Response(generar_stream(prompt), mimetype='text/plain')

# MÓDULO 3: CORRECCIÓN DE CÓDIGOS EXPRESS (Corrector Mecánico Profesional - NO INVENTAR LOGICA)
@app.route('/corregir_app', methods=['POST'])
def corregir_app():
    contexto_usuario = empaquetar_contexto(request.get_json())
    prompt = f"""
    Eres un Compilador y Corrector Mecánico Ultra-Preciso. Tu única misión es REPARAR y RECTIFICAR errores mecánicos del código.
    
    REGLAS DE PROTECCIÓN Y CONTROL:
    1. REGLA DE NO INVENCIÓN: Está estrictamente PROHIBIDO inventar lógica nueva, crear características que el usuario no pidió o alterar el funcionamiento de los códigos provistos.
    2. REGLA DE REPARACIÓN: Repara errores de sintaxis, comas duplicadas, corchetes, llaves faltantes, bloques cortados o mal estructurados. Asegura que los archivos mantengan su relación intacta.
    3. Si el código no tiene errores, devuélvelo exactamente igual pero limpio y formateado de forma legible.
    
    Devuelve CADA archivo corregido utilizando estrictamente este formato divisor:
    
    :::INICIO_ARCHIVO:::Nombre_Del_Archivo.extension
    (Código original formateado, corregido mecánicamente y libre de fallas de sintaxis, sin markdown)
    :::FIN_ARCHIVO:::
    
    :::INICIO_SUGERENCIAS:::
    ✓ Corrección Profesional Exitosa. Se rectificaron los errores mecánicos de sintaxis y acoplamiento sin alterar la lógica de la aplicación.
    :::FIN_SUGERENCIAS:::
    """ + contexto_usuario

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
        yield f":::INICIO_SUGERENCIAS:::\nError de comunicación con el motor de IA en Render: {str(e)}\n:::FIN_SUGERENCIAS:::"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
