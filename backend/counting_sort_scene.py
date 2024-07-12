from manim import *

class CountingSort(Scene):
    def construct(self):
        # Introducción
        self.introduccion()

        # Paso 0
        self.paso0()

        # Paso 1
        self.paso1()

        # Paso 2
        self.paso2()

        # Paso 3 - Iteraciones
        self.paso3_iteraciones()

        # Paso 4
        self.paso4()

    def introduccion(self):
        # Título Inicial
        title = Text("Counting Sort\n").scale(1).to_edge(UP)
        self.add(title)
        self.wait(1)

        # Introducción
        intro = Text(
            "Counting Sort ordena elementos sin comparaciones.\n"
            "Es eficiente con un rango limitado de valores.\n\n"
            "Cuenta la frecuencia de cada elemento y usa esa\n"
            "información para ordenar los elementos.\n"
        ).scale(0.7).next_to(title, DOWN, buff=0.5)
        self.add(intro)
        self.wait(6)
        self.remove(intro)

    def paso0(self):
        self.clear()
        # Texto del paso 0
        step0_text = Text(
            "Vamos a ordenar el siguiente arreglo:"
        ).scale(0.7).to_edge(LEFT).shift(UP)
        self.add(step0_text)
        self.wait(1)

        # Crear y mostrar el array de entrada
        input_array = [2, 5, 3, 0, 2, 3, 0, 3]
        input_array_mob = self.create_array_mobject(input_array, label="inputArray", scale=0.5)
        self.add(input_array_mob)
        self.input_array_mob = input_array_mob  # Guardar la referencia para usarla más tarde
        self.wait(6)
        self.remove(step0_text)

    def paso1(self):
        self.clear()
        # Texto del paso 1
        step1_text = Text(
            "Paso 1: Encontrar el elemento máximo."
        ).scale(0.7).to_edge(LEFT).shift(UP)
        self.add(step1_text)
        self.wait(1)

        # Crear y mostrar el array de entrada
        input_array = [2, 5, 3, 0, 2, 3, 0, 3]
        input_array_mob = self.create_array_mobject(input_array, label="inputArray", scale=0.5)
        self.add(input_array_mob)
        self.input_array_mob = input_array_mob  # Guardar la referencia para usarla más tarde
        self.wait(2)

        # Resaltar el número máximo
        max_value = max(input_array)
        max_index = input_array.index(max_value)
        max_square = input_array_mob[1][max_index][0]
        max_square.set_fill(BLUE, opacity=0.5)

        # Mostrar el valor máximo
        max_label = Text(f"max\n{max_value}", color=GREEN).scale(0.8).next_to(input_array_mob, RIGHT, buff=0.5)
        self.add(max_label)

        self.wait(3)
        self.remove(max_label)
        max_square.set_fill(WHITE, opacity=0)  # Resetear el color del máximo valor

    def paso2(self):
        self.clear()
        # Texto del paso 2
        step2_text = Text(
            "Paso 2: Inicializar countArray[] con ceros."
        ).scale(0.7).to_edge(LEFT).shift(UP)
        self.add(step2_text)
        self.wait(4)
        self.remove(step2_text)

        # Crear y mostrar el countArray
        count_array = [0, 0, 0, 0, 0, 0]
        count_array_mob = self.create_count_array_mobject(count_array, label="countArray", scale=0.7)
        self.add(count_array_mob)
        self.count_array_mob = count_array_mob  # Guardar la referencia para usarla más tarde
        self.wait(3)

    def paso3_iteraciones(self):
        self.clear()
        # Texto del paso 3
        step3_text = Text(
            "Paso 3: Registrar la frecuencia de cada elemento en countArray."
        ).scale(0.7).to_edge(LEFT).shift(UP)
        self.add(step3_text)
        self.wait(3)
        self.remove(step3_text)

        # Mostrar el array de entrada
        input_array = [2, 5, 3, 0, 2, 3, 0, 3]
        input_array_mob = self.create_array_mobject(input_array, label="inputArray", scale=0.5)
        input_array_mob.shift(UP * 1.5)  # Mover hacia arriba
        self.add(input_array_mob)

        # Crear y mostrar el countArray vacío
        count_array = [0, 0, 0, 0, 0, 0]
        count_array_mob = self.create_count_array_mobject(count_array, label="countArray", scale=0.5)
        count_array_mob.shift(DOWN * 1.5)  # Mover hacia abajo
        self.add(count_array_mob)

        self.wait(2)

        # Mostrar las iteraciones del llenado del countArray
        self.animate_count_array(input_array, count_array, count_array_mob, input_array_mob)

    
    def paso4(self):
        self.clear()
        # Texto del paso 4
        step4_text = Text(
        "Paso 4: Calcular sumas acumuladas en countArray.\n"
        "Realizamos countArray[i] = countArray[i-1] + countArray[i]."
        ).scale(0.7).to_edge(LEFT).shift(UP)
        self.add(step4_text)
        self.wait(3)
        self.remove(step4_text)

        # Mostrar el countArray inicial
        initial_count_array = [2, 0, 2, 3, 0, 1]
        count_array_mob = self.create_count_array_mobject(initial_count_array, label="countArray", scale=0.5)
        count_array_mob.shift(UP * 1.5)  # Mover hacia arriba
        self.add(count_array_mob)

        self.wait(2)

        # Calcular y mostrar las sumas acumuladas
        cumulative_count_array = initial_count_array[:]
        for i in range(1, len(cumulative_count_array)):
            cumulative_count_array[i] += cumulative_count_array[i - 1]

        cumulative_count_array_mob = self.create_count_array_mobject(cumulative_count_array, label="countArray", scale=0.5)
        cumulative_count_array_mob.shift(UP * 1.5)  # Mover hacia arriba
        self.play(Transform(count_array_mob, cumulative_count_array_mob))

        self.wait(3)





    def create_array_mobject(self, array, label="", scale=1):
        array_mob = VGroup()
        
        for i, val in enumerate(array):
            square = Square().scale(scale)
            square.set_fill(WHITE, opacity=0)
            square_label = Text(str(val)).scale(scale).move_to(square.get_center())
            square_group = VGroup(square, square_label)
            array_mob.add(square_group)
        
        array_mob.arrange(RIGHT, buff=0.1)

        if label:
            array_label = Text(label).scale(scale).next_to(array_mob, LEFT, buff=0.5)
            array_mob = VGroup(array_label, array_mob).arrange(RIGHT, buff=0.5)

        return array_mob

    def create_count_array_mobject(self, array, label="", scale=1):
        count_array_mob = VGroup()
        
        for i, val in enumerate(array):
            square = Square().scale(scale)
            square.set_fill(WHITE, opacity=0)
            square_label = Text(str(val)).scale(scale).move_to(square.get_center())
            square_group = VGroup(square, square_label)
            
            # Etiquetas encima del array, colocadas más arriba
            index_label = Text(str(i)).scale(scale * 1.2).move_to(square.get_center() + UP * 0.9)
            count_array_mob.add(VGroup(index_label, square_group))
        
        count_array_mob.arrange(RIGHT, buff=0.1)

        if label:
            array_label = Text(label).scale(scale).next_to(count_array_mob, LEFT, buff=0.5)
            count_array_mob = VGroup(array_label, count_array_mob).arrange(RIGHT, buff=0.5)

        return count_array_mob

    def animate_count_array(self, input_array, count_array, count_array_mob, input_array_mob):
        # Iterar a través del input_array y actualizar count_array
        for i, val in enumerate(input_array):
            self.wait(0.5)
            count_array[val] += 1

            # Resaltar la celda actual en input_array
            input_square = input_array_mob[1][i][0]
            input_square.set_fill(YELLOW, opacity=0.5)

            # Actualizar el countArray completo
            updated_count_array_mob = self.create_count_array_mobject(count_array, label="countArray", scale=0.5)
            updated_count_array_mob.shift(DOWN * 1.5)  # Mover hacia abajo como el original
            self.play(Transform(count_array_mob, updated_count_array_mob))

            self.wait(0.5)
            input_square.set_fill(WHITE, opacity=0)

        self.wait(3)

# Ejecuta la escena
if __name__ == "__main__":
    scene = CountingSort()
    scene.render()
