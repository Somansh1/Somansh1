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
from pathlib import Path
from urllib.parse import quote

import chess
import chess.svg

ROOT = Path(os.environ.get("CHESS_ROOT") or Path(__file__).resolve().parent.parent)
STATE = ROOT / "chess" / "state.json"
FRAGMENT = ROOT / "chess" / "fragment.md"
SVG = ROOT / "assets" / "chess-board.svg"
README = ROOT / "README.md"
REPO = "Somansh1/Somansh1"
MOVE_RE = re.compile(r"[a-h][1-8][a-h][1-8][qrbn]?")
LOGIN_RE = re.compile(r"[A-Za-z0-9-]{1,39}")
NAMES = {1: "Pawn", 2: "Knight", 3: "Bishop", 4: "Rook", 5: "Queen", 6: "King"}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


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


def apply_move(state, uci, by):
    """Mutates state. Returns (san, result or None). Raises ValueError on bad input."""
    if not isinstance(uci, str) or not MOVE_RE.fullmatch(uci):
        raise ValueError("That is not a valid move format.")
    if not isinstance(by, str) or not LOGIN_RE.fullmatch(by):
        raise ValueError("That is not a valid GitHub login.")
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
        "result": result,
        "moves": len(state["moves"]),
        "ended": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    }]
    state.clear()
    state.update(new_state(game + 1, history))
    return san, result


# ---------------------------------------------------------------- rendering
def safe_login(m):
    by = str(m.get("by", ""))
    return by if LOGIN_RE.fullmatch(by) else "unknown"


def piece_svg(sym):
    s = chess.svg.PIECES[sym]
    light, dark = "#f4eedd", "#0a0f24"
    if sym.isupper():
        s = s.replace('"#fff"', f'"{light}"').replace('"#000"', f'"{dark}"').replace('"#ececec"', f'"{light}"')
    else:
        s = s.replace('fill="#000"', f'fill="{dark}"').replace('stroke="#000"', f'stroke="{light}"')
        s = s.replace('"#fff"', f'"{light}"').replace('"#ececec"', f'"{light}"')
    if sym.isupper():
        s = s.replace("#ffffff", light).replace("#000000", dark)
    else:
        s = s.replace("fill:#000000", f"fill:{dark}").replace("stroke:#000000", f"stroke:{light}").replace("#ececec", light)
    return s.replace('stroke-width="1.5"', 'stroke-width="1.1"')


def status_lines(state, b):
    side = "WHITE" if b.turn else "BLACK"
    s1 = f"GAME {state['game']} · MOVE {b.fullmove_number} · {side} TO MOVE" + (" · CHECK" if b.is_check() else "")
    if state["moves"]:
        m = state["moves"][-1]
        s2 = f"LAST: {m['san']} by @{safe_login(m)}"
    else:
        s2 = "LAST: none yet, be the first to move"
    return s1, s2


