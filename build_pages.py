#!/usr/bin/env python3
"""
Generate package pages, gallery, legal drafts, and sync tier blocks on index.html
from data/pricing.json, data/gallery.json, and data/opisi.json.

Run from repo root before commit:
    python3 build_pages.py

Success gate: after running, `git diff index.html` should only show intentional
changes (BUILD markers, nav, Mehr erfahren links) — tier content must match pricing.json.
"""
from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://juznipetar.github.io/colorandplay-website"

PACKAGE_COMMENT = {
    "kindergeburtstage": "Kindergeburtstage",
    "firmen-teams": "Firmen & Teams",
    "wine-draw": "Wine & Draw",
    "private-feiern": "Private Feiern",
    "art-club": "Art Club Mitgliedschaft",
    "grundangebot": "Grundangebot",
    "solo-abend": "Solo-Abend",
    "familie-paare-60plus": "Familie / Paare / Senioren",
    "plus-angebot": "Plus-Angebot",
    "geschenkgutscheine": "Geschenkgutscheine",
    "ferien-workshops": "Ferien-Workshops",
}

EXTRA_CSS = """
.sig-head-left{display:flex; flex-wrap:wrap; align-items:baseline; gap:10px;}
.sig-more{flex-shrink:0; align-self:center;}
.breadcrumb{margin-bottom:24px; font-size:14px;}
.breadcrumb a{color:var(--teal-deep); text-decoration:none; font-weight:500;}
.breadcrumb a:hover{text-decoration:underline;}
.pkg-hero{padding-block:48px 36px;}
.pkg-hero-placeholder{aspect-ratio:16/9; max-height:360px; border-radius:var(--radius); background:linear-gradient(135deg, var(--teal-soft), var(--gold-soft)); position:relative; overflow:hidden; margin-bottom:24px;}
.pkg-hero-placeholder .blob{position:absolute; border-radius:50%; filter:blur(32px); opacity:.45;}
.pkg-hero-placeholder .b1{width:180px;height:180px;background:var(--teal);top:10%;left:8%;}
.pkg-hero-placeholder .b2{width:140px;height:140px;background:var(--gold);bottom:15%;right:12%;}
.pkg-hero-placeholder .b3{width:100px;height:100px;background:var(--coral);top:40%;right:35%;}
.pkg-faq{margin-top:40px;}
.pkg-faq details{background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:16px 20px; margin-bottom:10px;}
.pkg-faq summary{font-weight:600; cursor:pointer; list-style:none;}
.pkg-faq summary::-webkit-details-marker{display:none;}
.pkg-faq details[open] summary{margin-bottom:10px; color:var(--teal-deep);}
.pkg-faq p{font-size:14px; color:var(--ink-soft);}
.pkg-cta{text-align:center; padding-block:48px;}
.pkg-gallery{margin-top:40px;}
.gallery-grid{display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-top:24px;}
@media (min-width:680px){ .gallery-grid{grid-template-columns:repeat(3,1fr);} }
@media (min-width:980px){ .gallery-grid{grid-template-columns:repeat(4,1fr);} }
.gallery-item,.gallery-placeholder{aspect-ratio:4/3; border:0; padding:0; border-radius:var(--radius); overflow:hidden; cursor:pointer; background:var(--surface-2); position:relative;}
.gallery-item img{width:100%; height:100%; object-fit:cover; display:block;}
.gallery-placeholder{background:linear-gradient(145deg, var(--teal-soft), var(--surface-2)); display:flex; align-items:center; justify-content:center; cursor:default;}
.gallery-placeholder-text{font-family:var(--font-mono); font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--teal-deep); font-weight:600; text-align:center; padding:12px;}
.lightbox{position:fixed; inset:0; z-index:100; background:rgba(16,22,20,.88); display:flex; align-items:center; justify-content:center; padding:20px;}
.lightbox[hidden]{display:none!important;}
.lightbox-inner{position:relative; max-width:min(960px,100%); max-height:90vh;}
.lightbox-img{max-width:100%; max-height:85vh; border-radius:var(--radius); display:block;}
.lightbox-close{position:absolute; top:-44px; right:0; background:var(--surface); border:1px solid var(--line); border-radius:999px; width:36px; height:36px; cursor:pointer; font-size:20px; line-height:1;}
.lightbox-nav{position:absolute; top:50%; transform:translateY(-50%); background:var(--surface); border:1px solid var(--line); border-radius:999px; width:40px; height:40px; cursor:pointer; font-size:18px;}
.lightbox-prev{left:-52px;}
.lightbox-next{right:-52px;}
@media (max-width:760px){ .lightbox-prev{left:8px; top:auto; bottom:-52px; transform:none;} .lightbox-next{right:8px; top:auto; bottom:-52px; transform:none;} }
.legal-content{max-width:720px; margin-top:24px;}
.legal-content h2{font-size:1.2rem; margin:28px 0 10px;}
.legal-content p,.legal-content li{font-size:15px; color:var(--ink-soft); margin-top:8px;}
.legal-content ul{padding-left:20px;}
.legal-todo{background:var(--gold-soft); border:1px solid color-mix(in srgb, var(--gold) 40%, transparent); padding:10px 14px; border-radius:8px; font-size:14px; margin:12px 0;}
.footer-links{margin-top:8px;}
.footer-links a{color:var(--teal-deep); text-decoration:none; margin-right:14px;}
.footer-links a:hover{text-decoration:underline;}
@media (prefers-reduced-motion:reduce){
  .lightbox{transition:none;}
}
"""

