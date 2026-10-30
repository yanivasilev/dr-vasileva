# Makes the website's images from the originals in brand/originals/: smaller WebP files, sized for how
# big they are shown on the site (with room for sharp phone screens). Run it after changing an original:
#   python3 build/make-web-images.py
# then rebuild the site (build/build.py).
import os

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f'{REPO}/brand/originals'
OUT = f'{REPO}/public/images'

# (original, web file, longest side in pixels, quality)
IMAGES = [
    ('dr-vasileva.jpg', 'dr-vasileva.webp', 960, 82),          # home page, About page (shown up to ~520 px)
    ('dr-vasileva.jpg', 'dr-vasileva-small.webp', 240, 82),    # small round photos (article author box, preview screen)
] + [(f'logos/{f}', f'logos/{f[:-4]}.webp', 300, 88) for f in sorted(os.listdir(f'{SRC}/logos')) if f.endswith('.png')]


def make(src, dst, side, quality):
    im = Image.open(f'{SRC}/{src}')
    im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
    im.thumbnail((side, side), Image.LANCZOS)            # never enlarged
    os.makedirs(os.path.dirname(f'{OUT}/{dst}'), exist_ok=True)
    im.save(f'{OUT}/{dst}', 'WEBP', quality=quality, method=6)
    return im.size


if __name__ == '__main__':
    for src, dst, side, quality in IMAGES:
        size = make(src, dst, side, quality)
        print(f'{dst:45} {size[0]}×{size[1]}  {os.path.getsize(f"{SRC}/{src}") // 1024:>4} KB → {os.path.getsize(f"{OUT}/{dst}") // 1024:>3} KB')
