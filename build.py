#!/usr/bin/env python3
"""Baut aus content.json, style.css, assets/ und fonts/ eine einzelne HTML-Datei.

Bilder werden als WebP eingebettet, die Schrift auf die tatsächlich benutzten
Zeichen reduziert. Ergebnis laeuft per Doppelklick, ohne Server und ohne Netz.

    python3 build.py
"""

import base64
import html
import io
import json
import re
from pathlib import Path

from PIL import Image
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

ROOT = Path(__file__).parent
OUT = ROOT / "arduino.html"

CONTENT = ROOT / "content.json"
STYLE = ROOT / "style.css"
ASSETS = ROOT / "assets"
FONTS = ROOT / "fonts"

WEBP_QUALITY = 86


# --------------------------------------------------------------------------- Bilder


def embed_image(src: str) -> str:
    """'/assets/x.png' -> data-URI mit WebP. Lossless nur, wenn es kleiner ausfaellt."""
    img = Image.open(ASSETS / Path(src).name)
    variants = []
    for lossless in (False, True):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=WEBP_QUALITY, lossless=lossless, method=6)
        variants.append(buf.getvalue())
    data = min(variants, key=len)
    return "data:image/webp;base64," + base64.b64encode(data).decode()


# --------------------------------------------------------------------------- Schrift


def embed_font(path: Path, text: str) -> str:
    """Lato auf die vorkommenden Zeichen reduzieren und als WOFF2 einbetten."""
    font = TTFont(path)
    options = Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga"]
    options.desubroutinize = True
    options.drop_tables += ["GSUB", "GPOS"]
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()


# --------------------------------------------------------------------------- Code


KEYWORDS = (
    "void|int|long|unsigned|const|bool|float|char|static|if|else|for|while|"
    "return|true|false|HIGH|LOW|OUTPUT|INPUT_PULLUP|INPUT"
)
TOKENS = re.compile(
    r"(//[^\n]*|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|#[a-z]+"
    rf"|\b(?:{KEYWORDS})\b|\b\d+(?:\.\d+)?\b)"
)
KEYWORD_TOKEN = re.compile(rf"^(?:#[a-z]+|(?:{KEYWORDS})$)")


def highlight(code: str) -> str:
    """Faerbung schon beim Bauen, damit der Browser kein Highlighter-Skript braucht."""
    out = []
    for token in TOKENS.split(code):
        if not token:
            continue
        escaped = html.escape(token)
        if token.startswith("//"):
            cls = "code-comment"
        elif token[0] in "\"'":
            cls = "code-string"
        elif token[0].isdigit():
            cls = "code-number"
        elif KEYWORD_TOKEN.match(token):
            cls = "code-keyword"
        else:
            out.append(escaped)
            continue
        out.append(f'<span class="{cls}">{escaped}</span>')
    return "".join(out)


# --------------------------------------------------------------------------- Links


def rewrite_links(markup: str) -> str:
    """Seitenlinks der alten Routen auf die Hash-Navigation der Einzeldatei umbiegen."""
    return re.sub(r'href="/([a-z0-9-]+)(?:#([^"]+))?"', lambda m: f'href="#{m[1]}{"/" + m[2] if m[2] else ""}"', markup)


# --------------------------------------------------------------------------- Bausteine


ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2"/>'
    '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "play": '<path d="M6 3v18l15-9Z"/>',
}


def icon(name: str, size: int = 22, cls: str = "") -> str:
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{ICONS[name]}</svg>'
    )


BREADBOARD_COLUMNS = [146, 174, 202, 230, 258, 342, 370, 398, 426, 454]
BREADBOARD_ROWS = [90, 126, 162, 198, 234]


