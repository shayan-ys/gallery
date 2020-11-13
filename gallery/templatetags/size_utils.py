from django import template
from django.conf import settings
from ..utils import get_closest

register = template.Library()


def get_pixels_count_to_int(pixels: str) -> int:
    return int(pixels.replace('px', ''))


@register.filter(name='url')
def get_url_for_size_filter(photo, size_point: int) -> str:
    sizes = list(map(get_pixels_count_to_int, photo['filenames'].keys()))
    existing_size_point = get_closest(size_point, sizes)
    filename = photo['filenames'][f'{existing_size_point}px']
    return settings.GS_BASE_URL + filename


@register.filter
def get_photo_dimensions(photo, size_point: int):
    w, h = int(size_point * photo['img_ratio']), size_point
    return f'{w}x{h}'
