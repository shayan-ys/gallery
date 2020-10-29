from django import template

register = template.Library()


@register.filter
def get_photo_dimensions(photo, size_point: int):
    w, h = photo.get_dimensions(size_point)
    return f'{w}x{h}'


@register.filter
def get_url(photo, size_point: int):
    closest_size_point = min(photo.urls.keys(), key=lambda x: abs(x-size_point))
    return photo.urls[closest_size_point]