def breadboard() -> str:
    labels = "".join(
        f'<text x="{x}" y="35">{"abcdefghij"[i]}</text>'
        for i, x in enumerate(BREADBOARD_COLUMNS)
    )
    numbers = "".join(
        f'<text x="116" y="{y + 6}">{i + 1}</text>' for i, y in enumerate(BREADBOARD_ROWS)
    )
    rows = ""
    for y in BREADBOARD_ROWS:
        holes = "".join(
            f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#495253" stroke-width="2"/>'
            for x in [48, 80, *BREADBOARD_COLUMNS]
        )
        stroke = "#28735a" if y == 126 else "#acb7b3"
        rows += (
            f'<g><path d="M146 {y}H258 M342 {y}H454" stroke="{stroke}" stroke-width="8" '
            f'stroke-linecap="round"/>{holes}</g>'
        )
    return f"""<figure class="breadboard-guide">
<div class="breadboard-diagram" tabindex="0" role="region" aria-label="Breadboard-Diagramm, bei Bedarf seitlich verschiebbar">
<svg viewBox="0 0 500 312" role="img" aria-labelledby="breadboard-title breadboard-description">
<title id="breadboard-title">So sind die L&ouml;cher eines Breadboards verbunden</title>
<desc id="breadboard-description">Vereinfachter Ausschnitt. Pro nummerierter Reihe sind a bis e miteinander verbunden und f bis j miteinander verbunden. Zwischen e und f liegt eine trennende Mittelrille. Unterschiedliche Reihen sind getrennt. Die beiden links gezeigten Versorgungsschienen verlaufen l&auml;ngs und sind voneinander getrennt.</desc>
<rect x="14" y="46" width="470" height="220" rx="8" fill="#fff" stroke="#a8aaad"/>
<rect x="281" y="48" width="39" height="216" fill="#eef0f1"/>
<g font-family="Lato, Arial, sans-serif" font-size="18" text-anchor="middle" fill="#30383a">
<text x="48" y="35" fill="#9c2424">+</text><text x="80" y="35" fill="#1b5390">&minus;</text>{labels}{numbers}</g>
<path d="M48 74V249" stroke="#a72f2f" stroke-width="5"/>
<path d="M80 74V249" stroke="#245b98" stroke-width="5"/>{rows}
<path d="M300 275V290" stroke="#647074"/>
<text x="300" y="307" font-family="Lato, Arial, sans-serif" font-size="18" text-anchor="middle" fill="#30383a">Mittelrille: keine Verbindung</text>
</svg></div>
<figcaption>Vereinfachter Ausschnitt: Die Linien zeigen die Kontakte im Innern. Die seitlichen Schienen k&ouml;nnen je nach Breadboard unterbrochen sein.</figcaption>
</figure>"""


def render_block(block: dict) -> str:
    kind = block["type"]
    if kind == "html":
        return f'<div class="prose-content">{rewrite_links(block["html"])}</div>'
    if kind == "code":
        return f"""<div class="code-block"><div class="code-toolbar"><span>Codeausschnitt</span>
<button type="button" class="copy" aria-label="Code kopieren">{icon("copy", 14)}<span aria-live="polite">Code kopieren</span></button>
</div><pre tabindex="0" aria-label="Arduino-Code"><code>{highlight(block["code"])}</code></pre></div>"""
    if kind == "image":
        img = (
            f'<img src="{embed_image(block["src"])}" alt="{html.escape(block.get("alt") or "")}" '
            f'width="{block["width"]}" height="{block["height"]}" loading="lazy">'
        )
        if block.get("href"):
            img = f'<a href="{html.escape(block["href"])}">{img}</a>'
        return f"<figure>{img}</figure>"
    if kind == "video":
        return f"""<div class="video-block"><button type="button" class="video-load" data-src="{html.escape(block["src"])}" data-title="{html.escape(block.get("title") or "")}">
{icon("play", 30)}<span>Projektvideo abspielen</span><small>Video von SWITCHtube laden</small></button></div>"""
    if kind == "didactic":
        note_id = block["id"]
        diagram = breadboard() if block.get("diagram") == "breadboard" else ""
        return f"""<aside id="{note_id}" class="didactic-note" aria-labelledby="{note_id}-title">
<p class="didactic-title" id="{note_id}-title">{html.escape(block["title"])}</p>
{diagram}<div class="prose-content">{rewrite_links(block["html"])}</div></aside>"""
    return ""