LIGHTBOX_JS = """
  /* ---------- gallery lightbox (accessible) ---------- */
  (function(){
    var lb = document.getElementById("gallery-lightbox");
    if (!lb) return;
    var lbImg = document.getElementById("lightbox-img");
    var btnClose = document.getElementById("lightbox-close");
    var btnPrev = document.getElementById("lightbox-prev");
    var btnNext = document.getElementById("lightbox-next");
    var triggers = Array.prototype.slice.call(document.querySelectorAll(".gallery-item[data-index]"));
    var current = -1;
    var lastFocus = null;
    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function trapFocus(ev){
      if (ev.key !== "Tab" || lb.hidden) return;
      var focusable = lb.querySelectorAll('button, [href], [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (ev.shiftKey && document.activeElement === first){
        ev.preventDefault();
        last.focus();
      } else if (!ev.shiftKey && document.activeElement === last){
        ev.preventDefault();
        first.focus();
      }
    }

    function imgAltForLang(img){
      if (!img) return "";
      var lang = document.documentElement.lang === "en" ? "en" : "de";
      var key = lang === "en" ? "data-alt-en" : "data-alt-de";
      return img.getAttribute(key) || img.alt || "";
    }

    function syncGalleryAria(){
      var lang = document.documentElement.lang === "en" ? "en" : "de";
      triggers.forEach(function(btn){
        var key = lang === "en" ? "data-aria-en" : "data-aria-de";
        var label = btn.getAttribute(key);
        if (label) btn.setAttribute("aria-label", label);
      });
    }

    function openAt(idx){
      if (!triggers[idx]) return;
      lastFocus = triggers[idx];
      current = idx;
      var img = triggers[idx].querySelector("img");
      if (img && lbImg){
        lbImg.src = img.src;
        lbImg.alt = imgAltForLang(img);
      }
      lb.hidden = false;
      document.body.style.overflow = "hidden";
      btnClose.focus();
    }

    function closeLb(){
      lb.hidden = true;
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
      current = -1;
    }

    function showPrev(){ if (current > 0) openAt(current - 1); }
    function showNext(){ if (current < triggers.length - 1) openAt(current + 1); }

    triggers.forEach(function(btn, i){
      btn.addEventListener("click", function(){ openAt(i); });
    });
    if (btnClose) btnClose.addEventListener("click", closeLb);
    if (btnPrev) btnPrev.addEventListener("click", showPrev);
    if (btnNext) btnNext.addEventListener("click", showNext);
    lb.addEventListener("keydown", function(ev){
      trapFocus(ev);
      if (ev.key === "Escape") closeLb();
      if (ev.key === "ArrowLeft") showPrev();
      if (ev.key === "ArrowRight") showNext();
    });
    lb.addEventListener("click", function(ev){
      if (ev.target === lb) closeLb();
    });

    syncGalleryAria();
    var origSetLang = window.setLang;
    if (typeof origSetLang === "function"){
      window.setLang = function(lang){
        origSetLang(lang);
        syncGalleryAria();
        if (!lb.hidden && current >= 0){
          var activeImg = triggers[current] && triggers[current].querySelector("img");
          if (activeImg && lbImg) lbImg.alt = imgAltForLang(activeImg);
        }
      };
    }
  })();
"""


