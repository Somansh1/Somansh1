#!/usr/bin/env python3
"""Approximate GitHub's profile column: README.md -> preview/{index,light,dark}.html -> PNGs via headless Chrome."""
import html
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "preview")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def inline(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md(text):
    out, blocks = [], re.split(r"\n\s*\n", text.strip())
    for b in blocks:
        lines = b.split("\n")
        if b.startswith("<"):
            out.append(b)
        elif b.startswith("## "):
            out.append("<h2>%s</h2>" % inline(b[3:]))
        elif lines[0].startswith("|"):
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines if not re.match(r"^\|[-| ]+\|$", l)]
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (
                "".join("<th>%s</th>" % inline(c) for c in rows[0]),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows[1:])))
        elif lines[0].startswith("- "):
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(l[2:]) for l in lines))
        else:
            out.append("<p>%s</p>" % inline(b).replace("\n", "\n"))
    return "\n".join(out)


CSS = """
body{margin:0;padding:24px 0;font:16px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;background:%(bg)s;color:%(fg)s}
.col{width:846px;margin:0 auto}h2{font-size:24px;font-weight:600;border-bottom:1px solid %(rule)s;padding-bottom:.3em;margin:24px 0 16px}
a{color:%(link)s;text-decoration:none}img{max-width:100%%;vertical-align:middle}p{margin:0 0 16px}ul{padding-left:2em;margin:0 0 16px}
table{border-collapse:collapse;margin:0 0 16px;font-size:14px}td,th{border:1px solid %(rule)s;padding:6px 13px}details{margin:0 0 16px}summary{cursor:pointer}
"""
THEMES = {"light": dict(bg="#ffffff", fg="#1f2328", rule="#d1d9e0", link="#0969da"),
          "dark": dict(bg="#0d1117", fg="#f0f6fc", rule="#3d444d", link="#4493f8")}


def main():
    os.makedirs(OUT, exist_ok=True)
    body = md(open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()).replace('src="./assets/', 'src="../assets/').replace('srcset="./assets/', 'srcset="../assets/')
    def pick(b, dark):
        def f(m):
            src = re.search(r'srcset="([^"]+)"', m.group(0)).group(1)
            img = re.search(r'<img[^>]*>', m.group(0)).group(0)
            return re.sub(r'src="[^"]+"', 'src="%s"' % src, img) if dark else img
        return re.sub(r'<picture>.*?</picture>', f, b, flags=re.S)
    for name, t in list(THEMES.items()) + [("index", THEMES["light"])]:
        page_body = pick(body, name == "dark")
        page = "<!doctype html><meta charset=utf-8><style>%s</style><div class=col>%s</div>" % (CSS % t, page_body)
        open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(page)
    base = [CHROME, "--headless=new", "--hide-scrollbars", "--window-size=900,5200"]
    for name in THEMES:
        url = "file:///" + os.path.join(OUT, name + ".html").replace("\\", "/")
        subprocess.run(base + ["--force-prefers-reduced-motion", "--screenshot=" + os.path.join(OUT, name + ".png"), url])
    url = "file:///" + os.path.join(OUT, "dark.html").replace("\\", "/")
    subprocess.run(base + ["--virtual-time-budget=6000", "--screenshot=" + os.path.join(OUT, "dark-motion.png"), url])


if __name__ == "__main__":
    main()