def render_section(section: dict, slug: str) -> str:
    cells = "".join(
        f'<div class="content-cell">{"".join(render_block(b) for b in cell["blocks"])}</div>'
        for cell in section["cells"]
    )
    anchor = section.get("anchor") or section["id"]
    # Suchtreffer springen die Section an, darum haengen die Metadaten hier dran.
    meta = f'data-title="{html.escape(section.get("title") or "")}" data-anchor="{anchor}"'

    if section.get("accordion"):
        return f"""<details class="lesson" id="{anchor}" {meta}>
<summary class="lesson-title"><span class="lesson-heading"><span>{html.escape(section["title"])}</span></span>{icon("chevron", 20, "lesson-icon")}</summary>
<div class="lesson-content">{cells}</div></details>"""

    classes = "content-section"
    if section.get("gallery"):
        classes += " image-gallery"
    if section.get("layout"):
        classes += " " + section["layout"]
    style = f' style="--columns:{len(section["cells"])}"' if section.get("gallery") else ""
    return f'<section class="{classes}" id="{section["id"]}"{style} {meta}>{cells}</section>'


def render_page(page: dict, first: bool) -> str:
    sections = "".join(render_section(s, page["slug"]) for s in page["sections"])
    return (
        f'<article class="page article page-{page["slug"]}" id="page-{page["slug"]}" '
        f'data-slug="{page["slug"]}" data-label="{html.escape(page["label"])}" '
        f'data-page-title="{html.escape(page["title"])}"{"" if first else " hidden"}>{sections}</article>'
    )


# --------------------------------------------------------------------------- Seitengerüst


SCRIPT = """
const pages = [...document.querySelectorAll('.page')];
const navLinks = [...document.querySelectorAll('.site-navigation a')];
const body = document.body;

function show(slug, anchor) {
  const page = pages.find(p => p.dataset.slug === slug) || pages[0];
  const changed = page.hidden;
  pages.forEach(p => { p.hidden = p !== page; });
  navLinks.forEach(a => a.setAttribute('aria-current', a.hash.slice(1).split('/')[0] === page.dataset.slug ? 'page' : 'false'));
  document.title = page.dataset.pageTitle;
  body.classList.remove('nav-open');
  // Seitenwechsel springt direkt, sonst laufen zwei Smooth-Scrolls gegeneinander.
  if (!anchor) { window.scrollTo({ top: 0, behavior: 'instant' }); return; }
  const target = page.querySelector('#' + CSS.escape(anchor));
  if (!target) return;
  const lesson = target.closest('details');
  if (lesson) lesson.open = true;
  requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: changed ? 'instant' : 'smooth' }));
}

function route() {
  const [slug, anchor] = decodeURIComponent(location.hash.slice(1)).split('/');
  show(slug, anchor);
}
addEventListener('hashchange', route);
route();

// Navigation mobil
document.querySelector('.mobile-menu').onclick = () => body.classList.toggle('nav-open');

// Suche ueber die Abschnitte, die ohnehin schon im Dokument stehen
const search = document.querySelector('.site-search');
const field = document.getElementById('search-input');
const count = document.querySelector('.search-count');
const list = document.querySelector('.site-search ul');
const sections = pages.flatMap(p => [...p.querySelectorAll('[data-anchor]')].map(s => ({
  node: s, page: p, text: (s.dataset.title + ' ' + s.textContent).toLocaleLowerCase('de')
})));

document.querySelector('.search-toggle').onclick = function () {
  const open = search.hidden;
  search.hidden = !open;
  this.setAttribute('aria-expanded', open);
  this.setAttribute('aria-label', open ? 'Suche schliessen' : 'Website durchsuchen');
  this.innerHTML = open ? ICON_X : ICON_SEARCH;
  if (open) field.focus();
};
field.oninput = () => {
  const term = field.value.toLocaleLowerCase('de').trim();
  count.hidden = list.hidden = !term;
  list.textContent = '';
  if (!term) return;
  const hits = sections.filter(s => s.text.includes(term));
  count.textContent = hits.length + ' Treffer';
  for (const hit of hits) {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + hit.page.dataset.slug + '/' + hit.node.dataset.anchor;
    a.innerHTML = '<strong></strong><span></span>';
    a.firstChild.textContent = hit.node.dataset.title || hit.page.dataset.pageTitle;
    a.lastChild.textContent = hit.page.dataset.label;
    a.onclick = () => { search.hidden = true; field.value = ''; };
    li.append(a);
    list.append(li);
  }
};
field.onkeydown = e => { if (e.key === 'Escape') document.querySelector('.search-toggle').click(); };

// Code kopieren. execCommand zuerst, weil die Clipboard-API in Webviews haengen bleibt.
document.addEventListener('click', async e => {
  const button = e.target.closest('.copy');
  if (!button) return;
  const code = button.closest('.code-block').querySelector('code').textContent;
  const label = button.querySelector('span');
  let ok = false;
  const field = document.createElement('textarea');
  field.value = code;
  field.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
  field.readOnly = true;
  body.append(field);
  field.select();
  try { ok = document.execCommand('copy'); } catch { ok = false; }
  field.remove();
  if (!ok && navigator.clipboard && isSecureContext) {
    try { await navigator.clipboard.writeText(code); ok = true; } catch {}
  }
  button.firstChild.outerHTML = ok ? ICON_CHECK : ICON_COPY;
  label.textContent = ok ? 'Kopiert!' : 'Bitte Code markieren';
  setTimeout(() => {
    button.firstChild.outerHTML = ICON_COPY;
    label.textContent = 'Code kopieren';
  }, 2500);
});

// Video erst auf Klick laden
document.addEventListener('click', e => {
  const button = e.target.closest('.video-load');
  if (!button) return;
  const frame = document.createElement('iframe');
  frame.src = button.dataset.src;
  frame.title = button.dataset.title;
  frame.allow = 'fullscreen';
  frame.allowFullscreen = true;
  button.replaceWith(frame);
});

// Beim Drucken alles aufklappen
addEventListener('beforeprint', () => document.querySelectorAll('details').forEach(d => d.open = true));
"""


