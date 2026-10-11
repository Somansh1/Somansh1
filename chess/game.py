#!/usr/bin/env python3
"""Community chess for a GitHub profile README. Dependency: python-chess (see requirements.txt)."""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path
from urllib.parse import quote

import chess
import chess.svg

ROOT = Path(os.environ.get("CHESS_ROOT") or Path(__file__).resolve().parent.parent)
STATE = ROOT / "chess" / "state.json"
FRAGMENT = ROOT / "chess" / "fragment.md"
# GitHub caches README images by URL for several minutes, so a redrawn board at the same path keeps showing the
# old position. Each position therefore gets its own file name, and the previous one is deleted.
def board_rel(state):
    return f"assets/chess/board-g{state['game']}-m{len(state['moves'])}.svg"

def hist_rel(state):
    return f"assets/chess/history-{len(state['history'])}.svg"
README = ROOT / "README.md"
REPO = "Somansh1/Somansh1"
MOVE_RE = re.compile(r"[a-h][1-8][a-h][1-8][qrbn]?")
LOGIN_RE = re.compile(r"[A-Za-z0-9-]{1,39}")
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
NAMES = {1: "Pawn", 2: "Knight", 3: "Bishop", 4: "Rook", 5: "Queen", 6: "King"}
VALUES = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}
START_COUNTS = {1: 8, 2: 2, 3: 2, 4: 2, 5: 1}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# palette
BG, HAIR, MUTED, CREAM, AMBER, CORAL = "#0c0c0e", "#2c2b2a", "#9c988c", "#f4eedd", "#ffd43b", "#ff5a45"
LIGHT_SQ, DARK_SQ = "#d8cfb8", "#8a7d66"
W_FILL, W_LINE, B_FILL, B_LINE = "#f7f1e1", "#2b2118", "#1b1714", "#f4eedd"
GREY = "#6b675d"


def new_state(game=1, history=None):
    return {"fen": chess.STARTING_FEN, "moves": [], "game": game, "history": history or []}


def load():
    return json.loads(STATE.read_text(encoding="utf-8"))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def save(state):
    write(STATE, json.dumps(state, indent=2) + "\n")


def board_of(state):
    """Replay the game (keeps repetition history); fall back to the stored FEN."""
    b = chess.Board()
    try:
        for m in state["moves"]:
            b.push_uci(m["uci"])
        if b.fen() == state["fen"]:
            return b
    except ValueError:
        pass
    return chess.Board(state["fen"])


REASONS = {chess.Termination.CHECKMATE: "checkmate", chess.Termination.STALEMATE: "stalemate"}


def apply_move(state, uci, by, date=None):
    """Mutates state. Returns (san, result or None). Raises ValueError on bad input.
    `date` (YYYY-MM-DD) is the move time; defaults to today's UTC date, only evaluated here."""
    if not isinstance(uci, str) or not MOVE_RE.fullmatch(uci):
        raise ValueError("That is not a valid move format.")
    if not isinstance(by, str) or not LOGIN_RE.fullmatch(by):
        raise ValueError("That is not a valid GitHub login.")
    if date is not None and not DATE_RE.fullmatch(date):
        raise ValueError("That is not a valid date.")
    b = board_of(state)
    try:
        mv = b.parse_uci(uci)
    except ValueError:
        raise ValueError("That move is not legal in the current position.") from None
    san = b.san(mv)
    b.push(mv)
    state["moves"].append({"san": san, "uci": uci, "by": by})
    state["fen"] = b.fen()
    out = b.outcome(claim_draw=True)
    if out is None:
        return san, None
    result = out.result()
    game = state["game"]
    history = state["history"] + [{
        "final_fen": b.fen(),
        "result": result,
        "reason": REASONS.get(out.termination, "draw rule"),
        "moves": len(state["moves"]),
        "ended": date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        "last_san": san,
        "last_by": by,
    }]
    state.clear()
    state.update(new_state(game + 1, history))
    return san, result


