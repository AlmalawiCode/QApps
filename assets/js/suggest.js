/* suggest.js — the "Contact & suggest" page (/suggest/).
   Sends the visitor's message to /api/feedback (saved in the site's
   database, see functions/api/feedback.js). If the site's system is not set
   up or cannot be reached, the same message can still go by WhatsApp or
   email, so a visitor's idea is never lost.
   ?app=docmatic | vault | countdown-keeper pre-selects the app. */
(function () {
  "use strict";

  var form = document.querySelector("[data-fb-form]");
  if (!form) return;
  var t0 = Date.now();
  var sent = document.querySelector("[data-fb-sent]");
  var fallback = form.querySelector("[data-fb-fallback]");
  var status = form.querySelector("[data-fb-status]");
  var submit = form.querySelector("[data-fb-submit]");
  var siteKey = form.getAttribute("data-sitekey") || "";

  function lang() {
    return document.documentElement.getAttribute("data-lang") === "ar" ? "ar" : "en";
  }
  // On the /<lang>/ pages (French, Urdu, …) the visitor's texts come from
  // window.QAPPS_T (written by tools/site_i18n.py); missing ones stay English.
  function T(en, ar) { return lang() === "ar" ? ar : ((window.QAPPS_T || {})[en] || en); }
  // The message itself goes to the owner: English or Arabic only.
  function TA(en, ar) { return lang() === "ar" ? ar : en; }

  // App from the link. Apps also send their context:
  //   ?app=…&lang=<app language>&src=app&platform=ios|android&v=<version>
  // so a message sent from inside an app is marked (and gets priority).
  var P = new URLSearchParams(location.search);
  var fromApp = P.get("src") === "app";
  var platform = /^(ios|android)$/.test(P.get("platform") || "") ? P.get("platform") : "";
  var appVersion = (P.get("v") || "").replace(/[^0-9A-Za-z.+-]/g, "").slice(0, 20);
  var userLang = /^[a-z]{2}$/.test(P.get("lang") || "") ? P.get("lang") : "";
  var want = P.get("app");
  if (want && form.elements.app.querySelector('option[value="' + want + '"]')) form.elements.app.value = want;

  // The question and hint change with the type.
  var types = form.querySelectorAll('input[name="type"]');
  function updateType() {
    var sel = form.querySelector('input[name="type"]:checked');
    if (!sel) return;
    var l = form.querySelector("[data-fb-question]");
    l.setAttribute("data-q-en", sel.getAttribute("data-q-en"));
    l.setAttribute("data-q-ar", sel.getAttribute("data-q-ar"));
    l.textContent = T(sel.getAttribute("data-q-en"), sel.getAttribute("data-q-ar"));
    form.elements.message.placeholder = T(sel.getAttribute("data-ph-en"), sel.getAttribute("data-ph-ar"));
  }
  types.forEach(function (r) { r.addEventListener("change", updateType); });
  updateType();
  // Follow the language switch.
  new MutationObserver(updateType).observe(document.documentElement, { attributes: true, attributeFilter: ["data-lang"] });

  function show(msg, kind) {
    status.textContent = msg;
    status.className = "fb-status" + (kind ? " " + kind : "");
    status.hidden = !msg;
  }

  function appLabel() {
    var o = form.elements.app.selectedOptions[0];
    return o ? o.getAttribute("data-" + lang()) || o.textContent : "";
  }
  function typeLabel() {
    var sel = form.querySelector('input[name="type"]:checked');
    return sel ? sel.getAttribute("data-label-" + lang()) : "";
  }
  function composed() {
    var name = form.elements.name.value.trim();
    var contact = form.elements.contact.value.trim();
    var tag = fromApp
      ? "📱 " + TA("From the app", "من التطبيق") + (platform ? " · " + platform : "") + (appVersion ? " · " + appVersion : "") + (userLang ? " · " + userLang : "") + "\n"
      : "";
    return tag + "[" + appLabel() + " · " + typeLabel() + "]\n\n" + form.elements.message.value.trim() +
      (name || contact ? "\n\n—" : "") +
      (name ? "\n" + TA("Name: ", "الاسم: ") + name : "") +
      (contact ? "\n" + TA("Reply to: ", "للرد: ") + contact : "");
  }

  function openFallback(reason) {
    fallback.hidden = false;
    show(reason, "warn");
  }
  var waBtn = form.querySelector("[data-fb-wa]");   // absent while WhatsApp is hidden
  if (waBtn) waBtn.addEventListener("click", function () {
    window.open("https://wa.me/" + form.getAttribute("data-wa") + "?text=" + encodeURIComponent(composed()), "_blank", "noopener");
  });
  form.querySelector("[data-fb-mail]").addEventListener("click", function () {
    location.href = "mailto:" + form.getAttribute("data-email") +
      "?subject=" + encodeURIComponent("[" + appLabel() + " · " + typeLabel() + "]") +
      "&body=" + encodeURIComponent(composed());
  });

  function done() {
    var app = form.elements.app.value;
    var back = sent.querySelector("[data-fb-back]");
    if (["docmatic", "vault", "countdown-keeper"].indexOf(app) >= 0) {
      var fixed = document.documentElement.hasAttribute("data-fixed-lang");
      back.href = (fixed ? "/" + document.documentElement.getAttribute("lang") : "") + "/apps/" + app + "/";
      var be = back.querySelector("[data-en]"), ba = back.querySelector("[data-ar]");
      if (be) be.textContent = "Back to " + (form.elements.app.selectedOptions[0].getAttribute("data-en"));
      if (ba) ba.textContent = "عُد إلى صفحة " + (form.elements.app.selectedOptions[0].getAttribute("data-ar"));
      if (fixed) back.textContent = "← " + form.elements.app.selectedOptions[0].textContent;
    }
    form.hidden = true;
    sent.hidden = false;
    sent.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = form.elements.message.value.trim();
    if (text.length < 10) {
      show(T("Please write a little more (at least 10 letters).", "فضلًا اكتب أكثر قليلًا (10 أحرف على الأقل)."), "err");
      form.elements.message.focus();
      return;
    }
    if (!siteKey) {
      openFallback(T("Sending from the website is not ready yet — send it by email below.",
                     "الإرسال من الموقع غير جاهز بعد — أرسلها بالبريد بالأسفل."));
      return;
    }
    var tokenField = form.querySelector('[name="cf-turnstile-response"]');
    var token = tokenField ? tokenField.value : "";
    if (!token) {
      show(T("One moment — we are checking you are not a robot…", "لحظة — نتحقق أنك لست روبوتًا…"), "");
      return;
    }
    var sel = form.querySelector('input[name="type"]:checked');
    submit.disabled = true;
    show(T("Sending…", "جارٍ الإرسال…"), "");
    fetch("/api/feedback", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        app: form.elements.app.value,
        type: sel ? sel.value : "message",
        message: text,
        name: form.elements.name.value,
        contact: form.elements.contact.value,
        lang: lang(),
        source: fromApp ? "app" : "web",
        platform: platform,
        appVersion: appVersion,
        userLang: userLang || lang(),
        website: form.elements.website.value,
        t: Date.now() - t0,
        token: token
      })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (d) { return { code: r.status, d: d }; });
    }).then(function (res) {
      submit.disabled = false;
      if (res.code === 200 && res.d.ok) return done();
      if (window.turnstile) try { window.turnstile.reset(); } catch (x) {}
      var err = res.d.error;
      if (err === "rate_limited") return show(T("You have sent several messages already — please try again later.", "أرسلت عدة رسائل بالفعل — حاول مرة أخرى لاحقًا."), "err");
      if (err === "bot_check") return show(T("We could not confirm you are not a robot. Please try again.", "تعذّر التأكد أنك لست روبوتًا. حاول مرة أخرى."), "err");
      if (err === "length") return show(T("Your message is too short or too long.", "رسالتك قصيرة جدًا أو طويلة جدًا."), "err");
      openFallback(T("We could not send it from the website right now — send it by email below.",
                     "تعذّر الإرسال من الموقع الآن — أرسلها بالبريد بالأسفل."));
    }).catch(function () {
      submit.disabled = false;
      openFallback(T("No connection to the website right now — send it by email below.",
                     "لا اتصال بالموقع الآن — أرسلها بالبريد بالأسفل."));
    });
  });
})();