def h(text: str) -> str:
    return escape(text, quote=False)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def render_unit(jedinica_de: str, jedinica_en: str) -> str:
    if not jedinica_de and not jedinica_en:
        return ""
    de = h(jedinica_de)
    en = h(jedinica_en)
    return (
        f'<span class="unit i18n" data-lang="de"> {de}</span>'
        f'<span class="unit i18n" data-lang="en" hidden> {en}</span>'
    )


def render_tier(tier: dict, index: int) -> str:
    classes = "tier"
    if tier.get("popular"):
        classes += " popular"
    badge = ""
    if tier.get("popular"):
        badge = (
            '<span class="badge i18n" data-lang="de">Beliebt</span>'
            '<span class="badge i18n" data-lang="en" hidden>Popular</span>\n        '
        )
    feats = []
    for pog in tier["pogodnosti"]:
        feats.append(
            f'<li class="i18n" data-lang="de">{h(pog["de"])}</li>'
            f'<li class="i18n" data-lang="en" hidden>{h(pog["en"])}</li>'
        )
    unit = render_unit(tier.get("jedinica_de", ""), tier.get("jedinica_en", ""))
    return (
        f'      <div class="{classes}" style="--i:{index}">\n'
        f"        {badge}\n"
        f'        <div class="tname">{h(tier["naziv"])}</div>\n'
        f'        <div class="tprice">{h(tier["cena"])}{unit}</div>\n'
        f'        <ul class="tfeat">\n          {"\n          ".join(feats)}\n'
        f"        </ul>\n"
        f"      </div>"
    )


def render_tiers_block(paket: dict) -> str:
    tiers = "\n".join(render_tier(t, i) for i, t in enumerate(paket["tiers"]))
    return f'    <div class="tiers reveal-stagger reveal">\n{tiers}\n    </div>'


def render_signature_head(paket: dict, learn_more_prefix: str = "pakete") -> str:
    slug = paket["slug"]
    if paket["naziv_de"] == paket["naziv_en"]:
        h3 = f"<h3>{h(paket['naziv_de'])}</h3>"
    else:
        h3 = (
            f'<h3 class="i18n" data-lang="de">{h(paket["naziv_de"])}</h3>'
            f'<h3 class="i18n" data-lang="en" hidden>{h(paket["naziv_en"])}</h3>'
        )
    tag = (
        f'<span class="sig-tag i18n" data-lang="de">{h(paket["tag_de"])}</span>'
        f'<span class="sig-tag i18n" data-lang="en" hidden>{h(paket["tag_en"])}</span>'
    )
    more = (
        f'<a class="cta ghost small sig-more" href="{learn_more_prefix}/{slug}/">'
        '<span class="i18n" data-lang="de">Mehr erfahren</span>'
        '<span class="i18n" data-lang="en" hidden>Learn more</span></a>'
    )
    return (
        f'    <div class="sig-head">\n'
        f'      <div class="sig-head-left">\n        {h3}\n        {tag}\n'
        f"      </div>\n      {more}\n    </div>"
    )


def render_signature(paket: dict, learn_more_prefix: str = "pakete") -> str:
    comment = PACKAGE_COMMENT.get(paket["slug"], paket["naziv_de"])
    return (
        f"  <!-- {comment} -->\n"
        f'  <div class="signature reveal">\n'
        f"{render_signature_head(paket, learn_more_prefix)}\n"
        f"{render_tiers_block(paket)}\n"
        f"  </div>"
    )


def min_max_price(paket: dict) -> tuple[int, int]:
    nums = [t["cena_broj"] for t in paket["tiers"]]
    return min(nums), max(nums)


def lowest_price_label(paket: dict) -> str:
    low, _ = min_max_price(paket)
    for tier in paket["tiers"]:
        if tier["cena_broj"] == low:
            return tier["cena"]
    return f"CHF {low}"


