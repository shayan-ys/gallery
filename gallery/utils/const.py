from typing import Union
from enum import Enum


class Size(Enum):
    FULL = 2000
    INSTA_MAX = 1350
    INSTA_STANDARD = 1080
    MEDIUM = 750
    HD = 720
    SMALL = 640
    THUMBNAIL = 293


square_sizes = []
rendition_sizes = [Size.FULL, Size.MEDIUM, Size.THUMBNAIL]


def is_square(size: Union[Size, int]) -> bool:
    if isinstance(size, int):
        for square in square_sizes:
            if size == square.value:
                return True
        return False
    else:
        return size in square_sizes
