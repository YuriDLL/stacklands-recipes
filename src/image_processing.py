from PIL import Image
from PIL import ImageOps
import os


def prepare_image(name_key: str, color: str, out_suffix: str = '') -> None:
    ico_size = 64, 64

    source_images_path = 'data/raw_img/'
    images_path = 'static/generated/img/'
    icons_path = 'static/generated/icon/'

    if not os.path.exists(icons_path):
        os.makedirs(icons_path)
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    file = os.path.join(source_images_path, name_key + '.png')

    with Image.open(file, mode='r') as im:
        path, file = os.path.split(file)
        file, ext = os.path.splitext(file)
        im = _change_color(im, color)

        png_file = os.path.join(images_path, file + out_suffix + ".png")
        if not os.path.exists(png_file):
            im.save(png_file, "PNG")
        ico_file = os.path.join(icons_path, file + out_suffix + ".ico")
        if not os.path.exists(ico_file):
            im.thumbnail(ico_size)
            im.save(ico_file, "ICO")


def _change_color(image: Image, color: str) -> Image:
    color_table = {
        'black': (True, 'rgb(64, 63, 58)'),
        'yellow': (False, 'rgb(255, 250, 228)'),
        'gray': (True, 'rgb(100, 111, 128)'),
        'orange': (False, 'rgb(227, 147, 79)'),
        'red': (False, 'rgb(214, 91, 91)'),
        'brown': (False, 'rgb(144, 102, 69)'),
        'purple': (False, 'rgb(178, 100, 181)'),
        'green': (False, 'rgb(169, 215, 128)'),
        'gold': (False, 'rgb(244, 217, 151)'),
        'pink': (False, 'rgb(239, 181, 167)'),
    }
    invert, color = color_table[color]
    lines_color = 'white' if invert else 'black'
    image = image.convert('RGBA')
    alpha = image.getchannel('A')
    image_new = image.convert('L')
    image_new = ImageOps.colorize(image_new, lines_color, color)
    image_new.putalpha(alpha)
    return image_new
