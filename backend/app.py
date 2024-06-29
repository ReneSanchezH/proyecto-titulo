from flask import Flask, request, jsonify, send_from_directory
import os
from manim import config
from radix_sort_scene import RadixSortScene
from radix_detailed_scene import RadixDetailedScene  # Importar escena detallada
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize
from nltk.data import find

app = Flask(__name__)
CORS(app)

output_dir = os.path.join(os.path.dirname(__file__), 'videos')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Verificar y descargar recursos de nltk si es necesario
try:
    find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def should_generate_detailed_video(prompt):
    detailed_keywords = ["detallado", "detalles", "explicaciones", "explicación"]
    tokens = word_tokenize(prompt.lower())
    return any(word in tokens for word in detailed_keywords)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.json
        numbers_string = data.get('numbers')
        prompt = data.get('prompt')  # Añadir el prompt al payload de la solicitud

        if not numbers_string or not isinstance(numbers_string, str):
            return jsonify({"error": "Invalid input format"}), 400

        # Convert the string of comma-separated numbers to a list of integers
        try:
            numbers = [int(num) for num in numbers_string.split(',')]
            formatted_string = ''.join(numbers_string.split(','))
        except ValueError:
            return jsonify({"error": "Invalid input format"}), 400
        
        output_file = os.path.join(output_dir, f'{formatted_string}.mp4')
        
        config.media_dir = output_dir
        config.output_file = output_file

        if should_generate_detailed_video(prompt):
            class RadixDetailedSceneWrapper(RadixDetailedScene):
                def __init__(self, **kwargs):
                    super().__init__(numbers, **kwargs)
            
            scene = RadixDetailedSceneWrapper()
        else:
            class RadixSortSceneWrapper(RadixSortScene):
                def __init__(self, **kwargs):
                    super().__init__(numbers, **kwargs)
            
            scene = RadixSortSceneWrapper()

        scene.render()
        
        video_url = f'/videos/{formatted_string}.mp4'
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
