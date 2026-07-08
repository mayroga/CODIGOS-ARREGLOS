import os
from flask import Flask, request, jsonify, send_from_directory
from google import genai

app = Flask(__name__, static_folder='public', static_url_path='')

# Tomamos la clave de Render y forzamos al cliente a inicializarse con el formato 'AIza'
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
        # Prompt optimizado y modelo ligero para evitar retrasos y congelamientos
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=(
                "Eres un compilador experto. Corrige estrictamente los errores de sintaxis, "
                "comas mal puestas, corchetes, llaves faltantes o problemas de sangría en este código. "
                "Devuelve SOLAMENTE el código completamente corregido y limpio, sin introducciones, "
                f"sin textos explicativos y sin bloques de marcado markdown como ```:\n\n{codigo}"
            )
        )
        
        return jsonify({'codigoCorregido': response.text})
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({'error': 'Error interno al procesar el código o clave inválida.'}), 500

if __name__ == '__main__':
    # Render asigna dinámicamente el puerto, usamos 3000 por defecto en desarrollo local
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
