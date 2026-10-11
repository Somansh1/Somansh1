#!/usr/bin/env python3
"""The Observatory: builds every SVG in assets/ from scratch.

    python scripts/build.py          # build all panels
    python scripts/build.py --check  # run the streak/total self-check only

Deterministic: seeded randomness, and the "last exposure" date comes from the
newest day of the contribution calendar, never the wall clock. Same data in,
same bytes out.
"""
import datetime as dt
import json
import math
import os
import random
import subprocess
import sys
import urllib.request
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
LOGIN = "Somansh1"

SKY0, SKY1, HAZE = "#0c0c0e", "#151517", "#3a2413"
CREAM, DIM, AMBER = "#f4eedd", "#9c988c", "#ffd43b"
CORAL, TEAL, HAIR = "#ff5a45", "#19b5a5", "#2c2b2a"
BLUE, WARM = "#a9c4ff", "#ffd9a0"
PINK, GREEN, GOLD = "#ff7ab6", "#8fd44f", "#e8c27a"
INK, INKDIM, VERM, PARCH, RULE = "#2b2118", "#7a6a55", "#c8401f", "#efe6d0", "#b8a98a"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "ui-sans-serif,system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


# ---------------------------------------------------------------- numbers --
def n(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def sunday_index(d):
    return (d.weekday() + 1) % 7


def stats(days):
    """days: list of (date, count) sorted ascending, one per calendar day."""
    total = sum(c for _, c in days)
    best = (0, None, None)
    run = []
    for d, c in days:
        if c > 0 and (not run or (d - run[-1]).days == 1):
            run.append(d)
        elif c > 0:
            run = [d]
        else:
            run = []
        if len(run) > best[0]:
            best = (len(run), run[0], run[-1])
    # current streak: counts back from the newest day; a zero on the newest
    # day (today, not over yet) does not break it.
    i = len(days) - 1
    if i >= 0 and days[i][1] == 0:
        i -= 1
    cur = []
    while i >= 0 and days[i][1] > 0 and (not cur or (cur[-1] - days[i][0]).days == 1):
        cur.append(days[i][0])
        i -= 1
    current = (len(cur), cur[-1] if cur else None, cur[0] if cur else None)
    busiest = max(days, key=lambda x: (x[1], -x[0].toordinal())) if days else (None, 0)
    per = [0] * 7
    for d, c in days:
        per[sunday_index(d)] += c
    wd = per.index(max(per))
    return dict(total=total, active=sum(1 for _, c in days if c > 0), ndays=len(days), longest=best, current=current, busiest=(busiest[1], busiest[0]),
                weekday=(WEEKDAYS[wd], per[wd]))


def self_check():
    D = dt.date
    counts = [0, 1, 2, 3, 0, 1, 1, 0, 2, 4]
    days = [(D(2024, 1, 1) + dt.timedelta(i), c) for i, c in enumerate(counts)]
    s = stats(days)
    assert s["total"] == 14, s
    assert s["longest"] == (3, D(2024, 1, 2), D(2024, 1, 4)), s
    assert s["current"] == (2, D(2024, 1, 9), D(2024, 1, 10)), s
    assert s["busiest"] == (4, D(2024, 1, 10)), s
    assert s["weekday"] == ("Wednesday", 6), s
    assert s["active"] == 7 and s["ndays"] == 10, s
    days2 = days[:-1] + [(D(2024, 1, 10), 0)]
    assert stats(days2)["current"] == (1, D(2024, 1, 9), D(2024, 1, 9))
    assert stats([(D(2024, 1, 1), 0)])["current"][0] == 0
    print("self-check ok")


# ------------------------------------------------------------------- data --
def fetch_calendar():
    cache = os.path.join(ROOT, "data", "contributions.json")
    q = ("query($l:String!){user(login:$l){contributionsCollection{contributionCalendar"
         "{totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}")
    try:
        tok = os.environ.get("PROFILE_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if tok:
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                json.dumps({"query": q, "variables": {"l": LOGIN}}).encode(),
                {"Authorization": "bearer " + tok, "User-Agent": "observatory-build"})
            raw = urllib.request.urlopen(req, timeout=30).read()
        else:
            raw = subprocess.run(["gh", "api", "graphql", "-f", "query=" + q, "-F", "l=" + LOGIN],
                                 capture_output=True, check=True, timeout=60).stdout
        cal = json.loads(raw)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        assert cal["weeks"]
        text = json.dumps(cal, indent=1) + "\n"
        if not os.path.exists(cache) or open(cache, encoding="utf-8").read() != text:
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            with open(cache, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        print("contributions: fetched")
    except Exception as e:  # never break the build over the network
        print("contributions: fetch failed (%s), using cache" % e)
        with open(cache, encoding="utf-8") as f:
            cal = json.load(f)
    return cal


# ------------------------------------------------------------------ fonts --
class Face:
    def __init__(self, path, loc):
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
        f = TTFont(path)
        instantiateVariableFont(f, loc, inplace=True)
        self.gs, self.cmap = f.getGlyphSet(), f.getBestCmap()
        self.upm, self.hmtx = f["head"].unitsPerEm, f["hmtx"]

    def width(self, text, size, track=0):
        k = size / self.upm
        return sum(self.hmtx[self.cmap[ord(c)]][0] for c in text) * k + track * (len(text) - 1)

    def path(self, text, size, x, y, anchor="start", fill=CREAM, track=0, opacity=None):
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen
        k = size / self.upm
        x0 = x - self.width(text, size, track) * {"start": 0, "middle": .5, "end": 1}[anchor]
        out, cx = [], 0.0
        for ch in text:
            g = self.cmap[ord(ch)]
            if ch != " ":
                pen = SVGPathPen(self.gs, ntos=n)
                self.gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x0 + cx, y)))
                out.append(pen.getCommands())
            cx += self.hmtx[g][0] * k + track
        op = "" if opacity is None else ' opacity="%s"' % opacity
        return '<path fill="%s"%s d="%s"/>' % (fill, op, "".join(out))


FONTS = {}


def face(kind):
    if not FONTS:
        d = os.path.join(ROOT, "fonts")
        FONTS["r"] = Face(os.path.join(d, "Fraunces-var.ttf"), dict(wght=440, opsz=110, SOFT=0, WONK=0))
        FONTS["i"] = Face(os.path.join(d, "Fraunces-Italic-var.ttf"), dict(wght=360, opsz=40, SOFT=0, WONK=1))
        FONTS["rb"] = Face(os.path.join(d, "Fraunces-var.ttf"), dict(wght=400, opsz=22, SOFT=0, WONK=0))
        FONTS["ib"] = Face(os.path.join(d, "Fraunces-Italic-var.ttf"), dict(wght=380, opsz=24, SOFT=0, WONK=0))
    return FONTS[kind]


def text_path(text, size, x, y, anchor="start", italic=False, fill=CREAM, track=0, opacity=None):
    return face("i" if italic else "r").path(text, size, x, y, anchor, fill, track, opacity)


def text_width(text, size, italic=False):
    return face("i" if italic else "r").width(text, size)


# ----------------------------------------------------------------- svg bits --
BASE_CSS = (".m{font-family:%s}.s{font-family:%s}" % (MONO, SANS)
            + ".tw{opacity:1}")


def motion(css):
    return "@media (prefers-reduced-motion:no-preference){%s}" % css


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;')


def svg(w, h, body, title, desc, css="", defs="", bg="url(#sky)", border=True):
    sky = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/>'
           '<stop offset="1" stop-color="%s"/></linearGradient>' % (SKY0, SKY1))
    frame = ('<rect x=".5" y=".5" width="%d" height="%d" rx="13.5" fill="none" stroke="%s"/>'
             % (w - 1, h - 1, HAIR)) if border else ""
    back = '<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
            'aria-labelledby="t d"><title id="t">%s</title><desc id="d">%s</desc><defs>%s'
            '<clipPath id="rr"><rect width="%d" height="%d" rx="14"/></clipPath><style>%s</style></defs>'
            '<g clip-path="url(#rr)">%s%s</g>%s</svg>\n'
            % (w, h, w, h, esc(title), esc(desc), sky + defs, w, h, BASE_CSS + css, back, body, frame))


def mono(x, y, s, size=20, fill=DIM, anchor="start", ls=0, extra=""):
    return ('<text class="m" x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" letter-spacing="%s"%s>%s</text>'
            % (n(x), n(y), size, fill, anchor, ls, extra, s))


