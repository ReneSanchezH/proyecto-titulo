from flask import Flask, request, jsonify, send_from_directory
import os
from manim import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Asegúrate de que la carpeta `public` exista
output_dir = os.path.join(os.path.dirname(__file__), '../public')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class SortScene(Scene):
    def __init__(self, numbers, **kwargs):
        self.numbers = numbers
        super().__init__(**kwargs)

    def construct(self):
        title = Text("Radix Sort Visualization").to_edge(UP)
        self.play(Write(title))

        array_mobjects = VGroup(*[Square().set_fill(BLUE, opacity=0.5).set_stroke(BLUE_E, width=1).scale(0.7) for _ in self.numbers])
        array_mobjects.arrange(RIGHT, buff=0.1)
        array_mobjects.to_edge(DOWN)

        number_mobjects = VGroup(*[Text(str(num)).move_to(square) for num, square in zip(self.numbers, array_mobjects)])

        self.play(Write(array_mobjects))
        self.play(Write(number_mobjects))
        self.wait(2)
        
        # Simulación de radix sort para la visualización
        self.radix_sort(array_mobjects, number_mobjects)
        
    def radix_sort(self, array_mobjects, number_mobjects):
        # Implementa tu lógica de Radix Sort aquí y usa self.play() para animar los pasos
        pass

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    numbers = data['numbers']
    
    # Especifica la ruta de salida
    output_file = os.path.join(output_dir, 'sort_video.mp4')
    
    config.media_dir = output_dir
    config.output_file = output_file

    scene = SortScene(numbers)
    scene.render()
    
    # Devolver la URL del video generado
    video_url = '/public/sort_video.mp4'
    return jsonify({"message": "Video generated successfully!", "video_url": video_url})

# Endpoint para servir el video
@app.route('/public/<path:filename>', methods=['GET'])
def serve_video(filename):
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
