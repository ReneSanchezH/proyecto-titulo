from manim import *
import argparse

class CountingSortScene(Scene):
    def __init__(self, integer_array, **kwargs):
        self.integer_array = integer_array
        super().__init__(**kwargs)

    def construct(self):
        integer_array = self.integer_array
        array_length = len(integer_array)

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

        # Create the count array (buckets for counting sort)
        max_num = max(integer_array)
        count_array_length = max_num + 1
        count_squares = VGroup(*[Square(side_length=1).scale(0.7) for _ in range(count_array_length)])
        count_squares.arrange(RIGHT, buff=0.1)
        count_squares.shift(DOWN * 1.5)

        self.play(Create(count_squares))
        self.wait(1)

        # Create the count numbers and place them in the count squares
        count_texts = VGroup(*[Text('0').scale(0.5) for _ in range(count_array_length)])
        for idx, count_text in enumerate(count_texts):
            count_text.move_to(count_squares[idx].get_center())

        self.play(*[FadeIn(count_text) for count_text in count_texts])
        self.wait(1)

        # Create labels for the count squares
        count_labels = VGroup(*[Text(str(i)).scale(0.5).next_to(count_squares[i], UP, buff=0.1) for i in range(count_array_length)])
        self.play(*[FadeIn(label) for label in count_labels])
        self.wait(1)

        # Step 1: Count the occurrences of each number
        for num in integer_array:
            count_text = count_texts[num]
            self.play(Indicate(num_texts[integer_array.index(num)]), run_time=0.5)
            new_count = int(count_text.text) + 1
            count_text.set_text(str(new_count))
            self.play(Transform(count_text, count_text.copy().move_to(count_squares[num].get_center())), run_time=0.5)

        self.wait(1)

        # Step 2: Modify the count array by adding the previous counts
        for i in range(1, count_array_length):
            prev_count = int(count_texts[i-1].text)
            current_count = int(count_texts[i].text)
            new_count = prev_count + current_count
            count_texts[i].set_text(str(new_count))
            self.play(Transform(count_texts[i], count_texts[i].copy().move_to(count_squares[i].get_center())), run_time=0.5)

        self.wait(1)

        # Step 3: Place numbers into their correct positions
        output_array = [None] * array_length
        num_text_positions = {num_text: idx for idx, num_text in enumerate(num_texts)}

        for num_text in reversed(num_texts):
            num = int(num_text.text)
            count = int(count_texts[num].text)
            position = count - 1
            output_array[position] = num
            count_texts[num].set_text(str(count - 1))
            self.play(
                num_text.animate.move_to(squares[position].get_center()),
                Transform(count_texts[num], count_texts[num].copy().move_to(count_squares[num].get_center())),
                run_time=0.5
            )

        self.wait(1)

        # Final step: Display the sorted array
        final_text = Text("Arreglo Final Ordenado").scale(0.5)
        final_text.to_edge(UP)
        self.play(FadeIn(final_text))
        self.wait(2)

def main():
    parser = argparse.ArgumentParser(description="Run sorting scenes with Manim.")
    parser.add_argument('--detailed', action='store_true', help="Generate detailed Radix Sort video.")
    parser.add_argument('--counting', action='store_true', help="Generate Counting Sort video.")
    parser.add_argument('--numbers', type=str, default="170,45,75,90,802,24,2,66", help="Comma-separated list of numbers to sort.")
    
    args = parser.parse_args()
    numbers = [int(num) for num in args.numbers.split(',')]
    
    if args.counting:
        scene = CountingSortScene(numbers)
    elif args.detailed:
        scene = RadixDetailedScene(numbers)
    else:
        scene = RadixSortScene(numbers)
    
    scene.render()

if __name__ == "__main__":
    main()
