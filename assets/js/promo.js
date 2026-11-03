/* promo.js — the «free full version» section at the bottom of an app page
   (tools/promo_section.py; proposal qapps_free_codes).
   1. Asks /api/promo/status?app=<slug>; shows the section (and the hero badge)
      only while the offer is on. Fails closed: no answer = stays hidden.
   2. Android: «Get your offer code» → Turnstile (invisible unless needed) →
      /api/promo/claim with a random per-device request id, so the same phone
      always gets the same code back. The code is kept on the device too.
   3. Every tap in the section is one row of the download statistic
      (/api/promo/e), like the store buttons on every page (site.js). */
(function () {
  "use strict";
  var box = document.querySelector("[data-promo-app]");
  if (!box) return;
  var app = box.getAttribute("data-promo-app");
  var siteKey = box.getAttribute("data-sitekey") || "";
  var badge = document.querySelector("[data-pf-badge]");
  var apple = box.querySelector("[data-pf-apple]");
  var android = box.querySelector("[data-pf-android]");
  var PLAY_REDEEM = "https://play.google.com/redeem?code=";
  // Testing: ?promo-reset forgets this device's code (the owner first puts
  // the code back with «↩ إرجاع» in /admin/promo/).
  if (/[?&]promo-reset\b/.test(location.search)) {
    try { localStorage.removeItem("qapps_promo_rid_" + app); localStorage.removeItem("qapps_promo_code_" + app); } catch (e) {}
  }
  var code = "";
  var busy = false;
  var widget = null;

  function lang() { return document.documentElement.getAttribute("data-lang") === "ar" ? "ar" : "en"; }
  function src() { try { return sessionStorage.getItem("qapps_src") || ""; } catch (e) { return ""; } }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  function rid() {
    var k = "qapps_promo_rid_" + app;
    var id = store(k);
    if (id) return id;
    id = (self.crypto && crypto.randomUUID) ? crypto.randomUUID()
      : "r-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 12);
    store(k, id);
    return id;
  }

  function beat(kind, platform) {
    var body = JSON.stringify({ app: app, kind: kind, platform: platform, page: location.pathname, src: src(), lang: lang() });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon("/api/promo/e", body)) return;
    } catch (e) { /* fall through */ }
    try { fetch("/api/promo/e", { method: "POST", body: body, keepalive: true, headers: { "content-type": "text/plain" } }); } catch (e) {}
  }

  function state(name) {
    android.querySelectorAll("[data-pf-state]").forEach(function (s) { s.hidden = s.getAttribute("data-pf-state") !== name; });
  }

  function showCode(c) {
    code = c;
    box.querySelector("[data-pf-code]").textContent = c;
    box.querySelector("[data-pf-play-redeem]").href = PLAY_REDEEM + encodeURIComponent(c);
    state("code");
  }

  function claimBtn(on) {
    var b = box.querySelector("[data-pf-claim]");
    b.disabled = !on;
  }

  function post(token) {
    fetch("/api/promo/claim", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ app: app, rid: rid(), token: token || "", src: src(), lang: lang(), page: location.pathname }),
      cache: "no-store",
    })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (d) {
        busy = false; claimBtn(true);
        if (d.status === "ok" && d.code) { store("qapps_promo_code_" + app, d.code); showCode(d.code); }
        else if (d.status === "empty" || d.status === "ended") state("empty");
        else if (d.status === "limit") state("limit");
        else state("error");
      })
      .catch(function () { busy = false; claimBtn(true); state("error"); });
  }

  function claim() {
    if (busy) return;
    busy = true; claimBtn(false);
    if (!siteKey || !window.turnstile) return post("");
    var slot = box.querySelector("[data-pf-ts]");
    try {
      if (widget === null) {
        widget = window.turnstile.render(slot, {
          sitekey: siteKey, execution: "execute", appearance: "interaction-only",
          language: lang(), theme: "dark",
          callback: function (t) { post(t); },
          "error-callback": function () { busy = false; claimBtn(true); state("error"); },
          "expired-callback": function () { window.turnstile.reset(widget); },
        });
      } else {
        window.turnstile.reset(widget);
      }
      window.turnstile.execute(widget);
    } catch (e) {
      post("");
    }
  }

  function loadTurnstile() {
    if (!siteKey || window.turnstile) return;
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true;
    document.head.appendChild(s);
  }

  box.addEventListener("click", function (e) {
    var t = e.target.closest("a,button");
    if (!t) return;
    if (t.hasAttribute("data-pf-claim")) { e.preventDefault(); claim(); return; }
    if (t.hasAttribute("data-pf-retry")) { e.preventDefault(); state("intro"); return; }
    if (t.hasAttribute("data-pf-copy")) {
      e.preventDefault();
      beat("copy", "android");
      var ok = function () { var m = box.querySelector("[data-pf-copied]"); m.hidden = false; setTimeout(function () { m.hidden = true; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(code).then(ok, function () {});
      return;
    }
    var kind = t.getAttribute("data-pf-kind");
    if (kind) beat(kind, t.getAttribute("data-pf-platform"));
  });

  fetch("/api/promo/status?app=" + encodeURIComponent(app), { cache: "no-store" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (s) {
      if (!s || !s.ok || !s.active || (!s.apple.on && !s.android.on)) return;
      if (s.apple.on && s.apple.url) {
        box.querySelector("[data-pf-apple-redeem]").href = s.apple.url;
        apple.hidden = false;
      }
      var saved = store("qapps_promo_code_" + app);
      if (s.android.on || saved) {
        android.hidden = false;
        if (saved) showCode(saved);
        else loadTurnstile();
        if (s.android.on) {
          var left = box.querySelector("[data-pf-left]");
          left.innerHTML = '<span data-en>' + s.android.left + ' left for Android</span><span data-ar>باقي ' + s.android.left + ' لأندرويد</span>';
          left.hidden = false;
        }
      }
      // Android visitors see their card first.
      if (/Android/.test(navigator.userAgent || "")) android.parentNode.insertBefore(android, apple);
      box.hidden = false;
      if (badge) badge.hidden = false;
    })
    .catch(function () {});
})();
