"""staging/<id>.html 카드마다 사진+제목+설명을 한 장 모아 보기로 만든다."""
import re, sys, pathlib, html as H
from PIL import Image, ImageDraw, ImageFont
root = pathlib.Path(sys.argv[1]); sid = sys.argv[2]; out = pathlib.Path(sys.argv[3])
src = (root / 'staging' / f'{sid}.html').read_text(encoding='utf-8')
cards = re.findall(r'<section[^>]*data-ch="([^"]+)"[^>]*>(.*?)</section>', src, re.S)
font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 17)
fb = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 18)
W, IH, TH, cols = 420, 236, 66, 5
rows = (len(cards) + cols - 1) // cols
sheet = Image.new('RGB', (cols * W, rows * (IH + TH)), 'white'); d = ImageDraw.Draw(sheet)
def txt(s): return H.unescape(re.sub(r'<[^>]+>', '', s)).strip()
for i, (ch, body) in enumerate(cards):
    x, y = (i % cols) * W, (i // cols) * (IH + TH)
    imgs = re.findall(r'src="([^"]+)"', body)
    if imgs:
        w = W // len(imgs)
        for j, p in enumerate(imgs):
            try:
                im = Image.open(root / p).convert('RGB'); im.thumbnail((w - 4, IH - 4)); sheet.paste(im, (x + j * w + 2, y + 2))
            except Exception as e:
                d.text((x + 4, y + 40), f'ERR {p}', fill='red', font=font)
    else:
        rows_t = re.findall(r'<b>(.*?)</b><span>(.*?)</span>', body)
        for k, (a, b) in enumerate(rows_t[:6]):
            d.text((x + 6, y + 6 + k * 34), f'{txt(a)}: {txt(b)}'[:30], fill='#333', font=font)
    h2 = re.search(r'<h2>(.*?)</h2>', body); ds = re.search(r'<p class="desc"[^>]*>(.*?)</p>', body)
    d.text((x + 4, y + IH), f'{i+1}.[{ch}] ' + (txt(h2.group(1)) if h2 else ''), fill='#c32f28', font=fb)
    d.text((x + 4, y + IH + 24), txt(ds.group(1)) if ds else '', fill='#1f2b4d', font=font)
    d.rectangle([x, y, x + W - 1, y + IH + TH - 1], outline='#ccc')
sheet.save(out, quality=80); print(len(cards), sheet.size)
