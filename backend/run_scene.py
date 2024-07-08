from manim import *
from radix_sort_scene import RadixSortScene
from radix_detailed_scene import RadixDetailedScene
from counting_sort_scene import CountingSortScene
from introduction_scene import IntroductionScene
import argparse
import os
import glob

class RadixSortSceneWrapper(RadixSortScene):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class RadixDetailedSceneWrapper(RadixDetailedScene):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class CountingSortSceneWrapper(CountingSortScene):
    def __init__(self, integer_array, **kwargs):
        super().__init__(integer_array, **kwargs)

class IntroductionSceneWrapper(IntroductionScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def main():
    parser = argparse.ArgumentParser(description="Run sorting scenes with Manim.")
    parser.add_argument('--detailed', action='store_true', help="Generate detailed Radix Sort video.")
    parser.add_argument('--counting', action='store_true', help="Generate Counting Sort video.")
    parser.add_argument('--introduction', action='store_true', help="Generate Introduction video.")
    parser.add_argument('--numbers', type=str, default="170,45,75,90,802,24,2,66", help="Comma-separated list of numbers to sort.")
    
    args = parser.parse_args()
    numbers = [int(num) for num in args.numbers.split(',')]
    
    if args.introduction:
        scene = IntroductionSceneWrapper()
        output_file = "IntroductionScene.mp4"
    elif args.counting:
        scene = CountingSortSceneWrapper(numbers)
        output_file = "CountingSortScene.mp4"
    elif args.detailed:
        scene = RadixDetailedSceneWrapper(numbers)
        output_file = "RadixDetailedScene.mp4"
    else:
        scene = RadixSortSceneWrapper(numbers)
        output_file = "RadixSortScene.mp4"
    
    # Render the scene
    scene.render()

    # Rename the latest video file to the desired output name
    output_directory = "media/videos/1080p60/"
    default_output_file = max(glob.glob(output_directory + "*.mp4"), key=os.path.getctime)
    os.rename(default_output_file, os.path.join(output_directory, output_file))

if __name__ == "__main__":
    main()
