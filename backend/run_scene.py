from manim import *
from radix_sort_scene import RadixSort
from radix_detailed_scene import RadixDetailed
from counting_sort_scene import CountingSort
from bucket_scene import Bucket
import argparse
import os

class RadixSortWrapper(RadixSort):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class RadixDetailedWrapper(RadixDetailed):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class CountingSortWrapper(CountingSort):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class BucketWrapper(Bucket):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def main():
    parser = argparse.ArgumentParser(description="Run sorting scenes with Manim.")
    parser.add_argument('--detailed', action='store_true', help="Generate detailed Radix Sort video.")
    parser.add_argument('--counting', action='store_true', help="Generate Counting Sort video.")
    parser.add_argument('--bucket', action='store_true', help="Generate Bucket Explanation video.")
    parser.add_argument('--numbers', type=str, default="90,316,482,149,5", help="Comma-separated list of numbers to sort.")
    
    args = parser.parse_args()
    numbers = [int(num) for num in args.numbers.split(',')]
    
    output_dir = "videos/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    config.media_dir = output_dir  # Establecer el directorio de salida para Manim
    
    if args.bucket:
        scene = BucketWrapper()
        output_file = os.path.join(output_dir, "bucket.mp4")
    elif args.counting:
        scene = CountingSortWrapper(numbers)
        output_file = os.path.join(output_dir, "counting_sort.mp4")
    elif args.detailed:
        scene = RadixDetailedWrapper(numbers)
        output_file = os.path.join(output_dir, "radix_detailed.mp4")
    else:
        scene = RadixSortWrapper(numbers)
        output_file = os.path.join(output_dir, f'{"".join(map(str, numbers))}.mp4')
    
    # Render the scene
    scene.render()

if __name__ == "__main__":
    main()
