from manim import *
from radix_sort_scene import RadixSortScene
from radix_detailed_scene import RadixDetailedScene
from counting_sort_scene import CountingSortScene
import argparse

class RadixSortSceneWrapper(RadixSortScene):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class RadixDetailedSceneWrapper(RadixDetailedScene):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class CountingSortSceneWrapper(CountingSortScene):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

def main():
    parser = argparse.ArgumentParser(description="Run sorting scenes with Manim.")
    parser.add_argument('--detailed', action='store_true', help="Generate detailed Radix Sort video.")
    parser.add_argument('--counting', action='store_true', help="Generate Counting Sort video.")
    parser.add_argument('--numbers', type=str, default="170,45,75,90,802,24,2,66", help="Comma-separated list of numbers to sort.")
    
    args = parser.parse_args()
    numbers = [int(num) for num in args.numbers.split(',')]
    
    if args.counting:
        scene = CountingSortSceneWrapper(numbers)
    elif args.detailed:
        scene = RadixDetailedSceneWrapper(numbers)
    else:
        scene = RadixSortSceneWrapper(numbers)
    
    scene.render()

if __name__ == "__main__":
    main()
