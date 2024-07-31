from flask import Flask, request, jsonify, send_from_directory
import os
from manim import config
from radix_sort_scene import RadixSort
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)

output_dir = os.path.join(os.path.dirname(__file__), 'videos')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Cargar el modelo de lenguaje de spaCy
nlp = spacy.load("en_core_web_sm")

def should_generate_detailed_video(prompt):
    detailed_keywords = [
        "detallado", "detalles", "explicaciones", "explicación", "analítico", "minucioso", "paso a paso", 
        "detalladamente", "explicación completa", "en profundidad", "descripción detallada", "en detalle", 
        "con detalle", "explicación exhaustiva", "detallada explicación", "en detalle", "paso por paso", 
        "detallada", "completamente", "explicaciones detalladas", "descripción en detalle", "información completa", 
        "desglose detallado"
    ]
    doc = nlp(prompt.lower())
    return any(token.text in detailed_keywords for token in doc)

def should_generate_counting_sort_video(prompt):
    counting_sort_keywords = [
        "counting sort", "ordenación por conteo", "ordenación de conteo", "ordenamiento por conteo",
        "ordenamiento de conteo", "sort counting", "conteo", "ordenar por conteo", "sort de conteo",
        "sort conteo", "explicación counting sort", "detalles de counting sort", "cómo funciona counting sort",
        "algoritmo counting sort", "counting sort paso a paso", "ordenar por conteo", "sort de conteo", 
        "counting sort explicado", "counting sort detallado", "contar y ordenar", "explicación de counting sort",
        "ordenación por contaje", "ordenar mediante conteo", "sort basado en conteo", "explicación exhaustiva counting sort"
    ]
    doc = nlp(prompt.lower())
    return any(token.text in counting_sort_keywords for token in doc)

def should_generate_bucket_sort_video(prompt):
    bucket_sort_keywords = [
        "bucket sort", "ordenación por cubetas", "ordenación de cubetas", "ordenamiento por cubetas",
        "ordenamiento de cubetas", "sort bucket", "cubetas", "ordenar por cubetas", "sort de cubetas",
        "sort cubetas", "explicación bucket sort", "detalles de bucket sort", "cómo funciona bucket sort",
        "algoritmo bucket sort", "bucket sort paso a paso", "ordenar por cubetas", "sort de cubetas",
        "bucket sort explicado", "bucket sort detallado", "cubetas de ordenamiento", "explicación de bucket sort",
        "ordenación mediante cubetas", "bucket sort detalladamente"
    ]
    doc = nlp(prompt.lower())
    return any(token.text in bucket_sort_keywords for token in doc)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.json
        numbers_string = data.get('numbers')
        prompt = data.get('prompt')
        print("prompt", prompt)
        print("numbers_string", numbers_string)

        if not numbers_string or not isinstance(numbers_string, str):
            return jsonify({"error": "Invalid input format"}), 400

        # Convertir la cadena de números en una lista de enteros
        try:
            numbers = [int(num) for num in numbers_string.split(',')]
            formatted_string = ''.join(numbers_string.split(','))
        except ValueError:
            return jsonify({"error": "Invalid input format"}), 400

        config.media_dir = output_dir

        # Definir rutas de salida para cada tipo de video
        detailed_output_file = os.path.join(output_dir, 'radix_detailed.mp4')
        counting_sort_output_file = os.path.join(output_dir, 'counting_sort.mp4')
        bucket_sort_output_file = os.path.join(output_dir, 'bucket.mp4')
        dynamic_output_file = os.path.join(output_dir, f'radix_sort_{formatted_string}.mp4')

        # Verificar si se debe usar un video estático
        if should_generate_detailed_video(prompt):
            video_url = '/videos/radix_detailed.mp4'
        elif should_generate_counting_sort_video(prompt):
            video_url = '/videos/counting_sort.mp4'
        elif should_generate_bucket_sort_video(prompt):
            video_url = '/videos/bucket.mp4'
        else:
            # Generar dinámicamente el video de Radix Sort si no se encontraron palabras clave estáticas
            if not os.path.exists(dynamic_output_file):
                class RadixSortSceneWrapper(RadixSort):
                    def __init__(self, **kwargs):
                        super().__init__(numbers, **kwargs)
                scene = RadixSortSceneWrapper()
                scene.render()
                # Renombrar el archivo generado a dynamic_output_file
                os.rename(
                    os.path.join(output_dir, 'videos/1080p60/RadixSortSceneWrapper.mp4'),
                    dynamic_output_file
                )
            video_url = f'/videos/radix_sort_{formatted_string}.mp4'

        return jsonify({"message": "Video generated successfully!", "video_url": video_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/videos/<path:filename>', methods=['GET'])
def serve_video(filename):
    try:
        return send_from_directory(output_dir, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
