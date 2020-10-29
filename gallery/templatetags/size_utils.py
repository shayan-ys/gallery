from django import template
from ..utils.const import is_square

register = template.Library()


@register.filter(name='is_square')
def is_square_filter(size_point: int) -> bool:
    return is_square(size_point)