def build() -> None:
    pages = json.loads(CONTENT.read_text())
    body = "".join(render_page(p, i == 0) for i, p in enumerate(pages))

    nav = "".join(
        f'<a href="#{p["slug"]}">{html.escape(p["label"])}</a>' for p in pages
    )

    script = (
        SCRIPT.replace("ICON_SEARCH", repr(icon("search")))
        .replace("ICON_X", repr(icon("x")))
        .replace("ICON_CHECK", repr(icon("check", 15)))
        .replace("ICON_COPY", repr(icon("copy", 15)))
    )

    page = f"""<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(pages[0]["title"])}</title>
<link rel="icon" href="data:image/svg+xml;base64,{base64.b64encode((ROOT / "favicon.svg").read_bytes()).decode()}">
<style>__STYLE__</style>
</head>
<body>
<a href="#main" class="skip-link">Zum Inhalt springen</a>
<nav class="site-sidebar" aria-label="Hauptnavigation">
<div class="brand"><a href="#home">ARDUINO</a></div>
<div class="site-navigation">{nav}</div>
</nav>
<div class="site-main">
<header class="utility-bar">
<button class="mobile-menu icon-button" aria-label="Navigation &ouml;ffnen">{icon("menu", 23)}</button>
<button class="icon-button search-toggle" aria-label="Website durchsuchen" aria-expanded="false">{icon("search")}</button>
</header>
<section class="site-search" aria-label="Website durchsuchen" hidden>
<label for="search-input">Website durchsuchen</label>
<input id="search-input" type="search" placeholder="Suchbegriff eingeben &hellip;">
<output class="search-count" hidden></output>
<ul hidden></ul>
</section>
<main id="main">{body}</main>
</div>
<script>{script}</script>
</body>
</html>"""

    # Schrift erst jetzt, wenn feststeht, welche Zeichen wirklich vorkommen.
    text = re.sub(r"<[^>]+>", " ", page) + "".join(chr(c) for c in range(32, 127))
    style = STYLE.read_text().replace(
        "/* Arduino-Einfuehrung",
        "@font-face{font-family:Lato;font-weight:400;font-style:normal;font-display:swap;"
        f'src:url("{embed_font(FONTS / "Lato-Regular.ttf", text)}") format("woff2")}}\n'
        "@font-face{font-family:Lato;font-weight:700 900;font-style:normal;font-display:swap;"
        f'src:url("{embed_font(FONTS / "Lato-Bold.ttf", text)}") format("woff2")}}\n'
        "/* Arduino-Einfuehrung",
        1,
    )
    page = page.replace("__STYLE__", style)

    OUT.write_text(page)
    print(f"{OUT.name}: {len(page.encode()) / 1024 / 1024:.2f} MB, {len(pages)} Seiten")


if __name__ == "__main__":
    build()
