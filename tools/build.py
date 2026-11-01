#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for qeuapps.com (Q Apps).

Why a generator: the site is bilingual (English + Modern Standard Arabic,
with real RTL) across ~15 routes, and every page shares the same header,
footer, SEO/Open-Graph head and language switch. Authoring that by hand in
~15 files would drift out of sync. This script emits plain, dependency-free
static HTML into the repository root — the OUTPUT needs no Node, no runtime,
and is fully portable to Netlify / Cloudflare Pages / Vercel / S3.

Run:  python3 tools/build.py
It only writes *.html, sitemap.xml, robots.txt (never touches /assets except
to read). Safe to run repeatedly.

To add a new app: add an entry to APPS below and a page function, then re-run.
"""

import os
import json
import hashlib

import site_layout  # icon grid, app section bar, help cards (redesign 2026-11-02)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE_URL = "https://qeuapps.com"


def asset_ver(rel):
    """Short content hash for cache-busting (?v=) so browsers never pair new
    HTML with a stale cached CSS/JS after a deploy."""
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


CSS_HREF = f"/assets/css/styles.css?v={asset_ver('assets/css/styles.css')}"
JS_SRC = f"/assets/js/site.js?v={asset_ver('assets/js/site.js')}"
SUPPORT_EMAIL = "thibantechsolutions@gmail.com"
# Cloudflare Turnstile site key for the "Contact & suggest" form (public; the
# secret lives only in the Pages environment). Set it as a build environment
# variable in Cloudflare Pages. Empty = the form offers WhatsApp/email only.
TURNSTILE_SITE_KEY = os.environ.get("TURNSTILE_SITE_KEY", "")
WHATSAPP_DISPLAY = "+966 55 426 0804"          # shown to visitors
WHATSAPP_NUMBER = "966554260804"               # E.164 digits for wa.me
WHATSAPP_LINK = f"https://wa.me/{WHATSAPP_NUMBER}"

# Public branded campaign URL /vault -> existing Google Apps Script web app.
# To change the destination later, edit ONLY this constant and rebuild;
# the public URL (https://qeuapps.com/vault) never changes.
VAULT_TARGET = ("https://script.google.com/macros/s/"
                "AKfycbwnPfxZyhVzHT7LeKh_t9bJ6PtqDBxNoT1-1OBdc8belWGpx3gQmF7jtBUZ1f-DXbaK/exec")

# NEW (v2) architecture: /vault-new hosts the FULL campaign UI on our own domain
# and calls the Apps Script v2 deployment as a JSON/JSONP backend API. This keeps
# the visitor on our own domain (no "created by a Google Apps Script user" banner).
# Edit ONLY this constant to re-point the backend; the public URL never changes.
VAULTNEW_EXEC_URL = ("https://script.google.com/macros/s/"
                     "AKfycbxPmeFcL5oLIY-5UEoo7R_NyJS2J4xALkBgoKuswFQU4z9sEwNO1EC_KFraQ1-opBf2NQ/exec")

# First-party proxy for /vault-new: a Cloudflare Worker on api.thiban1.com
# forwards to VAULTNEW_EXEC_URL. The page calls this base with a normal fetch().
# Kept unchanged after the move to qeuapps.com: the Worker answers CORS with
# "Access-Control-Allow-Origin: *". (On thiban1.com it was also same-site, which
# kept iOS tracking-protection / content blockers from dropping the call; a
# future api.qeuapps.com route on the same Worker would restore that.)
VAULTNEW_API_BASE = "https://api.thiban1.com/"

# Full campaign page for /vault and /vault-new. Lives in its own file (the live,
# hand-tuned page) so the builder never rolls it back. __API_BASE__ is replaced
# with VAULTNEW_API_BASE at build time.
with open(os.path.join(HERE, "templates", "vault-campaign.html"), encoding="utf-8") as _f:
    _VAULTNEW_HTML = _f.read()

WHATSAPP_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" width="20" height="20" fill="currentColor">'
                '<path d="M.06 24l1.68-6.13A11.87 11.87 0 0 1 .16 11.9C.16 5.34 5.5.02 12.06.02c3.18 0 '
                '6.17 1.24 8.42 3.49a11.8 11.8 0 0 1 3.49 8.4c0 6.56-5.35 11.88-11.9 11.88a11.9 11.9 0 0 '
                '1-5.7-1.45L.06 24zM6.6 20.13c1.68.99 3.28 1.59 5.45 1.59 5.45 0 9.9-4.43 9.9-9.88a9.8 '
                '9.8 0 0 0-2.9-6.99A9.8 9.8 0 0 0 12.06 2c-5.45 0-9.9 4.43-9.9 9.88 0 2.24.66 3.92 1.75 '
                '5.68l-1 3.63 3.69-.96zM17.6 14.6c-.07-.12-.27-.2-.56-.34-.3-.15-1.75-.86-2.02-.96-.27-.1-'
                '.47-.15-.66.15-.2.3-.76.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-'
                '1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.14.3-.35.44-.53.15-.17.2-.3.3-.5.1-.2.05-.37-'
                '.02-.52-.08-.15-.66-1.6-.9-2.18-.24-.58-.48-.5-.66-.5l-.57-.02c-.2 0-.52.07-.8.37-.27.3-'
                '1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.23 '
                '1.36.2 1.87.12.57-.08 1.75-.72 2-1.4.24-.7.24-1.28.17-1.4z"/></svg>')


def whatsapp_button():
    # Action button only — the number itself is shown as a tappable link on the
    # contact card and in the footer. Keeping the number out of the button avoids
    # mid-number wrapping and any LTR/RTL bidi issues.
    return (f'<a class="wa-btn" href="{WHATSAPP_LINK}" target="_blank" rel="noopener">'
            f'{WHATSAPP_SVG}'
            f'<span data-en>Message on WhatsApp</span><span data-ar>راسلنا على واتساب</span></a>')


YEAR = "2026"

# Brand mark: a Q ring whose tail is an app tile. Colours come from CSS
# (.qmark .qm-ring / .qm-tile / .qm-dot) so it works on light and dark.
def qmark(cls="qmark", size=38):
    return (f'<svg class="{cls}" viewBox="0 0 120 120" width="{size}" height="{size}" aria-hidden="true">'
            '<circle class="qm-ring" cx="56" cy="56" r="37" fill="none" stroke-width="19"/>'
            '<rect class="qm-tile" x="72" y="72" width="40" height="40" rx="12" stroke-width="7" paint-order="stroke"/>'
            '<circle class="qm-dot" cx="92" cy="92" r="5"/></svg>')

ARROW_SVG = ('<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
ICON_CODE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>')
ICON_PHONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
              'stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="3"/><path d="M10.5 18.5h3"/></svg>')
ICON_TARGET = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
               '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/></svg>')
ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
              'stroke-linejoin="round" aria-hidden="true"><path d="M12 3 4 6v6c0 4.5 3.4 8.2 8 9 4.6-.8 8-4.5 8-9V6Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>')
ICON_USER = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 21.5l8.8-8.8a5 5 0 0 0 0-7.1Z"/></svg>')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alexandria:wght@500..700'
         '&family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700'
         '&family=JetBrains+Mono:wght@500&family=Manrope:wght@400..800&display=swap">')
THEME_COLOR = "#0F1B2D"

# ---------------------------------------------------------------------------
# small bilingual helpers — each text node is emitted twice (data-en/data-ar);
# CSS shows only the active language. Both languages ship in the HTML so the
# page is crawlable and readable even before JavaScript runs.
# ---------------------------------------------------------------------------

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def t(en, ar):
    return f'<span data-en>{en}</span><span data-ar>{ar}</span>'

def p(en, ar, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c} data-en>{en}</p><p{c} data-ar>{ar}</p>'

def h(n, en, ar, cls="", _id=""):
    c = f' class="{cls}"' if cls else ""
    i = f' id="{_id}"' if _id else ""
    return f'<h{n}{i}{c} data-en>{en}</h{n}><h{n}{i}{c} data-ar>{ar}</h{n}>'

def li(en, ar):
    return f'<li data-en>{en}</li><li data-ar>{ar}</li>'

def ul(items):
    lis = "".join(li(e, a) for e, a in items)
    return f"<ul>{lis}</ul>"

def feature(icon, en_t, ar_t, en_d, ar_d):
    return (f'<div class="feature"><div class="dot" aria-hidden="true">{icon}</div><div>'
            f'<h4 data-en>{en_t}</h4><h4 data-ar>{ar_t}</h4>'
            f'<p data-en>{en_d}</p><p data-ar>{ar_d}</p></div></div>')

def steps(items):
    out = []
    for en_t, ar_t, en_d, ar_d in items:
        out.append(f'<li><h4 data-en>{en_t}</h4><h4 data-ar>{ar_t}</h4>'
                   f'<p data-en>{en_d}</p><p data-ar>{ar_d}</p></li>')
    return f'<ol class="steps">{"".join(out)}</ol>'

def faq(items):
    out = []
    for en_q, ar_q, en_a, ar_a in items:
        out.append('<details><summary>'
                   f'<span data-en>{en_q}</span><span data-ar>{ar_q}</span></summary>'
                   f'<p data-en>{en_a}</p><p data-ar>{ar_a}</p></details>')
    return f'<div class="faq">{"".join(out)}</div>'

# ---------------------------------------------------------------------------
# store buttons
# ---------------------------------------------------------------------------
APPLE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 1.6c.1 1-.3 2-1 2.8-.7.8-1.8 1.4-2.9 1.3-.1-1 .4-2 1-2.7.7-.8 1.9-1.4 2.9-1.4zM19 17.3c-.5 1.2-.8 1.7-1.5 2.8-1 1.5-2.3 3.3-4 3.3-1.5 0-1.9-1-4-1-2 0-2.5 1-4 1-1.6 0-2.9-1.6-3.9-3.1-2.7-4.2-3-9.1-1.3-11.7 1.2-1.8 3-2.9 4.8-2.9 1.8 0 2.9 1 4.4 1 1.4 0 2.3-1 4.4-1 1.6 0 3.2.9 4.4 2.4-3.9 2.1-3.2 7.6.2 9.1z"/></svg>')
PLAY_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.6 2.2c-.3.3-.5.7-.5 1.3v17c0 .6.2 1 .5 1.3l.1.1L13 12.6v-.2L3.7 2.1l-.1.1zm11.9 8.5L5.9 1.4l11.7 6.7-2.1 2.6zM5.9 22.6l9.6-9.3 2.1 2.6-11.7 6.7zM19.6 9.3l-2.5 1.4 2.4 3-2.4 3 2.5 1.4c.9-.5 1.5-1.3 1.5-2.4v-4c0-1.1-.6-1.9-1.5-2.4l-.5.6.5-.6z"/></svg>')
YT_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.5s-.2-1.6-.9-2.3c-.9-.9-1.8-.9-2.3-1C16.6 4 12 4 12 4s-4.6 0-7.8.2c-.5.1-1.4.1-2.3 1C1.2 5.9 1 7.5 1 7.5S.8 9.4.8 11.3v1.4C.8 14.6 1 16.5 1 16.5s.2 1.6.9 2.3c.9.9 2 .9 2.6 1 1.9.2 7.5.2 7.5.2s4.6 0 7.8-.3c.5-.1 1.4-.1 2.3-1 .7-.7.9-2.3.9-2.3s.2-1.9.2-3.8v-1.4c0-1.9-.2-3.7-.2-3.7zM9.8 15.1V8.9l6 3.1-6 3.1z"/></svg>')

def store_button(kind, url):
    if kind == "apple":
        return (f'<a class="store-btn" href="{url}" target="_blank" rel="noopener">{APPLE_SVG}'
                f'<span><small data-en>Download on the</small><small data-ar>حمّله من</small>'
                f'<strong>App Store</strong></span></a>')
    if kind == "play":
        return (f'<a class="store-btn" href="{url}" target="_blank" rel="noopener">{PLAY_SVG}'
                f'<span><small data-en>Get it on</small><small data-ar>احصل عليه من</small>'
                f'<strong>Google Play</strong></span></a>')
    if kind == "youtube":
        return (f'<a class="store-btn" style="background:#c4302b" href="{url}" target="_blank" rel="noopener">{YT_SVG}'
                f'<span><small data-en>Watch on</small><small data-ar>شاهده على</small>'
                f'<strong>YouTube</strong></span></a>')
    return ""

# ---------------------------------------------------------------------------
# app registry
# ---------------------------------------------------------------------------
APPS = {
    "countdown-keeper": {
        "slug": "countdown-keeper",
        "name_en": "Countdown Keeper",
        # One Arabic name everywhere = the App Store name (redesign, decision ح).
        "name_ar": "كم مضى وكم بقي",
        "privacy_name_ar": "كم مضى وكم بقي",
        "icon": "/assets/img/apps/countdown/icon.png",
        "tagline_en": "Count down to what matters — and count up from what already happened.",
        "tagline_ar": "عُدّ تنازليًا لما يهمّك، وتصاعديًا لما مضى من أحداثك.",
        "status": "live",   # App Store (2026-11); Google Play not yet
        "appstore": "https://apps.apple.com/app/id6806348941",
        # Language availability is tracked per CONTENT TYPE — an app may ship
        # its privacy policy in more languages than its other content.
        "overview_langs": ["en", "ar"],
        "privacy_langs": ["en", "ar", "de", "fr", "es", "tr", "ja", "ko",
                          "id", "ms", "zh", "pt", "it", "ru", "nl", "ur", "bn",
                          "hi"],
        "tutorial_langs": ["en", "ar"],
        "support_langs": ["en", "ar"],
        "screens": [
            ("/assets/img/apps/countdown/Countdown_Home.jpg", "Countdown Keeper home screen with event counters", "الشاشة الرئيسية لتطبيق «كم مضى وكم بقي» تعرض عدّادات المناسبات"),
            ("/assets/img/apps/countdown/event.jpg", "Creating an event in Countdown Keeper", "إنشاء مناسبة في تطبيق «كم مضى وكم بقي»"),
            ("/assets/img/apps/countdown/tools.jpg", "Date and time tools in Countdown Keeper", "أدوات التاريخ والوقت في تطبيق «كم مضى وكم بقي»"),
            ("/assets/img/apps/countdown/Countdown_Settings.jpg", "Countdown Keeper settings screen", "شاشة الإعدادات في تطبيق «كم مضى وكم بقي»"),
        ],
    },
    "docmatic": {
        "slug": "docmatic",
        "name_en": "DocMatic",
        "name_ar": "DocMatic",
        "privacy_name_ar": "DocMatic: أدوات المستندات",
        "icon": "/assets/img/apps/docmatic/icon.png",
        "tagline_en": "Scan, sign and send clean PDFs — all on your phone.",
        "tagline_ar": "امسح ووقّع وأرسل ملفات PDF نظيفة — على جوالك.",
        "status": "soon",   # internal testing on Google Play
        # App page (tools/docmatic_page.py) + privacy policy; no tutorial or
        # support page yet, so cards link only to these.
        "pages": ["app", "privacy"],
        "overview_langs": ["en", "ar"],
        "privacy_langs": ["en", "ar"],
        "tutorial_langs": ["en", "ar"],
        "support_langs": ["en", "ar"],
        "screens": [],
    },
    "vault": {
        "slug": "vault",
        "name_en": "Vault — Warranty Manager",
        "name_ar": "خزنة الضمانات",
        "icon": "/assets/img/apps/vault/icon.png",
        "tagline_en": "Keep your invoices, organize your products, and never miss a warranty expiry.",
        "tagline_ar": "احفظ فواتيرك، ونظّم منتجاتك، ولا يفوتك موعد انتهاء أي ضمان.",
        "status": "live",
        "appstore": "https://apps.apple.com/app/id6773164894",
        "playstore": "https://play.google.com/store/apps/details?id=com.vault.warranty",
        "youtube": "https://www.youtube.com/watch?v=SjafmkwycsA&t=167s",
        "youtube_embed": "https://www.youtube.com/embed/SjafmkwycsA?start=167",
        # Vault ships its privacy policy in 8 languages (real, authoritative
        # translations preserved from the app project); other content is EN/AR.
        "overview_langs": ["en", "ar"],
        "privacy_langs": ["en", "ar", "fr", "de", "es", "tr", "ja", "ko"],
        "tutorial_langs": ["en", "ar"],
        "support_langs": ["en", "ar"],
        "screens": [
            ("/assets/img/apps/vault/dashboard.jpg", "Vault dashboard showing warranty overview", "لوحة معلومات خزنة الضمانات تعرض ملخّص الضمانات"),
            ("/assets/img/apps/vault/list.jpg", "List of saved purchases in Vault", "قائمة المشتريات المحفوظة في خزنة الضمانات"),
            ("/assets/img/apps/vault/invoice.jpg", "A scanned invoice inside Vault", "فاتورة ممسوحة داخل خزنة الضمانات"),
            ("/assets/img/apps/vault/warranty.jpg", "A warranty countdown in Vault", "عدّاد انتهاء ضمان في خزنة الضمانات"),
        ],
    },
}

# Native display name + text direction for every content language we support.
# The GLOBAL website language is only English/Arabic; these extra languages
# exist purely for APP-SPECIFIC content (e.g. Vault's privacy policy).
LANG_META = {
    "en": ("English",  "ltr"),
    "ar": ("العربية",  "rtl"),
    "fr": ("Français", "ltr"),
    "de": ("Deutsch",  "ltr"),
    "es": ("Español",  "ltr"),
    "tr": ("Türkçe",   "ltr"),
    "ja": ("日本語",    "ltr"),
    "ko": ("한국어",    "ltr"),
    "id": ("Bahasa Indonesia", "ltr"),
    "ms": ("Bahasa Melayu", "ltr"),
    "zh": ("简体中文",  "ltr"),
    "pt": ("Português (Brasil)", "ltr"),
    "it": ("Italiano", "ltr"),
    "ru": ("Русский",  "ltr"),
    "nl": ("Nederlands", "ltr"),
    "ur": ("اردو",     "rtl"),
    "bn": ("বাংলা",    "ltr"),
    "hi": ("हिन्दी",    "ltr"),
}

# Four links only (redesign proposal, decision ج). Tutorials live on each app's
# page; the old /tutorials/ URLs keep working, they are just not in the menu.
NAV = [
    ("apps", "Apps", "التطبيقات", "/apps/"),
    ("suggest", "Suggest", "اقترح", "/suggest/"),
    ("support", "Support", "الدعم", "/support/"),
    ("about", "About", "من نحن", "/about/"),
]

# pre-paint language script (kept as a plain string to avoid f-string braces)
PREPAINT = (
    "<script>(function(){try{var l=localStorage.getItem('qapps-lang');"
    "if(!l){l=((navigator.language||navigator.userLanguage||'en')"
    ".slice(0,2)==='ar')?'ar':'en';}var d=document.documentElement;"
    "d.setAttribute('data-lang',l);d.setAttribute('lang',l);"
    "d.setAttribute('dir',l==='ar'?'rtl':'ltr');"
    "var m={en:d.getAttribute('data-title-en'),ar:d.getAttribute('data-title-ar')};"
    "if(m[l]){document.title=m[l];}}catch(e){}})();</script>"
)

TITLE_SYNC = (
    "<script>document.addEventListener('click',function(e){"
    "var b=e.target.closest&&e.target.closest('[data-lang-toggle]');if(!b)return;"
    "setTimeout(function(){var d=document.documentElement,l=d.getAttribute('data-lang');"
    "var m={en:d.getAttribute('data-title-en'),ar:d.getAttribute('data-title-ar')};"
    "if(m[l]){document.title=m[l];}},0);});</script>"
)


def header(active):
    links = []
    for key, en, ar, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{cur}><span data-en>{en}</span><span data-ar>{ar}</span></a>')
    links_html = "".join(links)
    return f'''<a class="skip" href="#main"><span data-en>Skip to content</span><span data-ar>تخطَّ إلى المحتوى</span></a>
<header class="site-header"><div class="container"><nav class="nav" aria-label="Main">
  <a class="brand" href="/" aria-label="Q Apps">{qmark()}<span data-en><b>Q</b> Apps</span><span data-ar><b>كيو</b> آبز</span></a>
  <button class="nav-toggle" data-nav-toggle aria-expanded="false" aria-controls="nav-links" aria-label="Menu">☰</button>
  <div class="nav-links" id="nav-links">{links_html}
    <button class="lang-btn" data-lang-toggle type="button" aria-label="التبديل إلى العربية">العربية</button>
  </div>
</nav></div></header>'''


def footer():
    def col(title_en, title_ar, items):
        lis = "".join(
            f'<li><a href="{href}"><span data-en>{en}</span><span data-ar>{ar}</span></a></li>'
            for en, ar, href in items)
        return (f'<div><h4><span data-en>{title_en}</span><span data-ar>{title_ar}</span></h4>'
                f'<ul>{lis}</ul></div>')

    apps_col = col("Apps", "التطبيقات", [
        *[(APPS[s]["name_en"], APPS[s]["name_ar"], f"/apps/{s}/") for s in site_layout.APP_ORDER],
        ("All apps", "كل التطبيقات", "/apps/"),
    ])
    help_col = col("Help", "المساعدة", [
        ("Tutorials", "الشروحات", "/tutorials/"),
        ("Suggest a feature", "اقترح ميزة", "/suggest/"),
        ("Support", "الدعم", "/support/"),
        ("Contact", "تواصل معنا", "/contact/"),
    ])
    legal_col = col("Company", "الشركة", [
        ("About", "من نحن", "/about/"),
        ("Privacy", "الخصوصية", "/privacy/"),
    ])
    return f'''<footer class="site-footer"><div class="container">
  <div class="footer-grid">
    <div>
      <div class="footer-brand">{qmark(size=40)}<span data-en><b>Q</b> Apps</span><span data-ar><b>كيو</b> آبز</span></div>
      <p style="max-width:34ch" data-en>Valuable apps at tiny prices — pay once, yours for life.</p>
      <p style="max-width:34ch" data-ar>تطبيقات قيّمة بأسعار زهيدة — ادفع مرّة، ولك مدى الحياة.</p>
      <p style="margin-top:14px"><a href="mailto:{SUPPORT_EMAIL}"><bdi dir="ltr">{SUPPORT_EMAIL}</bdi></a></p>
      <p style="margin-top:4px"><a href="{WHATSAPP_LINK}" target="_blank" rel="noopener"><span data-en>WhatsApp</span><span data-ar>واتساب</span>: <bdi dir="ltr">{WHATSAPP_DISPLAY}</bdi></a></p>
    </div>
    {apps_col}{help_col}{legal_col}
  </div>
  <div class="footer-bottom">
    <span>&copy; {YEAR} <span data-en>Q Apps. All rights reserved.</span><span data-ar>كيو آبز. جميع الحقوق محفوظة.</span></span>
    <span><a href="/privacy/"><span data-en>Privacy</span><span data-ar>الخصوصية</span></a>
      &nbsp;·&nbsp;
      <a href="/support/"><span data-en>Support</span><span data-ar>الدعم</span></a></span>
  </div>
</div></footer>'''


def crumbs(items):
    # items: list of (en, ar, href or None)
    parts = []
    for i, (en, ar, href) in enumerate(items):
        sep = '<span aria-hidden="true">/</span>' if i > 0 else ''
        if href:
            parts.append(f'{sep}<a href="{href}"><span data-en>{en}</span><span data-ar>{ar}</span></a>')
        else:
            parts.append(f'{sep}<span data-en>{en}</span><span data-ar>{ar}</span>')
    return f'<div class="container"><nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav></div>'


def render(path, title_en, title_ar, desc_en, desc_ar, body,
           active="", og_image="/assets/img/brand/og-default.png", is404=False,
           canonical_override=None, head_extra=""):
    """Write <path>/index.html (or a bare file for 404).

    canonical_override lets a page point its canonical elsewhere (used by the
    /privacy/<app>/ entry point, which canonicalises to its /en/ URL).
    head_extra injects extra <head> markup (used for hreflang alternates)."""
    if is404:
        canonical = ""
        out_file = os.path.join(ROOT, "404.html")
    else:
        url = path if path.endswith("/") else path + "/"
        canonical = SITE_URL + url
        rel = url.strip("/")
        out_dir = ROOT if rel == "" else os.path.join(ROOT, rel)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "index.html")

    canonical_href = canonical_override or canonical
    og_abs = SITE_URL + og_image
    canonical_tag = f'<link rel="canonical" href="{canonical_href}">' if canonical_href else ''
    og_url = f'<meta property="og:url" content="{canonical_href}">' if canonical_href else ''

    html = f'''<!DOCTYPE html>
<html lang="en" dir="ltr" data-lang="en" data-title-en="{esc(title_en)}" data-title-ar="{esc(title_ar)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{PREPAINT}
<title>{esc(title_en)}</title>
<meta name="description" content="{esc(desc_en)}">
{canonical_tag}
<meta name="theme-color" content="{THEME_COLOR}">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Q Apps">
<meta property="og:title" content="{esc(title_en)}">
<meta property="og:description" content="{esc(desc_en)}">
{og_url}
<meta property="og:image" content="{og_abs}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="ar_SA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title_en)}">
<meta name="twitter:description" content="{esc(desc_en)}">
<meta name="twitter:image" content="{og_abs}">
{head_extra}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/favicon-16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{FONTS}
<link rel="stylesheet" href="{CSS_HREF}">
<style>{site_layout.CSS}</style>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="{JS_SRC}" defer></script>
{TITLE_SYNC}
</body>
</html>'''

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    return canonical


# ---------------------------------------------------------------------------
# screenshots strip (kept for app_overview_body)
# ---------------------------------------------------------------------------

def shots(app):
    imgs = "".join(
        f'<img src="{src}" alt="{esc(alt_en)}" loading="lazy" width="230">'
        for src, alt_en, alt_ar in app["screens"])
    return f'<div class="shots">{imgs}</div>'


# ===========================================================================
# PAGES
# ===========================================================================

def home_sections():
    """The sections of the former long home page. Since the redesign (decision هـ)
    «the idea», «why Q Apps» and «we build for you» live on /about/; nothing was
    deleted."""
    idea = f'''<section id="idea" style="padding-top:24px"><div class="container">
  <div class="section-head">
    <span class="kicker" data-en>The idea</span><span class="kicker" data-ar>الفكرة</span>
    {h(2, "Why pay again and again?", "لماذا تدفع مرّة بعد مرّة؟")}
    {p("We kept noticing the same thing: much of what people pay a lot for can be offered for very little. Many apps charge a monthly or yearly subscription — and over time you pay many times the value. That is where Q Apps came from: useful apps, a small one-time price, and lifetime access.",
       "لاحظنا الأمر نفسه مرارًا: كثير ممّا يدفع الناس فيه الكثير يمكن أن يُقدَّم بسعر زهيد جدًّا. تطبيقات كثيرة تطلب اشتراكًا شهريًا أو سنويًا، ومع الوقت تدفع أضعاف قيمتها. من هنا جاءت فكرة كيو آبز: تطبيقات مفيدة، بسعر زهيد تدفعه مرّة واحدة، ووصول مدى الحياة.")}
  </div>
  <div class="compare">
    <article class="compare-card compare-sub">
      <span class="compare-tag" data-en>Typical subscription</span><span class="compare-tag" data-ar>الاشتراك المعتاد</span>
      {h(3, "Every month. Every year. Forever.", "كل شهر، وكل سنة، إلى ما لا نهاية.")}
      <div class="ticks" aria-hidden="true">{"<i></i>" * 36}</div>
      {p("The payments keep coming, and the total keeps growing — often many times the price of the app itself.",
         "الدفعات لا تتوقّف، والمجموع يكبر باستمرار — وكثيرًا ما يبلغ أضعاف قيمة التطبيق نفسه.")}
    </article>
    <article class="compare-card compare-q">
      <span class="compare-tag" data-en><b>Q</b> Apps</span><span class="compare-tag" data-ar><b>كيو</b> آبز</span>
      {h(3, "One small payment. Yours for life.", "دفعة واحدة زهيدة، ولك مدى الحياة.")}
      <div class="ticks" aria-hidden="true"><i></i></div>
      {p("Pay once and keep using what you bought, with no renewals and no surprise charges.",
         "ادفع مرّة واحدة واستمرّ في استخدام ما اشتريته، بلا تجديد ولا رسوم مفاجئة.")}
    </article>
  </div>
</div></section>'''

    services = f'''<section id="services" style="padding-top:24px"><div class="container">
  <div class="section-head">
    <span class="kicker" data-en>Services</span><span class="kicker" data-ar>الخدمات</span>
    {h(2, "We also build apps for you", "ونبني تطبيقك أيضًا")}
    {p("Beyond our own apps, we design and develop web and mobile applications for businesses and individuals.",
       "إلى جانب تطبيقاتنا، نصمّم ونطوّر تطبيقات الويب والجوال للشركات والأفراد.")}
  </div>
  <div class="services">
    <article class="service-card">
      <div class="service-icon">{ICON_CODE}</div>
      {h(3, "Web Application Development", "تطوير تطبيقات الويب")}
      {p("Responsive, secure, and maintainable web applications designed around real business and user requirements.",
         "تطبيقات ويب متجاوبة وآمنة وقابلة للصيانة، مصمّمة وفق احتياجات العمل والمستخدم الفعلية.")}
    </article>
    <article class="service-card">
      <div class="service-icon">{ICON_PHONE}</div>
      {h(3, "Mobile Application Development", "تطوير تطبيقات الجوال")}
      {p("Polished cross-platform mobile applications for Android and iOS, with a strong focus on usability, reliability, performance, and a consistent experience.",
         "تطبيقات جوال متقنة تعمل على أندرويد و iOS، مع تركيز قوي على سهولة الاستخدام والموثوقية والأداء وتجربة متناسقة.")}
    </article>
  </div>
</div></section>'''

    why = f'''<section id="about" style="padding-top:24px"><div class="container">
  <div class="section-head">
    <span class="kicker" data-en>Why Q Apps</span><span class="kicker" data-ar>لماذا كيو آبز</span>
    {h(2, "More value, less money.", "قيمة أكبر، بمال أقل.")}
  </div>
  <div class="why-grid">
    <article class="why-card"><div class="service-icon">{ICON_TARGET}</div>
      <strong data-en>Tiny prices</strong><strong data-ar>أسعار زهيدة</strong>
      {p("We keep our prices small on purpose, so a good app is within everyone’s reach.",
         "نُبقي أسعارنا زهيدة عن قصد، ليكون التطبيق الجيّد في متناول الجميع.")}</article>
    <article class="why-card"><div class="service-icon">{ICON_CHECK}</div>
      <strong data-en>Pay once, keep it</strong><strong data-ar>ادفع مرّة واحتفظ به</strong>
      {p("No monthly or yearly subscriptions. One purchase, and the app is yours for life.",
         "لا اشتراكات شهرية ولا سنوية. عملية شراء واحدة، ويبقى التطبيق لك مدى الحياة.")}</article>
    <article class="why-card"><div class="service-icon">{ICON_USER}</div>
      <strong data-en>Built with you</strong><strong data-ar>نبنيه معك</strong>
      {p("Tell us what you need. When we see a good opportunity, we add it — at no extra cost to you.",
         "أخبرنا بما تحتاجه. وإذا وجدنا فرصة مناسبة أضفناه — دون أي تكلفة إضافية عليك.")}</article>
  </div>
</div></section>'''

    suggest = f'''<section style="padding-top:24px"><div class="container"><div class="suggest-band">
  <div class="suggest-copy">
    <span class="kicker" data-en>Your voice</span><span class="kicker" data-ar>صوتك</span>
    {h(2, "Your idea could be our next feature.", "فكرتك قد تكون ميزتنا القادمة.")}
    {p("Send us your opinion, a suggestion, or a feature you wish an app had. We read every message, and when we find a good opportunity to build it, we add it for everyone — free of charge.",
       "أرسل لنا رأيك أو اقتراحك أو ميزة تتمنّى وجودها في أحد التطبيقات. نقرأ كل رسالة، وإذا وجدنا فرصة مناسبة لتنفيذها أضفناها للجميع — دون أي مقابل.")}
  </div>
  <a class="btn btn-accent" href="/suggest/"><span data-en>Suggest a feature</span><span data-ar>اقترح ميزة</span>{ARROW_SVG}</a>
</div></div></section>'''

    cta = f'''<section style="padding-top:0"><div class="container"><div class="cta-band">
  <div>
    {h(2, "Have an application idea?", "لديك فكرة لتطبيق؟")}
    {p("Let's turn it into a clear, useful web or mobile application.", "لنحوّلها إلى تطبيق ويب أو جوال واضح ومفيد.")}
  </div>
  <a class="btn btn-secondary" href="/contact/"><span data-en>Contact us</span><span data-ar>تواصل معنا</span>{ARROW_SVG}</a>
</div></div></section>'''

    return {"idea": idea, "why": why, "suggest": suggest, "services": services, "cta": cta}


INSPIRE = (
    '<figure class="inspire"><blockquote>'
    '<p data-en>I drew the idea of Q Apps from Mohammed Omar\'s experience with “<a class="inspire-link" href="https://qeu.app/" target="_blank" rel="noopener">Q</a>”: just as he made everyday needs — groceries, fresh fruit and skincare — affordable for people, I aim to offer useful apps at prices within everyone\'s reach.</p>'
    '<p data-ar>استلهمتُ فكرة كيو آبز من تجربة محمد عمر في «<a class="inspire-link" href="https://qeu.app/" target="_blank" rel="noopener">كيو</a>»؛ فكما أتاح للناس احتياجاتهم اليومية — من المقاضي والفواكه الطازجة إلى منتجات العناية — بأسعار ميسّرة، أسعى لتقديم تطبيقات مفيدة بأسعار في متناول الجميع.</p>'
    '</blockquote></figure>')


def page_home():
    """Home = one intro line, the grid of app icons, «suggest», the Qeu quote
    (redesign proposal, decision أ)."""
    intro = f'''<section class="qa-intro"><div class="container">
  <h1 data-en>Useful apps at a tiny price. <em>Pay once, yours for life.</em></h1>
  <h1 data-ar>تطبيقات مفيدة بسعر زهيد. <em>تدفع مرّة، وتبقى لك.</em></h1>
  {p("No monthly or yearly subscription. In Arabic and English, and your data stays on your phone.",
     "بلا اشتراك شهري ولا سنوي. بالعربية والإنجليزية، وبياناتك تبقى على جوالك.", "lead")}
</div></section>'''
    grid = f'''<section class="qa-apps" id="apps"><div class="container">
  {site_layout.icon_grid(APPS)}
</div></section>'''
    quote = f'''<section class="qa-quote"><div class="container">{INSPIRE}</div></section>'''
    return intro + grid + home_sections()["suggest"] + quote


def page_apps():
    """/apps/ shows the same icon grid as the home page (decision و)."""
    body = f'''{crumbs([("Home","الرئيسية","/"),("Apps","التطبيقات",None)])}
<section class="qa-apps" style="padding-top:28px"><div class="container">
  {site_layout.icon_grid(APPS, h_tag="h1")}
</div></section>'''
    return render("/apps/",
                  "Our Apps — Q Apps",
                  "تطبيقاتنا — كيو آبز",
                  "Explore the mobile apps by Q Apps: DocMatic, Vault — Warranty Manager and Countdown Keeper. Private, offline-first, in Arabic and English.",
                  "استعرض تطبيقات كيو آبز: DocMatic وخزنة الضمانات و«كم مضى وكم بقي». تطبيقات خاصة تعمل دون اتصال، بالعربية والإنجليزية.",
                  body, active="apps")


def app_overview_body(app, features_list, intro_en, intro_ar, extra=""):
    slug = app["slug"]
    if app["status"] == "live":
        stores = []
        if app.get("appstore"):
            stores.append(store_button("apple", app["appstore"]))
        if app.get("playstore"):
            stores.append(store_button("play", app["playstore"]))
        if app.get("youtube"):
            stores.append(store_button("youtube", app["youtube"]))
        store_block = f'<div class="stores" style="margin-top:8px">{"".join(stores)}</div>'
    else:
        store_block = ('<div class="chips" style="margin-top:8px">'
                       '<span class="chip"><span data-en>App Store — coming soon</span><span data-ar>App Store — قريبًا</span></span>'
                       '<span class="chip"><span data-en>Google Play — coming soon</span><span data-ar>Google Play — قريبًا</span></span></div>')

    feats = "".join(feature(*f) for f in features_list)

    # Available languages — tracked per content type (privacy may exceed the rest)
    priv_pills = "".join(
        f'<a class="lang-pill" href="/privacy/{slug}/{L}/" hreflang="{L}" lang="{L}">{LANG_META[L][0]}</a>'
        for L in app["privacy_langs"])
    other_langs = " · ".join(LANG_META[L][0] for L in app["overview_langs"])
    availability = f'''<section class="section section-soft"><div class="container">
  {h(2, "Available languages", "اللغات المتوفّرة", "center")}
  {p("Privacy Policy is available in every language below. App overview, tutorials, and support are available in English and Arabic.",
     "سياسة الخصوصية متوفّرة بكل اللغات أدناه. أمّا نبذة التطبيق والشروحات والدعم فمتوفّرة بالعربية والإنجليزية.", "lead center")}
  <div class="avail">
    <div class="avail-row">
      <span class="avail-label"><span data-en>Privacy Policy</span><span data-ar>سياسة الخصوصية</span></span>
      <div class="lang-pills">{priv_pills}</div>
    </div>
    <div class="avail-row">
      <span class="avail-label"><span data-en>Overview · Tutorials · Support</span><span data-ar>النبذة · الشروحات · الدعم</span></span>
      <div class="lang-pills"><span class="lang-pill static">{other_langs}</span></div>
    </div>
  </div>
</div></section>'''

    return f'''{crumbs([("Home","الرئيسية","/"),("Apps","التطبيقات","/apps/"),(app['name_en'],app['name_ar'],None)])}
<section class="section"><div class="container">
  <div class="app-head" style="margin-bottom:18px">
    <img src="{app['icon']}" alt="{esc(app['name_en'])} icon" width="80" height="80" style="border-radius:18px;box-shadow:var(--shadow-md)">
    <div>{h(1, app['name_en'], app['name_ar'])}
      <p class="muted" data-en>{app['tagline_en']}</p><p class="muted" data-ar>{app['tagline_ar']}</p></div>
  </div>
  {p(intro_en, intro_ar, "lead")}
  {store_block}
  <div class="linkrow" style="margin-top:16px">
    <a href="/tutorials/{slug}/"><span data-en>Tutorial</span><span data-ar>الشرح</span></a>
    <a href="/support/{slug}/"><span data-en>Support</span><span data-ar>الدعم</span></a>
    <a href="/privacy/{slug}/"><span data-en>Privacy policy</span><span data-ar>سياسة الخصوصية</span></a>
  </div>
</div></section>
<section class="section section-soft"><div class="container">
  {h(2, "Screenshots", "لقطات من التطبيق", "center")}
  {shots(app)}
</div></section>
<section class="section"><div class="container">
  {h(2, "Features", "المزايا", "center")}
  <div class="features" style="margin-top:30px">{feats}</div>
  {extra}
</div></section>
{availability}'''


def page_app_countdown():
    """/apps/countdown-keeper/ — long hand-tuned page kept in tools/countdown_page.py."""
    import countdown_page
    return countdown_page.build_page(render, h, p, crumbs, APPS["countdown-keeper"], store_button)


def page_app_docmatic():
    """/apps/docmatic/ — long hand-tuned page kept in tools/docmatic_page.py."""
    import docmatic_page
    return docmatic_page.build_page(render, h, p, crumbs, APPS["docmatic"])


def page_app_vault():
    """/apps/vault/ — long hand-tuned page kept in tools/vault_page.py."""
    import vault_page
    return vault_page.build_page(render, h, p, crumbs, APPS["vault"], store_button)


# ---------------------------- tutorials ------------------------------------

def page_tutorials():
    cards = []
    for slug in ("countdown-keeper", "vault"):
        a = APPS[slug]
        cards.append(f'''<article class="card">
          <div class="app-head"><img src="{a['icon']}" alt="" width="56" height="56" style="width:56px;height:56px;border-radius:14px">
          <h3><a href="/tutorials/{slug}/"><span data-en>{a['name_en']}</span><span data-ar>{a['name_ar']}</span></a></h3></div>
          <p style="margin-top:12px" data-en>Step-by-step guides, tips and answers to common questions.</p>
          <p style="margin-top:12px" data-ar>أدلة خطوة بخطوة ونصائح وإجابات عن الأسئلة الشائعة.</p>
          <p style="margin-top:10px"><a href="/tutorials/{slug}/"><span data-en>Open tutorials →</span><span data-ar>افتح الشروحات →</span></a></p>
        </article>''')
    body = f'''{crumbs([("Home","الرئيسية","/"),("Tutorials","الشروحات",None)])}
<section class="section"><div class="container">
  {h(1, "Tutorials", "الشروحات")}
  {p("Learn how to get the most out of each of our apps. Guides grow over time — pick an app to begin.",
     "تعلّم كيف تستفيد من كل تطبيق من كيو آبز استفادةً كاملة. تنمو الأدلة مع الوقت — اختر تطبيقًا لتبدأ.", "lead")}
  <div class="grid grid-2" style="margin-top:32px">{"".join(cards)}</div>
</div></section>'''
    return render("/tutorials/",
                  "Tutorials — Q Apps",
                  "الشروحات — كيو آبز",
                  "Step-by-step tutorials and guides for Q Apps: Countdown Keeper and Vault — Warranty Manager.",
                  "شروحات وأدلة خطوة بخطوة لتطبيقات كيو آبز: «كم مضى وكم بقي» وخزنة الضمانات.",
                  body, active="tutorials")


def tutorial_page(slug, title_en, title_ar, desc_en, desc_ar, intro_en, intro_ar,
                  steps_list, tips, faqs, video_embed=None):
    a = APPS[slug]
    video = ""
    if video_embed:
        video = f'''<div style="margin:28px 0">
          <div class="video-wrap"><iframe src="{video_embed}" title="{esc(title_en)}" loading="lazy"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div></div>'''
    tips_html = ""
    if tips:
        tips_html = f'{h(2,"Tips","نصائح")}{ul(tips)}'
    body = f'''{crumbs([("Home","الرئيسية","/"),("Tutorials","الشروحات","/tutorials/"),(a['name_en'],a['name_ar'],None)])}
<section class="section"><div class="container prose">
  {h(1, title_en, title_ar)}
  {p(intro_en, intro_ar, "lead")}
  {video}
  {h(2, "Getting started", "البداية")}
  {steps(steps_list)}
  {tips_html}
  {h(2, "Frequently asked questions", "أسئلة شائعة")}
  {faq(faqs)}
  <div class="callout" style="margin-top:28px">
    {p(f'Need more help? Visit <a href="/support/{slug}/">{a["name_en"]} support</a> or email us.',
       f'تحتاج مزيدًا من المساعدة؟ تفضّل بزيارة <a href="/support/{slug}/">دعم {a["name_ar"]}</a> أو راسلنا عبر البريد.')}
  </div>
</div></section>'''
    return render(f"/tutorials/{slug}/", title_en, title_ar, desc_en, desc_ar, body, active="tutorials")


def page_tutorial_countdown():
    steps_list = [
        ("Add your first event", "أضِف مناسبتك الأولى", "Tap the + button, type a title, and pick the date (and time, if it matters).", "اضغط زر +، واكتب عنوانًا، واختر التاريخ (والوقت إن كان مهمًّا)."),
        ("Choose a calendar", "اختر التقويم", "Pick Gregorian or Hijri for how the date is calculated and shown.", "اختر التقويم الميلادي أو الهجري لطريقة حساب التاريخ وعرضه."),
        ("Make it recognizable", "اجعلها مميّزة", "Give the event a colour and an emoji, or attach your own photo, and add notes.", "امنح المناسبة لونًا ورمزًا تعبيريًا، أو أرفق صورتك الخاصة، وأضِف ملاحظات."),
        ("Turn on a reminder", "فعّل التذكير", "Optionally enable a notification for the time, a day, or a week before.", "فعّل — إن شئت — إشعارًا عند الموعد أو قبله بيوم أو بأسبوع."),
        ("Pin what matters", "ثبّت المهمّ", "Pin important events to keep them at the top of your list.", "ثبّت المناسبات المهمّة لتبقى أعلى قائمتك."),
    ]
    tips = [
        ("Repeat an event monthly from the event editor to track recurring dates automatically.",
         "كرِّر المناسبة شهريًا من محرّر المناسبة لتتبّع التواريخ المتكرّرة تلقائيًا."),
        ("Use the Tools tab for the age calculator, date difference, and the retirement estimator.",
         "استخدم تبويب الأدوات لحاسبة العمر وفرق التاريخين ومقدّر التقاعد."),
        ("Export your events to a JSON file as a personal backup you fully control.",
         "صدّر مناسباتك إلى ملف JSON كنسخة احتياطية شخصية تتحكّم بها تمامًا."),
    ]
    faqs = [
        ("Do I need an internet connection?", "هل أحتاج إلى اتصال بالإنترنت؟",
         "No. Countdown Keeper works fully offline; your events stay on your device.",
         "لا. يعمل تطبيق «كم مضى وكم بقي» دون اتصال تمامًا، وتبقى مناسباتك على جهازك."),
        ("How do I recover a deleted event?", "كيف أستعيد مناسبة محذوفة؟",
         "Open the Recycle bin and restore it before it is permanently purged.",
         "افتح سلة المحذوفات واستعد المناسبة قبل إزالتها نهائيًا."),
        ("Can I show dates in the Hijri calendar?", "هل يمكن عرض التواريخ بالتقويم الهجري؟",
         "Yes. You can view dates in the Hijri (Umm al-Qura) or Gregorian calendar, and even repeat events on Hijri dates.",
         "نعم. يمكنك عرض التواريخ بالتقويم الهجري (أم القرى) أو الميلادي، بل وتكرار المناسبات على تواريخ هجرية."),
    ]
    return tutorial_page("countdown-keeper",
                         "Countdown Keeper Tutorials",
                         "شروحات تطبيق «كم مضى وكم بقي»",
                         "How to use Countdown Keeper: add events, set recurring Hijri/Gregorian dates, reminders, and use the built-in date tools.",
                         "كيفية استخدام تطبيق «كم مضى وكم بقي»: إضافة المناسبات، وضبط التواريخ المتكرّرة الهجرية/الميلادية، والتذكيرات، واستخدام أدوات التاريخ.",
                         "Learn how to add events, use reminders, recurring dates and the built-in date tools.",
                         "تعلّم كيف تضيف المناسبات، وتستخدم التذكيرات والتواريخ المتكرّرة وأدوات التاريخ المدمجة.",
                         steps_list, tips, faqs)


def page_tutorial_vault():
    steps_list = [
        ("Add a purchase", "أضِف عملية شراء", "Tap add and scan the paper receipt, read its QR code, or import an existing image or PDF.", "اضغط «إضافة» وامسح الإيصال الورقي، أو اقرأ رمز QR، أو استورد صورة أو ملف PDF موجودًا."),
        ("Fill in the details", "أدخِل التفاصيل", "Add the store, purchase date and the products, each with its own warranty period.", "أضِف المتجر وتاريخ الشراء والمنتجات، لكلٍّ منها مدة ضمانه."),
        ("Set the warranty", "حدّد الضمان", "Enter the warranty length so Vault can remind you before it expires.", "أدخِل مدة الضمان لتذكّرك الخزنة قبل انتهائه."),
        ("Save the store location", "احفظ موقع المتجر", "Optionally capture the store's location so you can reopen it in your maps app later.", "التقط — إن شئت — موقع المتجر لتعيد فتحه لاحقًا في تطبيق الخرائط."),
        ("Back up your data", "انسخ بياناتك احتياطيًا", "Create an encrypted, password-protected backup and keep it somewhere safe.", "أنشئ نسخة احتياطية مشفّرة ومحمية بكلمة مرور واحفظها في مكان آمن."),
    ]
    tips = [
        ("Share a PDF or photo from WhatsApp, Gmail or Files directly into Vault to file it instantly.",
         "شارك ملف PDF أو صورة من واتساب أو Gmail أو الملفات مباشرةً إلى الخزنة لحفظها فورًا."),
        ("Export a bulk warranty report as a PDF to print or send.",
         "صدّر تقرير ضمانات مجمّعًا بصيغة PDF للطباعة أو الإرسال."),
        ("Lifetime Access removes the free limit of 3 invoices with one product each.",
         "يزيل «الوصول مدى الحياة» حدَّ النسخة المجانية البالغ 3 فواتير بمنتج واحد لكلٍّ منها."),
    ]
    faqs = [
        ("Where is my data stored?", "أين تُخزَّن بياناتي؟",
         "On your device. Vault is local-first and does not upload your invoices to any server.",
         "على جهازك. تعمل الخزنة محليًا ولا ترفع فواتيرك إلى أي خادم."),
        ("How do reminders work?", "كيف تعمل التذكيرات؟",
         "Vault schedules a local notification on your device before a warranty's expiry date.",
         "تجدول الخزنة إشعارًا محليًا على جهازك قبل تاريخ انتهاء الضمان."),
        ("Is the backup safe?", "هل النسخة الاحتياطية آمنة؟",
         "Backups are encrypted with AES-256 using a password you set. Keep the password safe — it cannot be recovered.",
         "تُشفَّر النسخ الاحتياطية بمعيار AES-256 بكلمة مرور تحدّدها. احتفظ بكلمة المرور — إذ لا يمكن استعادتها."),
        ("What is Lifetime Access?", "ما هو «الوصول مدى الحياة»؟",
         "A single one-time purchase that unlocks unlimited invoices and products. There are no subscriptions.",
         "عملية شراء واحدة تفتح عددًا غير محدود من الفواتير والمنتجات. ولا توجد اشتراكات."),
    ]
    return tutorial_page("vault",
                         "Vault — Warranty Manager Tutorials",
                         "شروحات خزنة الضمانات",
                         "How to use Vault: scan receipts and QR codes, track warranties, save store locations, export reports, and create encrypted backups.",
                         "كيفية استخدام خزنة الضمانات: مسح الإيصالات ورموز QR، وتتبّع الضمانات، وحفظ مواقع المتاجر، وتصدير التقارير، وإنشاء نسخ احتياطية مشفّرة.",
                         "Learn how to scan receipts, track warranties, and back up your data securely.",
                         "تعلّم كيف تمسح الإيصالات، وتتبّع الضمانات، وتنسخ بياناتك احتياطيًا بأمان.",
                         steps_list, tips, faqs,
                         video_embed=APPS["vault"]["youtube_embed"])


# ---------------------------- privacy --------------------------------------

def page_privacy_index():
    cards = []
    for slug in ("countdown-keeper", "vault"):
        a = APPS[slug]
        cards.append(f'''<article class="card">
          <div class="app-head"><img src="{a['icon']}" alt="" width="56" height="56" style="width:56px;height:56px;border-radius:14px">
          <h3><a href="/privacy/{slug}/"><span data-en>{a['name_en']}</span><span data-ar>{a['name_ar']}</span></a></h3></div>
          <p style="margin-top:12px"><a href="/privacy/{slug}/"><span data-en>Read the privacy policy →</span><span data-ar>اقرأ سياسة الخصوصية →</span></a></p>
        </article>''')
    body = f'''{crumbs([("Home","الرئيسية","/"),("Privacy","الخصوصية",None)])}
<section class="section"><div class="container prose">
  {h(1, "Privacy", "الخصوصية")}
  {p("We build privacy-first apps. Our apps are local-first: your data stays on your device, we do not run accounts or servers for your content, and we do not use ads, analytics, or third-party trackers.",
     "نحن نبني تطبيقات تضع الخصوصية أولًا. تطبيقاتنا تعمل محليًا: بياناتك تبقى على جهازك، ولا نُشغّل حسابات أو خوادم لمحتواك، ولا نستخدم إعلانات أو تحليلات أو أدوات تتبّع من طرف ثالث.", "lead")}
  {h(2, "Per-app privacy policies", "سياسات الخصوصية لكل تطبيق")}
  {p("Each app has its own policy describing exactly what it handles:", "لكل تطبيق سياسته الخاصة التي تصف بدقّة ما يتعامل معه:")}
</div>
<div class="container"><div class="grid grid-2" style="margin-top:20px">{"".join(cards)}</div></div>
<div class="container prose" id="messages" style="margin-top:44px">
  {h(2, "Messages you send from this website", "الرسائل التي ترسلها من هذا الموقع")}
  {p("When you send a message, suggestion, idea or problem from the «Contact &amp; suggest» page, we keep what you wrote: the app you chose, the type of message, your text, the page language, and your name and a way to reply only if you write them. We use it only to read and answer your message and to improve our apps. We never sell it, share it, or use it for advertising.",
     "حين ترسل رسالة أو اقتراحًا أو فكرة أو مشكلة من صفحة «تواصل واقترح»، نحفظ ما كتبته: التطبيق الذي اخترته، ونوع الرسالة، ونصّها، ولغة الصفحة، واسمك وطريقة الرد فقط إن كتبتهما. نستخدمها فقط لنقرأ رسالتك ونرد عليها ولنحسّن تطبيقاتنا، ولا نبيعها ولا نشاركها مع أحد ولا نستخدمها للإعلان.")}
  {p("To stop robots and floods of messages, the page uses Cloudflare Turnstile (from Cloudflare, which hosts this website), and we keep a fingerprint of your connection's address — salted and one-way, so it cannot be turned back into the address — for no more than 24 hours. Messages are stored in our database on Cloudflare and only we can read them. To have a message deleted, write to us from the same page or by email.",
     "ولمنع الروبوتات وسيل الرسائل، تستخدم الصفحة Cloudflare Turnstile (من Cloudflare التي تستضيف هذا الموقع)، ونحفظ بصمة مشفّرة لعنوان اتصالك — باتجاه واحد لا يمكن إعادتها إلى العنوان — مدة لا تزيد على 24 ساعة. وتُحفظ الرسائل في قاعدة بياناتنا على Cloudflare، ولا يقرؤها أحد غيرنا. ولحذف رسالة أرسلتها، راسلنا من الصفحة نفسها أو بالبريد.")}
  {p("Our apps do not send anything themselves; this applies only to what you send from this website.",
     "تطبيقاتنا لا ترسل شيئًا بنفسها؛ هذا يخص فقط ما ترسله من هذا الموقع.", "fineprint")}
</div>
</section>'''
    return render("/privacy/",
                  "Privacy — Q Apps",
                  "الخصوصية — كيو آبز",
                  "Privacy at Q Apps: local-first apps with no ads, analytics, or third-party tracking. Read each app's privacy policy.",
                  "الخصوصية في كيو آبز: تطبيقات تعمل محليًا بلا إعلانات أو تحليلات أو تتبّع من طرف ثالث. اقرأ سياسة خصوصية كل تطبيق.",
                  body, active="privacy")


def load_privacy(slug, lang):
    with open(os.path.join(ROOT, "content", "privacy", slug, f"{lang}.json"), encoding="utf-8") as f:
        return json.load(f)


def privacy_hreflang(slug, langs):
    tags = [f'<link rel="alternate" hreflang="{L}" href="{SITE_URL}/privacy/{slug}/{L}/">' for L in langs]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/privacy/{slug}/en/">')
    return "\n".join(tags)


GLOBE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" '
             'stroke-width="1.8" d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm0 0c2.5 2.5 2.5 15.5 0 18M12 '
             '3c-2.5 2.5-2.5 15.5 0 18M3.5 9h17M3.5 15h17"/></svg>')


def lang_dropdown(app, current):
    """Compact language switcher for a single-language privacy page. Native
    <details> disclosure — no JavaScript needed; every option is a direct URL,
    so the content stays one language but other languages are easy to find."""
    langs = app["privacy_langs"]
    if len(langs) <= 1:
        return ""
    slug = app["slug"]
    label = "تغيير اللغة" if current == "ar" else "Change language"
    items = []
    for L in langs:
        name = LANG_META[L][0]
        active = " active" if L == current else ""
        cur = ' aria-current="true"' if L == current else ""
        items.append(f'<a class="lang-opt{active}" href="/privacy/{slug}/{L}/" '
                     f'hreflang="{L}" lang="{L}"{cur}>{name}</a>')
    return (f'<details class="lang-dd">'
            f'<summary aria-label="{esc(label)}">{GLOBE_SVG}'
            f'<span class="lang-cur">{LANG_META[current][0]}</span>'
            f'<span class="chev" aria-hidden="true">▾</span></summary>'
            f'<div class="lang-dd-menu">{"".join(items)}</div></details>')


def privacy_doc(app, lang, data, canonical):
    """A self-contained, single-language privacy document (no global site
    header/footer). Shows only this language's policy, but includes a compact
    language switcher so the other languages are easy to reach. Every language
    is a direct URL; hreflang keeps the set linked for SEO / store crawlers.
    Works with zero JavaScript."""
    slug = app["slug"]
    d = data["dir"]
    app_name = (app.get("privacy_name_ar", app["name_ar"]) if lang == "ar"
                else app["name_en"])
    parts = []
    for b in data["blocks"]:
        if b["t"] == "h2":
            parts.append(f'<h2>{b["html"]}</h2>')
        elif b["t"] == "p":
            parts.append(f'<p>{b["html"]}</p>')
        else:
            parts.append(b["html"])
    hreflang = privacy_hreflang(slug, app["privacy_langs"])
    if lang == "ar":
        foot = f'© {YEAR} Q Apps · <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>'
    else:
        foot = f'© {YEAR} Q Apps · <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>'
    title = f"{data['title']} — {app['name_en']}"
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(data['title'])}">
<link rel="canonical" href="{canonical}">
{hreflang}
<meta name="theme-color" content="{THEME_COLOR}">
<meta name="color-scheme" content="light dark">
<meta name="robots" content="index,follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="{CSS_HREF}">
</head>
<body class="doc">
<main class="doc-wrap">
  <header class="doc-head">
    <div class="doc-topbar">{lang_dropdown(app, lang)}</div>
    <img class="doc-icon" src="{app['icon']}" alt="{esc(app['name_en'])} icon" width="72" height="72">
    <div class="doc-app">{esc(app_name)}</div>
    <h1 class="doc-title">{data['title']}</h1>
    <p class="doc-date">{data['effective']}</p>
  </header>
  <article class="policy prose">
    {"".join(parts)}
  </article>
  <footer class="doc-foot">{foot}</footer>
</main>
</body>
</html>'''


def _write(path, html):
    rel = path.strip("/")
    out_dir = os.path.join(ROOT, rel)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return SITE_URL + (path if path.endswith("/") else path + "/")


def gen_privacy(slug):
    """Write one standalone page per privacy language + a canonical entry point
    at /privacy/<slug>/ (English, canonicalised to /en/). Returns localized URLs
    for the sitemap."""
    app = APPS[slug]
    langs = app["privacy_langs"]
    sitemap_urls = []
    for L in langs:
        data = load_privacy(slug, L)
        canonical = f"{SITE_URL}/privacy/{slug}/{L}/"
        u = _write(f"/privacy/{slug}/{L}/", privacy_doc(app, L, data, canonical))
        sitemap_urls.append(u)
    # entry point = English document, canonical -> /en/
    data = load_privacy(slug, "en")
    _write(f"/privacy/{slug}/", privacy_doc(app, "en", data, f"{SITE_URL}/privacy/{slug}/en/"))
    return sitemap_urls


# ---------------------------- support --------------------------------------

def page_support_index():
    cards = []
    for slug in ("countdown-keeper", "vault"):
        a = APPS[slug]
        cards.append(f'''<article class="card">
          <div class="app-head"><img src="{a['icon']}" alt="" width="56" height="56" style="width:56px;height:56px;border-radius:14px">
          <h3><a href="/support/{slug}/"><span data-en>{a['name_en']}</span><span data-ar>{a['name_ar']}</span></a></h3></div>
          <p style="margin-top:12px"><a href="/support/{slug}/"><span data-en>Open support →</span><span data-ar>افتح الدعم →</span></a></p>
        </article>''')
    body = f'''{crumbs([("Home","الرئيسية","/"),("Support","الدعم",None)])}
<section class="section"><div class="container prose">
  {h(1, "Support", "الدعم")}
  {p("We're here to help. Choose your app below for common questions and troubleshooting, or contact us directly.",
     "نحن هنا للمساعدة. اختر تطبيقك أدناه لتطّلع على الأسئلة الشائعة وحلول المشكلات، أو تواصل معنا مباشرةً.", "lead")}
  <div class="callout">
    {p(f'Email us any time: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>',
       f'راسلنا في أي وقت: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>')}
    <div style="margin-top:10px">{whatsapp_button()}</div>
  </div>
</div>
<div class="container"><div class="grid grid-2" style="margin-top:8px">{"".join(cards)}</div></div>
</section>'''
    return render("/support/",
                  "Support — Q Apps",
                  "الدعم — كيو آبز",
                  "Get help with Q Apps. Common questions, troubleshooting, and how to contact support for Countdown Keeper and Vault.",
                  "احصل على المساعدة لتطبيقات كيو آبز. أسئلة شائعة وحلول للمشكلات وطريقة التواصل مع الدعم لتطبيقَي «كم مضى وكم بقي» وخزنة الضمانات.",
                  body, active="support")


def support_page(slug, title_en, title_ar, desc_en, desc_ar, faqs, trouble):
    a = APPS[slug]
    body = f'''{crumbs([("Home","الرئيسية","/"),("Support","الدعم","/support/"),(a['name_en'],a['name_ar'],None)])}
<section class="section"><div class="container prose">
  {h(1, a['name_en'] + " Support", "دعم " + a['name_ar'])}
  {p("Find quick answers below. If you still need help, email us and we'll respond as soon as we can.",
     "ستجد إجابات سريعة أدناه. وإن بقيت بحاجة إلى المساعدة، فراسلنا عبر البريد وسنردّ في أقرب وقت ممكن.", "lead")}
  {h(2, "Common questions", "أسئلة شائعة")}
  {faq(faqs)}
  {h(2, "Troubleshooting", "حلّ المشكلات")}
  {ul(trouble)}
  {h(2, "More help", "مزيد من المساعدة")}
  <p><a href="/tutorials/{slug}/"><span data-en>Read the {a['name_en']} tutorials</span><span data-ar>اقرأ شروحات {a['name_ar']}</span></a>
     &nbsp;·&nbsp;
     <a href="/privacy/{slug}/"><span data-en>Privacy policy</span><span data-ar>سياسة الخصوصية</span></a></p>
  <div class="callout">
    {p(f'Contact support: <a href="mailto:{SUPPORT_EMAIL}?subject={a["name_en"]} support">{SUPPORT_EMAIL}</a>',
       f'تواصل مع الدعم: <a href="mailto:{SUPPORT_EMAIL}?subject={a["name_ar"]} - دعم">{SUPPORT_EMAIL}</a>')}
    <div style="margin-top:10px">{whatsapp_button()}</div>
  </div>
</div></section>'''
    return render(f"/support/{slug}/", title_en, title_ar, desc_en, desc_ar, body, active="support")


def page_support_countdown():
    faqs = [
        ("Is Countdown Keeper free?", "هل تطبيق «كم مضى وكم بقي» مجاني؟",
         "The app is in development and will be available on the App Store and Google Play soon.",
         "التطبيق قيد التطوير وسيتوفّر قريبًا على App Store وGoogle Play."),
        ("Will my data sync between devices?", "هل تتزامن بياناتي بين الأجهزة؟",
         "No. Data is stored on each device. Use the JSON export/import to move events between devices.",
         "لا. تُخزَّن البيانات على كل جهاز. استخدم تصدير/استيراد JSON لنقل المناسبات بين الأجهزة."),
        ("How do I turn on reminders?", "كيف أفعّل التذكيرات؟",
         "Enable a reminder when adding or editing an event, then allow notifications when prompted.",
         "فعّل التذكير عند إضافة مناسبة أو تعديلها، ثم اسمح بالإشعارات عند الطلب."),
    ]
    trouble = [
        ("Reminders not appearing? Make sure notifications are allowed for the app in your device settings and that the reminder time is in the future.",
         "لا تظهر التذكيرات؟ تأكّد من السماح بالإشعارات للتطبيق في إعدادات جهازك، وأن وقت التذكير في المستقبل."),
        ("A date looks off by a day? Check whether the event uses the Hijri or Gregorian calendar in its settings.",
         "يبدو التاريخ مزاحًا بيوم؟ تحقّق مما إذا كانت المناسبة تستخدم التقويم الهجري أو الميلادي في إعداداتها."),
        ("Restoring events on a new phone? Use Import and select your exported JSON file.",
         "تستعيد المناسبات على هاتف جديد؟ استخدم «استيراد» واختر ملف JSON الذي صدّرته."),
    ]
    return support_page("countdown-keeper",
                        "Countdown Keeper Support — Q Apps",
                        "دعم تطبيق «كم مضى وكم بقي» — كيو آبز",
                        "Support for Countdown Keeper: common questions, troubleshooting reminders and calendars, and how to contact us.",
                        "دعم تطبيق «كم مضى وكم بقي»: أسئلة شائعة، وحلول لمشكلات التذكيرات والتقويم، وطريقة التواصل معنا.",
                        faqs, trouble)


def page_support_vault():
    faqs = [
        ("How do I restore a backup?", "كيف أستعيد نسخة احتياطية؟",
         "Open the backup screen, choose Restore, select your backup file, and enter the password you used to create it.",
         "افتح شاشة النسخ الاحتياطي، واختر «استعادة»، وحدّد ملف نسختك، وأدخِل كلمة المرور التي أنشأتها بها."),
        ("I forgot my backup password.", "نسيت كلمة مرور النسخة الاحتياطية.",
         "Backups are encrypted and the password cannot be recovered. Your current data on the device is unaffected.",
         "النسخ الاحتياطية مشفّرة ولا يمكن استعادة كلمة المرور. أمّا بياناتك الحالية على الجهاز فلا تتأثّر."),
        ("What does Lifetime Access include?", "ماذا يتضمّن «الوصول مدى الحياة»؟",
         "A one-time purchase that unlocks unlimited invoices and products. There are no subscriptions.",
         "عملية شراء لمرة واحدة تفتح عددًا غير محدود من الفواتير والمنتجات. ولا توجد اشتراكات."),
        ("Does scanning work offline?", "هل يعمل المسح دون اتصال؟",
         "Yes. Receipt and QR scanning is processed on your device and does not require an internet connection.",
         "نعم. يُعالَج مسح الإيصالات ورموز QR على جهازك ولا يتطلّب اتصالًا بالإنترنت."),
    ]
    trouble = [
        ("Scanner won't open? Allow camera access for Vault in your device settings.",
         "لا يفتح الماسح؟ اسمح بالوصول إلى الكاميرا للخزنة في إعدادات جهازك."),
        ("Warranty reminder didn't arrive? Allow notifications for Vault, and note reminders may be delayed slightly to save battery.",
         "لم يصل تذكير الضمان؟ اسمح بالإشعارات للخزنة، وانتبه إلى أن التذكيرات قد تتأخّر قليلًا لتوفير البطارية."),
        ("\"Use my current location\" not working? Allow location access when prompted; it is only used to save a store's location.",
         "لا يعمل «استخدام موقعي الحالي»؟ اسمح بالوصول إلى الموقع عند الطلب؛ فهو يُستخدم فقط لحفظ موقع المتجر."),
        ("Purchase not recognized? Use the Restore Purchases option on the store/paywall screen.",
         "لم يُتعرَّف على عملية الشراء؟ استخدم خيار «استعادة المشتريات» في شاشة المتجر أو الاشتراك."),
    ]
    return support_page("vault",
                        "Vault — Warranty Manager Support — Q Apps",
                        "دعم خزنة الضمانات — كيو آبز",
                        "Support for Vault — Warranty Manager: backups, purchases, scanning, notifications and location troubleshooting, and how to contact us.",
                        "دعم خزنة الضمانات: النسخ الاحتياطي والمشتريات والمسح والإشعارات وحلّ مشكلات الموقع، وطريقة التواصل معنا.",
                        faqs, trouble)


# ---------------------------- contact & about ------------------------------

def page_contact():
    body = f'''{crumbs([("Home","الرئيسية","/"),("Contact","تواصل معنا",None)])}
<section class="section"><div class="container prose">
  {h(1, "Contact us", "تواصل معنا")}
  {p("Questions, feedback, or need help with one of our apps? We'd love to hear from you.",
     "أسئلة أو ملاحظات أو تحتاج إلى مساعدة في أحد تطبيقاتنا؟ يسعدنا أن نسمع منك.", "lead")}
  <div class="grid grid-2" style="margin-top:24px">
    <div class="card">
      {h(3, "WhatsApp", "واتساب")}
      <p style="font-size:1.15rem"><a href="{WHATSAPP_LINK}" target="_blank" rel="noopener" dir="ltr">{WHATSAPP_DISPLAY}</a></p>
      {p("Message us on WhatsApp for the quickest reply.", "راسلنا على واتساب لأسرع ردّ.")}
      <div style="margin-top:14px">{whatsapp_button()}</div>
    </div>
    <div class="card">
      {h(3, "Email", "البريد الإلكتروني")}
      <p style="font-size:1.15rem"><a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
      {p("We aim to respond to support requests as soon as possible.", "نسعى للردّ على طلبات الدعم في أقرب وقت ممكن.")}
    </div>
  </div>
  <div style="margin-top:24px">
    {p("Looking for something specific?", "تبحث عن شيء محدّد؟")}
    <p><a href="/support/"><span data-en>Support center</span><span data-ar>مركز الدعم</span></a>
       &nbsp;·&nbsp;
       <a href="/tutorials/"><span data-en>Tutorials</span><span data-ar>الشروحات</span></a>
       &nbsp;·&nbsp;
       <a href="/privacy/"><span data-en>Privacy</span><span data-ar>الخصوصية</span></a></p>
  </div>
</div></section>'''
    return render("/contact/",
                  "Contact — Q Apps",
                  "تواصل معنا — كيو آبز",
                  f"Contact Q Apps by email at {SUPPORT_EMAIL} for questions, feedback, or app support.",
                  f"تواصل مع كيو آبز عبر البريد {SUPPORT_EMAIL} للأسئلة أو الملاحظات أو دعم التطبيقات.",
                  body, active="")


def _about_moved():
    """Sections moved here from the former home page (decision هـ)."""
    hs = home_sections()
    return hs["idea"] + hs["why"] + hs["services"] + hs["cta"]


def page_about():
    body = f'''{crumbs([("Home","الرئيسية","/"),("About","من نحن",None)])}
<section class="section"><div class="container prose">
  {h(1, "About Q Apps", "عن كيو آبز")}
  {p("Q Apps makes valuable apps at tiny prices. You pay once, and the app is yours for life — no monthly or yearly subscription.",
     "تصنع كيو آبز تطبيقات قيّمة بأسعار زهيدة. تدفع مرّة واحدة، ويبقى التطبيق لك مدى الحياة — بلا اشتراك شهري أو سنوي.", "lead")}
  {h(2, "How the idea started", "كيف بدأت الفكرة")}
  {p("We were often surprised to find that things sold at high prices can be offered to people for very little — and still be good. Apps are no different: many useful apps ask for a subscription that, over the years, adds up to many times their real value.",
     "كثيرًا ما تفاجأنا بأن أشياء تُباع بأسعار مرتفعة يمكن أن تُقدَّم للناس بأسعار زهيدة جدًّا وتبقى جيّدة. والتطبيقات ليست استثناءً: تطبيقات مفيدة كثيرة تطلب اشتراكًا يتراكم مع السنين حتى يبلغ أضعاف قيمتها الحقيقية.")}
  {p("So we started Q Apps: apps at a small one-time price, with lifetime access and plenty of real benefit. You may find similar apps that charge many times more through a monthly or yearly subscription — ours you buy once.",
     "فأطلقنا كيو آبز: تطبيقات بسعر زهيد تدفعه مرّة واحدة، مع وصول مدى الحياة وفوائد حقيقية كثيرة. قد تجد أحيانًا تطبيقات مشابهة تدفع فيها أضعاف ذلك باشتراك شهري أو سنوي — أمّا تطبيقاتنا فتشتريها مرّة واحدة.")}
  {h(2, "Built with your ideas", "نبنيها بأفكارك")}
  {p('We welcome your opinions, suggestions and the features you wish our apps had. When we find a good opportunity to build a suggestion, we add it for everyone at no extra cost. <a href="/suggest/">Suggest a feature</a>.',
     'نرحّب بآرائك واقتراحاتك والميزات التي تتمنّاها في تطبيقاتنا. وإذا وجدنا فرصة مناسبة لتنفيذ اقتراح، أضفناه للجميع دون أي تكلفة إضافية. <a href="/suggest/">اقترح ميزة</a>.')}
  <p class="fineprint" data-en>“Lifetime” means you pay once and keep using the app you bought, with no renewal fees, for as long as the app is offered on the App Store or Google Play. Suggestions are welcome, but we cannot promise to build every one or to build it by a certain date.</p>
  <p class="fineprint" data-ar>«مدى الحياة» تعني أنك تدفع مرّة واحدة وتستمرّ في استخدام التطبيق الذي اشتريته دون رسوم تجديد، طالما كان التطبيق متاحًا على App Store أو Google Play. نرحّب بكل الاقتراحات، لكننا لا نتعهّد بتنفيذ كل اقتراح ولا بموعد محدّد لتنفيذه.</p>
  {h(2, "What we believe", "بماذا نؤمن")}
  <div class="features" style="margin-top:20px">
    {feature("💸","Fair prices","سعر عادل","A small price you pay once. No subscriptions and no surprise charges.","سعر زهيد تدفعه مرّة واحدة. بلا اشتراكات ولا رسوم مفاجئة.")}
    {feature("🔒","Privacy by default","الخصوصية افتراضيًا","Your data belongs to you and stays on your device. No ads, no analytics, no tracking.","بياناتك مِلكك وتبقى على جهازك. بلا إعلانات ولا تحليلات ولا تتبّع.")}
    {feature("💬","Your voice counts","صوتك مسموع","We read every suggestion, and the good ones become features for everyone.","نقرأ كل اقتراح، والجيّد منها يصبح ميزة للجميع.")}
    {feature("✨","Simplicity","البساطة","We remove everything that gets in the way, so each app does its job quickly.","نزيل كل ما يعترض الطريق، ليؤدّي كل تطبيق مهمّته بسرعة.")}
    {feature("🌍","Arabic &amp; English","العربية والإنجليزية","First-class Arabic with proper right-to-left layout, alongside English.","لغة عربية من الطراز الأول مع تخطيط سليم من اليمين إلى اليسار، إلى جانب الإنجليزية.")}
    {feature("🛠️","Craftsmanship","الإتقان","Careful engineering and attention to the details that make apps reliable.","هندسة دقيقة واهتمام بالتفاصيل التي تجعل التطبيقات موثوقة.")}
  </div>
  {h(2, "Our apps", "تطبيقاتنا")}
  {p("Vault — Warranty Manager and Countdown Keeper are available now, and DocMatic is on the way.",
     "خزنة الضمانات و«كم مضى وكم بقي» متاحان الآن، وDocMatic قريبًا.")}
  <p><a class="btn btn-primary" href="/apps/"><span data-en>See our apps</span><span data-ar>شاهد تطبيقاتنا</span></a></p>
  {h(2, "Get in touch", "تواصل معنا")}
  {p(f'For anything at all, email <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.',
     f'لأي أمر، راسلنا على <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>.')}
</div></section>{_about_moved()}'''
    return render("/about/",
                  "About — Q Apps",
                  "من نحن — كيو آبز",
                  "Q Apps makes valuable apps at tiny prices: pay once, yours for life — no subscriptions. In Arabic and English.",
                  "كيو آبز تصنع تطبيقات قيّمة بأسعار زهيدة: ادفع مرّة ولك مدى الحياة — بلا اشتراكات. بالعربية والإنجليزية.",
                  body, active="about")


def page_suggest():
    """/suggest/ — «Contact & suggest» (proposal proposals/qapps_feedback_proposal_ar.html,
    approved 2026-11-01): which app, four message types, and «Send» to the
    site's own database (functions/api/feedback.js) behind Turnstile and rate
    limits. WhatsApp/email remain as a fallback if the system is unavailable.
    ?app=<slug> pre-selects the app (links from each app page)."""
    apps = [("docmatic", "DocMatic", "DocMatic"),
            ("vault", "Vault — Warranty Manager", "خزنة الضمانات"),
            ("countdown-keeper", "Countdown Keeper", "كم مضى وكم بقي"),
            ("new-app", "An idea for a new app", "فكرة لتطبيق جديد"),
            ("general", "The website / in general", "الموقع / رأي عام")]
    options = "".join(
        f'<option value="{k}" data-en="{esc(en)}" data-ar="{esc(ar)}">{esc(en)} — {esc(ar)}</option>'
        for k, en, ar in apps)
    types = [
        ("message", "💬", "Message or question", "رسالة أو سؤال",
         "Write your message", "اكتب رسالتك",
         "Hello, is it possible to…", "السلام عليكم، هل يمكن…"),
        ("improve", "💡", "Improvement", "اقتراح تحسين",
         "What could be better? And how?", "ما الذي تراه يكون أفضل؟ وكيف؟",
         "It would be better if…", "سيكون أفضل لو…"),
        ("feature", "🚀", "New feature idea", "فكرة ميزة جديدة",
         "Which feature do you wish for? And why do you need it?", "ما الميزة التي تتمنّاها؟ ولماذا تحتاجها؟",
         "I wish I could… because…", "أتمنى أن أستطيع… لأن…"),
        ("problem", "🐞", "A problem I had", "مشكلة واجهتني",
         "What did you do? What happened? What did you expect?", "ماذا فعلت؟ وماذا حدث؟ وماذا كنت تتوقع؟",
         "I tapped… then… and I expected…", "ضغطت… ثم حدث… وكنت أتوقع…"),
    ]
    type_html = "".join(
        f'<label class="fb-type"><input type="radio" name="type" value="{k}"{" checked" if k == "feature" else ""} '
        f'data-label-en="{esc(en)}" data-label-ar="{esc(ar)}" data-q-en="{esc(qen)}" data-q-ar="{esc(qar)}" '
        f'data-ph-en="{esc(phen)}" data-ph-ar="{esc(phar)}">'
        f'<span><i aria-hidden="true">{ic}</i><span data-en>{en}</span><span data-ar>{ar}</span></span></label>'
        for k, ic, en, ar, qen, qar, phen, phar in types)
    turnstile = (f'<div class="cf-turnstile" data-sitekey="{TURNSTILE_SITE_KEY}" data-theme="auto" '
                 f'data-language="auto" data-size="flexible"></div>') if TURNSTILE_SITE_KEY else ""
    body = f'''{crumbs([("Home","الرئيسية","/"),("Contact & suggest","تواصل واقترح",None)])}
<section class="section"><div class="container prose">
  {h(1, "Contact &amp; suggest", "تواصل واقترح")}
  {p("Send us a message, an improvement, an idea for a new feature, or a problem you ran into. We read every message ourselves. When we find a good opportunity to build your idea, we add it for everyone — at no extra cost to you.",
     "أرسل لنا رسالة، أو اقتراح تحسين، أو فكرة ميزة جديدة، أو مشكلة واجهتك. نقرأ كل رسالة بأنفسنا، وإذا وجدنا فرصة مناسبة لتنفيذ فكرتك أضفناها للجميع — دون أي تكلفة إضافية عليك.", "lead")}
  <form class="card suggest-form fb-form" data-fb-form data-sitekey="{TURNSTILE_SITE_KEY}" data-email="{SUPPORT_EMAIL}" data-wa="{WHATSAPP_NUMBER}" novalidate>
    <label><span class="lbl"><span data-en>Which app?</span><span data-ar>عن أي تطبيق؟</span></span>
      <select name="app">{options}</select></label>
    <fieldset class="fb-types"><legend class="lbl"><span data-en>What would you like to send?</span><span data-ar>ماذا تريد أن ترسل؟</span></legend>{type_html}</fieldset>
    <label><span class="lbl" data-fb-question></span>
      <textarea name="message" rows="6" maxlength="2000" required></textarea></label>
    <div class="fb-two">
      <label><span class="lbl"><span data-en>Your name (optional)</span><span data-ar>اسمك (اختياري)</span></span>
        <input name="name" type="text" maxlength="80" autocomplete="name"></label>
      <label><span class="lbl"><span data-en>How can we reply? (optional: email or number)</span><span data-ar>كيف نرد عليك؟ (اختياري: بريد أو رقم)</span></span>
        <input name="contact" type="text" maxlength="120" autocomplete="email"></label>
    </div>
    <label class="fb-hp" aria-hidden="true">Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
    {turnstile}
    <p class="fb-status" data-fb-status role="status" hidden></p>
    <div class="btn-row"><button class="btn btn-accent" type="submit" data-fb-submit><span data-en>Send</span><span data-ar>أرسل</span></button></div>
    <div class="fb-fallback" data-fb-fallback hidden>
      <button class="btn btn-secondary" type="button" data-fb-wa><span data-en>Send on WhatsApp</span><span data-ar>أرسل عبر واتساب</span></button>
      <button class="btn btn-secondary" type="button" data-fb-mail><span data-en>Send by email</span><span data-ar>أرسل بالبريد</span></button>
    </div>
    <p class="fineprint" data-en>No files or pictures. We keep your message, and your name and contact only if you write them, to read and answer it — nothing else. See <a href="/privacy/#messages">Privacy</a>.</p>
    <p class="fineprint" data-ar>لا ملفات ولا صور. نحفظ رسالتك، واسمك وطريقة التواصل إن كتبتهما، لنقرأها ونرد عليها فقط. انظر <a href="/privacy/#messages">الخصوصية</a>.</p>
  </form>
  <div class="card fb-sent" data-fb-sent hidden>
    <div class="fb-sent-icon" aria-hidden="true">🙏</div>
    {h(2, "Thank you — we got your message", "شكرًا لك، وصلتنا رسالتك")}
    {p("We read every message ourselves. If we find a good opportunity to build your idea, we add it for everyone in an update — at no extra cost.",
       "نقرأ كل رسالة بأنفسنا. وإذا وجدنا فرصة مناسبة لتنفيذ فكرتك أضفناها للجميع في تحديث — دون أي رسوم إضافية.")}
    {p("If you left a way to reach you, we will let you know when your idea is in the app.",
       "إن تركت طريقة للتواصل، نخبرك حين تصبح فكرتك في التطبيق.", "fineprint")}
    <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/" data-fb-back><span data-en>Back to the home page</span><span data-ar>عُد إلى الصفحة الرئيسية</span></a></div>
  </div>
  {h(2, "How we handle your messages", "كيف نتعامل مع رسائلك")}
  {ul([("We read every message.", "نقرأ كل رسالة."),
       ("We pick the ideas that help the most people and fit the app.", "نختار الأفكار التي تفيد أكبر عدد من المستخدمين وتناسب التطبيق."),
       ("If we build your suggestion, it reaches everyone in an update — no extra charge.", "إذا نفّذنا اقتراحك، يصل للجميع في تحديث — دون أي رسوم إضافية.")])}
  <p class="fineprint" data-en>We welcome every suggestion, but we cannot promise to build each one or to build it by a certain date.</p>
  <p class="fineprint" data-ar>نرحّب بكل اقتراح، لكننا لا نتعهّد بتنفيذ كل اقتراح ولا بموعد محدّد لتنفيذه.</p>
</div></section>'''
    head = (f"<style>{FB_CSS}</style>\n"
            + ('<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>\n' if TURNSTILE_SITE_KEY else "")
            + f'<script src="/assets/js/suggest.js?v={asset_ver("assets/js/suggest.js")}" defer></script>')
    return render("/suggest/",
                  "Contact & suggest — Q Apps",
                  "تواصل واقترح — كيو آبز",
                  "Send Q Apps a message, an improvement, a new feature idea or a problem you ran into. We read every message, and add good ideas for everyone at no extra cost.",
                  "أرسل إلى كيو آبز رسالة أو اقتراح تحسين أو فكرة ميزة أو مشكلة واجهتك. نقرأ كل رسالة، ونضيف الأفكار المناسبة للجميع دون أي تكلفة إضافية.",
                  body, active="suggest", head_extra=head)


# Page-only styles for /suggest/ (kept out of the shared stylesheet).
FB_CSS = """
.fb-form{display:grid;gap:18px}
.fb-form[hidden],.fb-sent[hidden],.fb-fallback[hidden],.fb-status[hidden]{display:none!important}
.fb-types{border:0;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:10px}
.fb-types legend{width:100%;margin-bottom:8px}
.fb-type{cursor:pointer;position:relative;display:inline-block}
.fb-type input{position:absolute;top:0;inset-inline-start:0;width:1px!important;height:1px!important;margin:0;padding:0;opacity:0;pointer-events:none}
.fb-type>span{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--line);background:var(--surface);border-radius:999px;padding:8px 16px;font-weight:650;color:var(--ink);transition:background .15s,border-color .15s}
.fb-type i{font-style:normal}
.fb-type input:checked+span{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.fb-type input:focus-visible+span{outline:2.5px solid var(--accent);outline-offset:3px}
.fb-two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:640px){.fb-two{grid-template-columns:1fr}}
.fb-hp{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
.fb-form{position:relative}
.fb-status{margin:0;padding:10px 14px;border-radius:12px;background:var(--soft);color:var(--ink);font-weight:600}
.fb-status.err{background:#FDECEA;color:#8A1C14}
.fb-status.warn{background:#FFF4DC;color:#6B4A00}
.fb-fallback{display:flex;flex-wrap:wrap;gap:10px}
.fb-sent{text-align:center;display:grid;gap:12px;justify-items:center;padding:36px 24px}
.fb-sent-icon{width:84px;height:84px;border-radius:50%;background:var(--mint-soft);display:grid;place-items:center;font-size:40px}
"""


def page_404():
    body = f'''<div class="center-screen">
  <div>
    {qmark(size=96)}
    {h(1, "Page not found", "الصفحة غير موجودة")}
    {p("The page you were looking for doesn't exist or has moved.", "الصفحة التي تبحث عنها غير موجودة أو تم نقلها.", "lead")}
    <div class="btn-row" style="justify-content:center;margin-top:20px">
      <a class="btn btn-primary" href="/"><span data-en>Go home</span><span data-ar>العودة للرئيسية</span></a>
      <a class="btn btn-ghost" href="/apps/"><span data-en>Browse apps</span><span data-ar>تصفّح التطبيقات</span></a>
    </div>
  </div>
</div>'''
    return render("/404", "Page not found — Q Apps",
                  "الصفحة غير موجودة — كيو آبز",
                  "The page you were looking for doesn't exist or has moved.",
                  "الصفحة التي تبحث عنها غير موجودة أو تم نقلها.",
                  body, is404=True)


# ---------------------------- sitemap & robots -----------------------------

def write_sitemap(urls):
    lastmod = "2026-09-02"
    items = "".join(
        f"  <url><loc>{u}</loc><lastmod>{lastmod}</lastmod></url>\n" for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{items}</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def write_robots():
    txt = ("User-agent: *\n"
           "Allow: /\n"
           "Disallow: /admin/\n"
           "Disallow: /api/\n\n"
           f"Sitemap: {SITE_URL}/sitemap.xml\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def write_manifest():
    import json
    manifest = {
        "name": "Q Apps",
        "short_name": "Q Apps",
        "start_url": "/",
        "display": "browser",
        "background_color": "#F3F5F7",
        "theme_color": THEME_COLOR,
        "icons": [
            {"src": "/assets/img/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/img/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def page_vault_redirect():
    """/vault/ now serves the FULL campaign page (same as /vault-new/).

    Was a client-side redirect to the Apps Script web app (VAULT_TARGET, kept
    above for reference/rollback); cut over on 2026-09-11 so visitors stay on
    our own domain — no Google "created by an Apps Script user" banner. All
    previously distributed /vault?utm_source=... links keep working unchanged.
    Rollback = git revert of this cutover commit + rebuild."""
    html = _VAULTNEW_HTML.replace("__API_BASE__", VAULTNEW_API_BASE)
    out_dir = os.path.join(ROOT, "vault")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def page_vaultnew():
    """Full Vault campaign UI at /vault-new/, hosted on our own domain.

    Ported from the Apps Script Index.html, with TWO changes:
      1. utm_source is parsed CLIENT-SIDE from the URL (normalized to match the
         backend's normalizeSource_), replacing the old server '<?= source ?>'.
      2. The two google.script.run calls (which only work inside Apps-Script HTML)
         become JSONP calls to VAULTNEW_EXEC_URL — no CORS issues, no Google banner.
    Marked noindex and kept out of the sitemap while it's the staging route."""
    html = _VAULTNEW_HTML.replace("__API_BASE__", VAULTNEW_API_BASE)
    out_dir = os.path.join(ROOT, "vault-new")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    urls = []
    urls.append(render_home_and_collect())
    for fn in (page_apps, page_app_countdown, page_app_vault, page_app_docmatic,
               page_tutorials, page_tutorial_countdown, page_tutorial_vault,
               page_privacy_index,
               page_support_index, page_support_countdown, page_support_vault,
               page_contact, page_about, page_suggest):
        urls.append(fn())
    # Localized privacy policies (one direct URL per language, per app).
    priv_count = 0
    for slug in APPS:
        localized = gen_privacy(slug)   # also writes the /privacy/<slug>/ entry
        urls.extend(localized)          # /privacy/<slug>/<lang>/ in sitemap
        priv_count += len(localized)
    page_vault_redirect()  # branded /vault redirect, not in sitemap
    page_vaultnew()  # v2 campaign frontend (staging), not in sitemap
    page_404()  # not in sitemap
    write_sitemap([u for u in urls if u])
    write_robots()
    write_manifest()
    print(f"Built {len(urls)} sitemap URLs ({priv_count} localized privacy pages) + 404, sitemap, robots, manifest.")


def render_home_and_collect():
    body = page_home()
    return render("/",
                  "Q Apps — Valuable apps at tiny prices, yours for life",
                  "كيو آبز — تطبيقات قيّمة بأسعار زهيدة، لك مدى الحياة",
                  "Q Apps makes useful mobile apps you buy once at a small price and keep for life — no monthly or yearly subscriptions. In Arabic and English.",
                  "كيو آبز تصنع تطبيقات جوّال مفيدة تشتريها مرّة واحدة بسعر زهيد وتبقى لك مدى الحياة — بلا اشتراكات شهرية أو سنوية. بالعربية والإنجليزية.",
                  body, active="home")


if __name__ == "__main__":
    main()
