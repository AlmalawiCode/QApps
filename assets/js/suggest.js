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
  function T(en, ar) { return lang() === "ar" ? ar : en; }

  // App from the link.
  var want = new URLSearchParams(location.search).get("app");
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
    return "[" + appLabel() + " · " + typeLabel() + "]\n\n" + form.elements.message.value.trim() +
      (name || contact ? "\n\n—" : "") +
      (name ? "\n" + T("Name: ", "الاسم: ") + name : "") +
      (contact ? "\n" + T("Reply to: ", "للرد: ") + contact : "");
  }

  function openFallback(reason) {
    fallback.hidden = false;
    show(reason, "warn");
  }
  form.querySelector("[data-fb-wa]").addEventListener("click", function () {
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
      back.href = "/apps/" + app + "/";
      back.querySelector("[data-en]").textContent = "Back to " + (form.elements.app.selectedOptions[0].getAttribute("data-en"));
      back.querySelector("[data-ar]").textContent = "عُد إلى صفحة " + (form.elements.app.selectedOptions[0].getAttribute("data-ar"));
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
      openFallback(T("Sending from the website is not ready yet — send it by WhatsApp or email below.",
                     "الإرسال من الموقع غير جاهز بعد — أرسلها عبر واتساب أو البريد بالأسفل."));
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
      openFallback(T("We could not send it from the website right now — send it by WhatsApp or email below.",
                     "تعذّر الإرسال من الموقع الآن — أرسلها عبر واتساب أو البريد بالأسفل."));
    }).catch(function () {
      submit.disabled = false;
      openFallback(T("No connection to the website right now — send it by WhatsApp or email below.",
                     "لا اتصال بالموقع الآن — أرسلها عبر واتساب أو البريد بالأسفل."));
    });
  });
})();
