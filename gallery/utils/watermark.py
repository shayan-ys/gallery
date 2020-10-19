from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from django.conf import settings


def add_watermark():
    photo = Image.open(settings.MEDIA_ROOT / "self.jpg")

    # Store image width and height
    w, h = photo.size
    print(w, h)

    # make the image editable
    drawing = ImageDraw.Draw(photo)
    font_path = str(settings.STATICFILES_DIRS[0] / "fonts/Roboto/Roboto-Black.ttf")
    font = ImageFont.truetype(font_path, 10)

    # get text width and height
    text = "© Shayan Ys"
    text_w, text_h = drawing.textsize(text, font)
    print(text_w, text_h)

    pos = w - text_w, (h - text_h) - 50

    c_text = Image.new('RGB', (text_w, text_h), color='#000000')
    drawing = ImageDraw.Draw(c_text)

    drawing.text((0, 0), text, fill="#ffffff", font=font)
    c_text.putalpha(100)

    photo.paste(c_text, pos, c_text)
    photo.save(str(settings.MEDIA_ROOT / "self-w.jpg"))
