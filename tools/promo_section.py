"""The «free full version» section at the bottom of an app page, plus the small
badge in the hero that jumps to it (proposal qapps_free_codes, decision أ).

The markup ships hidden; /assets/js/promo.js asks /api/promo/status?app=<slug>
and shows it only while the offer is on (switched on in /admin/promo/, end
date not passed). No code is ever in the page: a Google Play code is fetched
from /api/promo/claim only when the visitor taps «Get your offer code».
"""


def two(en, ar, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-en>{en}</{tag}><{tag}{c} data-ar>{ar}</{tag}>'


def badge():
    return ('<a class="pf-badge" href="#free" data-pf-badge hidden>'
            + two("🎁 Full version free for a limited time ↓", "🎁 النسخة الكاملة مجانًا لفترة محدودة ↓")
            + "</a>")


def section(slug, apple_store, play_store, after_en, after_ar, turnstile_key, js_src):
    return f'''<section id="free" class="pf-wrap" data-promo-app="{slug}" data-sitekey="{turnstile_key}" hidden><div class="container">
<div class="pf">
  <div class="pf-head">
    <span class="pf-gift" aria-hidden="true">🎁</span>
    <div>
      {two("The full version free, for life", "النسخة الكاملة مجانًا مدى الحياة", "h2")}
      <p>{two("Limited number, for a limited time. Download first, then activate the offer.", "العدد محدود والمدة محدودة. نزّل التطبيق أولًا، ثم فعّل العرض.")}
      <b class="pf-left" data-pf-left hidden></b></p>
    </div>
  </div>
  <div class="pf-grid" data-pf-grid>
    <div class="pf-card" data-pf-apple hidden>
      {two("🍎 iPhone &amp; iPad", "🍎 آيفون وآيباد", "h3")}
      <a class="pf-btn pf-btn-2" href="{apple_store}" target="_blank" rel="noopener" data-pf-kind="download" data-pf-platform="ios">
        <i>1</i>{two("Download from the App Store", "نزّل من App Store")}</a>
      <a class="pf-btn pf-btn-1" href="#" target="_blank" rel="noopener" data-pf-kind="redeem" data-pf-platform="ios" data-pf-apple-redeem>
        <i>2</i>{two("Activate the free offer", "فعّل العرض المجاني")}</a>
      <p class="pf-note">{two("Step 2 opens the App Store with the offer code already filled in.", "الخطوة 2 تفتح App Store وكود العرض مكتوب فيه.")}</p>
    </div>
    <div class="pf-card" data-pf-android hidden>
      {two("🤖 Android", "🤖 أندرويد", "h3")}
      <div data-pf-state="intro">
        <a class="pf-btn pf-btn-2" href="{play_store}" target="_blank" rel="noopener" data-pf-kind="download" data-pf-platform="android">
          <i>1</i>{two("Download from Google Play", "نزّل من Google Play")}</a>
        <button type="button" class="pf-btn pf-btn-1" data-pf-claim>
          <i>2</i>{two("Get your offer code", "احصل على كود العرض")}</button>
        <p class="pf-note">{two("One code for you, used once.", "كود واحد لك، يُستخدم مرة واحدة.")}</p>
      </div>
      <div data-pf-state="code" hidden>
        <p class="pf-note">{two("Your offer code:", "كود العرض الخاص بك:")}</p>
        <div class="pf-code" data-pf-code dir="ltr"></div>
        <a class="pf-btn pf-btn-1" href="#" target="_blank" rel="noopener" data-pf-kind="redeem" data-pf-platform="android" data-pf-play-redeem>
          {two("Activate the code in Google Play ›", "فعّل الكود في Google Play ›")}</a>
        <button type="button" class="pf-btn pf-btn-2" data-pf-copy>{two("Copy the code", "انسخ الكود")}</button>
        <p class="pf-note" data-pf-copied hidden>{two("Copied ✓", "تم النسخ ✓")}</p>
      </div>
      <div data-pf-state="empty" hidden>
        <p class="pf-msg">💛 {two("The free codes have all been taken.", "نفدت الأكواد المجانية لاكتمال العدد.")}</p>
        <a class="pf-btn pf-btn-2" href="{play_store}" target="_blank" rel="noopener" data-pf-kind="download" data-pf-platform="android">{two("Download from Google Play", "حمّل من Google Play")}</a>
      </div>
      <div data-pf-state="limit" hidden>
        <p class="pf-msg">{two("Codes from this connection have reached today's limit. Please try again tomorrow.", "وصلت الأكواد من هذه الشبكة إلى حدّ اليوم. حاول مرة أخرى غدًا.")}</p>
      </div>
      <div data-pf-state="error" hidden>
        <p class="pf-msg">{two("We could not get a code. Please try again.", "تعذّر الحصول على الكود. حاول مرة أخرى.")}</p>
        <button type="button" class="pf-btn pf-btn-2" data-pf-retry>{two("Try again", "أعد المحاولة")}</button>
      </div>
      <div class="pf-ts" data-pf-ts></div>
    </div>
  </div>
  <p class="pf-fine">{two(after_en, after_ar)}
    <a href="/privacy/#free">{two("What we keep", "ماذا نحفظ")}</a></p>
</div>
</div></section>
<script src="{js_src}" defer></script>'''


CSS = """
.pf-wrap[hidden],.pf-wrap [hidden],.pf-badge[hidden]{display:none!important}
.pf-badge{display:inline-flex;align-items:center;gap:6px;background:var(--accent-soft);color:var(--ink);border:1.5px dashed var(--accent);border-radius:999px;padding:6px 14px;font-weight:700;font-size:14.5px;text-decoration:none;width:max-content;max-width:100%}
.pf-badge:hover{color:var(--ink);text-decoration:none;transform:translateY(-1px)}
.pf-wrap{padding-top:0}
.pf{background:var(--night);color:var(--on-night);border-radius:var(--radius);padding:36px;display:grid;gap:22px}
.pf-head{display:flex;gap:16px;align-items:flex-start}
.pf-gift{font-size:44px;line-height:1}
.pf h2{color:#fff;font-size:clamp(26px,3.4vw,40px);margin:0 0 6px}
.pf-head p{color:var(--on-night-muted);margin:0;font-size:17px}
.pf-left{display:inline-block;margin-inline-start:8px;background:var(--accent);color:var(--accent-ink);border-radius:999px;padding:0 10px;font-size:14px}
.pf-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.pf-card{background:var(--night-2);border:1px solid rgba(255,255,255,.08);border-radius:var(--radius-sm);padding:20px;display:grid;gap:10px;align-content:start}
.pf-card h3{color:#fff;font-size:19px;margin:0 0 4px}
.pf-card [data-pf-state]{display:grid;gap:10px}
.pf-card [data-pf-state][hidden]{display:none}
.pf-btn{display:flex;align-items:center;justify-content:center;gap:10px;border-radius:14px;padding:13px 16px;font:inherit;font-weight:700;font-size:16px;text-decoration:none;cursor:pointer;border:1.5px solid transparent;transition:transform .2s;width:100%}
.pf-btn:hover{transform:translateY(-1px);text-decoration:none}
.pf-btn i{font-style:normal;display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;font-size:13px;background:rgba(0,0,0,.18)}
.pf-btn-1{background:var(--accent);color:var(--accent-ink)}
.pf-btn-1:hover{color:var(--accent-ink)}
.pf-btn-2{background:transparent;color:#fff;border-color:rgba(255,255,255,.35)}
.pf-btn-2:hover{color:#fff;border-color:#fff}
.pf-btn[disabled]{opacity:.6;cursor:wait}
.pf-note{color:var(--on-night-muted);font-size:14px;margin:0}
.pf-msg{color:#fff;margin:0}
.pf-code{border:2px dashed var(--accent);border-radius:14px;text-align:center;font-family:var(--f-mono);font-size:clamp(16px,4.6vw,22px);font-weight:700;letter-spacing:1px;padding:12px 8px;color:#fff;word-break:break-all;user-select:all}
.pf-fine{color:var(--on-night-muted);font-size:14px;margin:0}
.pf-fine a{color:var(--on-night);margin-inline-start:6px}
.pf-ts:empty{display:none}
@media (max-width:620px){.pf{padding:22px}.pf-gift{font-size:34px}}
"""
