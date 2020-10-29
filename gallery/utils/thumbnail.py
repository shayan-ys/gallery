from PIL import Image
from .const import Size, rendition_sizes, is_square


def get_thumbnails(photo: Image, sizes: [Size] = rendition_sizes) -> [int, Image]:
    thumbnails = []

    size: Size
    for size in sizes:
        thumb = photo.copy()

        if is_square(size):
            thumb = crop_max_square(thumb)
        thumb.thumbnail((size.value, size.value), resample=Image.ANTIALIAS)

        thumbnails.append((size.value, thumb))

    return thumbnails


def crop_center(pil_img, crop_width, crop_height) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img) -> Image:
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))