def extract_style(index_html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", index_html, re.DOTALL)
    if not m:
        raise SystemExit("Could not extract <style> from index.html")
    return m.group(1)


def extract_script(index_html: str) -> str:
    m = re.search(r"<script>\s*\(function\(\)\{.*?</script>", index_html, re.DOTALL)
    if not m:
        raise SystemExit("Could not extract <script> from index.html")
    return m.group(0)


def render_nav(depth: int, active: str = "") -> str:
    prefix = "../" * depth if depth else ""
    home = f"{prefix}index.html" if depth else "#top"
    galerie_href = f"{prefix}galerie/" if depth else "galerie/"
    pakete = f"{prefix}index.html#pakete" if depth else "#pakete"
    ablauf = f"{prefix}index.html#ablauf" if depth else "#ablauf"
    standort = f"{prefix}index.html#standort" if depth else "#standort"
    kontakt = f"{prefix}index.html#kontakt" if depth else "#kontakt"
    galerie_active = ' aria-current="page"' if active == "galerie" else ""
    return f"""<div class="topbar">
  <div class="wrap topbar-inner">
    <a class="brandmark" href="{home}" aria-label="Color and Play — Startseite / Home">
      <span class="dot" aria-hidden="true"></span>
      <span class="brandmark-text">Color and Play</span>
    </a>
    <div class="topbar-right">
      <nav class="navlinks" aria-label="Hauptnavigation / Main navigation">
        <a href="{pakete}" class="i18n" data-lang="de">Pakete</a><a href="{pakete}" class="i18n" data-lang="en" hidden>Packages</a>
        <a href="{galerie_href}" class="i18n" data-lang="de"{galerie_active}>Galerie</a><a href="{galerie_href}" class="i18n" data-lang="en" hidden{galerie_active}>Gallery</a>
        <a href="{ablauf}" class="i18n" data-lang="de">Ablauf</a><a href="{ablauf}" class="i18n" data-lang="en" hidden>How it works</a>
        <a href="{standort}" class="i18n" data-lang="de">Standort</a><a href="{standort}" class="i18n" data-lang="en" hidden>Location</a>
        <a class="cta small" href="{kontakt}"><span class="i18n" data-lang="de">Termin sichern</span><span class="i18n" data-lang="en" hidden>Reserve a spot</span></a>
      </nav>
      <div class="langtoggle" role="group" aria-label="Sprache / Language">
        <button type="button" id="btn-de" aria-pressed="true" aria-label="Deutsch" onclick="setLang('de')">DE</button>
        <button type="button" id="btn-en" aria-pressed="false" aria-label="English" onclick="setLang('en')">EN</button>
      </div>
    </div>
  </div>
</div>"""


def render_footer(depth: int) -> str:
    prefix = "../" * depth if depth else ""
    impressum = f"{prefix}impressum/"
    datenschutz = f"{prefix}datenschutz/"
    return f"""<footer class="wrap">
  <div class="footgrid">
    <div class="footer-brand">Color and Play</div>
    <div class="footer-meta">
      <span class="i18n" data-lang="de">Baar, Kanton Zug — exklusives Kreativatelier für jeden Anlass.</span>
      <span class="i18n" data-lang="en" hidden>Baar, Canton of Zug — an exclusive creative studio for every occasion.</span><br>
      <span class="i18n" data-lang="de">© <span id="year-de"></span> Color and Play.</span>
      <span class="i18n" data-lang="en" hidden>© <span id="year-en"></span> Color and Play.</span>
      <div class="footer-links">
        <a href="{impressum}" class="i18n" data-lang="de">Impressum</a><a href="{impressum}" class="i18n" data-lang="en" hidden>Legal notice</a>
        <a href="{datenschutz}" class="i18n" data-lang="de">Datenschutz</a><a href="{datenschutz}" class="i18n" data-lang="en" hidden>Privacy</a>
      </div>
    </div>
  </div>
</footer>"""


def render_head_links(depth: int) -> str:
    prefix = "../" * depth
    return f"""<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="{prefix}favicon.ico">
<link rel="icon" sizes="16x16" href="{prefix}favicon-16.png">
<link rel="icon" sizes="32x32" href="{prefix}favicon-32.png">
<link rel="icon" sizes="192x192" href="{prefix}favicon-192.png">
<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">"""


def render_gallery_grid(images: list[dict], prefix: str, placeholder_count: int = 6) -> str:
    if not images:
        tiles = []
        for _ in range(placeholder_count):
            tiles.append(
                '<div class="gallery-placeholder" aria-hidden="true">'
                '<span class="gallery-placeholder-text i18n" data-lang="de">Fotos folgen in Kürze</span>'
                '<span class="gallery-placeholder-text i18n" data-lang="en" hidden>Photos coming soon</span>'
                "</div>"
            )
        return '<div class="gallery-grid">\n    ' + "\n    ".join(tiles) + "\n  </div>"

    items = []
    for i, img in enumerate(images):
        src = f"{prefix}{img['fajl']}" if not img["fajl"].startswith(("http", "../")) else img["fajl"]
        alt_de = h(img["alt_de"])
        alt_en = h(img["alt_en"])
        items.append(
            f'<button type="button" class="gallery-item" data-index="{i}" '
            f'data-aria-de="{alt_de}" data-aria-en="{alt_en}" '
            f'aria-label="{alt_de}">'
            f'<img src="{h(src)}" alt="" width="400" height="300" loading="lazy" '
            f'data-alt-de="{alt_de}" data-alt-en="{alt_en}"></button>'
        )
    return '<div class="gallery-grid">\n    ' + "\n    ".join(items) + "\n  </div>"


def render_lightbox() -> str:
    return """<div id="gallery-lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="Bildansicht / Image view" hidden>
  <div class="lightbox-inner">
    <button type="button" class="lightbox-close" id="lightbox-close" aria-label="Schliessen / Close">×</button>
    <button type="button" class="lightbox-nav lightbox-prev" id="lightbox-prev" aria-label="Vorheriges Bild / Previous image">‹</button>
    <img class="lightbox-img" id="lightbox-img" alt="" width="960" height="720">
    <button type="button" class="lightbox-nav lightbox-next" id="lightbox-next" aria-label="Nächstes Bild / Next image">›</button>
  </div>
</div>"""


def render_faq(faq: list[dict]) -> str:
    if not faq:
        return ""
    items = []
    for item in faq:
        items.append(
            f"    <details>\n"
            f'      <summary><span class="i18n" data-lang="de">{h(item["pitanje_de"])}</span>'
            f'<span class="i18n" data-lang="en" hidden>{h(item["pitanje_en"])}</span></summary>\n'
            f'      <p class="i18n" data-lang="de">{h(item["odgovor_de"])}</p>\n'
            f'      <p class="i18n" data-lang="en" hidden>{h(item["odgovor_en"])}</p>\n'
            f"    </details>"
        )
    return (
        '  <section class="block wrap reveal pkg-faq">\n'
        '    <h2 class="i18n" data-lang="de">Häufige Fragen</h2>\n'
        '    <h2 class="i18n" data-lang="en" hidden>Frequently asked questions</h2>\n'
        + "\n".join(items)
        + "\n  </section>"
    )


def service_json_ld(paket: dict) -> str:
    low, high = min_max_price(paket)
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": paket["naziv_de"],
        "provider": {"@type": "LocalBusiness", "name": "Color and Play"},
        "areaServed": "Baar, Kanton Zug",
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "CHF",
            "lowPrice": str(low),
            "highPrice": str(high),
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def page_shell(
    title: str,
    description: str,
    depth: int,
    body: str,
    base_style: str,
    base_script: str,
    extra_script: str = "",
    json_ld: str = "",
    nav_active: str = "",
) -> str:
    head_links = render_head_links(depth)
    style = base_style + EXTRA_CSS
    script = base_script
    if extra_script:
        script = script.replace("</script>", extra_script + "\n</script>", 1)
    ld_block = f"\n<script type=\"application/ld+json\">\n{json_ld}\n</script>\n" if json_ld else ""
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)}</title>
<meta name="description" content="{h(description)}">
{head_links}
{ld_block}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,600&amp;family=Work+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,600&amp;family=Work+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,600&amp;family=Work+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap"></noscript>
<style>
{style}
</style>
</head>
<body>

