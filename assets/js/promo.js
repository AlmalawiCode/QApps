/* promo.js — the «free full version» section at the bottom of an app page
   (tools/promo_section.py; proposal qapps_free_codes).
   1. Asks /api/promo/status?app=<slug>; shows the section (and the hero badge)
      only while the offer is on. Fails closed: no answer = stays hidden.
   2. Android, and Apple when the app has App Store one-time offer codes
      (since 2026-11-14): «Get your offer code» → Turnstile (invisible unless
      needed) → /api/promo/claim with a random per-device request id, so the
      same phone always gets the same code back. The code is kept on the
      device too. Apple without codes: one shared offer link (status.apple.url).
   3. Every tap in the section is one row of the download statistic
      (/api/promo/e), like the store buttons on every page (site.js). */
(function () {
  "use strict";
  var box = document.querySelector("[data-promo-app]");
  if (!box) return;
  var app = box.getAttribute("data-promo-app");
  var siteKey = box.getAttribute("data-sitekey") || "";
  var badge = document.querySelector("[data-pf-badge]");
  var cards = { ios: box.querySelector("[data-pf-apple]"), android: box.querySelector("[data-pf-android]") };
  var REDEEM = { android: "https://play.google.com/redeem?code=", ios: "" };   // ios: from /api/promo/status
  // Android keeps its original storage key (codes given before iOS existed).
  function codeKey(p) { return "qapps_promo_code_" + (p === "ios" ? "ios_" : "") + app; }
  // Testing: ?promo-reset forgets this device's codes (the owner first puts
  // the code back with «↩ إرجاع» in /admin/promo/).
  if (/[?&]promo-reset\b/.test(location.search)) {
    try {
      localStorage.removeItem("qapps_promo_rid_" + app);
      localStorage.removeItem(codeKey("android"));
      localStorage.removeItem(codeKey("ios"));
    } catch (e) {}
  }
  var code = { ios: "", android: "" };
  var busy = { ios: false, android: false };
  var widget = { ios: null, android: null };

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

  function state(p, name) {
    cards[p].querySelectorAll("[data-pf-state]").forEach(function (s) { s.hidden = s.getAttribute("data-pf-state") !== name; });
  }

  function showCode(p, c) {
    code[p] = c;
    cards[p].querySelector("[data-pf-code]").textContent = c;
    var r = cards[p].querySelector("[data-pf-redeem]");
    if (REDEEM[p]) r.href = REDEEM[p] + encodeURIComponent(c);
    else r.hidden = true;   // no redeem link known: copy the code instead
    state(p, "code");
  }

  function claimBtn(p, on) {
    cards[p].querySelector("[data-pf-claim]").disabled = !on;
  }

  function post(p, token) {
    fetch("/api/promo/claim", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ app: app, platform: p, rid: rid(), token: token || "", src: src(), lang: lang(), page: location.pathname }),
      cache: "no-store",
    })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (d) {
        busy[p] = false; claimBtn(p, true);
        if (d.status === "ok" && d.code) { store(codeKey(p), d.code); showCode(p, d.code); }
        else if (d.status === "empty" || d.status === "ended") state(p, "empty");
        else if (d.status === "limit") state(p, "limit");
        else state(p, "error");
      })
      .catch(function () { busy[p] = false; claimBtn(p, true); state(p, "error"); });
  }

  function claim(p) {
    if (busy[p]) return;
    busy[p] = true; claimBtn(p, false);
    if (!siteKey || !window.turnstile) return post(p, "");
    var slot = cards[p].querySelector("[data-pf-ts]");
    try {
      if (widget[p] === null) {
        widget[p] = window.turnstile.render(slot, {
          sitekey: siteKey, execution: "execute", appearance: "interaction-only",
          language: lang(), theme: "dark",
          callback: function (t) { post(p, t); },
          "error-callback": function () { busy[p] = false; claimBtn(p, true); state(p, "error"); },
          "expired-callback": function () { window.turnstile.reset(widget[p]); },
        });
      } else {
        window.turnstile.reset(widget[p]);
      }
      window.turnstile.execute(widget[p]);
    } catch (e) {
      post(p, "");
    }
  }

  function loadTurnstile() {
    if (!siteKey || window.turnstile || document.querySelector("script[data-pf-turnstile]")) return;
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true;
    s.setAttribute("data-pf-turnstile", "");
    document.head.appendChild(s);
  }

  function platformOf(el) { return cards.ios && cards.ios.contains(el) ? "ios" : "android"; }

  box.addEventListener("click", function (e) {
    var t = e.target.closest("a,button");
    if (!t) return;
    var p = platformOf(t);
    if (t.hasAttribute("data-pf-claim")) { e.preventDefault(); claim(p); return; }
    if (t.hasAttribute("data-pf-retry")) { e.preventDefault(); state(p, "intro"); return; }
    if (t.hasAttribute("data-pf-copy")) {
      e.preventDefault();
      beat("copy", p);
      var ok = function () { var m = cards[p].querySelector("[data-pf-copied]"); m.hidden = false; setTimeout(function () { m.hidden = true; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(code[p]).then(ok, function () {});
      return;
    }
    var kind = t.getAttribute("data-pf-kind");
    if (kind) beat(kind, t.getAttribute("data-pf-platform"));
  });

  function leftBadge(p, n) {
    var el = box.querySelector("[data-pf-left]");
    var en = p === "ios" ? " left for iPhone" : " left for Android";
    var ar = p === "ios" ? "لآيفون" : "لأندرويد";
    el.insertAdjacentHTML("beforeend", (el.innerHTML ? " · " : "") +
      '<span data-en>' + n + en + '</span><span data-ar>باقي ' + n + ' ' + ar + '</span>');
    el.hidden = false;
  }

  // A card that hands out codes: the saved code, or the claim button.
  function codeCard(p, on, left, end) {
    var saved = store(codeKey(p));
    // A saved code past the store's expiry no longer works: do not show it.
    if (saved && end && new Date(end) <= new Date()) saved = null;
    if (!on && !saved) return false;
    cards[p].hidden = false;
    if (saved) showCode(p, saved);
    else { state(p, "intro"); loadTurnstile(); }
    if (on) leftBadge(p, left);
    return true;
  }

  fetch("/api/promo/status?app=" + encodeURIComponent(app), { cache: "no-store" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (s) {
      if (!s || !s.ok || !s.active) return;
      var shown = false;
      if (s.apple && s.apple.redeem) REDEEM.ios = s.apple.redeem;
      if (s.apple && (s.apple.codes || s.apple.total)) {
        shown = codeCard("ios", !!s.apple.codes, s.apple.left, s.apple.codes_end) || shown;
      } else if (s.apple && s.apple.on && s.apple.url) {
        cards.ios.querySelector("[data-pf-apple-redeem]").href = s.apple.url;
        state("ios", "link");
        cards.ios.hidden = false;
        shown = true;
      }
      shown = codeCard("android", !!(s.android && s.android.on), s.android && s.android.left) || shown;
      if (!shown) return;
      // Android visitors see their card first.
      if (/Android/.test(navigator.userAgent || "")) cards.android.parentNode.insertBefore(cards.android, cards.ios);
      box.hidden = false;
      if (badge) badge.hidden = false;
    })
    .catch(function () {});
})();
