from .utils.const import Size, rendition_sizes


def rendition_sizes_renderer(request):
    return {
        'rendition_sizes': rendition_sizes
    }


def sizes_renderer(request):
    return {name: size.value for name, size in Size.__members__.items()}
