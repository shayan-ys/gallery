from django import template

register = template.Library()


@register.filter
def get_photo_dimensions(photo, size_point: int):
    w, h = int(size_point * photo.img_ratio), size_point
    return f'{w}x{h}'
