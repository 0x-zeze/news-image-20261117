#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Runs offline with Pillow + DejaVu fonts only. Every story below was
reported on Tuesday 17 November 2026 (BBC, Reuters, Le Monde, Al Jazeera).
The entry program (main.ts) ships the finished PNG; this script is the
drawing tool that produced it, kept in the repo for transparency.
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
SKY = (178, 205, 225)
SEA = (23, 84, 110)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
MUTED = (75, 85, 99)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
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


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def card(draw, box, fill=CARD, outline=(203, 213, 225), width=2):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def kicker(draw, xy, text, color):
    draw.text(xy, text, font=font(SANS_B, 19), fill=color)


def draw_bridge_scene(d, x0, y0, x1, y1):
    """Kerch Strait: intact arch left, collapsed arch right, smoke, sea."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun
    d.ellipse([x1 - 92, y0 + 18, x1 - 38, y0 + 72], fill=(253, 224, 130), outline=(240, 180, 60), width=3)
    # clouds
    for cx, cy in [(x0 + 60, y0 + 34), (x0 + 150, y0 + 58), (x1 - 210, y0 + 30)]:
        d.ellipse([cx, cy, cx + 74, cy + 22], fill=(255, 255, 255))
        d.ellipse([cx + 18, cy - 10, cx + 62, cy + 14], fill=(255, 255, 255))
    sea_y = y1 - 92
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    # waves
    for wx in range(x0 + 8, x1 - 20, 46):
        d.arc([wx, sea_y + 18, wx + 40, sea_y + 46], 200, 340, fill=(255, 255, 255), width=3)
        d.arc([wx + 10, sea_y + 52, wx + 50, sea_y + 80], 200, 340, fill=(186, 220, 235), width=3)
    deck_y = sea_y - 58
    mid = (x0 + x1) // 2
    # deck: left standing, gap in the middle, right standing
    d.rectangle([x0, deck_y, mid - 78, deck_y + 12], fill=(55, 65, 81))
    d.rectangle([mid + 118, deck_y, x1, deck_y + 12], fill=(55, 65, 81))
    # collapsed deck pieces tilted into the water
    d.polygon([(mid - 78, deck_y), (mid - 18, deck_y + 34), (mid - 30, deck_y + 52), (mid - 92, deck_y + 16)],
              fill=(75, 85, 99))
    d.polygon([(mid + 118, deck_y), (mid + 62, deck_y + 44), (mid + 44, deck_y + 30), (mid + 104, deck_y - 6)],
              fill=(75, 85, 99))
    # piers
    for px in (x0 + 46, x0 + 210, mid + 190, x1 - 60):
        d.rectangle([px, deck_y + 12, px + 12, sea_y + 6], fill=(75, 85, 99))
    # intact arch (left)
    d.arc([x0 + 60, deck_y - 108, x0 + 300, deck_y + 30], 180, 360, fill=(185, 28, 28), width=10)
    # broken arch stubs (right of the gap)
    d.arc([mid + 40, deck_y - 108, mid + 280, deck_y + 30], 300, 360, fill=(185, 28, 28), width=10)
    d.line([(mid + 118, deck_y - 84), (mid + 96, deck_y - 30)], fill=(185, 28, 28), width=10)
    # smoke over the gap
    for sx, sy, sr in [(mid - 20, deck_y - 96, 26), (mid + 18, deck_y - 122, 32),
                       (mid + 58, deck_y - 98, 24), (mid + 2, deck_y - 148, 20)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(107, 114, 128))
        d.ellipse([sx - sr + 8, sy - sr + 6, sx + sr - 6, sy + sr - 4], fill=(156, 163, 175))
    # blast flash at the gap
    d.polygon([(mid + 8, deck_y - 46), (mid + 26, deck_y - 78), (mid + 40, deck_y - 44),
               (mid + 66, deck_y - 66), (mid + 52, deck_y - 30), (mid + 74, deck_y - 18),
               (mid + 40, deck_y - 12), (mid + 22, deck_y + 6), (mid + 10, deck_y - 16)],
              fill=(249, 115, 22))
    # splash where the arch fell
    d.polygon([(mid - 46, sea_y + 6), (mid - 18, sea_y - 22), (mid + 6, sea_y + 4),
               (mid + 34, sea_y - 18), (mid + 62, sea_y + 6)], fill=(255, 255, 255))


def draw_plane(d, x, y, s, color):
    d.polygon([(x, y + 18 * s), (x + 74 * s, y + 18 * s), (x + 92 * s, y + 12 * s),
               (x + 74 * s, y + 8 * s), (x, y + 8 * s)], fill=color)
    d.polygon([(x + 30 * s, y + 8 * s), (x + 52 * s, y - 12 * s), (x + 62 * s, y - 12 * s),
               (x + 48 * s, y + 8 * s)], fill=color)
    d.polygon([(x + 44 * s, y + 18 * s), (x + 60 * s, y + 34 * s), (x + 68 * s, y + 34 * s),
               (x + 56 * s, y + 18 * s)], fill=color)
    d.polygon([(x + 84 * s, y + 10 * s), (x + 96 * s, y + 4 * s), (x + 96 * s, y + 18 * s)], fill=color)


def draw_chip(d, x, y, s, color):
    d.rectangle([x, y, x + 64 * s, y + 64 * s], fill=color)
    d.rectangle([x + 16 * s, y + 16 * s, x + 48 * s, y + 48 * s], fill=(247, 243, 234))
    d.rectangle([x + 26 * s, y + 26 * s, x + 38 * s, y + 38 * s], fill=color)
    for i in range(4):
        px = x + (10 + i * 14) * s
        d.line([(px, y - 12 * s), (px, y)], fill=color, width=4)
        d.line([(px, y + 64 * s), (px, y + 76 * s)], fill=color, width=4)
        py = y + (10 + i * 14) * s
        d.line([(x - 12 * s, py), (x, py)], fill=color, width=4)
        d.line([(x + 64 * s, py), (x + 76 * s, py)], fill=color, width=4)


def draw_tanker(d, x, y, s, color):
    d.polygon([(x, y + 26 * s), (x + 96 * s, y + 26 * s), (x + 84 * s, y + 46 * s),
               (x + 12 * s, y + 46 * s)], fill=color)
    d.rectangle([x + 14 * s, y + 6 * s, x + 34 * s, y + 26 * s], fill=(185, 28, 28))
    d.rectangle([x + 40 * s, y + 12 * s, x + 58 * s, y + 26 * s], fill=(201, 162, 39))
    d.rectangle([x + 64 * s, y + 8 * s, x + 80 * s, y + 26 * s], fill=(14, 116, 144))
    d.line([(x + 88 * s, y + 26 * s), (x + 88 * s, y + 2 * s)], fill=(55, 65, 81), width=4)
    for wx in range(0, 110, 26):
        d.arc([x + wx * s, y + 52 * s, x + (wx + 22) * s, y + 66 * s], 200, 340,
              fill=(14, 116, 144), width=3)
    # drone above
    d.ellipse([x + 96 * s, y - 22 * s, x + 108 * s, y - 10 * s], fill=(17, 24, 39))
    d.line([(x + 92 * s, y - 16 * s), (x + 112 * s, y - 16 * s)], fill=(17, 24, 39), width=3)


def draw_aid(d, x, y, s, color):
    d.rectangle([x, y + 14 * s, x + 78 * s, y + 58 * s], fill=color)
    d.polygon([(x, y + 14 * s), (x + 18 * s, y - 6 * s), (x + 60 * s, y - 6 * s), (x + 78 * s, y + 14 * s)],
              fill=(21, 101, 52))
    d.rectangle([x + 30 * s, y + 26 * s, x + 48 * s, y + 48 * s], fill=(255, 255, 255))
    d.rectangle([x + 36 * s, y + 22 * s, x + 42 * s, y + 52 * s], fill=(185, 28, 28))
    d.rectangle([x + 26 * s, y + 32 * s, x + 52 * s, y + 38 * s], fill=(185, 28, 28))


def draw_pin(d, x, y, s, color):
    d.ellipse([x + 12 * s, y, x + 60 * s, y + 48 * s], fill=color)
    d.polygon([(x + 18 * s, y + 38 * s), (x + 54 * s, y + 38 * s), (x + 36 * s, y + 72 * s)], fill=color)
    d.ellipse([x + 26 * s, y + 14 * s, x + 46 * s, y + 34 * s], fill=(255, 255, 255))


def draw_dots(d, x, y, s, color):
    for dx, dy, r in [(0, 8, 9), (22, 0, 11), (46, 10, 8), (14, 30, 10), (40, 32, 12), (64, 26, 8), (28, 52, 8), (54, 52, 9)]:
        d.ellipse([x + dx * s - r, y + dy * s - r, x + dx * s + r, y + dy * s + r], fill=color)
    d.polygon([(x + 84 * s, y + 2 * s), (x + 104 * s, y + 38 * s), (x + 64 * s, y + 38 * s)],
              outline=(185, 28, 28), width=5)
    d.text((x + 80 * s, y + 14 * s), "!", font=font(SANS_B, 22), fill=(185, 28, 28))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=font(SERIF_B, 56),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 82), "TUESDAY  17  NOVEMBER  2026", font=font(SANS_B, 25),
           fill=GOLD, anchor="ma")

    # ---- lead story: Kerch Bridge ----
    card(d, [24, 136, 1000, 470])
    draw_bridge_scene(d, 40, 152, 596, 454)
    d.text((48, 160), "KERCH STRAIT  •  UKRAINE", font=font(SANS_B, 16), fill=NAVY)
    tx = 620
    kicker(d, (tx, 156), "LEAD STORY — UKRAINE / RUSSIA", RED)
    d.text((tx, 184), "THE BRIDGE", font=font(SANS_B, 46), fill=INK)
    d.text((tx, 232), "FALLS", font=font(SANS_B, 46), fill=RED)
    para(d, (tx, 292), "Ukraine strike collapses the road arch of the Kerch Bridge to Crimea.",
         font(SANS_B, 23), 360, leading=29)
    para(d, (tx, 372), "Zelensky hails an “unprecedented” operation, weeks in the making. Two killed; road and rail traffic halted. The Kremlin vows to rebuild it.",
         font(SANS, 19), 360, fill=MUTED, leading=25)

    # ---- middle row: three stories ----
    mid = [
        ("TRUMP IN ASIA", TEAL, draw_plane,
         "TRUMP OPENS ASIA TOUR IN MANILA",
         "Quad summit at ASEAN; meets Xi and Putin in Shenzhen Thursday."),
        ("CHIP WAR", SLATE, draw_chip,
         "NVIDIA SPY SCANDAL ROCKS CHIP WAR",
         "US closes a chip-export loophole; Huang exits after the scandal."),
        ("GULF ON EDGE", RED, draw_tanker,
         "IRAN DRONES TARGET US BASE",
         "Iran drones hit a US base in Bahrain; attack intercepted."),
    ]
    x = 24
    for kicker_text, color, icon, headline, caption in mid:
        card(d, [x, 482, x + 322, 748])
        d.rectangle([x, 482, x + 322, 490], fill=color)
        kicker(d, (x + 16, 502), kicker_text, color)
        icon(d, x + 118, 546, 1.0, color)
        y = para(d, (x + 16, 622), headline, font(SANS_B, 23), 290, leading=28)
        para(d, (x + 16, y + 4), caption, font(SANS, 16), 290, fill=MUTED, leading=20)
        x += 334

    # ---- bottom row: three stories ----
    bot = [
        ("GAZA", GREEN, draw_aid,
         "WEST URGES ISRAEL: OPEN GAZA CROSSINGS",
         "UK, Australia, Canada and Italy call the aid situation catastrophic."),
        ("EUROPE", PURPLE, draw_pin,
         "FIVE EU STATES PLAN RWANDA RETURN HUB",
         "Austria, Denmark, Germany, Greece and the Netherlands."),
        ("HEALTH", RED, draw_dots,
         "US LOSES MEASLES-FREE STATUS",
         "5,400+ cases and 10 deaths in 2026 — first loss in 26 years."),
    ]
    x = 24
    for kicker_text, color, icon, headline, caption in bot:
        card(d, [x, 760, x + 322, 930])
        kicker(d, (x + 16, 772), kicker_text, color)
        icon(d, x + 16, 802, 0.62, color)
        y = para(d, (x + 104, 802), headline, font(SANS_B, 20), 202, leading=24)
        para(d, (x + 16, max(882, y + 4)), caption, font(SANS, 16), 290, fill=MUTED, leading=20)
        x += 334

    # ---- footer ticker ----
    d.rectangle([0, 942, W, 1024], fill=NAVY)
    para(d, (24, 954), "ALSO ON 17 NOV:  Japan scrambles jets over a Russian airspace violation  •  "
         "Mongolia’s president resigns  •  Russian military plane crash kills 19  •  "
         "Robert Pattinson is the next James Bond",
         font(SANS_B, 17), 976, fill=(255, 255, 255), leading=21)
    d.text((24, 1000), "Drawn from reporting by BBC, Reuters, Le Monde and Al Jazeera on 17 November 2026.",
           font=font(SANS, 13), fill=(148, 163, 184))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
