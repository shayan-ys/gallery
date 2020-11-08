from django.conf import settings

from .utils.const import Size
from .models import rendition_sizes


def rendition_sizes_renderer(_request):
    return {
        'rendition_sizes': rendition_sizes
    }


def sizes_renderer(_request):
    return {name: size.value for name, size in Size.__members__.items()}


def settings_renderer(_request):
    return {
        'settings': settings
    }
