# Wednesday 25 November 2026 - THE WORLD IN ONE DAY
# A one-page newspaper front page drawn entirely with the Python standard
# library. Every shape and letter is drawn by this program itself: filled
# rectangles, lines, circles and a small 5x7 bitmap letter set below.
# No image files, no fonts from disk, no network, no wall-clock time and
# no randomness: two runs produce byte-identical output.
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (250, 248, 240)
INK = (18, 18, 24)
NAVY = (16, 36, 74)
NAVY2 = (28, 58, 110)
RED = (178, 32, 32)
WHITE = (255, 255, 255)
LGREY = (238, 240, 244)
MGREY = (120, 124, 132)
DGREY = (70, 72, 80)
ORANGE = (232, 116, 24)
YELLOW = (244, 196, 48)
GOLD = (212, 160, 32)
SKY = (178, 208, 232)
PALE = (246, 236, 200)
GREEN = (34, 120, 60)
TEAL = (24, 120, 116)
BROWN = (120, 72, 32)

# 5 wide x 7 tall bitmap letters. '#' is ink, '.' is blank.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy), 1)
        for s in range(steps + 1):
            x = x0 + dx * s // steps
            y = y0 + dy * s // steps
            self.rect(x - t // 2, y - t // 2, t, t, c)

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def ring(self, cx, cy, r, c, t=2):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d <= r * r:
                    self.set(xx, yy, c)

    def triangle(self, x0, y0, x1, y1, x2, y2, c):
        # Scanline fill of one triangle.
        ys = sorted([y0, y1, y2])
        for y in range(ys[0], ys[2] + 1):
            xs = []
            for (ax, ay, bx, by) in ((x0, y0, x1, y1), (x1, y1, x2, y2), (x2, y2, x0, y0)):
                if ay == by:
                    continue
                if min(ay, by) <= y < max(ay, by) or (y == ys[2] and y == max(ay, by)):
                    xs.append(ax + (bx - ax) * (y - ay) // (by - ay))
            if len(xs) >= 2:
                self.hline(min(xs), y, max(xs) - min(xs) + 1, c)

    def text(self, s, x, y, scale, c, bold=False):
        adv = 5 * scale + 1
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                cx += adv
                continue
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '1':
                        bx = cx + col * scale
                        by = y + r * scale
                        self.rect(bx, by, scale, scale, c)
                        if bold:
                            self.rect(bx + scale, by, 1, scale, c)
            cx += adv
        return cx

    def text_w(self, s, scale):
        return len(s) * (5 * scale + 1) - 1

    def text_center(self, s, cx, y, scale, c, bold=False):
        self.text(s, cx - self.text_w(s, scale) // 2, y, scale, c, bold)


def png_bytes(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]

    def chunk(kind, data):
        out = struct.pack('>I', len(data)) + kind + data
        out += struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(bytes(raw), 6))
            + chunk(b'IEND', b''))


def flame(cv, x, y, s):
    # A stylised flame: stacked triangles, yellow core, orange, red base.
    cv.triangle(x, y, x + s // 2, y - s, x + s, y, YELLOW)
    cv.triangle(x + s // 4, y, x + s // 2, y - s // 2, x + 3 * s // 4, y, ORANGE)
    cv.triangle(x + s // 3, y, x + s // 2, y - s // 3, x + 2 * s // 3, y, RED)


def smoke(cv, x, y, r, c=MGREY):
    cv.circle(x, y, r, c)
    cv.circle(x + r, y - r // 2, r * 3 // 4, c)
    cv.circle(x - r, y - r // 3, r * 2 // 3, c)


def draw_lead1(cv, x, y, w, h):
    # Tariffs: bar chart rising to 40%.
    cv.rect(x, y, w, h, SKY)
    cv.rect(x, y + h - 14, w, 4, INK)
    bars = [18, 32, 50, 72]
    bw = 34
    gap = 14
    bx = x + 16
    for i, bh in enumerate(bars):
        col = RED if i == 3 else NAVY2
        cv.rect(bx + i * (bw + gap), y + h - 14 - bh, bw, bh, col)
    cv.text("40%", x + w - 78, y + 8, 3, RED, bold=True)
    cv.text("TARIFFS", x + 14, y + 8, 2, NAVY, bold=True)


def draw_lead2(cv, x, y, w, h):
    # Cairo tanker fire: tanker, flames, smoke over a ring road.
    cv.rect(x, y, w, h, (52, 40, 36))
    cv.rect(x, y + h - 16, w, 16, (30, 30, 34))
    cv.rect(x, y + h - 20, w, 4, YELLOW)
    smoke(cv, x + w // 2, y + 22, 12)
    smoke(cv, x + w // 2 + 34, y + 14, 9)
    # Tanker body and cab.
    cv.rect(x + 40, y + 52, 150, 22, (200, 200, 205))
    cv.rect(x + 190, y + 56, 44, 18, (180, 60, 40))
    cv.rect(x + 196, y + 60, 14, 8, SKY)
    cv.circle(x + 70, y + 76, 8, INK)
    cv.circle(x + 150, y + 76, 8, INK)
    cv.circle(x + 208, y + 76, 8, INK)
    flame(cv, x + 70, y + 52, 26)
    flame(cv, x + 130, y + 52, 20)
    flame(cv, x + 196, y + 56, 18)


def draw_lead3(cv, x, y, w, h):
    # Ras Tanura refinery and a Riyadh tower.
    cv.rect(x, y, w, h, PALE)
    smoke(cv, x + 70, y + 18, 11)
    smoke(cv, x + 120, y + 12, 8)
    # Refinery towers and pipes.
    cv.rect(x + 30, y + 34, 18, 52, NAVY2)
    cv.rect(x + 56, y + 22, 18, 64, NAVY2)
    cv.rect(x + 82, y + 42, 18, 44, NAVY2)
    cv.rect(x + 24, y + 30, 84, 6, DGREY)
    cv.rect(x + 24, y + 62, 84, 6, DGREY)
    flame(cv, x + 56, y + 22, 14)
    # Tower block on the right.
    cv.rect(x + 200, y + 10, 52, 76, (90, 96, 110))
    for r in range(4):
        for col in range(3):
            cv.rect(x + 208 + col * 15, y + 18 + r * 16, 9, 9, YELLOW)


def draw_sec_kyiv(cv, x, y, w, h):
    cv.rect(x, y, w, h, (24, 32, 64))
    cv.rect(x + 12, y + 22, 26, 30, (70, 76, 96))
    cv.rect(x + 46, y + 14, 30, 38, (90, 96, 116))
    cv.rect(x + 84, y + 26, 24, 26, (70, 76, 96))
    cv.circle(x + 130, y + 16, 7, YELLOW)
    cv.circle(x + 130, y + 16, 3, ORANGE)
    cv.line(x + 118, y + 4, x + 142, y + 28, YELLOW, 2)
    cv.line(x + 142, y + 4, x + 118, y + 28, YELLOW, 2)
    cv.line(x + 130, y + 2, x + 130, y + 30, YELLOW, 2)


def draw_sec_rocket(cv, x, y, w, h):
    cv.rect(x, y, w, h, (10, 16, 48))
    for sx, sy in ((14, 8), (60, 14), (120, 6), (160, 18), (40, 30), (150, 34)):
        cv.rect(x + sx, y + sy, 2, 2, WHITE)
    cv.rect(x + 84, y + 8, 16, 26, WHITE)
    cv.triangle(x + 84, y + 8, x + 92, y - 2, x + 100, y + 8, RED)
    cv.rect(x + 78, y + 26, 6, 8, RED)
    cv.rect(x + 100, y + 26, 6, 8, RED)
    flame(cv, x + 86, y + 40, 12)


def draw_sec_cartagena(cv, x, y, w, h):
    cv.rect(x, y, w, h, (214, 232, 220))
    cv.rect(x + 20, y + 14, 144, 30, (180, 60, 50))
    for i in range(6):
        cv.rect(x + 20 + i * 24, y + 14, 12, 30, WHITE if i % 2 == 0 else (180, 60, 50))
    cv.rect(x + 20, y + 44, 144, 8, DGREY)
    cv.rect(x + 76, y + 30, 32, 22, NAVY)
    cv.text("76", x + 84, y + 32, 2, WHITE, bold=True)


def draw_sec_solomon(cv, x, y, w, h):
    cv.rect(x, y, w, h, (150, 200, 228))
    cv.rect(x, y + 34, w, 18, (24, 110, 160))
    cv.circle(x + 150, y + 12, 8, YELLOW)
    cv.circle(x + 60, y + 46, 18, GREEN)
    cv.rect(x + 58, y + 18, 4, 24, BROWN)
    cv.line(x + 60, y + 18, x + 44, y + 10, GREEN, 3)
    cv.line(x + 60, y + 18, x + 76, y + 10, GREEN, 3)
    cv.line(x + 60, y + 16, x + 60, y + 6, GREEN, 3)


def draw_sec_tech(cv, x, y, w, h):
    cv.rect(x, y, w, h, WHITE)
    bars = [34, 28, 22, 16]
    for i, bh in enumerate(bars):
        cv.rect(x + 16 + i * 40, y + h - 8 - bh, 24, bh, NAVY2)
    cv.line(x + 14, y + 10, x + 60, y + 22, RED, 3)
    cv.line(x + 60, y + 22, x + 106, y + 30, RED, 3)
    cv.line(x + 106, y + 30, x + 152, y + 44, RED, 3)
    cv.triangle(x + 152, y + 44, x + 140, y + 38, x + 152, y + 34, RED)


def lead_panel(cv, x, y, w, h, art, kicker, heads, summ, srcs):
    cv.rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, 3, NAVY)
    cv.rect(x, y, 3, h, NAVY)
    cv.rect(x + w - 3, y, 3, h, NAVY)
    cv.rect(x, y + h - 3, w, 3, NAVY)
    art(cv, x + 8, y + 8, w - 16, 88)
    cv.text(kicker, x + 10, y + 104, 2, RED, bold=True)
    hy = y + 124
    for ln in heads:
        cv.text(ln, x + 10, hy, 3, INK, bold=True)
        hy += 23
    sy = y + 198
    for ln in summ:
        cv.text(ln, x + 10, sy, 2, INK)
        sy += 14
    sy = y + 230
    for ln in srcs:
        cv.text(ln, x + 10, sy, 2, MGREY)
        sy += 13


def sec_panel(cv, x, y, w, h, art, kicker, heads, summ, srcs):
    cv.rect(x, y, w, h, LGREY)
    cv.rect(x, y, w, 2, NAVY2)
    cv.rect(x, y, 2, h, NAVY2)
    cv.rect(x + w - 2, y, 2, h, NAVY2)
    cv.rect(x, y + h - 2, w, 2, NAVY2)
    art(cv, x + 6, y + 6, w - 12, 52)
    cv.text(kicker, x + 8, y + 64, 2, RED, bold=True)
    hy = y + 82
    for ln in heads:
        cv.text(ln, x + 8, hy, 2, INK, bold=True)
        hy += 15
    sy = y + 116
    for ln in summ:
        cv.text(ln, x + 8, sy, 2, INK)
        sy += 14
    sy = y + 162
    for ln in srcs:
        cv.text(ln, x + 8, sy, 2, MGREY)
        sy += 13


def build():
    cv = Canvas(W, H, PAPER)
    # Top strip.
    cv.rect(0, 0, W, 34, NAVY)
    cv.text("THE WORLD IN ONE DAY", 14, 10, 2, WHITE, bold=True)
    right = "8 STORIES, 8 REGIONS, EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    cv.text(right, W - 14 - cv.text_w(right, 2), 10, 2, WHITE, bold=True)
    # Masthead: the date, the biggest text on the page.
    cv.text_center("Wednesday 25 November 2026", W // 2, 46, 6, NAVY, bold=True)
    cv.hline(60, 98, W - 120, RED, 3)
    # One-sentence summary of the three leads.
    cv.text_center("US tariffs hit 40%, Cairo tanker fire kills 30+, Houthis claim Ras Tanura.",
                   W // 2, 108, 2, INK)
    # Numbers strip: six big figures.
    nums = [
        ("40%", "TOP TARIFF", "ON CHINA"),
        ("30+", "KILLED IN", "CAIRO FIRE"),
        ("76", "HOSTAGES", "FREED"),
        ("490,334", "RUSSIAN DEAD", "(BBC COUNT)"),
        ("36%", "BANGLADESH", "WAGE RISE"),
        ("19", "KILLED IN", "SUDAN DRONES"),
    ]
    nx = 12
    nw = 162
    for fig, l1, l2 in nums:
        cv.rect(nx, 126, nw, 66, NAVY)
        cv.text_center(fig, nx + nw // 2, 130, 4, WHITE, bold=True)
        cv.text_center(l1, nx + nw // 2, 162, 2, (200, 210, 230))
        cv.text_center(l2, nx + nw // 2, 177, 2, (200, 210, 230))
        nx += nw + 6
    # Region bar.
    cv.rect(12, 198, 1000, 24, LGREY)
    cv.text_center("NORTH AMERICA | AFRICA | MIDDLE EAST | EUROPE | ASIA | LATIN AMERICA | OCEANIA | GLOBAL",
                   W // 2, 203, 2, NAVY, bold=True)
    # Three lead panels.
    leads = [
        (draw_lead1, "NORTH AMERICA - TRADE",
         ["NEW US TARIFFS", "UP TO 40%", "ON CHINA"],
         ["14 partners hit; India 25%,", "EU rejects, Brazil objects."],
         ["(NPR, France 24, CNBC)"]),
        (draw_lead2, "AFRICA - CAIRO",
         ["CAIRO TANKER", "FIRE KILLS", "AT LEAST 30"],
         ["Tanker overturns; 27 vehicles", "burn; 21 hurt, toll may rise."],
         ["(BBC, Al Jazeera, Guardian)"]),
        (draw_lead3, "MIDDLE EAST - SAUDI ARABIA",
         ["HOUTHIS CLAIM", "RAS TANURA", "REFINERY HIT"],
         ["Coalition says missiles shot", "down; oil up 2%. Claim only."],
         ["(CBC, Asharq Al-Awsat,", "CNBC, Reuters)"]),
    ]
    lx = 12
    for art, kick, heads, summ, srcs in leads:
        lead_panel(cv, lx, 230, 328, 260, art, kick, heads, summ, srcs)
        lx += 328 + 8
    # Five secondary panels.
    secs = [
        (draw_sec_kyiv, "EUROPE - KYIV",
         ["RUSSIA HITS KYIV", "WITH MISSILES"],
         ["Shopping centre", "hit; 7 killed", "by drones."],
         ["(Straits Times,", "Le Monde,", "Euronews)"]),
        (draw_sec_rocket, "ASIA - SPACE",
         ["SHENZHOU-24", "LAUNCHES"],
         ["First Pakistani", "in orbit; 90+", "tests, 5 days."],
         ["(Guardian, BBC,", "Euronews)"]),
        (draw_sec_cartagena, "LATIN AMERICA",
         ["ALL 76 HOSTAGES", "FREED"],
         ["Troops storm", "shop; siege", "ends, 76 free."],
         ["(BBC, Guardian,", "ANSA)"]),
        (draw_sec_solomon, "OCEANIA",
         ["SOLOMONS PICK", "AUSTRALIA"],
         ["Treaty names", "Australia No.1;", "ends China pact."],
         ["(RNZ, Japan", "Times, NBC)"]),
        (draw_sec_tech, "GLOBAL - MARKETS",
         ["TECH STOCKS", "TUMBLE"],
         ["Nikkei -2.8%;", "Nvidia -7%;", "Nasdaq -4%."],
         ["(BBC, CNBC)"]),
    ]
    sx = 12
    for art, kick, heads, summ, srcs in secs:
        sec_panel(cv, sx, 498, 196, 210, art, kick, heads, summ, srcs)
        sx += 196 + 8
    # Also on.
    cv.text("ALSO ON - WEDNESDAY 25 NOVEMBER 2026", 12, 718, 2, NAVY, bold=True)
    cv.hline(12, 734, 1000, NAVY, 2)
    also = [
        "POLAND NO-FLY ZONE on Ukraine border; presses for permanent US troops.",
        "BENGHAZI: 2 Libyan officers die of wounds from Ukraine strike on Merkury.",
        "SUDAN: RSF drones kill 19 in Blue Nile; 20+ wounded.",
        "GAZA: Israeli strike kills Hamas security chief, wife and 2 daughters.",
        "INDONESIA: 26-29 miners trapped by floodwater in West Java gold mine.",
        "SHANGHAI: party chief Chen Jining probed; 4th Politburo member since 2025.",
    ]
    ay = 742
    for ln in also:
        cv.text("- " + ln, 12, ay, 2, INK)
        ay += 15
    # Date check box: stories left out because they are NOT 25 November.
    cv.rect(12, 840, 1000, 104, WHITE)
    cv.rect(12, 840, 1000, 3, RED)
    cv.rect(12, 941, 1000, 3, RED)
    cv.rect(12, 840, 3, 104, RED)
    cv.rect(1009, 840, 3, 104, RED)
    cv.text_center("DATE CHECK - LEFT OUT ON PURPOSE: NOT 25 NOVEMBER", W // 2, 850, 2, RED, bold=True)
    left = [
        "Sparta II confirmed - Mon 24 Nov",
        "Huawei guilty verdict - Tue 24 Nov",
        "CIA breach first reported - 24 Nov",
        "Giuliani medal - Tue 24 Nov",
    ]
    right_items = [
        "COP31 ends, no deal - Sun 22 Nov",
        "Merkury sinking - Sun 22 Nov",
        "Riyadh tower strike, 11 hurt - Tue 24 Nov",
    ]
    dy = 872
    for ln in left:
        cv.text("x " + ln, 24, dy, 2, INK)
        dy += 16
    dy = 872
    for ln in right_items:
        cv.text("x " + ln, 524, dy, 2, INK)
        dy += 16
    # Footer.
    cv.text_center("Every story here happened, or was first reported, on Wednesday 25 November 2026.",
                   W // 2, 956, 2, INK)
    cv.text_center("Officials' counts are attributed. Sources named beside each story. Original drawings.",
                   W // 2, 972, 2, INK)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(build())
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
