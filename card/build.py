# 프로필 카드(card.svg) 생성 스크립트
# 아래 INFO / CONTACT 내용을 고친 뒤 `python card/build.py` 를 실행하면 card.svg 가 다시 만들어져요.
import os
import unicodedata
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))

HEADER = "yeeeehs@github"
INFO = [
    ("Name", "이현서"),
    ("Status", "Learning (student)"),
    ("School", "OO대학교 OO학과"),
    ("Focus", "Web & App"),
    ("Languages", "JavaScript, TypeScript, Java"),
    ("Frameworks", "React, React Native, Spring"),
    ("Tools", "Node.js, Git, GitHub"),
    ("Project", "같이가요"),
]
CONTACT = [
    ("Email", "leeihs122@gmail.com"),
    ("GitHub", "github.com/yeeeehs"),
]
FOOTER = "// 오늘도 배우는 중"

# 색상
BG, ART, TEXT, KEY, VALUE, DOTS, MUTED = "#1c2128", "#c9d1d9", "#c9d1d9", "#d2a8ff", "#a5d6ff", "#636e7b", "#768390"

# 레이아웃
ART_FONT, ART_CW, ART_LH = 8.5, 4.8, 9.6
INFO_FONT, INFO_CW, INFO_LH = 14, 8.2, 24
INFO_COLS = 58
PAD = 32
FONT = "Consolas, 'SF Mono', Menlo, 'D2Coding', 'Malgun Gothic', monospace"


def cells(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def seg(x, y, s, color, cw):
    """한 조각의 텍스트를 글자 칸 수에 맞춰 폭을 고정해서 그림 (폰트가 달라도 정렬 유지)"""
    if not s:
        return "", x
    w = cells(s) * cw
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" textLength="{w:.1f}" '
            f'lengthAdjust="spacingAndGlyphs">{escape(s)}</text>'), x + w


def row(y, parts):
    out, x = [], info_x
    for s, color in parts:
        t, x = seg(x, y, s, color, INFO_CW)
        out.append(t)
    return "".join(out)


def kv(y, key, value):
    left = f". {key}: "
    dots = "." * max(INFO_COLS - cells(left) - cells(value) - 1, 2)
    return row(y, [(". ", DOTS), (key, KEY), (": ", TEXT), (dots + " ", DOTS), (value, VALUE)])


def rule(y, title=""):
    head = f"{title} " if title else ""
    return row(y, [(head, TEXT), ("-" * (INFO_COLS - cells(head)), MUTED)])


art = open(os.path.join(HERE, "ascii.txt"), encoding="utf-8").read().split("\n")
art_cols = max(len(l) for l in art)
art_w, art_h = art_cols * ART_CW, len(art) * ART_LH
info_x = PAD + art_w + 36
info_w = INFO_COLS * INFO_CW

lines = [rule(0, HEADER)]
lines += [kv(0, k, v) for k, v in INFO]
lines.append(rule(0, "- Contact"))
lines += [kv(0, k, v) for k, v in CONTACT]
lines.append(rule(0))
n = len(lines) + 1
info_h = n * INFO_LH

H = max(art_h, info_h) + PAD * 2
W = info_x + info_w + PAD
info_top = (H - info_h) / 2 + INFO_LH * 0.75

info = []
y = info_top
for builder in ([lambda y: rule(y, HEADER)]
                + [lambda y, k=k, v=v: kv(y, k, v) for k, v in INFO]
                + [lambda y: rule(y, "- Contact")]
                + [lambda y, k=k, v=v: kv(y, k, v) for k, v in CONTACT]
                + [lambda y: rule(y)]):
    info.append(builder(y))
    y += INFO_LH
fw = cells(FOOTER) * INFO_CW
info.append(f'<text x="{info_x + info_w - fw:.1f}" y="{y:.1f}" fill="{MUTED}" textLength="{fw:.1f}" '
            f'lengthAdjust="spacingAndGlyphs">{escape(FOOTER)}</text>')

art_top = (H - art_h) / 2 + ART_LH * 0.8
art_svg = []
for i, l in enumerate(art):
    if l.strip():
        art_svg.append(f'<text x="{PAD}" y="{art_top + i * ART_LH:.1f}" textLength="{len(l) * ART_CW:.1f}" '
                       f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(l)}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">
<rect width="100%" height="100%" rx="12" fill="{BG}"/>
<g font-family="{FONT}" font-size="{ART_FONT}" fill="{ART}">
{chr(10).join(art_svg)}
</g>
<g font-family="{FONT}" font-size="{INFO_FONT}" xml:space="preserve">
{chr(10).join(info)}
</g>
</svg>
'''
open(os.path.join(os.path.dirname(HERE), "card.svg"), "w", encoding="utf-8").write(svg)
print("card.svg 생성 완료")
