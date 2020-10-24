from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO

from django.conf import settings


def add_watermark(file):
    photo = Image.open(file)

    # Store image width and height
    w, h = photo.size

    # make the image editable
    drawing = ImageDraw.Draw(photo)
    font_path = str(settings.STATICFILES_DIRS[0] / "fonts/Roboto/Roboto-Black.ttf")
    font = ImageFont.truetype(font_path, int(min(w, h) / 45))

    # get text width and height
    text = "© Shayan Ys"
    text_w, text_h = drawing.textsize(text, font)

    pos = int((w - text_w) - w / 11), int((h - text_h) - h / 15)

    text_canvas = Image.new('RGB', (int(text_w + w / 11), int(text_h + h / 58)), color='#000000')
    drawing = ImageDraw.Draw(text_canvas)

    drawing.text((int(w / 200) + 3, int(h / 136)), text, fill="#ffffff", font=font)
    text_canvas.putalpha(170)

    photo.paste(text_canvas, pos, text_canvas)
    # photo = photo.convert('RGB')

    blob = BytesIO()
    photo.save(blob, 'JPEG')
    return blob.getvalue()