<a class="skip-link i18n" data-lang="de" href="#main">Zum Inhalt springen</a>
<a class="skip-link i18n" data-lang="en" href="#main" hidden>Skip to content</a>

{render_nav(depth, nav_active)}

{body}

{render_footer(depth)}

{script}
</body>
</html>
"""


def gallery_images_for_slug(gallery: dict, slug: str | None, limit: int = 6) -> list[dict]:
    out = []
    for img in gallery.get("slike", []):
        tags = img.get("tagovi", [])
        if slug is None or slug in tags:
            out.append(img)
        if len(out) >= limit:
            break
    return out


def validate_gallery_hero(gallery: dict) -> None:
    seen: dict[str, str] = {}
    for img in gallery.get("slike", []):
        hero = img.get("je_hero_za")
        if not hero:
            continue
        if hero in seen:
            raise SystemExit(
                f"gallery.json: duplicate je_hero_za '{hero}' "
                f"({seen[hero]} and {img.get('fajl')})"
            )
        seen[hero] = img.get("fajl", "?")


def generate_package_page(
    paket: dict,
    opis: dict,
    gallery: dict,
    base_style: str,
    base_script: str,
) -> str:
    slug = paket["slug"]
    low_label = lowest_price_label(paket)
    title = f"{paket['naziv_de']} in Baar | Color and Play"
    description = (
        f"{paket['naziv_de']} bei Color and Play in Baar — {paket['tag_de']}. "
        f"Ab {low_label}."
    )
    hero_img = None
    for img in gallery.get("slike", []):
        if img.get("je_hero_za") == slug:
            hero_img = img
            break

    if hero_img:
        hero_html = (
            f'<img class="pkg-hero-img" src="../../{h(hero_img["fajl"])}" '
            f'alt="" width="1200" height="675" loading="eager">'
        )
    else:
        hero_html = (
            '<div class="pkg-hero-placeholder" aria-hidden="true">'
            '<span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span>'
            "</div>"
        )

    if paket["naziv_de"] == paket["naziv_en"]:
        h1 = f"<h1>{h(paket['naziv_de'])}</h1>"
    else:
        h1 = (
            f'<h1 class="i18n" data-lang="de">{h(paket["naziv_de"])}</h1>'
            f'<h1 class="i18n" data-lang="en" hidden>{h(paket["naziv_en"])}</h1>'
        )

    mini = gallery_images_for_slug(gallery, slug, 6)
    faq = opis.get("faq", [])

    body = f"""<main id="main">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html#pakete">
        <span class="i18n" data-lang="de">‹ Zurück zu allen Paketen</span>
        <span class="i18n" data-lang="en" hidden>‹ Back to all packages</span>
      </a>
    </nav>
  </div>

  <section class="block wrap reveal pkg-hero">
    {hero_html}
    <span class="kicker i18n" data-lang="de">{h(paket["tag_de"])}</span>
    <span class="kicker i18n" data-lang="en" hidden>{h(paket["tag_en"])}</span>
    {h1}
    <p class="lead i18n" data-lang="de">{h(opis.get("opis_de", ""))}</p>
    <p class="lead i18n" data-lang="en" hidden>{h(opis.get("opis_en", ""))}</p>
  </section>

  <section class="block wrap reveal">
{render_tiers_block(paket)}
  </section>

  <section class="block wrap reveal pkg-gallery">
    <h2 class="i18n" data-lang="de">Impressionen</h2>
    <h2 class="i18n" data-lang="en" hidden>Impressions</h2>
    {render_gallery_grid(mini, "../../", 4)}
  </section>

  <section class="block wrap reveal pkg-cta">
    <a class="cta" href="../../index.html?paket={slug}#kontakt">
      <span class="i18n" data-lang="de">Jetzt anfragen</span>
      <span class="i18n" data-lang="en" hidden>Enquire now</span>
    </a>
  </section>
{render_faq(faq)}
</main>
{render_lightbox()}"""

    extra = LIGHTBOX_JS
    return page_shell(
        title,
        description,
        2,
        body,
        base_style,
        base_script,
        extra_script=extra,
        json_ld=service_json_ld(paket),
    )


def generate_gallery_page(gallery: dict, base_style: str, base_script: str) -> str:
    images = gallery.get("slike", [])
    body = f"""<main id="main">
  <section class="block wrap reveal">
    <span class="kicker i18n" data-lang="de">Galerie</span>
    <span class="kicker i18n" data-lang="en" hidden>Gallery</span>
    <h1 class="i18n" data-lang="de">Einblicke ins Atelier</h1>
    <h1 class="i18n" data-lang="en" hidden>Studio impressions</h1>
    <p class="lead i18n" data-lang="de">Echte Fotos aus dem Atelier folgen in Kürze — hier sehen Sie bald Workshops, Räume und fertige Werke.</p>
    <p class="lead i18n" data-lang="en" hidden>Real photos from the studio are coming soon — you'll soon see workshops, spaces and finished pieces here.</p>
    {render_gallery_grid(images, "../", 8)}
  </section>
