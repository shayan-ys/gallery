from django import template

register = template.Library()


@register.filter(name='url')
def get_url_for_size_filter(photo, size_point: int) -> str:
    return photo.get_url_for_size(size_point)