def star4(x, y, L, fill=CREAM, w=0.16, cls="", extra=""):
    p = [(0, -L), (L * w, -L * w), (L, 0), (L * w, L * w), (0, L), (-L * w, L * w), (-L, 0), (-L * w, -L * w)]
    d = "M" + "L".join("%s %s" % (n(x + a), n(y + b)) for a, b in p) + "Z"
    return '<path%s fill="%s" d="%s"%s/>' % (' class="%s"' % cls if cls else "", fill, d, extra)


def specks(rnd, count, x0, y0, x1, y1, rmin=.5, rmax=1.3, op0=.25, op1=.7, tw=0):
    out, twl = [], []
    for i in range(count):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r, op = rnd.uniform(rmin, rmax), rnd.uniform(op0, op1)
        if i < tw:
            twl.append('<circle class="tw" style="animation-delay:-%ss;animation-duration:%ss" cx="%s" cy="%s" r="%s" fill="%s"/>'
                       % (n(rnd.uniform(0, 5)), n(rnd.uniform(3, 6)), n(x), n(y), n(r + .4), CREAM))
        else:
            out.append('<circle cx="%s" cy="%s" r="%s" opacity="%s"/>' % (n(x), n(y), n(r), n(op)[:4]))
    return '<g fill="%s">%s</g>' % (CREAM, "".join(out)) + "".join(twl)


TWINKLE_CSS = motion("@keyframes tw{0%,100%{opacity:1}50%{opacity:.25}}.tw{animation:tw 4s ease-in-out infinite}")
SPIN_CSS = "@keyframes spin{to{transform:rotate(360deg)}}@keyframes rspin{to{transform:rotate(-360deg)}}"


# -------------------------------------------------------------------- hero --
def ridge(base, amp, phase, sharp=0.0, bump=None):
    pts = []
    for x in range(-16, 1297, 16):
        t = x / 1280
        v = (.5 * math.sin(t * 4.3 + phase) + .3 * math.sin(t * 9.7 + phase * 2.3)
             + .16 * math.sin(t * 23 + phase * 4.1) + .07 * math.sin(t * 61 + phase * 7))
        if sharp:
            v = v * (1 - sharp) + sharp * (1 - 2 * abs(math.sin(t * 7.1 + phase * 1.7)))
        if bump:
            v += bump[0] * math.exp(-((x - bump[1]) / bump[2]) ** 2)
        pts.append((x, base - amp * v))
    return pts


