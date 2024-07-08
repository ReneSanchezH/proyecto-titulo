from manim import *

class RadixDetailedScene(Scene):
    def __init__(self, integer_array, **kwargs):
        self.integer_array = integer_array
        super().__init__(**kwargs)

    def construct(self):
        integer_array = self.integer_array
        array_length = len(integer_array)

        # Título Inicial
        title = Text("Radix Sort").scale(1).to_edge(UP)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Texto Introductorio
        intro_text = Text(
            "Radix Sort es un algoritmo de ordenamiento no comparativo\n"
            "que ordena los números procesando dígitos individuales.\n"
            "En este ejemplo, veremos cómo funciona paso a paso."
        ).scale(0.6).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(intro_text))
        self.wait(3)
        self.play(FadeOut(intro_text))

        # Determine the scale factor based on array length
        if array_length <= 5:
            scale_factor = 1.2
        elif array_length <= 7:
            scale_factor = 1.0
        elif array_length <= 9:
            scale_factor = 0.8
        elif array_length <= 10:
            scale_factor = 0.7
        else:
            scale_factor = 0.5

        # Create the initial empty squares
        squares = VGroup(*[Square(side_length=1).scale(scale_factor) for _ in integer_array])
        squares.arrange(RIGHT, buff=0)
        squares.shift(UP * 1.5)

        self.play(Create(squares))
        self.wait(1)

        # Create the numbers and place them in the squares
        num_texts = VGroup(*[Text(str(num)).scale(scale_factor * 0.8) for num in integer_array])
        for idx, num_text in enumerate(num_texts):
            num_text.move_to(squares[idx].get_center())

        self.play(*[FadeIn(num_text) for num_text in num_texts])
        self.wait(1)

        # Create the buckets
        bucket_height = 1.5
        bucket_width = 0.7
        bucket_spacing = 0.6
        buckets = VGroup(*[Rectangle(height=bucket_height, width=bucket_width) for _ in range(10)])
        buckets.arrange(RIGHT, buff=bucket_spacing)
        buckets.next_to(squares, DOWN, buff=1)

        self.add(buckets)  # Add buckets without animation
        self.wait(1)

        # Create the labels manually and adjust spacing
        labels = VGroup(*[Text(str(i)).scale(0.5).next_to(buckets[i], UP, buff=0.1) for i in range(10)])
        self.add(labels)  # Add labels without animation
        self.wait(1)

        def counting_sort(arr, exp):
            n = len(arr)
            output = [0] * n
            count = [0] * 10

            for i in range(n):
                index = (arr[i] // exp) % 10
                count[index] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            i = n - 1
            while i >= 0:
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                i -= 1

            for i in range(n):
                arr[i] = output[i]

        def radix_sort(arr):
            max1 = max(arr)
            exp = 1
            steps = [arr[:]]  # Record the initial state
            while max1 // exp > 0:
                counting_sort(arr, exp)
                steps.append(arr[:])  # Record state after each counting sort pass
                exp *= 10
            return steps

        steps = radix_sort(integer_array[:])

        for i, exp in enumerate([1, 10, 100], start=1):
            if i >= len(steps):
                break

            stage_text = Text(f"Etapa {i}: Ordenando por el dígito de las {['unidades', 'decenas', 'centenas'][i-1]}").scale(0.5)
            stage_text.to_edge(UP)

            self.play(FadeIn(stage_text))
            self.wait(1)

            bucket_positions = {i: 0 for i in range(10)}
            for digit in range(10):
                bucket_rect = buckets[digit]
                bucket_rect.set_color(BLUE)
                self.wait(0.5)  # Short wait to highlight the bucket

                for idx, num_text in enumerate(num_texts):
                    num = int(num_text.text)
                    current_digit = (num // exp) % 10
                    if current_digit == digit:
                        self.play(
                            num_text.animate.scale(0.6).move_to(
                                bucket_rect.get_top() + DOWN * (bucket_positions[digit] + 0.5) * 0.3 + DOWN * 0.1
                            ),
                            run_time=0.5
                        )
                        bucket_positions[digit] += 1
                        self.wait(0.2)

                bucket_rect.set_color(WHITE)

            self.wait(1)

            for idx, num in enumerate(steps[i]):
                num_text = next(t for t in num_texts if int(t.text) == num)
                self.play(
                    num_text.animate.scale(1 / 0.6).move_to(squares[idx].get_center()), run_time=0.5
                )

            self.wait(1)
            self.play(FadeOut(stage_text))

        final_text = Text("Arreglo Final Ordenado").scale(0.5)
        final_text.to_edge(UP)
        self.play(FadeIn(final_text))
        self.wait(2)

integer_array = [10, 123, 456, 789, 4]
scene = RadixDetailedScene(integer_array)
scene.render()
