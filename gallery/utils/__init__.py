from PIL import Image
from io import BytesIO


def get_bytes(photo: Image):
    blob = BytesIO()
    photo = photo.convert('RGB')
    photo.save(blob, 'JPEG', quality=100)
    return blob.getvalue()


def get_closest(needle: int, haystack: list):
    return min(haystack, key=lambda x: abs(x - needle))
