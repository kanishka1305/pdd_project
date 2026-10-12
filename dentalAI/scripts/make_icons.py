"""App icons and splash screens for Android and iOS, from the Dental AI logo.

    python scripts/make_icons.py        (run after `npx cap add android` / `ios`)

Uses branding/logo-mark.png (the tooth) and branding/logo-full.png (with the name).
For the app stores, a 1024 px or larger original of the logo gives sharper icons."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / 'branding'
RES = ROOT / 'android' / 'app' / 'src' / 'main' / 'res'
XCASSETS = ROOT / 'ios' / 'App' / 'App' / 'Assets.xcassets'
WHITE = (255, 255, 255, 255)

mark = Image.open(IMG / 'logo-mark.png').convert('RGBA')
full = Image.open(IMG / 'logo-full.png').convert('RGBA')


def scaled(img, width):
    height = round(img.height * width / img.width)
    out = img.resize((width, height), Image.LANCZOS)
    if width > img.width:   # enlarged: restore a little edge crispness
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    return out


def centred(size, img, fraction, background=None, shape=None):
    """img scaled to fraction of the canvas width, centred; optional background shape."""
    w, h = size
    canvas = Image.new('RGBA', size, (0, 0, 0, 0))
    if background:
        layer = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        if shape == 'circle':
            draw.ellipse((0, 0, w - 1, h - 1), fill=background)
        elif shape == 'rounded':
            draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=round(w * 0.18), fill=background)
        else:
            draw.rectangle((0, 0, w, h), fill=background)
        canvas = Image.alpha_composite(canvas, layer)
    piece = scaled(img, max(1, round(min(w, h) * fraction)))
    canvas.alpha_composite(piece, ((w - piece.width) // 2, (h - piece.height) // 2))
    return canvas


def save(img, path, rgb=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    (img.convert('RGB') if rgb else img).save(path, optimize=True)


def android():
    if not RES.exists():
        return print('android: skipped (run npx cap add android first)')
    for density, px in (('mdpi', 48), ('hdpi', 72), ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)):
        save(centred((px, px), mark, 0.80, WHITE, 'rounded'), RES / f'mipmap-{density}' / 'ic_launcher.png')
        save(centred((px, px), mark, 0.72, WHITE, 'circle'), RES / f'mipmap-{density}' / 'ic_launcher_round.png')
        fg = round(px * 108 / 48)   # adaptive icon layer: 108 dp, the visible part is the centre 66 dp
        save(centred((fg, fg), mark, 0.52), RES / f'mipmap-{density}' / 'ic_launcher_foreground.png')
    (RES / 'values' / 'ic_launcher_background.xml').write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <color name="ic_launcher_background">#FFFFFF</color>\n</resources>\n', encoding='utf-8')
    for splash in RES.glob('drawable*/splash.png'):
        size = Image.open(splash).size
        save(centred(size, full, 0.46, WHITE), splash, rgb=True)
    print('android: icons and splash screens written')


def ios():
    if not XCASSETS.exists():
        return print('ios: skipped (run npx cap add ios first)')
    # App Store icons must be square, 1024 px and without transparency (iOS rounds the corners)
    save(centred((1024, 1024), mark, 0.78, WHITE), XCASSETS / 'AppIcon.appiconset' / 'AppIcon-512@2x.png', rgb=True)
    for splash in (XCASSETS / 'Splash.imageset').glob('splash-*.png'):
        save(centred((2732, 2732), full, 0.30, WHITE), splash, rgb=True)
    print('ios: icon and splash screens written')


if __name__ == '__main__':
    android()
    ios()
