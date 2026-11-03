/* Q Apps — minimal vanilla JS.
   Handles the Arabic/English switch (persisted) and the mobile nav.
   The initial language is applied by a tiny inline script in <head>
   (see the generated pages) so there is no flash of the wrong language. */
(function () {
  "use strict";

  var STORAGE_KEY = "qapps-lang";

  function apply(lang) {
    var html = document.documentElement;
    html.setAttribute("data-lang", lang);
    html.setAttribute("lang", lang);
    html.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    // Update every language button label to show the *other* language.
    var btns = document.querySelectorAll("[data-lang-toggle]");
    for (var i = 0; i < btns.length; i++) {
      btns[i].textContent = lang === "ar" ? "English" : "العربية";
      btns[i].setAttribute(
        "aria-label",
        lang === "ar" ? "Switch to English" : "التبديل إلى العربية"
      );
    }
  }

  function current() {
    return document.documentElement.getAttribute("data-lang") || "en";
  }

  function setLang(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
    apply(lang);
  }

  // "Suggest a feature" form: nothing is sent from the website itself; we
  // open WhatsApp or the visitor's mail app with the message pre-filled.
  function sendSuggestion(btn) {
    var form = btn.closest("[data-suggest]");
    if (!form) return;
    var idea = form.elements.idea.value.trim();
    var err = form.querySelector("[data-suggest-error]");
    if (!idea) {
      if (err) err.hidden = false;
      form.elements.idea.focus();
      return;
    }
    if (err) err.hidden = true;
    var app = form.elements.app.value;
    var name = form.elements.name.value.trim();
    var ar = current() === "ar";
    var text = (ar ? "اقتراح لـ Q Apps" : "Suggestion for Q Apps") + "\n" +
      (ar ? "التطبيق: " : "App: ") + app + "\n\n" + idea +
      (name ? "\n\n" + (ar ? "الاسم: " : "Name: ") + name : "");
    var url;
    if (btn.getAttribute("data-suggest-send") === "wa") {
      url = "https://wa.me/" + form.getAttribute("data-wa") + "?text=" + encodeURIComponent(text);
      window.open(url, "_blank", "noopener");
    } else {
      url = "mailto:" + form.getAttribute("data-email") +
        "?subject=" + encodeURIComponent((ar ? "اقتراح: " : "Suggestion: ") + app) +
        "&body=" + encodeURIComponent(text);
      window.location.href = url;
    }
  }

  // Campaign source (?utm_source=…) for the download statistic, kept for the
  // visit so a tap on a later page still counts for the link that brought you.
  function source() {
    try {
      var m = (location.search || "").match(/[?&]utm_source=([^&#]*)/);
      if (m) sessionStorage.setItem("qapps_src", decodeURIComponent(m[1].replace(/\+/g, " ")).slice(0, 40));
      return sessionStorage.getItem("qapps_src") || "";
    } catch (e) { return ""; }
  }
  source();

  // Download statistic: a tap on an App Store / Google Play button is one row
  // (/api/promo/e — no cookie, no address; see /privacy/#free). A tap is not
  // an install; installs are in the store consoles.
  function countStoreTap(a) {
    var body = JSON.stringify({ href: a.href, kind: "download", page: location.pathname, src: source(), lang: current() });
    try { if (navigator.sendBeacon && navigator.sendBeacon("/api/promo/e", body)) return; } catch (e) {}
    try { fetch("/api/promo/e", { method: "POST", body: body, keepalive: true, headers: { "content-type": "text/plain" } }); } catch (e) {}
  }

  document.addEventListener("DOMContentLoaded", function () {
    // Sync button labels with whatever the head script already applied.
    apply(current());

    document.addEventListener("click", function (e) {
      var toggle = e.target.closest && e.target.closest("[data-lang-toggle]");
      if (toggle) {
        e.preventDefault();
        setLang(current() === "ar" ? "en" : "ar");
        return;
      }
      var storeLink = e.target.closest && e.target.closest("a.store-btn");
      if (storeLink && /apps\.apple\.com|play\.google\.com/.test(storeLink.href)) countStoreTap(storeLink);
      var send = e.target.closest && e.target.closest("[data-suggest-send]");
      if (send) {
        e.preventDefault();
        sendSuggestion(send);
        return;
      }
      var navToggle = e.target.closest && e.target.closest("[data-nav-toggle]");
      if (navToggle) {
        var links = document.getElementById("nav-links");
        if (links) {
          var open = links.classList.toggle("open");
          navToggle.setAttribute("aria-expanded", open ? "true" : "false");
        }
      }
    });
  });
})();
