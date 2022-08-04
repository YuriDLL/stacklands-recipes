from PIL import Image
from PIL import ImageOps
from PIL import ImageColor
import glob
import os

from game_info import Cards


def prepare_images() -> None:
    ico_size = 64, 64

    source_images_path = 'data/test'
    images_path = 'static/generated/img/'
    icons_path = 'static/generated/icon/'

    if not os.path.exists(icons_path):
        os.makedirs(icons_path)
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    for file in glob.glob(os.path.join(source_images_path, '*.png')):
        cards = Cards()
        with Image.open(file) as im:
            path, file = os.path.split(file)
            file, ext = os.path.splitext(file)
            print(file)
            im = _change_color(im, cards.get_card(file))
            im.save(os.path.join(images_path, file + ".png"), "PNG")
            im.thumbnail(ico_size)
            im.save(os.path.join(icons_path, file + ".ico"), "ICO")


def _change_color(image: Image, card: dict) -> Image:
    color_table = {
        'black': (True, 'rgb(64, 63, 58)')
    }
    invert, color = color_table[card['image_color']]
    lines_color = 'white' if invert else 'black'
    alpha = image.getchannel('A')
    image_new = image.convert('L')
    image_new = ImageOps.colorize(image_new, lines_color, color)
    image_new.putalpha(alpha)
    return image_new



if __name__ == '__main__':
    prepare_images()