def render_svg(state):
    b = board_of(state)
    S, X0, Y0 = 64, 64, 32

    def pos(sq):
        return X0 + chess.square_file(sq) * S, Y0 + (7 - chess.square_rank(sq)) * S

    side = "white" if b.turn else "black"
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="640" height="720" viewBox="0 0 640 720" role="img" aria-labelledby="t">',
         f'<title id="t">Chess game {state["game"]}, {side} to move</title>',
         '<rect width="640" height="720" rx="14" fill="#0a0f24"/>',
         '<rect x=".5" y=".5" width="639" height="719" rx="14" fill="none" stroke="#2a3263"/>']
    for sq in chess.SQUARES:
        x, y = pos(sq)
        c = "#141b3d" if (chess.square_file(sq) + chess.square_rank(sq)) % 2 == 0 else "#232c5c"
        o.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{c}"/>')
    if state["moves"]:
        m = chess.Move.from_uci(state["moves"][-1]["uci"])
        for sq in (m.from_square, m.to_square):
            x, y = pos(sq)
            o.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="#ffd43b" fill-opacity=".3"/>')
    o.append(f'<rect x="{X0}" y="{Y0}" width="{8*S}" height="{8*S}" fill="none" stroke="#2a3263"/>')
    if b.is_check():
        x, y = pos(b.king(b.turn))
        o.append(f'<circle cx="{x+S/2}" cy="{y+S/2}" r="29" fill="#ff5a45" fill-opacity=".18" stroke="#ff5a45" stroke-width="3"/>')
    k = S / 45
    for sq in chess.SQUARES:
        p = b.piece_at(sq)
        if p:
            x, y = pos(sq)
            o.append(f'<g transform="translate({x} {y}) scale({k:.4f})">{piece_svg(p.symbol())}</g>')
    mono = f'font-family="{MONO}" fill="#8f96b8" font-size="18"'
    for i in range(8):
        o.append(f'<text x="{X0+i*S+S/2}" y="{Y0+8*S+24}" text-anchor="middle" {mono}>{"abcdefgh"[i]}</text>')
        o.append(f'<text x="{X0-18}" y="{Y0+i*S+S/2+6}" text-anchor="middle" {mono}>{8-i}</text>')
    s1, s2 = status_lines(state, b)
    for text, y, fill, size in ((s1, 634, "#f4eedd", 20), (s2, 676, "#8f96b8", 18)):
        tl = f' textLength="{8*S}" lengthAdjust="spacingAndGlyphs"' if len(text) * size * 0.62 > 8 * S else ""
        o.append(f'<text x="{X0}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}"{tl}>{text}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def move_link(state, san, uci):
    url = ("https://github.com/" + REPO + "/issues/new?title="
           + quote(f"chess|move|{uci}|{state['game']}", safe="")
           + "&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.")
    return f"[{san}]({url})"


def render_fragment(state):
    b = board_of(state)
    side = "white" if b.turn else "black"
    rows = {}
    for mv in b.legal_moves:
        rows.setdefault(mv.from_square, []).append(mv)
    lines = ["## Your move", "",
             "This board is live. Pick a move below; it opens a pre-filled issue, and a GitHub Action plays it and redraws the board in about a minute.", "",
             '<p align="center">',
             f'  <img src="./assets/chess-board.svg" width="420" alt="Chess board, game {state["game"]}, move {b.fullmove_number}, {side} to move">',
             "</p>", "",
             f"Anyone can move for whichever side is to play. Right now it is {side}'s turn.", "",
             f"<details open><summary>Legal moves for {side} ({b.legal_moves.count()})</summary>", "",
             "| From | Moves |", "| --- | --- |"]
    for sq in sorted(rows, key=lambda s: (b.piece_type_at(s), s)):
        name = f"{NAMES[b.piece_type_at(sq)]} {chess.square_name(sq)}"
        links = " ".join(move_link(state, b.san(m), m.uci()) for m in sorted(rows[sq], key=lambda m: m.uci()))
        lines.append(f"| {name} | {links} |")
    lines += ["", "</details>", "", "<details><summary>Recent moves</summary>", ""]
    n = len(state["moves"])
    for i in range(max(0, n - 8), n):
        m = state["moves"][i]
        num = f"{i//2+1}." if i % 2 == 0 else f"{i//2+1}..."
        lines.append(f"- {num} {m['san']} by @{safe_login(m)}")
    if not n:
        lines.append("- No moves yet in this game.")
    h = state["history"]
    w, bl, d = (sum(1 for g in h if g["result"] == r) for r in ("1-0", "0-1", "1/2-1/2"))
    lines += ["", f"Finished games: {len(h)} (white won {w}, black won {bl}, drawn {d}). Game {state['game']} is in progress.",
              "", "</details>"]
    return "\n".join(lines) + "\n"


def render(state=None):
    state = state or load()
    write(SVG, render_svg(state))
    frag = render_fragment(state)
    write(FRAGMENT, frag)
    if README.exists():
        with open(README, encoding="utf-8", newline="") as f:
            t = f.read()
        pat = re.compile(r"(<!-- chess:start -->).*?(<!-- chess:end -->)", re.S)
        if pat.search(t):
            nl = "\r\n" if "\r\n" in t else "\n"
            # Blank line after the marker so the heading below is parsed as markdown, not as part of the comment block.
            body = nl + nl + frag.replace("\n", nl)
            t2 = pat.sub(lambda m: m.group(1) + body + m.group(2), t, count=1)
            if t2 != t:
                with open(README, "w", encoding="utf-8", newline="") as f:
                    f.write(t2)


# ---------------------------------------------------------------- commands
def do_move(uci, by):
    state = load()
    san, result = apply_move(state, uci, by)
    save(state)
    render(state)
    return san, result


def from_issue():
    """Reads ISSUE_TITLE / ISSUE_USER. Never echoes issue text. Always exits 0 so the workflow can reply."""
    title, user = os.environ.get("ISSUE_TITLE", ""), os.environ.get("ISSUE_USER", "")
    out_path = os.environ.get("RESULT_FILE", "chess-result.md")
    ok, san = False, ""
    parts = title.strip().split("|")
    try:
        if len(parts) != 4 or parts[0] != "chess" or parts[1] != "move" or not re.fullmatch(r"[0-9]{1,6}", parts[3]):
            raise ValueError("That title is not a chess move link. Please use the move links in the README.")
        if parts[3] != str(load()["game"]):
            raise ValueError("That move link is from an older position, so the game has moved on. Please pick a move from the current board.")
        san, result = do_move(parts[2], user)
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
    s = new_state(); s["fen"] = "8/P6k/8/8/8/8/8/K7 w - - 0 1"
    san, res = apply_move(s, "a7a8q", "carol")
    assert san == "a8=Q" and chess.Board(s["fen"]).piece_at(chess.A8).piece_type == chess.QUEEN and res is None
    s = new_state()
    for u in ("f2f3", "e7e5", "g2g4"):
        apply_move(s, u, "x")
    san, res = apply_move(s, "d8h4", "y")
    assert san == "Qh4#" and res == "0-1" and s["game"] == 2 and s["moves"] == [] and s["fen"] == chess.STARTING_FEN
    assert s["history"][0]["result"] == "0-1" and s["history"][0]["moves"] == 4
    for fen in (chess.STARTING_FEN, "8/P6k/8/8/8/8/8/K7 w - - 0 1", "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"):
        s = new_state(); s["fen"] = fen
        n = chess.Board(fen).legal_moves.count()
        assert render_fragment(s).count("issues/new?title=chess%7Cmove%7C") == n, fen
        assert render_fragment(s) == render_fragment(s) and render_svg(s) == render_svg(s)
    (tmp / "README.md").write_text("a\n<!-- chess:start -->\nold\n<!-- chess:end -->\nz\n")
    assert run("render").returncode == 0
    t = (tmp / "README.md").read_text()
    assert "old" not in t and t.startswith("a\n") and t.endswith("\nz\n") and "## Your move" in t
    shutil.rmtree(tmp)
    print("chess check: ok")


def main(argv):
    try:
        if len(argv) == 4 and argv[0] == "move" and argv[2] == "--by":
            san, result = do_move(argv[1], argv[3])
            print(f"played {san}" + (f" (game over {result})" if result else ""))
        elif argv == ["render"]:
            render()
        elif argv == ["check"]:
            check()
        elif argv == ["from-issue"]:
            from_issue()
        else:
            print("usage: game.py move <uci> --by <login> | render | check | from-issue", file=sys.stderr)
            return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