def ridge_y(pts, x):
    i = max(0, min(len(pts) - 2, int((x + 16) // 16)))
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def ridge_path(pts):
    return "M" + "L".join("%s %s" % (n(x), n(y)) for x, y in pts) + "L1296 520L-16 520Z"


def pine(x, y, h, fill):
    w = h * .26
    d = "M%s %sL%s %sL%s %s" % (n(x), n(y - h), n(x - w * .55), n(y - h * .62), n(x - w * .25), n(y - h * .62))
    d += "L%s %sL%s %sL%s %s" % (n(x - w * .8), n(y - h * .28), n(x - w * .3), n(y - h * .28), n(x - w), n(y - h * .02))
    d += "L%s %sL%s %sL%s %sL%s %s" % (n(x + w), n(y - h * .02), n(x + w * .3), n(y - h * .28), n(x + w * .8), n(y - h * .28), n(x + w * .25), n(y - h * .62))
    d += "L%s %sZ" % (n(x + w * .55), n(y - h * .62))
    return '<path d="%s" fill="%s"/>' % (d, fill)


def telescope(x, y, fill):
    return ('<g fill="%s" stroke="%s" stroke-linecap="round">'
            '<path d="M%s %sL%s %sM%s %sL%s %sM%s %sL%s %s" stroke-width="2.6" fill="none"/>'
            '<path d="M%s %sL%s %sM%s %sL%s %s" stroke-width="1.4" fill="none"/>'
            '<rect x="%s" y="%s" width="12" height="9" rx="2" stroke="none"/>'
            '<g transform="translate(%s %s) rotate(-50)" stroke="none">'
            '<rect x="-26" y="-6" width="84" height="12" rx="2"/><rect x="48" y="-8.5" width="20" height="17" rx="2"/>'
            '<rect x="2" y="-13" width="26" height="5" rx="1.5"/><rect x="-34" y="-3" width="10" height="6" rx="1"/></g></g>'
            % (fill, fill,
               n(x), n(y - 40), n(x - 27), n(y), n(x), n(y - 40), n(x + 25), n(y), n(x), n(y - 40), n(x + 3), n(y),
               n(x - 14), n(y - 14), n(x + 14), n(y - 14), n(x - 13), n(y - 1), n(x + 13), n(y - 1),
               n(x - 6), n(y - 48), n(x), n(y - 43)))


def hero():
    R = random.Random(11)
    PX, PY = 880, 210
    wpick = [CREAM] * 11 + [WARM] * 4 + [BLUE]
    arcs = []
    for _ in range(175):
        r = 16 + 900 * R.random() ** 1.2
        L = R.choice([R.uniform(10, 40)] * 5 + [R.uniform(40, 90)] * 3 + [R.uniform(90, 170)])
        a0 = R.uniform(0, 360)
        b = R.random() ** 2.2
        arcs.append((b, r, a0, L, R.choice(wpick)))
    arcs.sort()
    trails = []
    for b, r, a0, L, col in arcs:
        a1 = a0 + L
        x0, y0 = PX + r * math.cos(math.radians(a0)), PY + r * math.sin(math.radians(a0))
        x1, y1 = PX + r * math.cos(math.radians(a1)), PY + r * math.sin(math.radians(a1))
        dash = ' stroke-dasharray="%s"' % " ".join(n(R.uniform(60, 400)) if i % 2 == 0 else n(R.uniform(2, 7)) for i in range(8)) \
            if R.random() < .14 else ""
        trails.append('<path d="M%s %sA%s %s 0 %d 1 %s %s" stroke="%s" stroke-width="%s" opacity="%s"%s/>'
                      % (n(x0), n(y0), n(r), n(r), L > 180, n(x1), n(y1), col, n(.55 + 1.9 * b), ("%.2f" % (.25 + .65 * b)), dash))
    r_back = ridge(402, 46, 1.1, sharp=.35, bump=(.9, 1010, 190))
    r_mid = ridge(436, 30, 3.4, sharp=.1)
    r_front = ridge(476, 22, 5.9)
    tx = 410
    ty = ridge_y(r_mid, tx)
    pines = "".join(pine(x, ridge_y(r_front, x) + 3, h, "#070605")
                    for x, h in [(60, 30), (82, 22), (190, 26), (231, 34), (262, 24), (690, 28), (722, 36), (748, 24),
                                 (1038, 30), (1066, 40), (1100, 28), (1184, 34), (1214, 26), (1250, 36)])
    pines += "".join(pine(x, ridge_y(r_mid, x) + 3, h, "#110e0c") for x, h in [(540, 18), (560, 24), (1130, 20), (880, 16)])
    star_dust = specks(R, 170, 0, 0, 1280, 400, tw=0)
    tw_dust = specks(R, 9, 0, 0, 1280, 330, rmin=.9, rmax=1.5, op0=.8, op1=.9, tw=9)
    defs = ('<linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s" stop-opacity=".82"/>'
            '<stop offset=".5" stop-color="%s" stop-opacity=".45"/><stop offset=".72" stop-color="%s" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1c12" stop-opacity="0"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="1"/></linearGradient>'
            '<radialGradient id="pole"><stop offset="0" stop-color="%s" stop-opacity=".26"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="met" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s" stop-opacity="0"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>'
            '<filter id="bl" x="-30%%" y="-60%%" width="160%%" height="220%%"><feGaussianBlur stdDeviation="46"/></filter>'
            % (SKY0, SKY0, SKY0, HAZE, AMBER, AMBER, CREAM, CREAM))
    css = (SPIN_CSS + ".rot{transform-origin:%dpx %dpx}.mt{opacity:0}" % (PX, PY) + TWINKLE_CSS
           + motion(".rot{animation:rspin 240s linear infinite}"
                    "@keyframes mt{0%{opacity:0;transform:translate(0,0)}1.5%{opacity:1}6%{opacity:0;transform:translate(250px,120px)}100%{opacity:0;transform:translate(250px,120px)}}"
                    ".mt{animation:mt 11s linear infinite;animation-delay:-8s}"
                    "@keyframes po{0%,100%{opacity:.5}50%{opacity:1}}.po{animation:po 5s ease-in-out infinite}"))
    f = face("r")
    body = (
        '<ellipse cx="620" cy="190" rx="520" ry="60" fill="#8a7a66" opacity=".10" filter="url(#bl)" transform="rotate(-18 620 190)"/>'
        + star_dust + tw_dust +
        '<circle cx="%d" cy="%d" r="120" fill="url(#pole)"/>' % (PX, PY) +
        '<g class="rot" fill="none" stroke-linecap="round">%s</g>' % "".join(trails) +
        '<g class="po"><circle cx="%d" cy="%d" r="11" fill="%s" opacity=".28"/></g>' % (PX, PY, AMBER) +
        '<circle cx="%d" cy="%d" r="3.4" fill="%s"/>' % (PX, PY, AMBER) +
        star4(PX, PY, 17, AMBER, .12) +
        '<g class="mt"><path d="M900 40L1010 92" stroke="url(#met)" stroke-width="2.4" stroke-linecap="round"/></g>'
        '<rect y="250" width="1280" height="270" fill="url(#haze)"/>'
        '<rect width="1280" height="520" fill="url(#scrim)"/>'
        '<path d="%s" fill="#241b15"/>' % ridge_path(r_back) +
        '<path d="%s" fill="#15110e"/>' % ridge_path(r_mid) +
        '<g transform="translate(%s %s) scale(1.3) translate(%s %s)">' % (n(tx), n(ty + 2), n(-tx), n(-ty - 2)) + telescope(tx, ty + 2, "#070605") + "</g>" +
        '<path d="%s" fill="#070605"/>' % ridge_path(r_front) + pines +
        mono(64, 96, "OBSERVATORY LOG / 30.32°N 78.03°E / DEHRADUN", 20, DIM, ls=2.4) +
        text_path("Somansh Goel", 108, 60, 206) +
        text_path("builds software that ships,", 34, 64, 262, italic=True, fill="#d6d1c4") +
        text_path("then finds out how AI systems break.", 34, 64, 304, italic=True, fill="#d6d1c4") +
        mono(64, 494, "SOFTWARE ENGINEER · AI/ML · LLM RED-TEAMING", 20, CREAM, ls=2.4, extra=' opacity=".85"'))
    return svg(1280, 520, body, "Somansh Goel, observatory log",
               "A long-exposure star-trail sky over Himalayan foothills with a telescope on a ridge. "
               "Somansh Goel builds software that ships, then finds out how AI systems break.", css, defs)


# --------------------------------------------------------------------- sky --
def star_radius(c, cap):
    return 1.4 + 4.6 * math.sqrt(min(c, cap) / cap)


def sky(cal):
    CREAM, DIM, HAIR, SKY0, AMBER = INK, INKDIM, RULE, PARCH, VERM  # inverted: ink on parchment
    days = []
    for w in cal["weeks"]:
        for d in w["contributionDays"]:
            days.append((dt.date.fromisoformat(d["date"]), d["contributionCount"]))
    days.sort()
    S = stats(days)
    first = days[0][0]
    nw = len(cal["weeks"])
    start_off = sunday_index(first)           # first week may be partial
    cx, cy, R0, R, RD = 372, 288, 62, 200, 210
    step = (R - R0) / 6
    cap = max(8, max(c for _, c in days))

    def ang(i):                                # i = index into days
        return ((i + start_off) / (nw * 7)) * 2 * math.pi - math.pi / 2

    def pos(i, d):
        a = ang(i) + (zlib.crc32(str(d).encode()) % 100 - 50) / 50 * 0.004
        r = R0 + sunday_index(d) * step
        return cx + r * math.cos(a), cy + r * math.sin(a)

    top = sorted(range(len(days)), key=lambda i: (-days[i][1], days[i][0]))[:5]
    topset = set(top)
    bright = set(sorted(range(len(days)), key=lambda i: (-days[i][1], days[i][0]))[:9])

    g = ['<circle cx="%d" cy="%d" r="%d" fill="#f5eddb" stroke="%s"/>' % (cx, cy, RD, HAIR)]
    for k in range(7):
        g.append('<circle cx="%d" cy="%d" r="%s" fill="none" stroke="%s" opacity="%s"/>'
                 % (cx, cy, n(R0 + k * step), HAIR, "1" if k in (0, 6) else ".6"))
    # week ticks + month boundaries
    ticks = []
    for w in range(nw + 1):
        a = (w * 7 / (nw * 7)) * 2 * math.pi - math.pi / 2
        ticks.append("M%s %sL%s %s" % (n(cx + RD * math.cos(a)), n(cy + RD * math.sin(a)),
                                       n(cx + (RD + 6) * math.cos(a)), n(cy + (RD + 6) * math.sin(a))))
    g.append('<path d="%s" stroke="%s" fill="none"/>' % ("".join(ticks), DIM))
    spans, cur = [], None
    for i, (d, _) in enumerate(days):
        if cur is None or d.month != cur[0]:
            cur = [d.month, i, i]
            spans.append(cur)
        cur[2] = i
    labels, rays = [], []
    for m, a_i, b_i in spans:
        a0 = ang(a_i - .5)
        rays.append("M%s %sL%s %s" % (n(cx + R0 * math.cos(a0)), n(cy + R0 * math.sin(a0)),
                                      n(cx + (RD + 14) * math.cos(a0)), n(cy + (RD + 14) * math.sin(a0))))
        if b_i - a_i >= 14:
            am = ang((a_i + b_i) / 2)
            labels.append(mono(cx + 238 * math.cos(am), cy + 238 * math.sin(am) + 7, MONTHS[m - 1], 20, DIM, "middle", 1.5))
    g.append('<path d="%s" stroke="%s" fill="none" opacity=".75"/>' % ("".join(rays), HAIR))
    g += labels
    # silent days
    g.append('<g fill="%s" opacity=".45">%s</g>' % (DIM, "".join(
        '<circle cx="%s" cy="%s" r=".9"/>' % tuple(n(v) for v in pos(i, d)) for i, (d, c) in enumerate(days) if c == 0)))
    # constellations: 5+ day streaks
    lines, run = [], []
    for i, (d, c) in enumerate(days + [(None, 0)]):
        if c > 0:
            run.append(i)
        else:
            if len(run) >= 5:
                seg = [run[0]]
                for j in run[1:]:
                    if sunday_index(days[j][0]) < sunday_index(days[seg[-1]][0]):  # week wrap: break the line
                        if len(seg) > 1:
                            lines.append("M" + "L".join("%s %s" % tuple(n(v) for v in pos(k, days[k][0])) for k in seg))
                        seg = []
                    seg.append(j)
                if len(seg) > 1:
                    lines.append("M" + "L".join("%s %s" % tuple(n(v) for v in pos(k, days[k][0])) for k in seg))
            run = []
    g.append('<path d="%s" stroke="%s" stroke-width=".9" fill="none" opacity=".55"/>' % ("".join(lines), CREAM))
    # stars
    halos, dots, spikes, twink, tags = [], [], [], [], []
    for i, (d, c) in enumerate(days):
        if c == 0:
            continue
        x, y = pos(i, d)
        r = star_radius(c, cap)
        s = math.sqrt(min(c, cap) / cap)
        if c >= 3:
            halos.append('<circle cx="%s" cy="%s" r="%s"/>' % (n(x), n(y), n(r * 2.8)))
        dots.append('<circle cx="%s" cy="%s" r="%s" opacity="%s"/>' % (n(x), n(y), n(r), "%.2f" % (.55 + .45 * s)))
        if i in bright and i not in topset:
            twink.append('<circle class="tw" style="animation-delay:-%ss;animation-duration:%ss" cx="%s" cy="%s" r="%s"/>'
                         % (n(i % 7 * .7), n(3.5 + i % 3), n(x), n(y), n(r + .5)))
    for i in top:
        d, c = days[i]
        x, y = pos(i, d)
        spikes.append(star4(x, y, 15, CREAM, .13, cls="tw", extra=' style="animation-delay:-%ss;animation-duration:%ss"' % (n(i % 5), 4 + i % 3)))
        side = -1 if x < cx else 1
        tags.append(mono(x + side * 17, y + 7, "%s %02d" % (MONTHS[d.month - 1], d.day), 20, AMBER, "end" if side < 0 else "start",
                         extra=' stroke="%s" stroke-width="5" paint-order="stroke" stroke-linejoin="round"' % SKY0))
    g.append('<g fill="%s" opacity=".1">%s</g>' % (CREAM, "".join(halos)))
    g.append('<g fill="%s">%s</g>' % (CREAM, "".join(dots)))
    g.append('<g fill="%s">%s</g>' % (CREAM, "".join(twink)))
    g += spikes + tags
    # celestial pole at the centre
    g.append('<circle cx="%d" cy="%d" r="2.6" fill="%s"/>' % (cx, cy, AMBER) + star4(cx, cy, 11, AMBER, .14))

    # -- right column: the legend
    X, X2, W = 760, 1010, 230
    f = face("r")
    last = days[-1][0]

    def fmt(d):
        return "%s %02d" % (MONTHS[d.month - 1], d.day)

    def cell(x, y, label, big, unit, sub):
        size = 52
        wbig = text_width(big, size)
        wun = text_width(unit, 26, True) + 10 if unit else 0
        if wbig + wun > W:
            size = size * (W - wun) / wbig
        out = mono(x, y, label, 20, DIM, ls=1.2) + text_path(big, size, x, y + 52, fill=CREAM)
        if unit:
            out += text_path(unit, 26, x + text_width(big, size) + 10, y + 52, italic=True, fill=DIM)
        return out + mono(x, y + 84, sub, 20, DIM)

    lo = S["longest"]
    cu = S["current"]
    rng = lambda a, b: ("%s TO %s" % (fmt(a), fmt(b))) if a != b else fmt(a)
    right = (
        mono(X, 56, "CONTRIBUTIONS · LAST %d WEEKS" % nw, 20, DIM, ls=1.2)
        + text_path("{:,}".format(S["total"]), 124, X - 4, 172, fill=CREAM)
        + '<path d="M%d 200H1240" stroke="%s"/>' % (X, HAIR)
        + cell(X, 226, "LONGEST STREAK", str(lo[0]), "days", rng(lo[1], lo[2]) if lo[1] else "NONE")
        + cell(X2, 226, "ACTIVE DAYS", str(S["active"]), "days", "OF %d DAYS CHARTED" % S["ndays"])
        + cell(X, 352, "BUSIEST DAY", str(S["busiest"][0]), "in a day", fmt(S["busiest"][1]))
        + cell(X2, 352, "BUSIEST WEEKDAY", S["weekday"][0], "", "%d IN ALL" % S["weekday"][1])
        + '<path d="M%d 448H1240" stroke="%s"/>' % (X, HAIR)
        + mono(X, 478, "MAGNITUDE", 20, DIM, ls=1.2))
    lx = 920
    for c, lab in ((1, "1"), (5, "5"), (15, "15+")):
        r = star_radius(c, cap)
        right += '<circle cx="%d" cy="471" r="%s" fill="%s"/>' % (lx, n(r), CREAM)
        right += mono(lx + 14, 478, lab, 20, CREAM)
        lx += 14 + 12 * len(lab) + 26
    right += mono(X, 512, "REDRAWN NIGHTLY BY A GITHUB ACTION", 20, DIM) + mono(X, 534, "LAST EXPOSURE %s UTC" % last.isoformat(), 20, DIM)
    left_note = mono(40, 510, "SUN, INNER RING", 18, DIM) + mono(40, 532, "SAT, OUTER RING", 18, DIM)
    frame = ('<rect x="5" y="5" width="1270" height="550" rx="10" fill="none" stroke="#d9cdb0" stroke-width="10"/>'
             '<rect x="10" y="10" width="1260" height="540" rx="4" fill="none" stroke="%s" stroke-width="1.6"/>'
             '<rect x="15" y="15" width="1250" height="530" rx="2" fill="none" stroke="%s" stroke-width=".6"/>' % (INK, INK))
    body = frame + "".join(g) + right + '<path d="M700 40V500" stroke="%s"/>' % HAIR + left_note
    return svg(1280, 560, body, "A year of commits, charted",
               "A polar star chart of the last %d weeks of GitHub contributions: each commit day is a star, "
               "%s contributions in total, longest streak %d days, last exposure %s."
               % (nw, "{:,}".format(S["total"]), lo[0], last.isoformat()), motion('@keyframes tw{0%,100%{opacity:1}50%{opacity:.55}}.tw{animation:tw 5s ease-in-out infinite}'), bg=PARCH, border=False), S


# ------------------------------------------------------------------ plates --
def emb_chatlens(a, R):
    out = []
    for i in range(24):
        act = .16 + .84 * max(0, math.cos((i - 19) / 24 * 2 * math.pi)) ** 1.4 + .12 * math.sin(i * 1.9) ** 2
        act = min(act, 1)
        ln = 14 + act * 66
        out.append('<g transform="rotate(%d)"><rect class="b" style="animation-delay:-%ss" x="-3" y="%s" width="6" height="%s" rx="3" fill="%s" opacity="%s"/></g>'
                   % (i * 15, n(i * .17), n(-(34 + ln)), n(ln), a, "%.2f" % (.45 + .55 * act)))
    ticks = "".join('<path d="M0 %d V%d" transform="rotate(%d)" stroke="%s" stroke-width="2"/>' % (-122, -130, k * 90, CREAM) for k in range(4))
    return ('<circle r="120" fill="none" stroke="%s" stroke-dasharray="2 6"/><circle r="26" fill="none" stroke="%s" stroke-width="1.5"/>'
            '<circle r="3" fill="%s"/>%s%s' % (HAIR, CREAM, a, "".join(out), ticks)), \
        ".b{transform-box:fill-box;transform-origin:50% 100%}" + motion("@keyframes br{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.5)}}.b{animation:br 3.4s ease-in-out infinite}")


def emb_socialspace(a, R):
    body = ('<circle r="46" fill="none" stroke="%s"/><circle r="84" fill="none" stroke="%s"/>'
            '<g class="orb"><g transform="rotate(-28)">'
            '<path d="M-46 0H84" stroke="%s" stroke-dasharray="3 6"/>'
            '<circle class="pl" cx="-46" r="14" fill="none" stroke="%s" stroke-width="1.5"/>'
            '<circle class="pl" style="animation-delay:-1.8s" cx="84" r="8" fill="none" stroke="%s" stroke-width="1.5"/>'
            '<circle cx="-46" r="24" fill="%s" opacity=".12"/><circle cx="-46" r="14" fill="%s"/>'
            '<circle cx="84" r="8.5" fill="%s"/><circle class="mv" cx="-46" r="3.4" fill="%s"/>'
            '</g></g>' % (HAIR, HAIR, DIM, CREAM, a, CREAM, CREAM, a, CREAM))
    body += specks(random.Random(5), 14, -120, -110, 120, 110, op0=.2, op1=.5)
    return body, (".orb{}" + motion("@keyframes pl{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.2);opacity:0}}"
                                    ".pl{transform-box:fill-box;transform-origin:center;animation:pl 3.6s ease-out infinite}"
                                    "@keyframes mv{0%{transform:translateX(0);opacity:0}10%,90%{opacity:1}100%{transform:translateX(130px);opacity:0}}"
                                    ".mv{animation:mv 2.4s ease-in-out infinite alternate}.orb{animation:spin 18s linear infinite}"))


def emb_gem(a, R):
    """Anime-style VTuber bust: pink hair, cat-ear headset, blinking eyes, lip-sync mouth, pulsing audio ring."""
    LN, SKIN, HAIR_D, HAIR_L, GREY = "#1a0f14", "#f8e3d2", "#c4437f", "#ffb3d6", "#2a2a2e"
    ln = 'stroke="%s" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"' % LN
    bars = []
    N = 56
    for i in range(N):
        v = abs(math.sin(i * .55) * .6 + math.sin(i * 1.4 + 1) * .4)
        l = 5 + v * 20
        bars.append('<g transform="rotate(%s)"><rect class="b" style="animation-delay:-%ss" x="-1.6" y="%s" width="3.2" height="%s" rx="1.6" fill="%s" opacity="%s"/></g>'
                    % (n(i * 360 / N), n(i * .13 % 2.4), n(-(110 + l)), n(l), a, "%.2f" % (.35 + .55 * v)))

    def eye(sx):
        return ('<g transform="translate(%d -4) scale(%d 1)"><g class="eye"><ellipse rx="10.5" ry="13" fill="#fff"/>'
                '<ellipse cy="1" rx="8" ry="11.2" fill="%s"/><ellipse cy="5" rx="6" ry="5.5" fill="%s" opacity=".9"/>'
                '<ellipse cy="1" rx="3.6" ry="6" fill="%s"/><circle cx="-3" cy="-4" r="3.4" fill="#fff"/><circle cx="3" cy="5" r="1.7" fill="#fff"/></g>'
                '<path d="M-12 -7C-7 -15 6 -15 11 -8M11 -8L16 -12" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round"/></g>'
                % (sx * 17, sx, HAIR_D, a, LN, LN))
    fringe = ("M-46 -22C-52 -64 -22 -82 2 -82C28 -82 52 -62 46 -22C44 -34 40 -44 34 -50C30 -34 22 -28 14 -46"
              "C10 -30 2 -26 -6 -44C-10 -30 -20 -28 -26 -46C-32 -40 -40 -34 -46 -22Z")
    body = (
        '<circle r="106" fill="none" stroke="%s" stroke-dasharray="2 6"/>' % HAIR + "".join(bars)
        + '<clipPath id="gc"><circle r="108"/></clipPath><g clip-path="url(#gc)"><g class="bob">'
        '<path d="M0 -88C-40 -88 -62 -60 -60 -20C-60 10 -64 40 -54 68C-44 62 -40 52 -36 42L36 42C40 52 44 62 54 68C64 40 60 10 60 -20C62 -60 40 -88 0 -88Z" fill="%s" %s/>' % (HAIR_D, ln)
        + '<path d="M-10 28H10V60H-10Z" fill="#e8c8b2" %s/>' % ln
        + '<path d="M-100 150C-100 96 -52 68 -14 60L0 78L14 60C52 68 100 96 100 150Z" fill="%s" %s/>' % (GREY, ln)
        + '<path d="M-14 60L0 80L14 60" fill="none" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/>' % CREAM
        + '<path d="M-9 80L0 76L9 80L0 90Z" fill="%s" %s/>' % (a, ln)
        + '<path d="M-41 -28C-41 10 -28 38 0 42C28 38 41 10 41 -28C41 -52 20 -62 0 -62C-20 -62 -41 -52 -41 -28Z" fill="%s" %s/>' % (SKIN, ln)
        + '<ellipse cx="-27" cy="14" rx="7" ry="3.6" fill="%s" opacity=".4"/><ellipse cx="27" cy="14" rx="7" ry="3.6" fill="%s" opacity=".4"/>' % (a, a)
        + '<path d="M0 12L-1.6 17H1.6" fill="none" stroke="#c99a82" stroke-width="1.3" stroke-linecap="round"/>'
        + eye(-1) + eye(1)
        + '<ellipse class="mo" cx="0" cy="27" rx="5.2" ry="2.8" fill="#8a2236" %s/>' % ln.replace('1.6', '1.2')
        + '<path d="%s" fill="%s" %s/>' % (fringe, a, ln)
        + '<path d="M-28 -66C-10 -76 12 -76 28 -64" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" opacity=".7"/>' % HAIR_L
        + '<path d="M-46 -22C-54 2 -54 26 -44 48C-38 30 -36 8 -37 -14Z" fill="%s" %s/>' % (a, ln)
        + '<path d="M46 -22C54 2 54 26 44 48C38 30 36 8 37 -14Z" fill="%s" %s/>' % (a, ln)
        + '<path d="M2 -82C-6 -98 10 -102 12 -92" fill="none" stroke="%s" stroke-width="3.4" stroke-linecap="round"/>' % LN
        + '<path d="M2 -82C-6 -98 10 -102 12 -92" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % a
        # cat-ear headset
        + '<path d="M-50 -64L-44 -98L-22 -74ZM50 -64L44 -98L22 -74Z" fill="%s" %s/>' % (GREY, ln)
        + '<path d="M-44 -72L-42 -88L-32 -77ZM44 -72L42 -88L32 -77Z" fill="%s"/>' % a
        + '<path d="M-55 -28C-60 -90 60 -90 55 -28" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % GREY
        + '<path d="M-55 -28C-60 -90 60 -90 55 -28" fill="none" stroke="%s" stroke-width="1" opacity=".6"/>' % HAIR_L
        + '<circle cx="-56" cy="-12" r="12" fill="%s" %s/><circle cx="56" cy="-12" r="12" fill="%s" %s/>' % (GREY, ln, GREY, ln)
        + '<circle cx="-56" cy="-12" r="6" fill="none" stroke="%s" stroke-width="2"/><circle cx="56" cy="-12" r="6" fill="none" stroke="%s" stroke-width="2"/>' % (a, a)
        + '<path d="M-60 -2C-64 22 -50 40 -26 37" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % GREY
        + '<circle cx="-24" cy="37" r="4" fill="%s" %s/>' % (a, ln)
        + '</g></g>')
    return body, (".b,.mo,.eye{transform-box:fill-box}.b{transform-origin:50% 100%}.mo{transform-origin:center}.eye{transform-origin:50% 0%}" + motion(
        "@keyframes br{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.3)}}.b{animation:br 1.9s ease-in-out infinite}"
        "@keyframes mo{0%,100%{transform:scaleY(.5)}12%{transform:scaleY(1.7)}24%{transform:scaleY(.7)}38%{transform:scaleY(2.1)}"
        "50%{transform:scaleY(.4)}64%{transform:scaleY(1.5)}78%{transform:scaleY(.6)}90%{transform:scaleY(1.9)}}.mo{animation:mo 1.7s ease-in-out infinite}"
        "@keyframes bl{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.08)}}.eye{animation:bl 4s infinite}"
        "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2.5px)}}.bob{animation:bob 3.4s ease-in-out infinite}"))


def emb_sre(a, R):
    N = {"gw": (0, -92), "auth": (-86, -32), "api": (0, -30), "srch": (86, -32),
         "db": (-52, 56), "cache": (38, 60), "q": (104, 52)}
    E = [("gw", "auth"), ("gw", "api"), ("gw", "srch"), ("auth", "db"), ("api", "db"), ("api", "cache"), ("srch", "q"), ("cache", "q")]
    hot_e = {("auth", "db"), ("api", "db")}
    ed, nd = [], []
    for u, v in E:
        cls = "e%s" % ("1" if (u, v) in hot_e else "2" if (u, v) in {("gw", "auth"), ("gw", "api")} else "")
        ed.append('<path class="%s" d="M%d %dL%d %d" stroke="%s" stroke-width="2.4" fill="none"/>'
                  % (cls, *N[u], *N[v], CORAL if cls in ("e1",) else TEAL))
    lv = {"db": "n0", "auth": "n1", "api": "n1", "gw": "n2"}
    for k, (x, y) in N.items():
        cls = lv.get(k, "")
        col = CORAL if k == "db" else TEAL
        halo = '<circle class="h" cx="%d" cy="%d" r="26" fill="%s" opacity="%s"/>' % (x, y, CORAL, ".28" if k == "db" else "0") if k == "db" else ""
        nd.append(halo + '<circle class="%s" cx="%d" cy="%d" r="12" fill="%s" stroke="%s" stroke-width="3"/>' % (cls, x, y, SKY0, col))

    def kf(name, on, off, c_on, c_off, prop="stroke"):
        return ("@keyframes %s{0%%,%s%%{%s:%s}%s%%,%s%%{%s:%s}%s%%,100%%{%s:%s}}"
                % (name, on - 2, prop, c_off, on, off, prop, c_on, off + 10, prop, c_off))
    css = motion(
        kf("n0", 8, 62, CORAL, TEAL) + kf("e1", 18, 66, CORAL, TEAL) + kf("n1", 28, 70, CORAL, TEAL)
        + kf("e2", 38, 74, CORAL, TEAL) + kf("n2", 48, 78, CORAL, TEAL)
        + "@keyframes hh{0%,6%{opacity:0;transform:scale(.6)}12%{opacity:.5;transform:scale(1)}30%{opacity:.3;transform:scale(1.5)}62%{opacity:.25}76%,100%{opacity:0;transform:scale(1)}}"
        ".n0{animation:n0 10s ease-in-out infinite}.n1{animation:n1 10s ease-in-out infinite}.n2{animation:n2 10s ease-in-out infinite}"
        ".e1{animation:e1 10s ease-in-out infinite}.e2{animation:e2 10s ease-in-out infinite}"
        ".h{transform-box:fill-box;transform-origin:center;animation:hh 10s ease-in-out infinite}")
    return '<g>%s</g>%s' % ("".join(ed), "".join(nd)), css


def emb_appd(a, R):
    leaf = "M0 -92C62 -70 76 6 0 80C-76 6 -62 -70 0 -92Z"
    grid = "".join("M%d -96V96M-96 %dH96" % (k, k) for k in range(-96, 97, 24))
    veins = ""
    for k in range(6):
        y = -62 + k * 22
        veins += "M0 %dQ%d %d %d %d" % (y + 12, 22, y - 2, 40 - k * 2 if k < 4 else 30 - k * 3, y - 18)
        veins += "M0 %dQ%d %d %d %d" % (y + 12, -22, y - 2, -(40 - k * 2) if k < 4 else -(30 - k * 3), y - 18)
    spots = [(-24, -30, 6), (22, -2, 5), (-16, 34, 4), (30, 40, 5)]
    sp = "".join('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".85"/>' % (x, y, r, CORAL if i == 1 else a) for i, (x, y, r) in enumerate(spots))
    pos = [(-96 + 40 * c if r % 2 == 0 else -96 + 40 * (3 - c), -96 + 40 * r) for r in range(4) for c in range(4)]
    kfs = ""
    for i, (px, py) in enumerate(pos):
        t0 = i * 6.25
        kfs += "%s%%,%s%%{transform:translate(%dpx,%dpx)}" % (n(t0), n(t0 + 3.6), px + 16, py + 16)
    kfs += "100%%{transform:translate(%dpx,%dpx)}" % (pos[-1][0] + 16, pos[-1][1] + 16)
    body = ('<path d="%s" stroke="%s" fill="none" opacity=".5"/>'
            '<path d="%s" fill="%s" fill-opacity=".07" stroke="%s" stroke-width="2"/>'
            '<path d="M0 -84V96M0 80L8 100%s" stroke="%s" stroke-width="1.6" fill="none" opacity=".8"/>%s'
            '<g class="win"><rect x="-16" y="-16" width="72" height="72" fill="%s" fill-opacity=".1" stroke="%s" stroke-width="2.4"/>'
            '<path d="M-16 -4V-16H-4M44 -16H56V-4M56 44V56H44M-4 56H-16V44" stroke="%s" stroke-width="5" fill="none"/></g>'
            % (grid, HAIR, leaf, a, CREAM, veins and "", CREAM, sp, a, a, CREAM))
    body = body.replace('M0 80L8 100', 'M0 80L8 100' + veins)
    return body, motion("@keyframes win{%s}.win{animation:win 14s ease-in-out infinite}" % kfs)


def emb_fouress(a, R):
    pages, edges, subs = [], [], []
    for i in range(6):
        t = math.radians(-90 + i * 60)
        x, y = 64 * math.cos(t), 64 * math.sin(t)
        edges.append("M0 0L%s %s" % (n(x), n(y)))
        pages.append('<g transform="translate(%s %s)"><g class="cs"><rect x="-8" y="-10" width="16" height="20" rx="2.5" fill="%s" stroke="%s" stroke-width="2"/>'
                     '<path d="M-4 -3H4M-4 2H4M-4 6H1" stroke="%s" stroke-width="1.5"/></g></g>' % (n(x), n(y), SKY0, a, DIM))
        for dd in (-14, 14):
            t2 = t + math.radians(dd)
            x2, y2 = 112 * math.cos(t2), 112 * math.sin(t2)
            edges.append("M%s %sL%s %s" % (n(x), n(y), n(x2), n(y2)))
            subs.append('<circle cx="%s" cy="%s" r="4.5" fill="%s"/>' % (n(x2), n(y2), CREAM))
    home = ('<path d="M-13 2L0 -11L13 2" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M-9 0V13H9V0" fill="%s" fill-opacity=".25" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (a, a, a))
    t = math.radians(-90)
    body = ('<circle r="64" fill="none" stroke="%s" stroke-dasharray="2 6"/><g class="orb"><path d="%s" stroke="%s" stroke-width="1.5" fill="none"/>'
            '%s%s<circle class="pt" r="3.4" fill="%s"/></g><circle r="25" fill="%s" stroke="%s"/>%s'
            % (HAIR, "".join(edges), DIM, "".join(subs), "".join(pages), a, SKY0, HAIR, home))
    return body, ".cs{transform-box:fill-box;transform-origin:center}" + motion(
        ".orb{animation:spin 80s linear infinite}.cs{animation:rspin 80s linear infinite}"
        "@keyframes pt{0%%{transform:translate(0,0);opacity:0}15%%{opacity:1}85%%{opacity:1}100%%{transform:translate(%spx,%spx);opacity:0}}"
        ".pt{animation:pt 3s ease-in-out infinite}" % (n(64 * math.cos(t)), n(64 * math.sin(t)))) 


PLATES = [
    dict(slug="chatlens", scale=1.0, num="SG 01", name="ChatLens", cls="BROWSER / PRIVACY", accent=AMBER, emb=emb_chatlens,
         text="Chat analytics that never leave your browser. A Content-Security-Policy makes the browser refuse every outgoing request.",
         tags="Next.js · TypeScript · SVG charts", alt="ChatLens, a browser-only chat analytics tool, shown as a 24-spoke activity clock"),
    dict(slug="socialspace", scale=1.3, num="SG 02", name="SocialSpace", cls="REALTIME / WEBRTC", accent=CORAL, emb=emb_socialspace,
         text="A table for two: chat, calls, a shared canvas and watch-together over a small WebSocket relay.",
         tags="Next.js · WebSocket · WebRTC · PWA", alt="SocialSpace, a realtime space for two, shown as a binary star exchanging pulses"),
    dict(slug="gem-vtuber", scale=0.98, num="SG 03", name="Gem-VTuber", cls="DESKTOP / VOICE", accent=PINK, emb=emb_gem,
         text="A desktop companion: a Live2D avatar in a transparent window that talks through the Gemini Live API.",
         tags="Electron · PixiJS · Live2D · WebSocket", alt="Gem-VTuber, a desktop voice companion, shown as an audio ring around a face glyph"),
    dict(slug="sre-autopilot", scale=1.0, num="SG 04", name="SRE Autopilot", cls="RL ENVIRONMENT", accent=TEAL, emb=emb_sre,
         text="Seven microservices, a hidden root cause, noisy telemetry, and an agent on call.",
         tags="Python · FastAPI · OpenEnv · Docker", alt="SRE Autopilot, an incident-response environment, shown as a seven-node service graph with a fault spreading and healing"),
    dict(slug="appd-lite-net", scale=1.12, num="SG 05", name="AppD-Lite-Net", cls="COMPUTER VISION", accent=GREEN, emb=emb_appd,
         text="Apple leaf disease detection with a CNN under one million parameters: 99.53% on a held-out test set.",
         tags="TensorFlow · Keras · FastAPI · React", alt="AppD-Lite-Net, apple leaf disease detection, shown as a convolution window scanning a leaf"),
    dict(slug="fouress-bath", scale=1.08, num="SG 06", name="Fouress Bath", cls="PRODUCTION / SEO", accent=GOLD, emb=emb_fouress,
         text="The live catalogue site for a sanitaryware retailer, with structured data and technical SEO.",
         tags="Next.js · Tailwind CSS · JSON-LD", alt="Fouress Bath, a live retailer catalogue, shown as a sitemap of pages orbiting a home node"),
]


def wrap(text, size, maxw, k=0.54):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if len(t) * size * k > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    return lines + [cur]


def plate(p):
    a = p["accent"]
    emb_body, emb_css = p["emb"](a, None)
    size = 56
    while text_width(p["name"], size) > 334:
        size -= 1
    lines = wrap(p["text"], 21, 330)
    txt = "".join('<tspan x="30" dy="%s">%s</tspan>' % ("0" if i == 0 else "28", ln) for i, ln in enumerate(lines))
    rnd = random.Random(zlib.crc32(p["slug"].encode()))
    body = (
        specks(rnd, 34, 6, 6, 634, 394, op0=.12, op1=.45)
        + '<path d="M30 62H610" stroke="%s"/>' % HAIR + '<path d="M30 62H78" stroke="%s" stroke-width="2"/>' % a
        + mono(30, 44, p["num"], 22, a, ls=2)
        + mono(610, 44, p["cls"], 20, DIM, "end", 1)
        + text_path(p["name"], size, 28, 118)
        + '<text class="s" y="164" font-size="21" fill="#d6d1c4">%s</text>' % txt.replace('<tspan x="30"', '<tspan x="30"', 1)
        + '<g transform="translate(500 208) scale(%s)">%s</g>' % (p["scale"], emb_body)
        + mono(30, 372, p["tags"], 20, DIM)
        + mono(582, 372, "OPEN", 20, a, "end", 1.5)
        + '<path d="M590 380L606 364M594 364H606V376" stroke="%s" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % a)
    return svg(640, 400, body, "%s %s, %s" % (p["num"], p["name"], p["cls"].title()), p["alt"] + ". " + p["text"],
               SPIN_CSS + TWINKLE_CSS + emb_css)


# ------------------------------------------------------------- field notes --
def fieldnotes():
    rows = [.92, .78, .88, .6, .95, .7, .84, .5, .76]
    R = random.Random(23)
    SX, SY, SW, PITCH, RH = 660, 32, 560, 20, 12
    bars, dashes = [], []
    for i, f in enumerate(rows):
        y = SY + 24 + i * PITCH
        w = (SW - 48) * f
        rec = i < 5                       # the still shows the scan part-way down
        d, x = [], 0
        while x < w - 4:
            seg = R.choice([8, 14, 22, 30, 46])
            d += [min(seg, w - x), 5]
            x += seg + 5
        col = CORAL if i == 4 else CREAM
        bars.append('<rect class="rb" style="animation-delay:%ss" x="%d" y="%d" width="%s" height="%d" rx="2" fill="#3a3835" stroke="#4d4a45"%s/>'
                    % (n(i * .6), SX + 24, y, n(w), RH, ' opacity="0"' if rec else ""))
        dashes.append('<path class="rd" style="animation-delay:%ss" d="M%d %dh%s" stroke="%s" stroke-width="3.4" stroke-linecap="round" '
                      'stroke-dasharray="%s" opacity="%s"/>' % (n(i * .6), SX + 24, y + 6, n(w), col, " ".join(n(v) for v in d), "0.9" if rec else "0"))
    scan_y = SY + 24 - 4
    css = motion("@keyframes rb{0%,2%{opacity:1}4%,90%{opacity:0}97%,100%{opacity:1}}@keyframes rd{0%,2%{opacity:0}4%,90%{opacity:.9}97%,100%{opacity:0}}"
                 "@keyframes sc{0%{transform:translateY(0);opacity:0}2%{opacity:1}58%{opacity:1}62%{transform:translateY(180px);opacity:0}100%{transform:translateY(180px);opacity:0}}"
                 ".rb,.rd{animation-duration:9s;animation-iteration-count:infinite;animation-fill-mode:backwards}"
                 ".rb{animation-name:rb}.rd{animation-name:rd}.sc{animation:sc 9s linear infinite}")
    defs = ('<linearGradient id="glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="%s" stop-opacity=".4"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (CORAL, CORAL, CORAL))
    log = lambda y, a, b: mono(48, y, a, 20, CREAM, ls=1) + mono(48, y + 28, b, 20, DIM)
    body = (
        specks(random.Random(3), 60, 0, 0, 1280, 270, op0=.1, op1=.4)
        + mono(48, 64, "OBSERVATION LOG · SECURITY", 20, CORAL, ls=2)
        + text_path("Field notes:", 66, 46, 146)
        + text_path("how assistants leak", 52, 48, 208, italic=True, fill="#d6d1c4")
        + mono(48, 244, "FIG. 2 · A SYSTEM PROMPT, REDACTED THEN RECOVERED", 18, DIM)
        + '<rect x="%d" y="%d" width="%d" height="214" rx="8" fill="#151412" stroke="%s"/>' % (SX, SY, SW, HAIR)
        + "".join(bars) + "".join(dashes)
        + '<g transform="translate(0 %d)"><g class="sc" transform="translate(0 90)"><rect x="%d" y="-11" width="%d" height="22" fill="url(#glow)"/>'
          '<path d="M%d 0H%d" stroke="%s" stroke-width="2"/></g></g>' % (scan_y, SX + 6, SW - 12, SX + 6, SX + SW - 6, CORAL)
        + '<path d="M48 272H1232" stroke="%s"/>' % HAIR
        + log(306, "2025 · RED-TEAM AUDIT, PRODUCTION AI ASSISTANT", "Full system prompt recovered · 5 findings reported to the vendor")
        + log(366, "2025 · SIX CONSUMER ASSISTANTS, ONE PROMPT FAMILY", "3 returned instruction-like text · 2 refused · 1 returned nothing"))
    return svg(1280, 420, body, "Field notes: how assistants leak",
               "A system prompt shown as redaction bars while a scan line recovers the text beneath. "
               "Two 2025 research entries: a red-team audit of a production AI assistant that recovered its full system prompt, "
               "and a comparison of six consumer assistants.", css, defs)


# ------------------------------------------------------------ typeset text --
class Type:
    """Running text as <use> of shared glyph outlines (deduped per SVG)."""

    def __init__(self):
        self.defs = {}

    def adv(self, ch, size, kind):
        f = face(kind)
        g = f.cmap.get(ord(ch))
        return f.hmtx[g][0] * size / f.upm if g else size * .3

    def width(self, s, size, kind="rb"):
        return sum(self.adv(c, size, kind) for c in s)

    def draw(self, s, size, x, y, kind="rb", fill=CREAM):
        f = face(kind)
        out, cx = [], x
        for ch in s:
            g = f.cmap.get(ord(ch))
            if g and ch != " ":
                gid = "%s%s_%x" % (kind, n(size).replace(".", "p"), ord(ch))
                if gid not in self.defs:
                    from fontTools.pens.svgPathPen import SVGPathPen
                    from fontTools.pens.transformPen import TransformPen
                    pen = SVGPathPen(f.gs, ntos=n)
                    k = size / f.upm
                    f.gs[g].draw(TransformPen(pen, (k, 0, 0, -k, 0, 0)))
                    self.defs[gid] = pen.getCommands()
                out.append('<use href="#%s" x="%s" y="%s"/>' % (gid, n(cx), n(y)))
            cx += self.adv(ch, size, kind)
        return '<g fill="%s">%s</g>' % (fill, "".join(out)), cx - x

    def para(self, text, size, x, y, maxw, kind="rb", fill=CREAM, lh=1.45):
        """Returns (markup, baseline of last line, line count)."""
        lines, cur = [], ""
        for w in text.split(" "):
            t = (cur + " " + w) if cur else w
            if cur and self.width(t, size, kind) > maxw:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        out = [self.draw(l, size, x, y + i * size * lh, kind, fill)[0] for i, l in enumerate(lines)]
        return "".join(out), y + (len(lines) - 1) * size * lh, len(lines)

    def defs_markup(self):
        return "".join('<path id="%s" d="%s"/>' % kv for kv in self.defs.items())


# ------------------------------------------------------------- new panels --
def heading(title, kicker, sub, dark):
    T = Type()
    ink, kc, subc, rule = (CREAM, DIM, "#d6d1c4", "#3a3835") if dark else (INK, INKDIM, INKDIM, "#cfc3aa")
    body = mono(4, 26, kicker, 20, kc, ls=2.4) + text_path(title, 56, 2, 84, fill=ink, track=1.6)
    bottom = 84
    if sub:
        m, bottom, _ = T.para(sub, 26, 4, 122, 1200, "ib", subc, 1.35)
        body += m
    ly = bottom + 26
    body += ('<path d="M0 %s H1228M1252 %s H1280" stroke="%s" fill="none"/>' % (n(ly), n(ly), rule)
             + star4(1240, ly, 9, ink, .16))
    h = int(ly + 14)
    return svg(1280, h, body, title, "%s. %s" % (kicker.title(), sub or title), "", T.defs_markup(), bg=None, border=False)


def about():
    T = Type()
    txt = ("I'm a final-year B.Tech CSE (AI & ML) student at UPES, Dehradun, graduating in 2027. I build web and desktop "
           "software end to end, and I spend the rest of my time finding out how AI systems fail.")
    m, last, _ = T.para(txt, 32, 56, 116, 1120, "rb", CREAM, 1.5)
    h = int(last + 52)
    body = (specks(random.Random(41), 40, 0, 0, 1280, h, op0=.1, op1=.4)
            + mono(56, 58, "OBSERVER'S NOTE", 20, AMBER, ls=3)
            + star4(1214, 52, 12, AMBER, .15) + m)
    return svg(1280, h, body, "Observer's note", txt, "", T.defs_markup())


def link(label):
    w = int(28 + len(label) * 13.2 + 14 + 18 + 28)
    body = ('<rect x=".75" y=".75" width="%d" height="54.5" rx="27.25" fill="#151517" stroke="#3a3835" stroke-width="1.5"/>' % (w - 1.5)
            + mono(28, 35, label, 22, CREAM, extra=' font-weight="700"')
            + '<path d="M%s 38L%s 24M%s 24H%s V34" stroke="%s" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            % (n(w - 46), n(w - 32), n(w - 42), n(w - 32), AMBER))
    return svg(w, 56, body, label, "Link: %s" % label, bg=None, border=False)


def logbook():
    T = Type()
    bullets = ["Built a FAISS-backed retrieval pipeline on Llama 3.2 Vision over 100+ page internal documents, taking lookups for 50+ staff from hours to under 10 seconds.",
               "Scripted RHEL 9 environment setup, cutting per-machine provisioning from 3 hours to 15 minutes.",
               "Shipped a one-click installer so non-technical staff could set the system up on-prem."]
    entries = [("JUN 2025", "TO AUG 2025", "AI/ML & Software Engineering Intern", "Bharat Electronics Limited", bullets),
               ("MAR 2026", "TO PRESENT", "Secretary", "IEEE Computer Society (UPES)", [])]
    body, y, X = [], 58, 330
    for k, (d1, d2, role, org, bl) in enumerate(entries):
        y0 = y
        body.append(mono(56, y0 + 20, d1, 20, INKDIM, ls=1) + mono(56, y0 + 46, d2, 20, INKDIM, ls=1))
        body.append(T.draw(role, 36, X, y0 + 36, "r", INK)[0])
        body.append(T.draw(org, 28, X, y0 + 76, "ib", "#4a3b2c")[0])
        by = y0 + 76
        for b in bl:
            m, by, _ = T.para(b, 24, X + 28, by + 46, 1280 - X - 28 - 70, "rb", INK, 1.45)
            first = by - (_ - 1) * 24 * 1.45
            body.append(m + star4(X + 8, first - 8, 6.5, INK, .2))
        end = by + 26
        body.append('<path d="M300 %sV%s" stroke="%s"/>' % (n(y0 - 4), n(end), RULE))
        if k == 0:
            body.append('<path d="M56 %sH1224" stroke="%s"/>' % (n(end + 24), RULE))
        y = end + 24 + 46
    h = int(y - 46 + 56)
    frame = ('<rect x="5" y="5" width="1270" height="%d" rx="10" fill="none" stroke="#d9cdb0" stroke-width="10"/>'
             '<rect x="10" y="10" width="1260" height="%d" rx="4" fill="none" stroke="%s" stroke-width="1.6"/>'
             '<rect x="15" y="15" width="1250" height="%d" rx="2" fill="none" stroke="%s" stroke-width=".6"/>'
             % (h - 10, h - 20, INK, h - 30, INK))
    alt = " ".join("%s %s. %s, %s. %s" % (e[0], e[1].title(), e[2], e[3], " ".join(e[4])) for e in entries)
    return svg(1280, h, frame + "".join(body), "Logbook: experience", alt, "", T.defs_markup(), bg=PARCH, border=False)


def instruments():
    T = Type()
    rows = [("LANGUAGES", AMBER, ["Python", "TypeScript / JavaScript", "Java", "C / C++", "SQL"]),
            ("WEB", CORAL, ["React", "Next.js", "Tailwind CSS", "Node.js", "WebSocket", "WebRTC"]),
            ("AI / ML", TEAL, ["RAG pipelines", "FAISS", "LLM fine-tuning", "PyTorch", "TensorFlow", "scikit-learn"]),
            ("SYSTEMS", GREEN, ["Linux (RHEL)", "Docker", "Bash", "Electron", "Git"])]
    body, y, X, MAXW = [], 40, 300, 940
    for k, (lab, col, items) in enumerate(rows):
        base = y + 30
        body.append('<circle cx="62" cy="%s" r="4" fill="%s"/>' % (n(base - 7), col) + mono(80, base, lab, 20, col, ls=2.5))
        cx = X
        for j, it in enumerate(items):
            w = T.width(it, 26, "rb")
            if cx + w > X + MAXW:
                cx, base = X, base + 44
            body.append(T.draw(it, 26, cx, base, "rb", CREAM)[0])
            cx += w
            if j < len(items) - 1:
                body.append('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (n(cx + 18), n(base - 8), col))
                cx += 36
        y = base + 24
        if k < len(rows) - 1:
            body.append('<path d="M56 %sH1224" stroke="%s"/>' % (n(y), HAIR))
            y += 22
    h = int(y + 18)
    alt = " ".join("%s: %s." % (r[0].title(), ", ".join(r[2])) for r in rows)
    return svg(1280, h, specks(random.Random(77), 40, 0, 0, 1280, h, op0=.1, op1=.4) + "".join(body),
               "Instruments: toolbox", alt, "", T.defs_markup())


def colophon(dark):
    T = Type()
    ink, dim = (("#d6d1c4", DIM) if dark else (INK, INKDIM))
    line = "Away from the keyboard: astrophotography, chess, and games."
    m = T.draw(line, 34, 640 - T.width(line, 34, "ib") / 2, 52, "ib", ink)[0]
    body = (m + mono(640, 98, "EVERY IMAGE HERE IS HAND-WRITTEN SVG FROM scripts/build.py", 20, dim, "middle", .5)
            + mono(640, 126, "STAR CHART REDRAWN NIGHTLY · NO THIRD-PARTY WIDGETS", 20, dim, "middle", .5))
    return svg(1280, 150, body, "Colophon",
               line + " Every image here is hand-written SVG from scripts/build.py. "
               "Star chart redrawn nightly. No third-party widgets.", "", T.defs_markup(), bg=None, border=False)


HEADINGS = [("commits", "A year of commits, charted", "PLATE I · ACTIVITY", ""),
            ("catalogue", "Catalogue", "PLATE II · WORK", "Six objects, each one shipped. Click a plate to open it."),
            ("logbook", "Logbook", "PLATE IV · EXPERIENCE", ""),
            ("instruments", "Instruments", "PLATE V · TOOLBOX", ""),
            ("your-move", "Your move", "PLATE VI · CHESS",
             "This board is live. Click a move, press Create on the issue that opens, and the board redraws in about a minute.")]


# -------------------------------------------------------------------- main --
def write(name, text):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("%-28s %6.1f KB" % (name, len(text.encode()) / 1024))


def main():
    self_check()
    if "--check" in sys.argv:
        return
    old = os.path.join(ASSETS, "banner.svg")
    if os.path.exists(old):
        os.remove(old)
    cal = fetch_calendar()
    write("hero.svg", hero())
    text, S = sky(cal)
    write("sky.svg", text)
    print({k: (v if not isinstance(v, tuple) else tuple(str(x) for x in v)) for k, v in S.items()})
    for p in PLATES:
        write("plate-%s.svg" % p["slug"], plate(p))
    write("fieldnotes.svg", fieldnotes())
    for slug, title, kicker, sub in HEADINGS:
        for dark in (True, False):
            write("heading-%s-%s.svg" % (slug, "dark" if dark else "light"), heading(title, kicker, sub, dark))
    write("about.svg", about())
    for slug, label in (("portfolio", "somansh.in"), ("linkedin", "LinkedIn"), ("email", "somansh@somansh.in")):
        write("link-%s.svg" % slug, link(label))
    write("logbook.svg", logbook())
    write("instruments.svg", instruments())
    for dark in (True, False):
        write("colophon-%s.svg" % ("dark" if dark else "light"), colophon(dark))



if __name__ == "__main__":
    main()
