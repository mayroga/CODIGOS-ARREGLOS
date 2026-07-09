import os
from flask import Flask, request, jsonify, send_from_directory, Response
from google import genai

app = Flask(__name__, static_folder='public', static_url_path='')

# Configuración obligatoria para leer tu clave 'AIza' desde el entorno de Render
api_key_env = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key_env)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/corregir', methods=['POST'])
def corregir_codigo():
    data = request.get_json()
    codigo = data.get('codigo')
    if not codigo:
        return jsonify({'error': 'No se proporcionó ningún código.'}), 400
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Corrige estrictamente la sintaxis, comas, llaves y corchetes. Devuelve SOLO el código limpio sin explicaciones ni markdown:\n\n{codigo}"
        )
        return jsonify({'codigoCorregido': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MÓDULO AVANZADO: Generador y sincronizador de 3 archivos en tiempo real
@app.route('/generar_sistema', methods=['POST'])
def generar_sistema():
    data = request.get_json()
    descripcion = data.get('descripcion', '')
    cod1 = data.get('codigo1', '')
    cod2 = data.get('codigo2', '')
    cod3 = data.get('codigo3', '')

    prompt = f"""
    Eres un Ingeniero de Software de Alta Precisión. Tu objetivo es crear o rectificar un sistema basado en esta descripción: "{descripcion}".
    
    Analiza, corrige y relaciona perfectamente estos 3 archivos para que funcionen juntos sin errores de conexión, rutas o sintaxis.
    REGLA ESTRICTA DE PRESERVACIÓN: Si los campos de código ya contienen lógica funcional, respétala intacta, no la elimines. Limítate a conectar las dependencias cruzadas y reparar errores.
    Si los campos están vacíos, genéralos desde cero.
    
    Devuelve los 3 códigos estructurados EXACTAMENTE con este formato divisor para que el frontend pueda separarlos:
    
    ===ARCHIVO1===
    (Escribe aquí el código del Archivo 1 completo corregido)
    ===ARCHIVO2===
    (Escribe aquí el código del Archivo 2 completo corregido)
    ===ARCHIVO3===
    (Escribe aquí el código del Archivo 3 completo corregido)
    ===SUGERENCIAS===
    (Escribe aquí sugerencias de arquitectura, errores encontrados y optimizaciones para el despliegue)
    """

    def generate():
        try:
            # Usamos streaming para enviar fragmentos de texto en vivo y evitar congelamientos por timeout
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=prompt
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error en la transmisión de datos: {str(e)}"

    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
