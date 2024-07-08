from manim import *

class CountingSortScene(Scene):
    def __init__(self, integer_array, **kwargs):
        self.integer_array = integer_array
        super().__init__(**kwargs)

    def construct(self):
        integer_array = self.integer_array
        array_length = len(integer_array)

        # Título Inicial
        title = Text("Counting Sort").scale(1).to_edge(UP)
        self.play(Write(title))
        self.wait(2)

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

        # Create the initial squares representing the array
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

        # Create the count array below the buckets
        count_squares = VGroup(*[Square(side_length=1).scale(0.7) for _ in range(10)])
        count_squares.arrange(RIGHT, buff=bucket_spacing)
        count_squares.next_to(buckets, DOWN, buff=1)

        self.add(count_squares)
        self.wait(1)

        count_texts = VGroup(*[Text("0").scale(0.5).move_to(count_squares[i].get_center()) for i in range(10)])
        self.add(count_texts)
        self.wait(1)

        # Counting Sort Algorithm Visualization
        def counting_sort(arr):
            n = len(arr)
            output = [0] * n
            count = [0] * 10

            for i in range(n):
                index = arr[i]
                count[index] += 1

            for i in range(1, 10):
                count[i] += count[i - 1]

            for i in range(n-1, -1, -1):
                index = arr[i]
                output[count[index] - 1] = arr[i]
                count[index] -= 1

            for i in range(n):
                arr[i] = output[i]

        steps = []

        def update_count_array(count):
            for i, c in enumerate(count):
                count_texts[i].become(Text(str(c)).scale(0.5).move_to(count_squares[i].get_center()))

        count = [0] * 10
        for num in integer_array:
            count[num] += 1
            steps.append(count[:])
            update_count_array(count)
            self.wait(1)

        for i in range(1, 10):
            count[i] += count[i - 1]
            steps.append(count[:])
            update_count_array(count)
            self.wait(1)

        output = [0] * array_length
        for num in reversed(integer_array):
            output[count[num] - 1] = num
            count[num] -= 1
            steps.append(count[:])
            update_count_array(count)
            self.wait(1)

        sorted_squares = VGroup(*[Square(side_length=1).scale(scale_factor) for _ in output])
        sorted_squares.arrange(RIGHT, buff=0)
        sorted_squares.next_to(count_squares, DOWN, buff=1)

        self.play(Create(sorted_squares))
        self.wait(1)

        sorted_texts = VGroup(*[Text(str(num)).scale(scale_factor * 0.8) for num in output])
        for idx, num_text in enumerate(sorted_texts):
            num_text.move_to(sorted_squares[idx].get_center())

        self.play(*[FadeIn(num_text) for num_text in sorted_texts])
        self.wait(1)

        final_text = Text("Arreglo Final Ordenado").scale(0.5)
        final_text.to_edge(UP)
        self.play(FadeIn(final_text))
        self.wait(2)

integer_array = [3, 6, 4, 1, 3, 4, 1, 4]
scene = CountingSortScene(integer_array)
scene.render()