</main>
{render_lightbox()}"""
    extra = LIGHTBOX_JS
    return page_shell(
        "Galerie | Color and Play",
        "Galerie — Color and Play Kreativatelier in Baar. Fotos aus Workshops und Atelier folgen in Kürze.",
        1,
        body,
        base_style,
        base_script,
        extra_script=extra,
        nav_active="galerie",
    )


def generate_impressum(base_style: str, base_script: str) -> str:
    body = """<main id="main">
  <section class="block wrap reveal">
    <span class="kicker i18n" data-lang="de">Rechtliches</span>
    <span class="kicker i18n" data-lang="en" hidden>Legal</span>
    <h1 class="i18n" data-lang="de">Impressum</h1>
    <h1 class="i18n" data-lang="en" hidden>Legal notice</h1>
    <div class="legal-content">
      <p class="legal-todo i18n" data-lang="de">[TODO: potvrditi] — Rechtlicher Name und genaue Strasse/Adresse müssen vor Go-live bestätigt werden.</p>
      <p class="legal-todo i18n" data-lang="en" hidden>[TODO: confirm] — Legal name and exact street address must be confirmed before go-live.</p>
      <h2 class="i18n" data-lang="de">Anbieter</h2>
      <h2 class="i18n" data-lang="en" hidden>Provider</h2>
      <p><span class="i18n" data-lang="de">Color and Play</span><span class="i18n" data-lang="en" hidden>Color and Play</span><br>
      <span class="i18n" data-lang="de">[TODO: potvrditi — Rechtlicher Name]</span><span class="i18n" data-lang="en" hidden>[TODO: confirm — legal name]</span><br>
      <span class="i18n" data-lang="de">[TODO: potvrditi — Strasse und Hausnummer]</span><span class="i18n" data-lang="en" hidden>[TODO: confirm — street and number]</span><br>
      <span class="i18n" data-lang="de">Baar, Kanton Zug, Schweiz</span><span class="i18n" data-lang="en" hidden>Baar, Canton of Zug, Switzerland</span></p>
      <h2 class="i18n" data-lang="de">Kontakt</h2>
      <h2 class="i18n" data-lang="en" hidden>Contact</h2>
      <p><a href="mailto:suzana.androvic@gmail.com">suzana.androvic@gmail.com</a></p>
      <h2 class="i18n" data-lang="de">Haftungsausschluss</h2>
      <h2 class="i18n" data-lang="en" hidden>Disclaimer</h2>
      <p class="i18n" data-lang="de">Die Inhalte dieser Website werden mit grösster Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität können wir jedoch keine Gewähr übernehmen.</p>
      <p class="i18n" data-lang="en" hidden>The content of this website is prepared with great care. However, we cannot guarantee accuracy, completeness or timeliness.</p>
    </div>
  </section>
