// functions/api/feedback.js — POST /api/feedback: a visitor's message from
// the "Contact & suggest" page (/suggest/). Saves it in D1 after every
// protection layer of the approved proposal (decision ه):
//   site-only origin · hidden honeypot field · minimum time on the page ·
//   field checks · Cloudflare Turnstile · per-visitor hour/day limits ·
//   a daily cap for the whole site · "suspicious" flag for many links.
// Fails closed: without its configuration it answers 503 "not_configured"
// and the page falls back to WhatsApp / email, so nothing is lost.
//
// Env (Pages → Settings): DB (D1 binding), TURNSTILE_SECRET, IP_SALT,
// optional ALLOWED_ORIGINS (comma list), DAILY_CAP.

import { APPS, TYPES, LANGS, LIMITS, json, sha256hex, ensureSchema, nowIso } from "../../lib/feedback/common.js";

const DEFAULT_ORIGINS = ["https://qeuapps.com", "https://www.qeuapps.com"];

function clean(v, max) {
  return typeof v === "string" ? v.replace(/\u0000/g, "").trim().slice(0, max) : "";
}

export async function onRequestPost({ request, env }) {
  if (!env.DB || !env.TURNSTILE_SECRET || !env.IP_SALT) {
    return json({ ok: false, error: "not_configured" }, 503);
  }

  // Only from our own pages.
  const origins = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const allowed = origins.length ? origins : DEFAULT_ORIGINS;
  const origin = request.headers.get("Origin") || "";
  if (!allowed.includes(origin)) return json({ ok: false, error: "origin" }, 403);

  if (Number(request.headers.get("content-length") || 0) > 16_000) {
    return json({ ok: false, error: "too_large" }, 413);
  }
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: "bad_request" }, 400);
  }

  // Robots: the hidden field is filled, or the form was sent too fast.
  // Answer "ok" so a robot learns nothing, and save nothing.
  if (clean(data.website, 200) !== "") return json({ ok: true });
  if (!(Number(data.t) >= LIMITS.minMillis)) return json({ ok: true });

  const app = clean(data.app, 40);
  const type = clean(data.type, 20);
  const body = clean(data.message, LIMITS.maxText + 1);
  const name = clean(data.name, LIMITS.maxName);
  const contact = clean(data.contact, LIMITS.maxContact);
  const lang = LANGS.includes(data.lang) ? data.lang : "en";
  if (!APPS.includes(app) || !TYPES.includes(type)) return json({ ok: false, error: "bad_request" }, 400);
  if (body.length < LIMITS.minText || body.length > LIMITS.maxText) {
    return json({ ok: false, error: "length" }, 400);
  }

  // Cloudflare Turnstile ("not a robot"), checked on the server.
  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  const form = new FormData();
  form.append("secret", env.TURNSTILE_SECRET);
  form.append("response", clean(data.token, 4096));
  form.append("remoteip", ip);
  let verdict = { success: false };
  try {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
    verdict = await r.json();
  } catch {
    return json({ ok: false, error: "verify_unavailable" }, 503);
  }
  if (!verdict.success) return json({ ok: false, error: "bot_check" }, 403);

  const db = env.DB;
  await ensureSchema(db);

  // Per-visitor limits. The address is kept only as a salted fingerprint
  // that changes every day, and rows older than 24 hours are deleted.
  const now = Date.now();
  const day = new Date(now).toISOString().slice(0, 10);
  const ipHash = await sha256hex(`${env.IP_SALT}|${ip}|${day}`);
  await db.prepare("DELETE FROM rate_hits WHERE ts < ?").bind(now - 86_400_000).run();
  const hits = await db
    .prepare("SELECT SUM(ts >= ?) AS hour, COUNT(*) AS day FROM rate_hits WHERE ip_hash = ?")
    .bind(now - 3_600_000, ipHash)
    .first();
  if ((hits?.hour || 0) >= LIMITS.perHour || (hits?.day || 0) >= LIMITS.perDay) {
    return json({ ok: false, error: "rate_limited" }, 429);
  }

  // A cap for the whole site, so an attack can never flood the inbox.
  const cap = Number(env.DAILY_CAP) || LIMITS.dailyCap;
  const today = await db
    .prepare("SELECT COUNT(*) AS n FROM messages WHERE created_at >= ?")
    .bind(day + "T00:00:00.000Z")
    .first();
  if ((today?.n || 0) >= cap) return json({ ok: false, error: "busy" }, 429);

  const links = (body.match(/https?:\/\/|www\./gi) || []).length;
  const flagged = links > LIMITS.maxLinks ? 1 : 0;

  await db.batch([
    db.prepare(
      "INSERT INTO messages (created_at, app, type, body, name, contact, lang, status, flagged) VALUES (?, ?, ?, ?, ?, ?, ?, 'new', ?)"
    ).bind(nowIso(), app, type, body, name || null, contact || null, lang, flagged),
    db.prepare("INSERT INTO rate_hits (ip_hash, ts) VALUES (?, ?)").bind(ipHash, now),
  ]);
  return json({ ok: true });
}

export function onRequest() {
  return json({ ok: false, error: "method" }, 405);
}