def migrate(rec):
    """Old records only had result / moves / ended."""
    r = dict(rec)
    r.setdefault("final_fen", None)
    r.setdefault("reason", "")
    r.setdefault("last_san", "")
    r.setdefault("last_by", "")
    r.setdefault("moves", 0)
    r.setdefault("ended", "")
    if r.get("result") not in ("1-0", "0-1", "1/2-1/2"):
        r["result"] = "1/2-1/2"
    return r


# ---------------------------------------------------------------- svg helpers
def safe_login(m):
    by = str(m.get("by", ""))
    return by if LOGIN_RE.fullmatch(by) else "unknown"


def piece_svg(sym, k, px_white=1.4, px_black=1.2):
    """Vector piece from python-chess, restyled. k = svg scale of the 45x45 piece box."""
    s = chess.svg.PIECES[sym]
    if sym.isupper():
        s = s.replace("#ffffff", W_FILL).replace("#fff", W_FILL).replace("#000000", W_LINE).replace("#000", W_LINE)
        w = px_white
    else:
        s = s.replace("fill:#000000", f"fill:{B_FILL}").replace('fill="#000"', f'fill="{B_FILL}"')
        s = s.replace("stroke:#000000", f"stroke:{B_LINE}").replace('stroke="#000"', f'stroke="{B_LINE}"')
        s = s.replace("#ffffff", B_LINE).replace("#fff", B_LINE).replace("#ececec", B_LINE)
        w = px_black
    return s.replace('stroke-width="1.5"', f'stroke-width="{w / k:.3f}"')


def T(x, y, s, size=20, fill=CREAM, anchor=None, maxw=None, weight=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    wt = f' font-weight="{weight}"' if weight else ""
    tl = f' textLength="{maxw}" lengthAdjust="spacingAndGlyphs"' if maxw and len(s) * size * 0.61 > maxw else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}"{a}{wt}{tl}>'
            f'{escape(s)}</text>')


def draw_board(o, b, X0, Y0, S, last=None, ring=None, coords=False, label=20):
    sq_pos = lambda sq: (X0 + chess.square_file(sq) * S, Y0 + (7 - chess.square_rank(sq)) * S)
    for sq in chess.SQUARES:
        x, y = sq_pos(sq)
        c = DARK_SQ if (chess.square_file(sq) + chess.square_rank(sq)) % 2 == 0 else LIGHT_SQ
        o.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{c}"/>')
    for sq in last or ():
        x, y = sq_pos(sq)
        o.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{AMBER}" fill-opacity=".45"/>')
    o.append(f'<rect x="{X0}" y="{Y0}" width="{8*S}" height="{8*S}" fill="none" stroke="{HAIR}" stroke-width="2"/>')
    if ring is not None:
        x, y = sq_pos(ring)
        o.append(f'<circle cx="{x+S/2}" cy="{y+S/2}" r="{S*0.45:.1f}" fill="{CORAL}" fill-opacity=".2" '
                 f'stroke="{CORAL}" stroke-width="{max(2, S/20):.1f}"/>')
    k = S / 45
    for sq in chess.SQUARES:
        p = b.piece_at(sq)
        if p:
            x, y = sq_pos(sq)
            o.append(f'<g transform="translate({x} {y}) scale({k:.4f})">{piece_svg(p.symbol(), k)}</g>')
    if coords:
        for i in range(8):
            o.append(T(X0 + i * S + S / 2, Y0 + 8 * S + 26, "abcdefgh"[i], label, MUTED, "middle"))
            o.append(T(X0 - 20, Y0 + i * S + S / 2 + 7, str(8 - i), label, MUTED, "middle"))


def captured(b):
    """({piece_type: n} taken by white, taken by black, material lead for white).
    ponytail: promotions count as a captured pawn plus an extra piece; fine for a glance."""
    def cnt(color):
        return {t: len(b.pieces(t, color)) for t in VALUES}
    w, bl = cnt(chess.WHITE), cnt(chess.BLACK)
    by_white = {t: max(0, START_COUNTS[t] - bl[t]) for t in VALUES}
    by_black = {t: max(0, START_COUNTS[t] - w[t]) for t in VALUES}
    lead = sum(VALUES[t] * (w[t] - bl[t]) for t in VALUES)
    return by_white, by_black, lead