</main>"""
    return page_shell(
        "Impressum | Color and Play",
        "Impressum — Color and Play Kreativatelier Baar.",
        1,
        body,
        base_style,
        base_script,
    )


def generate_datenschutz(base_style: str, base_script: str) -> str:
    body = """<main id="main">
  <section class="block wrap reveal">
    <span class="kicker i18n" data-lang="de">Rechtliches</span>
    <span class="kicker i18n" data-lang="en" hidden>Legal</span>
    <h1 class="i18n" data-lang="de">Datenschutzerklärung</h1>
    <h1 class="i18n" data-lang="en" hidden>Privacy policy</h1>
    <div class="legal-content">
      <p class="legal-todo i18n" data-lang="de">[TODO: potvrditi] — Rechtlicher Name und genaue Adresse vor Go-live bestätigen.</p>
      <p class="legal-todo i18n" data-lang="en" hidden>[TODO: confirm] — Confirm legal name and exact address before go-live.</p>
      <h2 class="i18n" data-lang="de">Verantwortliche Stelle</h2>
      <h2 class="i18n" data-lang="en" hidden>Data controller</h2>
      <p><span class="i18n" data-lang="de">Color and Play, Baar (Kanton Zug)</span><span class="i18n" data-lang="en" hidden>Color and Play, Baar (Canton of Zug)</span><br>
      <a href="mailto:suzana.androvic@gmail.com">suzana.androvic@gmail.com</a></p>
      <h2 class="i18n" data-lang="de">Welche Daten wir erheben</h2>
      <h2 class="i18n" data-lang="en" hidden>What data we collect</h2>
      <p class="i18n" data-lang="de">Wenn Sie das Kontaktformular nutzen, verarbeiten wir die von Ihnen eingegebenen Daten (Name, E-Mail, optional Telefon, Nachricht, gewähltes Paket).</p>
      <p class="i18n" data-lang="en" hidden>When you use the contact form, we process the data you enter (name, email, optional phone, message, selected package).</p>
      <h2 class="i18n" data-lang="de">Auftragsverarbeiter</h2>
      <h2 class="i18n" data-lang="en" hidden>Processors</h2>
      <ul>
        <li class="i18n" data-lang="de"><strong>Formspree</strong> — Übermittlung und Zustellung von Kontaktanfragen (USA; Standardvertragsklauseln / Angemessenheitsbeschluss je nach Anbieterstand).</li>
        <li class="i18n" data-lang="en" hidden><strong>Formspree</strong> — transmission and delivery of contact enquiries (USA; standard contractual clauses / adequacy decision depending on provider).</li>
        <li class="i18n" data-lang="de"><strong>GitHub Pages</strong> — Hosting dieser statischen Website (Microsoft/GitHub).</li>
        <li class="i18n" data-lang="en" hidden><strong>GitHub Pages</strong> — hosting of this static website (Microsoft/GitHub).</li>
      </ul>
      <h2 class="i18n" data-lang="de">Ihre Rechte</h2>
      <h2 class="i18n" data-lang="en" hidden>Your rights</h2>
      <p class="i18n" data-lang="de">Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung und Widerspruch — kontaktieren Sie uns per E-Mail.</p>
      <p class="i18n" data-lang="en" hidden>You have the right to access, rectify, delete, restrict processing and object — contact us by email.</p>
      <h2 class="i18n" data-lang="de">Speicherdauer</h2>
      <h2 class="i18n" data-lang="en" hidden>Retention</h2>
      <p class="i18n" data-lang="de">Anfragen werden nur so lange gespeichert, wie für die Bearbeitung Ihrer Anfrage erforderlich.</p>
      <p class="i18n" data-lang="en" hidden>Enquiries are stored only as long as needed to handle your request.</p>
    </div>
  </section>
