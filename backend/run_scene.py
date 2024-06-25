from manim import *
from radix_sort_scene import RadixSortScene

class RadixSortSceneWrapper(RadixSortScene):
    def __init__(self, **kwargs):
        integer_array = kwargs.pop('integer_array', [170, 45, 75, 90, 802, 24, 2, 66])
        super().__init__(integer_array, **kwargs)

if __name__ == "__main__":
    scene = RadixSortSceneWrapper()
    scene.render()
