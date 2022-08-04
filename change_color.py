from PIL import Image
from PIL import ImageOps


with Image.open('composter.png') as im:
    alpha = im.getchannel('A')
    im = im.convert('L')
    im = ImageOps.colorize(im, 'black', 'red')
    im.putalpha(alpha)
    im.show()
