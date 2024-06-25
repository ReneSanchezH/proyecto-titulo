from manim import *

class RadixSortScene(Scene):
    def __init__(self, integer_array, **kwargs):
        self.integer_array = integer_array
        super().__init__(**kwargs)

    def construct(self):
        # Definir el arreglo de enteros a partir del parámetro pasado
        integer_array = self.integer_array

        # Convertir los enteros a cadenas para mostrarlos en la tabla
        string_array = [str(num) for num in integer_array]

        # Crear la tabla inicial en horizontal
        table = Table(
            [string_array],
            include_outer_lines=True
        )

        # Ajustar la escala de la tabla para que quepa en la escena
        table.scale(0.8)

        # Animar la aparición de la tabla
        self.play(Create(table))
        self.wait(1)

        # Radix Sort
        def counting_sort(arr, exp):
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            # Contar ocurrencias de los dígitos
            for i in range(n):
                index = (arr[i] // exp) % 10
                count[index] += 1

            # Cambiar count[i] para que contenga posiciones finales
            for i in range(1, 10):
                count[i] += count[i - 1]

            # Construir el arreglo ordenado
            i = n - 1
            while i >= 0:
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                i -= 1

            # Copiar el contenido de output a arr
            for i in range(n):
                arr[i] = output[i]

        def radix_sort(arr):
            # Encontrar el número máximo para saber el número de dígitos
            max1 = max(arr)

            # Hacer counting sort para cada dígito
            exp = 1
            while max1 // exp > 0:
                counting_sort(arr, exp)
                exp *= 10

        # Copiar el arreglo original para preservarlo
        sorted_array = integer_array[:]
        
        # Ordenar el arreglo usando Radix Sort
        radix_sort(sorted_array)

        # Animar los pasos del ordenamiento
        for i, exp in enumerate([1, 10, 100], start=1):
            # Mostrar el conteo y reordenamiento para cada dígito
            intermediate_array = integer_array[:]
            counting_sort(intermediate_array, exp)
            string_intermediate_array = [str(num) for num in intermediate_array]
            new_table = Table([string_intermediate_array], include_outer_lines=True).scale(0.8)

            # Crear un texto para indicar la etapa
            stage_text = Text(f"Etapa {i}: Ordenando por el dígito de las {['unidades', 'decenas', 'centenas'][i-1]}").scale(0.5).to_edge(UP)
            
            self.play(Transform(table, new_table), FadeIn(stage_text))
            self.wait(1)
            self.play(FadeOut(stage_text))

        # Mostrar la tabla final ordenada
        sorted_string_array = [str(num) for num in sorted_array]
        final_table = Table([sorted_string_array], include_outer_lines=True).scale(0.8)
        final_text = Text("Arreglo Final Ordenado").scale(0.5).to_edge(UP)
        self.play(Transform(table, final_table), FadeIn(final_text))
        self.wait(2)
