from manim import *

class RadixDetailedScene(Scene):
    def __init__(self, integer_array, **kwargs):
        self.integer_array = integer_array
        super().__init__(**kwargs)

    def construct(self):
        integer_array = self.integer_array
        string_array = [str(num) for num in integer_array]

        # Determine the scale factor
        array_length = len(integer_array)
        three_digit_count = sum(1 for num in integer_array if 100 <= num < 1000)

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

        if three_digit_count <= 3:
            scale_factor -= 0.1
        elif three_digit_count <= 5:
            scale_factor -= 0.2
        else:
            scale_factor -= 0.3

        # Create the initial table
        table = Table(
            [string_array],
            include_outer_lines=True
        ).scale(scale_factor)

        table.shift(UP * 1.5)

        self.play(Create(table))
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
            while max1 // exp > 0:
                counting_sort(arr, exp)
                exp *= 10

        sorted_array = integer_array[:]
        radix_sort(sorted_array)

        # Create the buckets
        bucket_height = 1.5
        bucket_width = 0.5
        bucket_spacing = 1

        buckets = VGroup()
        bucket_labels = VGroup()
        for i in range(10):
            bucket = Rectangle(height=bucket_height, width=bucket_width)
            bucket_label = Text(str(i)).scale(0.5).next_to(bucket, UP)
            buckets.add(bucket)
            bucket_labels.add(bucket_label)

        buckets.arrange(RIGHT, buff=bucket_spacing)
        buckets.next_to(table, DOWN, buff=1)
        bucket_labels.arrange(RIGHT, buff=bucket_spacing)
        bucket_labels.next_to(buckets, UP)

        self.play(Create(buckets), FadeIn(bucket_labels))
        self.wait(1)

        def get_bucket_position(digit, position):
            bucket = buckets[digit]
            return bucket.get_top() + DOWN * (position + 0.5) * 0.3

        for i, exp in enumerate([1, 10, 100], start=1):
            intermediate_array = integer_array[:]
            counting_sort(intermediate_array, exp)
            string_intermediate_array = [str(num) for num in intermediate_array]
            new_table = Table([string_intermediate_array], include_outer_lines=True).scale(scale_factor)

            stage_text = Text(f"Etapa {i}: Ordenando por el dígito de las {['unidades', 'decenas', 'centenas'][i-1]}").scale(0.5)
            stage_text.to_edge(UP)

            self.play(Transform(table, new_table.shift(UP * 1.5)), FadeIn(stage_text))
            self.wait(1)
            self.play(FadeOut(stage_text))

            bucket_positions = {i: 0 for i in range(10)}
            bucket_mobjects = {i: VGroup() for i in range(10)}
            for num in intermediate_array:
                digit = (num // exp) % 10
                num_text = Text(str(num)).scale(0.5)
                num_text.move_to(table.get_cell((1, intermediate_array.index(num) + 1)).get_center())
                self.play(num_text.animate.move_to(get_bucket_position(digit, bucket_positions[digit])), run_time=0.5)
                bucket_positions[digit] += 1
                bucket_mobjects[digit].add(num_text)

            self.wait(1)

            for digit in range(10):
                for num_text in bucket_mobjects[digit]:
                    self.play(num_text.animate.move_to(table.get_cell((1, intermediate_array.index(int(num_text.text)) + 1)).get_center()), run_time=0.5)
                bucket_mobjects[digit].remove(*bucket_mobjects[digit])

        sorted_string_array = [str(num) for num in sorted_array]
        final_table = Table([sorted_string_array], include_outer_lines=True).scale(scale_factor)
        final_text = Text("Arreglo Final Ordenado").scale(0.5)
        final_text.to_edge(UP)
        self.play(Transform(table, final_table.shift(UP * 1.5)), FadeIn(final_text))
        self.wait(2)

integer_array = [10, 123, 456, 789, 4]
scene = RadixDetailedScene(integer_array)
scene.render()
