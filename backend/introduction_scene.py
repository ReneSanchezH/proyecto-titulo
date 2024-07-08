from manim import *

class IntroductionScene(Scene):
    def construct(self):
        # Título Inicial
        title = Text("Radix Sort\n").scale(1).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Definición clara del algoritmo
        definition = Text(
            "Radix Sort es un algoritmo de ordenamiento no comparativo\n"
            "que ordena los números procesando dígitos individuales.\n\n"
            "A diferencia de otros algoritmos, no compara los elementos entre sí,\n"
            "sino que los agrupa en función de cada dígito, de menos significativo\n"
            "a más significativo (o viceversa). Esto lo hace especialmente útil\n"
            "para ordenar grandes conjuntos de datos numéricos de manera eficiente.\n\n"
            "Se usa comúnmente en aplicaciones como la ordenación de enteros,\n"
            "la clasificación de cadenas y la distribución de claves en bases de datos."
        ).scale(0.6).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(definition))
        self.wait(6)

        # Desvanecer el título y la definición
        self.play(FadeOut(title), FadeOut(definition))

        # Esperar un poco antes de mostrar el nuevo título
        self.wait(0.5)

        # Variedades del Radix Sort
        varieties_title = Text("Variedades del Radix Sort\n").scale(0.7).to_edge(UP)
        lsd_text = Text(
            "LSD (Least Significant Digit):\n"
            "Ordena los números empezando por el dígito menos significativo\n"
            "(el de más a la derecha) y avanza hacia la izquierda."
        ).scale(0.6).next_to(varieties_title, DOWN, buff=0.6)
        msd_text = Text(
            "MSD (Most Significant Digit):\n"
            "Ordena los números empezando por el dígito más significativo\n"
            "(el de más a la izquierda) y avanza hacia la derecha."
        ).scale(0.6).next_to(lsd_text, DOWN, buff=0.5).align_to(lsd_text, LEFT)

        self.add(varieties_title)
        self.play(FadeIn(lsd_text), FadeIn(msd_text))
        self.wait(4)
        self.play(FadeOut(varieties_title), FadeOut(lsd_text), FadeOut(msd_text))
