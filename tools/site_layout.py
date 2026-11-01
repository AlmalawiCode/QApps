"""site_layout.py — the shared pieces of the reorganized site (approved proposal
proposals/qapps_site_redesign_proposal_ar.html, 2026-11-02).

Why: the owner found the site confusing ("I can't even tell how many apps there
are"). The home page and /apps/ now show the apps as one grid of large icons
(decisions أ, ب, و), and every app page uses the same section bar and the same
help block (decision د). Kept in its own module so build.py and the three app
page modules only call into it.
"""

# Order of the apps everywhere (home grid, /apps/, footer).
APP_ORDER = ["docmatic", "vault", "countdown-keeper"]

# One short line under each icon (the long taglines are too long for a tile).
SHORT = {
    "docmatic": ("Photos to PDF · edit &amp; sign", "الصور إلى PDF · تحرير وتوقيع"),
    "vault": ("Invoices &amp; warranties in one place", "فواتيرك وضماناتك في مكان واحد"),
    "countdown-keeper": ("Live counters for your important dates", "عدّادات لتواريخك المهمة"),
}


def _two(en, ar, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-en>{en}</{tag}><{tag}{c} data-ar>{ar}</{tag}>'


def count_label(n):
    """«3 apps» / Arabic number agreement (1, 2, 3–10, 11+)."""
    if n == 1:
        ar = "تطبيق واحد"
    elif n == 2:
        ar = "تطبيقان"
    elif n <= 10:
        ar = f"{n} تطبيقات"
    else:
        ar = f"{n} تطبيقًا"
    return _two(f"{n} app{'s' if n != 1 else ''}", ar)


def icon_grid(apps, heading=True, h_tag="h2"):
    """The grid of app icons + the dotted «your next app?» tile (decision ب)."""
    tiles = []
    for slug in APP_ORDER:
        app = apps[slug]
        live = app["status"] == "live"
        badge = (f'<span class="badge badge-live">{_two("Available", "متوفر")}</span>' if live else
                 f'<span class="badge badge-soon">{_two("Coming soon", "قريبًا")}</span>')
        s_en, s_ar = SHORT.get(slug, (app["tagline_en"], app["tagline_ar"]))
        tiles.append(f'''<a class="qa-app" href="/apps/{slug}/">
    <img src="{app['icon']}" alt="" width="96" height="96" loading="eager">
    {_two(app['name_en'], app['name_ar'], 'b')}
    {_two(s_en, s_ar, 'small')}
    {badge}
  </a>''')
    tiles.append(f'''<a class="qa-app qa-next" href="/suggest/?app=new-app">
    <span class="qa-plus" aria-hidden="true">+</span>
    {_two("Your next app?", "تطبيقك القادم؟", 'b')}
    {_two("Suggest an idea", "اقترح فكرة", 'small')}
  </a>''')
    head = ""
    if heading:
        head = (f'<div class="qa-grid-head"><{h_tag}>{_two("Our apps", "تطبيقاتنا")}</{h_tag}>'
                f'<span class="qa-count">{count_label(len(APP_ORDER))}</span></div>')
    return f'{head}<div class="qa-grid">{"".join(tiles)}</div>'


def app_tabs(app, has_video=False):
    """The section bar under an app's header (decision د): in-page sections, then
    the app's other pages. Only pages the app really has are shown."""
    slug = app["slug"]
    have = app.get("pages", ["app", "tutorial", "privacy", "support"])
    items = [("#screens", "Screens", "الصور"),
             ("#features", "Features", "المزايا"),
             ("#story", "Story", "القصة")]
    if has_video:
        items.append(("#video", "Video", "الفيديو"))
    items.append(("#questions", "Questions", "أسئلة"))
    if "tutorial" in have:
        items.append((f"/tutorials/{slug}/", "Tutorial", "الشرح"))
    if "privacy" in have:
        items.append((f"/privacy/{slug}/", "Privacy", "الخصوصية"))
    if "support" in have:
        items.append((f"/support/{slug}/", "Support", "الدعم"))
    items.append((f"/suggest/?app={slug}", "Suggest", "اقترح"))
    links = "".join(f'<a href="{u}">{_two(en, ar)}</a>' for u, en, ar in items)
    return (f'<nav class="qa-tabs" aria-label="{app["name_en"]}"><div class="container">'
            f'<div class="qa-tabs-row">{links}</div></div></nav>')


def help_links(app):
    """«Help» cards on every app page: tutorial · privacy · support (only the
    pages the app has). «Suggest» has its own card right after (suggest_card)."""
    slug = app["slug"]
    have = app.get("pages", ["app", "tutorial", "privacy", "support"])
    cards = []
    if "tutorial" in have:
        cards.append((f"/tutorials/{slug}/", "📘", "Tutorial", "الشرح", "Step by step", "خطوة بخطوة"))
    if "privacy" in have:
        cards.append((f"/privacy/{slug}/", "🔒", "Privacy", "الخصوصية", "What happens to your data", "ماذا يحدث لبياناتك"))
    if "support" in have:
        cards.append((f"/support/{slug}/", "🛟", "Support", "الدعم", "Answers and contact", "إجابات وتواصل"))
    html = "".join(
        f'<a class="qa-help-card" href="{u}"><span class="qa-help-ic" aria-hidden="true">{ic}</span>'
        f'{_two(te, ta, "b")}{_two(de, da, "small")}</a>'
        for u, ic, te, ta, de, da in cards)
    return f'''<section class="qa-help"><div class="container">
  <h2 class="qa-help-h">{_two("Help", "مساعدة")}</h2>
  <div class="qa-help-grid">{html}</div>
</div></section>'''


CSS = """
.qa-grid-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:18px}
.qa-grid-head h1,.qa-grid-head h2{margin:0;font-size:clamp(26px,3vw,36px)}
.qa-count{color:var(--muted);font-weight:700;font-size:15px;background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:3px 14px}
.qa-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.qa-app{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;text-decoration:none;color:var(--ink);
  background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:22px 12px 18px;transition:transform .15s,box-shadow .15s}
.qa-app:hover{transform:translateY(-3px);box-shadow:var(--shadow-md)}
.qa-app img{width:96px;height:96px;border-radius:24px;box-shadow:var(--shadow-md);background:#fff;object-fit:cover;margin-bottom:6px}
.qa-app b{font-size:17px;line-height:1.35}
.qa-app small{color:var(--muted);font-size:13.5px;line-height:1.55}
.qa-app .badge{margin-top:4px}
.qa-next{border-style:dashed;background:transparent}
.qa-plus{width:96px;height:96px;border-radius:24px;border:2px dashed var(--line);display:grid;place-items:center;font-size:44px;color:var(--muted);margin-bottom:6px}
.qa-next b{color:var(--muted)}
@media (max-width:760px){.qa-grid{grid-template-columns:repeat(2,1fr);gap:12px}}
@media (max-width:560px){
  .qa-grid{grid-template-columns:repeat(2,1fr);gap:10px}
  .qa-app{padding:16px 8px 14px;border-radius:18px;gap:4px}
  .qa-app img,.qa-plus{width:76px;height:76px;border-radius:19px}
  .qa-plus{font-size:34px}
  .qa-app b{font-size:15px}
  .qa-app small{font-size:12.5px}
  .qa-app .badge{font-size:11.5px;padding:2px 9px}
}
/* home: short intro line above the grid */
.qa-intro{padding:56px 0 18px}
.qa-intro h1{font-size:clamp(32px,4.4vw,54px);line-height:1.15;margin:0 0 12px}
.qa-intro h1 em{font-style:normal;color:var(--accent)}
.qa-intro .lead{max-width:44em;margin:0}
.qa-apps{padding:18px 0 40px}
.qa-quote{padding:8px 0 40px}
.qa-quote .inspire{margin:0;max-width:none}
@media (max-width:720px){.qa-intro{padding:30px 0 8px}}
/* app pages: the section bar */
.qa-tabs{position:sticky;top:71px;z-index:40;background:color-mix(in srgb,var(--bg) 90%,transparent);
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);padding:0}
.qa-tabs-row{display:flex;gap:6px;overflow-x:auto;padding:10px 0;scrollbar-width:none}
.qa-tabs-row::-webkit-scrollbar{display:none}
.qa-tabs-row a{flex:0 0 auto;text-decoration:none;color:var(--ink);font-weight:650;font-size:14.5px;background:var(--surface);
  border:1px solid var(--line);border-radius:999px;padding:5px 14px}
.qa-tabs-row a:hover{border-color:var(--accent);color:var(--accent)}
.qa-tabs + section{padding-top:22px}
[id="screens"],[id="features"],[id="story"],[id="video"],[id="questions"]{scroll-margin-top:140px}
/* app pages: help cards */
.qa-help{padding:40px 0}
.qa-help-h{font-size:clamp(24px,3vw,32px);margin:0 0 16px}
.qa-help-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media (max-width:820px){.qa-help-grid{grid-template-columns:1fr}}
.qa-help-card{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:var(--ink);background:var(--surface);
  border:1px solid var(--line);border-radius:18px;padding:16px 18px;transition:box-shadow .15s}
.qa-help-card:hover{box-shadow:var(--shadow-md)}
.qa-help-ic{font-size:24px;margin-bottom:4px}
.qa-help-card small{color:var(--muted)}
/* footer: copyright line only */
.site-footer-min{padding:22px 0;margin-top:40px}
.site-footer-min .footer-bottom{margin:0;padding:0;border:0;justify-content:center;text-align:center}
"""
