#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Rebuilt 2026-11-18: 30 distinct stories, all reported on Tuesday
17 November 2026 (BBC, Reuters, AP, CNN, Al Jazeera, UN News, PAHO).
Runs offline with Pillow + DejaVu fonts only. main.ts ships entry.png.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 24, 39)
NAVY = (15, 42, 74)
NAVY_LT = (30, 64, 110)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
TEAL = (14, 116, 144)
SLATE = (51, 65, 85)
GREEN = (21, 101, 52)
PURPLE = (88, 28, 135)
ORANGE = (194, 65, 12)
SKY = (178, 205, 225)
SEA = (23, 84, 110)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
MUTED = (75, 85, 99)
LINE = (203, 213, 225)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=None, max_lines=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.25)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def card(draw, box, fill=CARD, outline=LINE, width=2):
    draw.rounded_rectangle(box, radius=9, fill=fill, outline=outline, width=width)


def kicker(draw, xy, text, color, size=15):
    draw.text(xy, text, font=font(SANS_B, size), fill=color)


# ---------- illustrations ----------
def draw_bridge_scene(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.ellipse([x1 - 92, y0 + 14, x1 - 38, y0 + 68], fill=(253, 224, 130), outline=(240, 180, 60), width=3)
    for cx, cy in [(x0 + 50, y0 + 30), (x0 + 140, y0 + 52)]:
        d.ellipse([cx, cy, cx + 74, cy + 22], fill=WHITE)
        d.ellipse([cx + 18, cy - 10, cx + 62, cy + 14], fill=WHITE)
    sea_y = y1 - 56
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for wx in range(x0 + 8, x1 - 20, 46):
        d.arc([wx, sea_y + 16, wx + 40, sea_y + 44], 200, 340, fill=WHITE, width=3)
    deck_y = sea_y - 36
    mid = (x0 + x1) // 2
    d.rectangle([x0, deck_y, mid - 72, deck_y + 12], fill=(55, 65, 81))
    d.rectangle([mid + 112, deck_y, x1, deck_y + 12], fill=(55, 65, 81))
    d.polygon([(mid - 72, deck_y), (mid - 16, deck_y + 32), (mid - 28, deck_y + 50), (mid - 86, deck_y + 16)], fill=(75, 85, 99))
    d.polygon([(mid + 112, deck_y), (mid + 58, deck_y + 42), (mid + 40, deck_y + 28), (mid + 98, deck_y - 6)], fill=(75, 85, 99))
    for px in (x0 + 46, x0 + 200, mid + 180, x1 - 60):
        d.rectangle([px, deck_y + 12, px + 12, sea_y + 6], fill=(75, 85, 99))
    d.arc([x0 + 56, deck_y - 58, x0 + 290, deck_y + 28], 180, 360, fill=RED, width=9)
    d.arc([mid + 36, deck_y - 58, mid + 270, deck_y + 28], 300, 360, fill=RED, width=9)
    d.line([(mid + 112, deck_y - 44), (mid + 90, deck_y - 28)], fill=RED, width=9)
    for sx, sy, sr in [(mid - 18, deck_y - 52, 20), (mid + 16, deck_y - 64, 24), (mid + 54, deck_y - 52, 18)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(107, 114, 128))
        d.ellipse([sx - sr + 8, sy - sr + 6, sx + sr - 6, sy + sr - 4], fill=(156, 163, 175))
    d.polygon([(mid + 8, deck_y - 42), (mid + 26, deck_y - 72), (mid + 40, deck_y - 40),
               (mid + 64, deck_y - 60), (mid + 50, deck_y - 26), (mid + 70, deck_y - 16),
               (mid + 38, deck_y - 10), (mid + 20, deck_y + 6), (mid + 10, deck_y - 14)],
              fill=(249, 115, 22))
    d.polygon([(mid - 44, sea_y + 6), (mid - 16, sea_y - 20), (mid + 6, sea_y + 4),
               (mid + 32, sea_y - 16), (mid + 58, sea_y + 6)], fill=WHITE)


def draw_plane(d, x, y, s, color):
    d.polygon([(x, y + 18 * s), (x + 74 * s, y + 18 * s), (x + 92 * s, y + 12 * s),
               (x + 74 * s, y + 8 * s), (x, y + 8 * s)], fill=color)
    d.polygon([(x + 30 * s, y + 8 * s), (x + 52 * s, y - 12 * s), (x + 62 * s, y - 12 * s),
               (x + 48 * s, y + 8 * s)], fill=color)
    d.polygon([(x + 44 * s, y + 18 * s), (x + 60 * s, y + 34 * s), (x + 68 * s, y + 34 * s),
               (x + 56 * s, y + 18 * s)], fill=color)


def draw_chip(d, x, y, s, color):
    d.rectangle([x, y, x + 64 * s, y + 64 * s], fill=color)
    d.rectangle([x + 16 * s, y + 16 * s, x + 48 * s, y + 48 * s], fill=PAPER)
    d.rectangle([x + 26 * s, y + 26 * s, x + 38 * s, y + 38 * s], fill=color)
    for i in range(4):
        px = x + (10 + i * 14) * s
        d.line([(px, y - 12 * s), (px, y)], fill=color, width=4)
        d.line([(px, y + 64 * s), (px, y + 76 * s)], fill=color, width=4)
        py = y + (10 + i * 14) * s
        d.line([(x - 12 * s, py), (x, py)], fill=color, width=4)
        d.line([(x + 64 * s, py), (x + 76 * s, py)], fill=color, width=4)


def draw_virus(d, x, y, s, color):
    d.ellipse([x + 10 * s, y + 10 * s, x + 54 * s, y + 54 * s], fill=color)
    for ang in range(0, 360, 45):
        import math
        cx, cy = x + 32 * s, y + 32 * s
        x2 = cx + 34 * s * math.cos(math.radians(ang))
        y2 = cy + 34 * s * math.sin(math.radians(ang))
        d.line([(cx, cy), (x2, y2)], fill=color, width=5)
        d.ellipse([x2 - 6 * s, y2 - 6 * s, x2 + 6 * s, y2 + 6 * s], fill=color)
    d.ellipse([x + 24 * s, y + 24 * s, x + 40 * s, y + 40 * s], fill=WHITE)


def draw_tanker(d, x, y, s, color):
    d.polygon([(x, y + 26 * s), (x + 96 * s, y + 26 * s), (x + 84 * s, y + 46 * s),
               (x + 12 * s, y + 46 * s)], fill=color)
    d.rectangle([x + 14 * s, y + 6 * s, x + 34 * s, y + 26 * s], fill=RED)
    d.rectangle([x + 40 * s, y + 12 * s, x + 58 * s, y + 26 * s], fill=GOLD)
    for wx in range(0, 110, 26):
        d.arc([x + wx * s, y + 52 * s, x + (wx + 22) * s, y + 66 * s], 200, 340, fill=TEAL, width=3)
    d.ellipse([x + 96 * s, y - 22 * s, x + 108 * s, y - 10 * s], fill=INK)
    d.line([(x + 92 * s, y - 16 * s), (x + 112 * s, y - 16 * s)], fill=INK, width=3)


def draw_aid(d, x, y, s, color):
    d.rectangle([x, y + 14 * s, x + 78 * s, y + 58 * s], fill=color)
    d.polygon([(x, y + 14 * s), (x + 18 * s, y - 6 * s), (x + 60 * s, y - 6 * s), (x + 78 * s, y + 14 * s)], fill=GREEN)
    d.rectangle([x + 36 * s, y + 22 * s, x + 42 * s, y + 52 * s], fill=RED)
    d.rectangle([x + 26 * s, y + 32 * s, x + 52 * s, y + 38 * s], fill=RED)


def draw_pin(d, x, y, s, color):
    d.ellipse([x + 12 * s, y, x + 60 * s, y + 48 * s], fill=color)
    d.polygon([(x + 18 * s, y + 38 * s), (x + 54 * s, y + 38 * s), (x + 36 * s, y + 72 * s)], fill=color)
    d.ellipse([x + 26 * s, y + 14 * s, x + 46 * s, y + 34 * s], fill=WHITE)


def draw_globe(d, x, y, s, color):
    d.ellipse([x, y, x + 64 * s, y + 64 * s], fill=(191, 219, 254), outline=color, width=4)
    d.ellipse([x + 12 * s, y + 12 * s, x + 34 * s, y + 30 * s], fill=GREEN)
    d.ellipse([x + 36 * s, y + 34 * s, x + 54 * s, y + 52 * s], fill=GREEN)
    d.arc([x + 8 * s, y + 4 * s, x + 56 * s, y + 60 * s], 300, 60, fill=color, width=3)


def draw_bond(d, x, y, s, color):
    d.rectangle([x, y, x + 64 * s, y + 64 * s], fill=INK)
    d.text((x + 32 * s, y + 30 * s), "007", font=font(SANS_B, int(20 * s)), fill=GOLD, anchor="mm")
    d.rectangle([x, y + 52 * s, x + 64 * s, y + 56 * s], fill=GOLD)


def draw_flame(d, x, y, s, color):
    d.polygon([(x + 32 * s, y), (x + 52 * s, y + 28 * s), (x + 58 * s, y + 52 * s),
               (x + 32 * s, y + 64 * s), (x + 6 * s, y + 52 * s), (x + 12 * s, y + 28 * s)], fill=color)
    d.ellipse([x + 22 * s, y + 34 * s, x + 42 * s, y + 54 * s], fill=(253, 224, 130))


# ---------- world map (stylised, equirectangular) ----------
# continents as rough polygons in map-box coordinates (0..620 x 0..150)
CONTINENTS = [
    # North America
    [(18, 18), (120, 8), (168, 22), (150, 48), (118, 58), (96, 44), (60, 52), (28, 44), (8, 30)],
    # South America
    [(118, 78), (150, 72), (168, 92), (152, 132), (128, 118), (112, 92)],
    # Europe
    [(292, 22), (340, 10), (372, 22), (360, 44), (322, 48), (296, 38)],
    # Africa
    [(296, 62), (340, 56), (372, 72), (362, 112), (330, 128), (306, 100)],
    # Asia
    [(378, 12), (500, 6), (590, 20), (580, 58), (520, 72), (470, 58), (430, 66), (392, 48)],
    # Australia
    [(500, 112), (556, 106), (566, 126), (520, 138), (496, 126)],
]
# (lon, lat, label) pins -> map coords computed in code
PINS = [
    (-100, 48, "1"),   # US measles / outages
    (28, -26, "2"),    # South Africa shootings
    (30, 55, "3"),     # Kerch / Ukraine
    (50, 26, "4"),     # Bahrain / Gulf
    (124, 11, "5"),    # Manila
    (110, 30, "6"),    # Shenzhen
    (139, 36, "7"),    # Japan
    (105, 47, "8"),    # Mongolia
    (35, 31, "9"),     # Gaza
    (-5, 50, "10"),    # Europe hoax threats
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(219, 234, 254))
    # graticule
    for gx in range(x0, x0 + w + 1, w // 6):
        d.line([(gx, y0), (gx, y0 + h)], fill=(191, 219, 254), width=1)
    for gy in range(y0, y0 + h + 1, h // 3):
        d.line([(x0, gy), (x0 + w, gy)], fill=(191, 219, 254), width=1)
    sx, sy = w / 620.0, h / 150.0
    for poly in CONTINENTS:
        pts = [(x0 + px * sx, y0 + py * sy) for px, py in poly]
        d.polygon(pts, fill=(148, 163, 184), outline=(71, 85, 105))
    for lon, lat, label in PINS:
        px = x0 + (lon + 180) / 360.0 * w
        py = y0 + (90 - lat) / 180.0 * h
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED, outline=WHITE, width=2)
        d.text((px, py), label, font=font(SANS_B, 13), fill=WHITE, anchor="mm")


# ---------- data: 30 distinct stories ----------
# grid stories: (kicker, color, icon, headline, deck)
GRID = [
    ("GULF ON EDGE", RED, draw_tanker,
     "IRAN DRONES HIT US RADAR",
     "Bahrain says it was intercepted; US jets hit Qeshm Island."),
    ("ASIA", TEAL, draw_plane,
     "JAPAN SCRAMBLES JETS",
     "Two Russian planes near Fukuoka for five minutes."),
    ("MONGOLIA", PURPLE, draw_pin,
     "PRESIDENT QUITS OVER $25M RAILWAY BRIBE CLAIM",
     "Khurelsukh quits; parliament must still approve it."),
    ("GAZA", GREEN, draw_aid,
     "WINTER RAINS FLOOD GAZA SHELTERS AS AID LAGS",
     "UN warns of hypothermia; West urges crossings open."),
    ("EUROPE", PURPLE, draw_pin,
     "FIVE EU STATES PLAN RWANDA HUB",
     "Five states plan the hub; UN rights chief alarmed."),
    ("CLIMATE", TEAL, draw_globe,
     "COP31 SPLIT OVER FOSSIL FUELS",
     "Hoekstra pushes clean energy; talks split on fossil fuels."),
    ("HEALTH", RED, draw_virus,
     "EBOLA IN CONGO TOPS 11,000 CASES, 5,568 DEAD",
     "WHO: cases more than doubled in three months."),
    ("EUROPE", ORANGE, draw_flame,
     "8,000+ HOAX THREATS HIT EUROPE",
     "Reuters: schools and airports hit; foreign links probed."),
    ("UKRAINE", RED, draw_flame,
     "UKRAINE'S DEADLIEST MONTH",
     "UN: 372 killed, 1,981 injured in October alone."),
    ("TECH", SLATE, draw_chip,
     "CHASE BUG DELAYS PAYMENTS ACROSS US BANKS",
     "Glitch hits Chase, BofA, Wells Fargo and Zelle."),
    ("CULTURE", GOLD, draw_bond,
     "PATTINSON IS THE NEXT 007",
     "Amazon MGM confirms it; Bezos helped pick him."),
    ("BLACK SEA", TEAL, draw_tanker,
     "LPG TANKER SINKS OFF BULGARIA",
     "Gas Husky sinks in the Black Sea; 19 crew rescued."),
]

# numbers box: 6 further distinct stories
NUMBERS = [
    ("1,441", "drones in Ukraine air attacks"),
    ("Storm watch", "Florida floods; Sierra snow threats"),
    ("Dirty-bomb claim", "US intel alleges Iran plot"),
    ("Megaspeed probe", "US chip-diversion inquiry began in 2024"),
    ("Brazil warning", "Tax reform may lift prices"),
    ("Australia backflip", "More backpackers for regions"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 104, W, 108], fill=GOLD)
    d.text((W // 2, 10), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52), fill=WHITE, anchor="ma")
    d.text((W // 2, 70), "TUESDAY  17  NOVEMBER  2026  •  30 STORIES FROM EVERY CONTINENT",
           font=font(SANS_B, 20), fill=GOLD, anchor="ma")

    # ---- lead: Kerch Bridge ----
    card(d, [24, 120, 1000, 322])
    draw_bridge_scene(d, 40, 136, 556, 306)
    d.text((48, 142), "KERCH STRAIT  •  UKRAINE", font=font(SANS_B, 15), fill=NAVY)
    tx = 576
    kicker(d, (tx, 132), "LEAD STORY — UKRAINE / RUSSIA", RED, 16)
    d.text((tx, 154), "THE BRIDGE", font=font(SANS_B, 40), fill=INK)
    d.text((tx, 196), "FALLS", font=font(SANS_B, 40), fill=RED)
    para(d, (tx, 240), "Ukraine strike collapses the road arch of the Kerch Bridge to Crimea.",
         font(SANS_B, 18), 408, leading=22, max_lines=2)
    para(d, (tx, 286), "Zelensky hails an “unprecedented” 7-stage operation. Two killed; road halted, rail resumes.",
         font(SANS, 13), 408, fill=MUTED, leading=15, max_lines=2)

    # ---- map + numbers ----
    card(d, [24, 332, 668, 512])
    d.text((40, 342), "THE DAY ON THE MAP — 10 FLASHPOINTS", font=font(SANS_B, 16), fill=NAVY)
    draw_map(d, 40, 366, 612, 132)
    d.text((40, 502), "1 US   2 S. Africa   3 Kerch   4 Bahrain   5 Manila   6 Shenzhen   7 Japan   8 Mongolia   9 Gaza   10 Europe",
           font=font(SANS, 11), fill=MUTED)
    card(d, [680, 332, 1000, 512], fill=(15, 42, 74), outline=NAVY)
    d.text((696, 342), "THE DAY IN NUMBERS", font=font(SANS_B, 16), fill=GOLD)
    y = 368
    for big, small in NUMBERS:
        bf = font(SANS_B, 14)
        d.text((696, y), big, font=bf, fill=GOLD)
        bw = d.textlength(big, font=bf)
        para(d, (696 + bw + 8, y + 1), small, font(SANS, 12), 1000 - 696 - bw - 16, fill=(226, 232, 240), leading=14, max_lines=1)
        y += 22

    # ---- featured row: 3 stories ----
    feat = [
        ("TRUMP IN ASIA", TEAL, draw_plane,
         "TRUMP LANDS IN MANILA",
         "First Quad meeting in two years; then Shenzhen for Xi and Putin talks."),
        ("CHIP WAR", SLATE, draw_chip,
         "NVIDIA BEATS FORECAST",
         "Revenue $115.8bn, up 103%. Board rules out Huang's return; Kress leads as interim CEO."),
        ("HEALTH", RED, draw_virus,
         "US LOSES MEASLES-FREE STATUS",
         "PAHO: 5,412 cases in 2026, the most in 35 years. Mexico and Bolivia lose status too."),
    ]
    x = 24
    for kick, color, icon, head, cap in feat:
        card(d, [x, 522, x + 322, 652])
        d.rectangle([x, 522, x + 322, 530], fill=color)
        kicker(d, (x + 14, 538), kick, color, 15)
        icon(d, x + 14, 562, 0.62, color)
        para(d, (x + 96, 562), head, font(SANS_B, 17), 214, leading=21, max_lines=2)
        para(d, (x + 14, 620), cap, font(SANS, 12), 294, fill=MUTED, leading=15, max_lines=2)
        x += 334

    # ---- grid: 12 more stories ----
    d.text((24, 662), "MORE OF THE DAY", font=font(SANS_B, 17), fill=NAVY)
    d.line([(200, 672), (1000, 672)], fill=GOLD, width=3)
    gx0, gy0 = 24, 682
    cw, ch, gapx, gapy = 322, 58, 12, 8
    for i, (kick, color, icon, head, deck) in enumerate(GRID):
        col, row = i % 3, i // 3
        x = gx0 + col * (cw + gapx)
        y = gy0 + row * (ch + gapy)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=LINE, width=1)
        d.rectangle([x, y, x + 5, y + ch], fill=color)
        kicker(d, (x + 12, y + 4), kick, color, 11)
        para(d, (x + 12, y + 20), head, font(SANS_B, 14), cw - 24, leading=16, max_lines=1)
        para(d, (x + 12, y + 38), deck, font(SANS, 11), cw - 24, fill=MUTED, leading=13, max_lines=1)

    # ---- footer ticker ----
    d.rectangle([0, 946, W, 1024], fill=NAVY)
    para(d, (24, 950), "ALSO ON 17 NOV:  Trump signs a Thailand trade deal  •  Saudi Arabia, Qatar, Jordan and Egypt condemn the Iran attack  •  17 killed in two shootings in South Africa  •  30,000 flee Ethiopia for Kenya  •  India beats Pakistan 2–1 for the SAFF title  •  Turkish police raid an opposition TV station  •  NSA's classified network goes down  •  Apple iCloud and App Store hit by an outage",
         font(SANS_B, 13), 976, fill=WHITE, leading=17, max_lines=3)
    d.text((24, 1006), "Drawn from reporting by BBC, Reuters, AP, CNN, Al Jazeera and UN News on 17 November 2026  •  30 stories",
           font=font(SANS, 12), fill=(148, 163, 184))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