</main>"""
    return page_shell(
        "Datenschutz | Color and Play",
        "Datenschutzerklärung — Color and Play Kreativatelier Baar.",
        1,
        body,
        base_style,
        base_script,
    )


def update_index_packages(index_path: Path, pakete: list[dict]) -> None:
    html = index_path.read_text(encoding="utf-8")
    start = "<!-- BUILD:PACKAGES-START -->"
    end = "<!-- BUILD:PACKAGES-END -->"
    if start not in html or end not in html:
        raise SystemExit(
            f"Missing {start} / {end} markers in index.html — add them around package blocks."
        )
    block = "\n\n".join(render_signature(p) for p in pakete)
    new_html = re.sub(
        rf"{start}.*?{end}",
        f"{start}\n{block}\n  {end}",
        html,
        count=1,
        flags=re.DOTALL,
    )
    index_path.write_text(new_html, encoding="utf-8")


def update_sitemap(sitemap_path: Path, pakete: list[dict]) -> None:
    urls = [
        f"""  <url>
    <loc>{BASE_URL}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]
    for p in pakete:
        urls.append(
            f"""  <url>
    <loc>{BASE_URL}/pakete/{p['slug']}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""
        )
    urls.append(
        f"""  <url>
    <loc>{BASE_URL}/galerie/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>"""
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    sitemap_path.write_text(xml, encoding="utf-8")


def main() -> int:
    pricing = load_json(ROOT / "data" / "pricing.json")
    gallery = load_json(ROOT / "data" / "gallery.json")
    opisi = load_json(ROOT / "data" / "opisi.json")
    pakete = pricing["pakete"]

    validate_gallery_hero(gallery)

    index_path = ROOT / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    base_style = extract_style(index_html)
    base_script = extract_script(index_html)

    update_index_packages(index_path, pakete)

    for paket in pakete:
        slug = paket["slug"]
        opis = opisi.get(slug, {})
        if not opis:
            print(f"Warning: no opisi.json entry for {slug}", file=sys.stderr)
        out = ROOT / "pakete" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            generate_package_page(paket, opis, gallery, base_style, base_script),
            encoding="utf-8",
        )
        print(f"Wrote {out.relative_to(ROOT)}")

    (ROOT / "galerie").mkdir(exist_ok=True)
    (ROOT / "galerie" / "index.html").write_text(
        generate_gallery_page(gallery, base_style, base_script),
        encoding="utf-8",
    )
    print("Wrote galerie/index.html")

    (ROOT / "impressum").mkdir(exist_ok=True)
    (ROOT / "impressum" / "index.html").write_text(
        generate_impressum(base_style, base_script), encoding="utf-8"
    )
    print("Wrote impressum/index.html")

    (ROOT / "datenschutz").mkdir(exist_ok=True)
    (ROOT / "datenschutz" / "index.html").write_text(
        generate_datenschutz(base_style, base_script), encoding="utf-8"
    )
    print("Wrote datenschutz/index.html")

    update_sitemap(ROOT / "sitemap.xml", pakete)
    print("Updated sitemap.xml")
    print("Done. Run: python3 check_i18n.py on all HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
