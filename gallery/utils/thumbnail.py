from PIL import Image


def get_thumbnails(photo: Image, sizes: [int]) -> [int, Image]:
    thumbnails = []

    for size in sizes:
        thumb = photo.copy()
        thumb.thumbnail((size, size), resample=Image.ANTIALIAS)
        thumbnails.append((size, thumb))

    return thumbnails
