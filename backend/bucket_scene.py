from manim import *

class Bucket(Scene):
    def construct(self):

        title = Text("Uso de Buckets en Radix Sort").scale(0.9).to_edge(UP)
        self.add(title)

        initial_text = Text(
            "El algoritmo Radix usa 'buckets' (contenedores temporales)\n"
            "para ordenar números del 0 al 9."
        ).scale(0.75).move_to(ORIGIN)
        self.add(initial_text)
        self.wait(6)
        self.remove(initial_text)

        # Primer texto
        first_text = Text(
            "Radix Sort ordena números por dígitos,\n"
            "usando 'buckets' para agrupar cada dígito.\n\n"
            "No compara números directamente, solo usa los dígitos."
        ).scale(0.7).move_to(ORIGIN)
        self.add(first_text)
        self.wait(5)
        self.remove(first_text)
        self.remove(title)

        # Segundo texto
        second_text = Text("Radix Sort usa dos métodos:\nLSD y MSD\n").scale(0.84).to_edge(UP)
        lsd_text = Text(
            "LSD: Empieza por el dígito menos significativo\n(el de la derecha)."
        ).scale(0.7).move_to(ORIGIN)
        self.add((second_text))
        self.add(lsd_text)
        self.wait(4)
        self.remove(lsd_text)

        # Tercer texto
        third_text = Text(
            "MSD: Empieza por el dígito más significativo\n(el de la izquierda)."
        ).scale(0.7).move_to(ORIGIN)
        self.add(third_text)
        self.wait(4)
        self.remove(third_text, second_text)

        # Cuarto texto
        fourth_text = Text(
            "Vamos a ver cómo funcionan los 'buckets'.\n"
            "Los números se guardan temporalmente en estos contenedores.\n\n"
            "Ejemplo: El número 816 se moverá a sus 'buckets' correspondientes,\n"
            "empezando por el dígito menos significativo (el de la derecha)."
        ).scale(0.65).move_to(ORIGIN)
        self.add(fourth_text)
        self.wait(8)
        self.remove(fourth_text)

        title = Text("Uso de buckets").to_edge(UP)
        self.play(Write(title))
        
        # Número a ordenar
        number = Text("816")
        number.next_to(title, DOWN, buff=1)
        self.play(Write(number))
        
        # Buckets
        buckets = VGroup(
            Square().set_height(1).move_to(2 * LEFT + 2 * DOWN),
            Square().set_height(1).move_to(0 * LEFT + 2 * DOWN),
            Square().set_height(1).move_to(2 * RIGHT + 2 * DOWN),
        )
        bucket_labels = VGroup(
            Text("6").next_to(buckets[0], DOWN),
            Text("8").next_to(buckets[1], DOWN),
            Text("1").next_to(buckets[2], DOWN),
        )
        
        self.play(LaggedStart(*[Create(bucket) for bucket in buckets], lag_ratio=0.5))
        self.play(LaggedStart(*[Write(label) for label in bucket_labels], lag_ratio=0.5))
        
        # Explicación de cada dígito
        digits = [("unidades", "6", buckets[0]), ("decenas", "1", buckets[2]), ("centenas", "8", buckets[1])]
        
        for place, digit, bucket in digits:
            digit_text = Text(f"Dígito en {place}: {digit}").scale(0.72).move_to(UP)
            self.play(Write(digit_text))

            digit_highlight = SurroundingRectangle(number, color=YELLOW)
            bucket_highlight = SurroundingRectangle(bucket, color=YELLOW)
            self.play(Create(digit_highlight), Create(bucket_highlight))
            
            self.play(number.animate.move_to(bucket.get_center()))
            
            self.play(FadeOut(digit_highlight), FadeOut(bucket_highlight), FadeOut(digit_text))

        self.wait(2)
