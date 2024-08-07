from flask import Flask, request, jsonify, send_from_directory
import os
from manim import config
from radix_sort_scene import RadixSort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

output_dir = os.path.join(os.path.dirname(__file__), 'videos')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

        # Generar dinámicamente el video de Radix Sort
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