def cap_row(o, x, y, taken, color_of_taken, lead_text):
    """Row of small glyphs of the pieces taken (pieces of color_of_taken)."""
    o.append(f'<rect x="{x}" y="{y}" width="536" height="36" rx="8" fill="#151416"/>')
    o.append(f'<circle cx="{x+20}" cy="{y+18}" r="8" fill="{W_FILL if color_of_taken == chess.BLACK else B_FILL}" '
             f'stroke="{B_LINE}" stroke-width="1.4"/>')
    k, gx = 28 / 45, x + 44
    for t in sorted(taken, reverse=True):
        for _ in range(taken[t]):
            sym = chess.Piece(t, color_of_taken).symbol()
            o.append(f'<g transform="translate({gx} {y+4}) scale({k:.4f})">{piece_svg(sym, k, 1.0, 1.0)}</g>')
            gx += 20
    if lead_text:
        o.append(T(x + 520, y + 26, lead_text, 20, AMBER, "end"))


# ---------------------------------------------------------------- main board
def render_svg(state):
    b = board_of(state)
    moves = state["moves"]
    S, X0, Y0 = 76, 56, 24
    side = "white" if b.turn else "black"
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="t">',
         f'<title id="t">Chess game {state["game"]}, move {b.fullmove_number}, {side} to move</title>',
         f'<rect width="1280" height="720" rx="14" fill="{BG}"/>',
         f'<rect x=".5" y=".5" width="1279" height="719" rx="14" fill="none" stroke="{HAIR}"/>']
    last = None
    if moves:
        m = chess.Move.from_uci(moves[-1]["uci"])
        last = (m.from_square, m.to_square)
    draw_board(o, b, X0, Y0, S, last, b.king(b.turn) if b.is_check() else None, coords=True)

    # scoresheet
    RX = 704
    o.append(T(RX, 58, f"GAME {state['game']}", 28, CREAM, weight="bold"))
    o.append(T(1240, 58, f"MOVE {b.fullmove_number}", 20, MUTED, "end"))
    o.append(f'<path d="M{RX} 76H1240" stroke="{HAIR}" stroke-width="2"/>')
    pairs = [(moves[i], moves[i + 1] if i + 1 < len(moves) else None) for i in range(0, len(moves), 2)]
    shown = pairs[-14:]
    first_no = len(pairs) - len(shown) + 1
    y0, rh = 88, 28
    r0 = 0
    if len(pairs) > len(shown):
        o.append(T(RX + 8, y0 + 21, "…", 20, MUTED))
        r0 = 1
    if not pairs:
        o.append(T(RX + 8, y0 + 21, "1.", 20, MUTED))
        o.append(T(RX + 96, y0 + 21, "…", 20, MUTED))
        o.append(T(RX + 8, y0 + rh + 21 + 8, "No moves yet. Be the first.", 20, MUTED))
    latest = len(moves) - 1
    for j, (wm, bm) in enumerate(shown):
        ry = y0 + (r0 + j) * rh
        no = first_no + j
        o.append(T(RX + 8, ry + 21, f"{no}.", 20, MUTED))
        for col, m, idx in ((RX + 96, wm, (no - 1) * 2), (RX + 256, bm, (no - 1) * 2 + 1)):
            if m is None:
                continue
            if idx == latest:
                o.append(f'<rect x="{col-8}" y="{ry+1}" width="{len(m["san"])*12.2+16:.0f}" height="26" rx="13" fill="{AMBER}"/>')
                o.append(T(col, ry + 21, m["san"], 20, BG, weight="bold"))
            else:
                o.append(T(col, ry + 21, m["san"], 20, CREAM))
    # captured material
    by_w, by_b, lead = captured(b)
    cap_row(o, RX, 522, by_w, chess.BLACK, f"+{lead}" if lead > 0 else "")
    cap_row(o, RX, 564, by_b, chess.WHITE, f"+{-lead}" if lead < 0 else "")
    o.append(f'<path d="M{RX} 616H1240" stroke="{HAIR}" stroke-width="2"/>')
    # status
    o.append(T(RX, 650, f"{side.upper()} TO MOVE", 24, CREAM, weight="bold"))
    if b.is_check():
        o.append(T(1240, 650, "CHECK", 24, CORAL, "end", weight="bold"))
    last_line = (f"LAST: {moves[-1]['san']} by @{safe_login(moves[-1])}" if moves else "LAST: none yet")
    o.append(T(RX, 688, last_line, 20, MUTED, maxw=536))
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- history
def render_history(state):
    hist = [migrate(r) for r in state["history"]]
    if not hist:
        o = ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="120" viewBox="0 0 1280 120" role="img" aria-labelledby="t">',
             '<title id="t">No finished chess games yet</title>',
             f'<rect width="1280" height="120" rx="14" fill="{BG}"/>',
             f'<rect x=".5" y=".5" width="1279" height="119" rx="14" fill="none" stroke="{HAIR}"/>',
             T(640, 70, f"NO FINISHED GAMES YET · GAME {state['game']} IN PROGRESS", 28, MUTED, "middle", maxw=1200),
             "</svg>"]
        return "\n".join(o) + "\n"
    n = len(hist)
    w, d, bl = (sum(1 for g in hist if g["result"] == r) for r in ("1-0", "1/2-1/2", "0-1"))
    recent = list(range(n - 1, max(-1, n - 9), -1))
    rows = (len(recent) + 3) // 4
    CW, CH, GAP, PX, TOP = 282, 392, 24, 40, 168
    H = TOP + rows * CH + (rows - 1) * GAP + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{H}" viewBox="0 0 1280 {H}" role="img" aria-labelledby="t">',
         f'<title id="t">Finished chess games: {n}. White won {w}, drawn {d}, black won {bl}.</title>',
         f'<rect width="1280" height="{H}" rx="14" fill="{BG}"/>',
         f'<rect x=".5" y=".5" width="1279" height="{H-1}" rx="14" fill="none" stroke="{HAIR}"/>',
         T(PX, 56, f"FINISHED GAMES · {n}", 26, CREAM, weight="bold")]
    BW = 1200
    x = PX
    segs = [(w, CREAM, None), (d, GREY, None), (bl, B_FILL, CREAM)]
    for i, (c, fill, line) in enumerate(segs):
        if not c:
            continue
        wd = round(BW * c / n) if i < 2 else PX + BW - x
        wd = min(wd, PX + BW - x)
        st = f' stroke="{line}" stroke-width="1.4"' if line else ""
        o.append(f'<rect x="{x}" y="76" width="{wd}" height="28" fill="{fill}"{st}/>')
        x += wd
    o.append(T(PX, 134, f"WHITE {w}", 22, CREAM))
    o.append(T(640, 134, f"DRAWS {d}", 22, MUTED, "middle"))
    o.append(T(PX + BW, 134, f"BLACK {bl}", 22, CREAM, "end"))
    for pos, gi in enumerate(recent):
        g = hist[gi]
        cx = PX + (pos % 4) * (CW + GAP)
        cy = TOP + (pos // 4) * (CH + GAP)
        o.append(f'<g class="card"><rect x="{cx}" y="{cy}" width="{CW}" height="{CH}" rx="12" fill="#151416" stroke="{HAIR}" stroke-width="2"/>')
        S = 26
        bx, by = cx + (CW - 8 * S) // 2, cy + 18
        if g["final_fen"]:
            fb = chess.Board(g["final_fen"])
            ring = fb.king(fb.turn) if g["reason"] == "checkmate" else None
            draw_board(o, fb, bx, by, S, None, ring)
        else:
            draw_board(o, chess.Board(None), bx, by, S)
        ty = by + 8 * S + 40
        o.append(T(cx + 16, ty, f"GAME {gi+1} · {g['result']}", 22, CREAM, weight="bold", maxw=CW - 32))
        if g["last_san"]:
            who = g["last_by"] or "unknown"
            room = 21 - len(g["last_san"]) - 5
            who = who if len(who) <= room else who[:max(3, room - 1)] + "…"
            o.append(T(cx + 16, ty + 34, f"{g['last_san']} by @{who}", 20, CREAM, maxw=CW - 32))
        mv = f"{g['moves']} moves" + (f" · {g['ended']}" if g["ended"] else "")
        o.append(T(cx + 16, ty + 68, mv, 20, MUTED, maxw=CW - 32))
        if g["reason"]:
            o.append(T(cx + 16, ty + 100, g["reason"], 20, MUTED, maxw=CW - 32))
        o.append("</g>")
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- fragment
def move_link(state, san, uci):
    url = ("https://github.com/" + REPO + "/issues/new?title="
           + quote(f"chess|move|{uci}|{state['game']}", safe="")
           + "&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.")
    return f"[{san}]({url})"


def history_alt(state):
    hist = [migrate(r) for r in state["history"]]
    if not hist:
        return f"No finished chess games yet. Game {state['game']} is in progress."
    w, d, bl = (sum(1 for g in hist if g["result"] == r) for r in ("1-0", "1/2-1/2", "0-1"))
    g = hist[-1]
    how = {"1-0": "white won", "0-1": "black won"}.get(g["result"], "drawn")
    why = f" by {g['reason']}" if g["reason"] and how != "drawn" else (f" ({g['reason']})" if g["reason"] else "")
    return (f"Finished chess games: {len(hist)}. White won {w}, drawn {d}, black won {bl}. "
            f"Most recent: game {len(hist)}, {how}{why}.")


ORDER = {chess.KING: 0, chess.QUEEN: 1, chess.ROOK: 2, chess.BISHOP: 3, chess.KNIGHT: 4}
PNAME = {1: "pawn", 2: "knight", 3: "bishop", 4: "rook", 5: "queen", 6: "king"}


def tok(san):
    """Filename-safe token for a SAN. Uppercase B gets a dash so Bxc3 and bxc3 differ on case-insensitive disks."""
    t = san.replace("+", "-check").replace("#", "-mate").replace("=", "-eq")
    return "B-" + t[1:] if t[0] == "B" else t


def pill(w, border, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="56" viewBox="0 0 {w} 56">\n'
            f'{body}\n</svg>\n')


def button_svg(san):
    """Pure function of the SAN string (GitHub caches images by URL)."""
    w = max(88, round(len(san) * 14.5 + 44))
    border = AMBER if san[-1] in "+#" else CORAL if "x" in san else "#3a3835"
    return pill(w, border,
                f'<rect x=".75" y=".75" width="{w-1.5}" height="54.5" rx="27.25" fill="#151517" stroke="{border}" stroke-width="1.5"/>\n'
                f'<text x="{w/2}" y="36" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="bold" fill="{CREAM}">{escape(san)}</text>')


def chip_svg(sym, label):
    w = 148  # fixed so the buttons line up in a column
    k = 40 / 45
    return pill(w, "",
                f'<rect x=".75" y=".75" width="{w-1.5}" height="54.5" rx="27.25" fill="{LIGHT_SQ}" stroke="{DARK_SQ}" stroke-width="1.5"/>\n'
                f'<g transform="translate(12 8) scale({k:.4f})">{piece_svg(sym, k, 1.2, 1.2)}</g>\n'
                f'<text x="58" y="36" font-family="{MONO}" font-size="24" font-weight="bold" fill="{W_LINE}">{escape(label)}</text>')


def picker(state, b):
    """Returns (html lines, {relpath: svg content})."""
    files, lines = {}, []
    col = "w" if b.turn else "b"
    groups, pawns = {}, []
    for mv in b.legal_moves:
        if b.piece_type_at(mv.from_square) == chess.PAWN:
            pawns.append(mv)
        else:
            groups.setdefault(mv.from_square, []).append(mv)

    def row(chip_name, chip_sym, label, alt, moves):
        files[f"assets/chess/{chip_name}.svg"] = chip_svg(chip_sym, label)
        cells = [f'<img src="./assets/chess/{chip_name}.svg" height="30" alt="{alt}">']
        for m in moves:
            san = b.san(m)
            files[f"assets/chess/m-{tok(san)}.svg"] = button_svg(san)
            href = move_link(state, san, m.uci())[len(san) + 3:-1]
            cells.append(f'<a href="{href}"><img src="./assets/chess/m-{tok(san)}.svg" height="30" alt="Play {escape(san)}"></a>')
        lines.append(" ".join(cells) + "<br>")

    cname = "White" if b.turn else "Black"
    for sq in sorted(groups, key=lambda s: (ORDER[b.piece_type_at(s)], s)):
        pt = b.piece_type_at(sq)
        n = chess.square_name(sq)
        row(f"p-{col}-{chess.piece_symbol(pt)}-{n}", chess.Piece(pt, b.turn).symbol(), n,
            f"{cname} {PNAME[pt]} on {n}:", sorted(groups[sq], key=lambda m: m.uci()))
    if pawns:
        row(f"p-{col}-pawns", chess.Piece(chess.PAWN, b.turn).symbol(), "PAWNS", f"{cname} pawns:",
            sorted(pawns, key=lambda m: (chess.square_file(m.from_square), m.uci())))
    return lines, files


def render_fragment(state):
    return fragment_and_files(state)[0]


def fragment_and_files(state):
    b = board_of(state)
    side = "white" if b.turn else "black"
    last = f", last move {state['moves'][-1]['san']}" if state["moves"] else ""
    pick, files = picker(state, b)
    lines = ['<p align="center">',
             '<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/heading-your-move-dark.svg">'
             '<img src="./assets/heading-your-move-light.svg" alt="Your move. This chess board is live: click a move below, press Create on the issue that opens, and the board redraws in about a minute." width="100%"></picture>',
             "</p>", "",
             '<p align="center">',
             f'<img src="./{board_rel(state)}" width="100%" alt="Chess board with the move list, game {state["game"]}, move {b.fullmove_number}, {side} to move{last}">',
             "</p>", "",
             '<p align="left">', *pick, "</p>", "",
             '<p align="center">',
             f'<img src="./{hist_rel(state)}" width="100%" alt="{escape(history_alt(state), quote=True)}">',
             "</p>", "",
             "<details><summary>Moves as text</summary>", "",
             f"Legal moves for {side} ({b.legal_moves.count()}):", ""]
    rows = {}
    for mv in b.legal_moves:
        rows.setdefault(mv.from_square, []).append(mv)
    for sq in sorted(rows, key=lambda s: (b.piece_type_at(s), s)):
        links = " ".join(move_link(state, b.san(m), m.uci()) for m in sorted(rows[sq], key=lambda m: m.uci()))
        lines.append(f"- {NAMES[b.piece_type_at(sq)]} {chess.square_name(sq)}: {links}")
    lines += ["", "Recent moves:", ""]
    n = len(state["moves"])
    for i in range(max(0, n - 8), n):
        m = state["moves"][i]
        num = f"{i//2+1}." if i % 2 == 0 else f"{i//2+1}..."
        lines.append(f"- {num} {m['san']} by @{safe_login(m)}")
    if not n:
        lines.append("- No moves yet in this game.")
    lines += ["", "</details>"]
    return "\n".join(lines) + "\n", files

def render(state=None):
    state = state or load()
    keep = {ROOT / board_rel(state): render_svg(state), ROOT / hist_rel(state): render_history(state)}
    for old in [*(ROOT / "assets" / "chess").glob("board-*.svg"), *(ROOT / "assets" / "chess").glob("history-*.svg"),
                ROOT / "assets" / "chess-board.svg", ROOT / "assets" / "chess-history.svg"]:
        if old not in keep and old.exists():
            old.unlink()
    for path, svg in keep.items():
        write(path, svg)
    frag, files = fragment_and_files(state)
    for rel, svg in files.items():
        p = ROOT / rel
        if not p.exists() or p.read_text(encoding='utf-8') != svg:
            write(p, svg)
    write(FRAGMENT, frag)
    if README.exists():
        with open(README, encoding="utf-8", newline="") as f:
            t = f.read()
        pat = re.compile(r"(<!-- chess:start -->).*?(<!-- chess:end -->)", re.S)
        if pat.search(t):
            nl = "\r\n" if "\r\n" in t else "\n"
            body = nl + frag.replace("\n", nl)
            t2 = pat.sub(lambda m: m.group(1) + body + m.group(2), t, count=1)
            if t2 != t:
                with open(README, "w", encoding="utf-8", newline="") as f:
                    f.write(t2)


# ---------------------------------------------------------------- commands
def do_move(uci, by, date=None):
    state = load()
    san, result = apply_move(state, uci, by, date)
    save(state)
    render(state)
    return san, result


def from_issue():
    """Reads ISSUE_TITLE / ISSUE_USER (/ ISSUE_DATE). Never echoes issue text. Always exits 0 so the workflow can reply."""
    title, user = os.environ.get("ISSUE_TITLE", ""), os.environ.get("ISSUE_USER", "")
    date = os.environ.get("ISSUE_DATE", "")[:10]
    date = date if DATE_RE.fullmatch(date) else None
    out_path = os.environ.get("RESULT_FILE", "chess-result.md")
    ok, san = False, ""
    parts = title.strip().split("|")
    try:
        if len(parts) != 4 or parts[0] != "chess" or parts[1] != "move" or not re.fullmatch(r"[0-9]{1,6}", parts[3]):
            raise ValueError("That title is not a chess move link. Please use the move links in the README.")
        if parts[3] != str(load()["game"]):
            raise ValueError("That move link is from an older position, so the game has moved on. Please pick a move from the current board.")
        san, result = do_move(parts[2], user, date)
        ok = True
        msg = f"Played **{san}** for @{user}. The board is updated."
        if result:
            msg += f" The game ended ({result}) and a new game has started."
    except ValueError as e:
        msg = f"Move rejected: {e}"
    write(Path(out_path), msg + "\n")
    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        with open(gh, "a", encoding="utf-8") as f:
            f.write(f"ok={'true' if ok else 'false'}\nsan={san}\n")
    print(msg)


def play(state, ucis, by="x"):
    for u in ucis.split():
        apply_move(state, u, by, "2026-10-12")
    return state


def check():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "chess").mkdir()
    env = dict(os.environ, CHESS_ROOT=str(tmp))
    st = tmp / "chess" / "state.json"

    def run(*a, e=env):
        return subprocess.run([sys.executable, __file__, *a], env=e, capture_output=True, text=True)

    st.write_text(json.dumps(new_state()))
    before = st.read_text()
    for bad in ("e2e5", "e2e4x", "E2E4", "e2e4;", "", "a7a8q"):
        r = run("move", bad, "--by", "alice")
        assert r.returncode != 0 and st.read_text() == before, bad
    for bad in ("bad login", "a" * 40, "x;y", ""):
        assert run("move", "e2e4", "--by", bad).returncode != 0 and st.read_text() == before, bad
    assert run("move", "e2e4", "--by", "alice", "--date", "nope").returncode != 0 and st.read_text() == before
    assert run("move", "e2e4", "--by", "alice").returncode == 0
    s = json.loads(st.read_text())
    assert s["moves"] == [{"san": "e4", "uci": "e2e4", "by": "alice"}] and " b " in s["fen"]
    e2 = dict(env, ISSUE_TITLE="chess|move|e7e5|9", ISSUE_USER="bob", RESULT_FILE=str(tmp / "r.md"))
    run("from-issue", e=e2)
    assert "older position" in (tmp / "r.md").read_text() and len(json.loads(st.read_text())["moves"]) == 1
    e2["ISSUE_TITLE"] = "chess|move|e7e5|1"
    run("from-issue", e=e2)
    assert len(json.loads(st.read_text())["moves"]) == 2
    e2["ISSUE_TITLE"] = "chess|move|e7e5|1|x"
    run("from-issue", e=e2)
    assert len(json.loads(st.read_text())["moves"]) == 2
    # scoresheet: e4 e5 Nf3 -> row 1 has e4 and e5, row 2 has Nf3
    sv = render_svg(play(new_state(), "e2e4 e7e5 g1f3"))
    yof = lambda t: re.search(rf'y="(\d+)"[^>]*>{t}</text>', sv).group(1)
    assert yof("e4") == yof("e5") != yof("Nf3") and yof("1\\.") == yof("e4") and ">2.<" in sv
    assert "WHITE TO MOVE" not in sv and "BLACK TO MOVE" in sv and "by @x" in sv
    assert "No moves yet. Be the first." in render_svg(new_state()) and ">1.<" in render_svg(new_state())
    s = new_state(); s["fen"] = "8/P6k/8/8/8/8/8/K7 w - - 0 1"
    san, res = apply_move(s, "a7a8q", "carol")
    assert san == "a8=Q" and chess.Board(s["fen"]).piece_at(chess.A8).piece_type == chess.QUEEN and res is None
    # fool's mate rolls over, history record complete
    s = play(new_state(), "f2f3 e7e5 g2g4")
    san, res = apply_move(s, "d8h4", "y", "2026-10-12")
    assert san == "Qh4#" and res == "0-1" and s["game"] == 2 and s["moves"] == [] and s["fen"] == chess.STARTING_FEN
    rec = s["history"][0]
    assert rec == {"final_fen": rec["final_fen"], "result": "0-1", "reason": "checkmate", "moves": 4,
                   "ended": "2026-10-12", "last_san": "Qh4#", "last_by": "y"}
    assert chess.Board(rec["final_fen"]).is_checkmate()
    # history svg: one card per finished game, max 8, old records migrate
    assert render_history(new_state()).count('class="card"') == 0 and "NO FINISHED GAMES YET" in render_history(new_state())
    for n in (1, 3, 8, 11):
        hs = new_state(n + 1, [rec] * n)
        assert render_history(hs).count('class="card"') == min(n, 8), n
    old = new_state(3, [{"result": "1-0", "moves": 20, "ended": "2026-01-01"}, rec])
    assert render_history(old).count('class="card"') == 2
    for fen in (chess.STARTING_FEN, "8/P6k/8/8/8/8/8/K7 w - - 0 1", "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"):
        s = new_state(); s["fen"] = fen
        n = chess.Board(fen).legal_moves.count()
        fr = render_fragment(s)
        assert len(re.findall(r'<a href="[^"]*chess%7Cmove%7C[^"]*"><img src="\./assets/chess/m-[^"]+" height="30" alt="Play ', fr)) == n, fen
        assert len(re.findall(r"\[[^\]]+\]\(https://[^)]*chess%7Cmove%7C", fr)) == n, fen
        assert fr.count("issues/new?title=chess%7Cmove%7C") == 2 * n
        assert "<table" not in fr and "|" not in re.sub(r"<details>.*?</details>", "", fr, flags=re.S).replace("%7C", "")
        assert fr == render_fragment(s) and render_svg(s) == render_svg(s) and render_history(s) == render_history(s)
        st.write_text(json.dumps(s))
        assert run("render").returncode == 0
        for ref in set(re.findall(r'\./(assets/chess/[^"]+\.svg)', fr)):
            assert (tmp / ref).exists(), ref
    assert button_svg("Nf3") == button_svg("Nf3") != button_svg("Nxf3")
    assert 'stroke="#ff5a45"' in button_svg("Nxf3") and 'stroke="#ffd43b"' in button_svg("Qh5+") and 'stroke="#ffd43b"' in button_svg("Qh4#")
    assert {tok("O-O"), tok("Bxc3"), tok("bxc3"), tok("e8=Q+")} == {"O-O", "B-xc3", "bxc3", "e8-eqQ-check"}
    (tmp / "README.md").write_text("a\n<!-- chess:start -->\nold\n<!-- chess:end -->\nz\n")
    assert run("render").returncode == 0
    t = (tmp / "README.md").read_text()
    assert "old" not in t and t.startswith("a\n") and t.endswith("\nz\n") and "heading-your-move" in t
    assert len(list((tmp / "assets" / "chess").glob("history-*.svg"))) == 1 and len(list((tmp / "assets" / "chess").glob("board-*.svg"))) == 1
    shutil.rmtree(tmp)
    print("chess check: ok")


def main(argv):
    try:
        if len(argv) in (4, 6) and argv[0] == "move" and argv[2] == "--by" and (len(argv) == 4 or argv[4] == "--date"):
            san, result = do_move(argv[1], argv[3], argv[5] if len(argv) == 6 else None)
            print(f"played {san}" + (f" (game over {result})" if result else ""))
        elif argv == ["render"]:
            render()
        elif argv == ["check"]:
            check()
        elif argv == ["from-issue"]:
            from_issue()
        else:
            print("usage: game.py move <uci> --by <login> [--date YYYY-MM-DD] | render | check | from-issue", file=sys.stderr)
            return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
