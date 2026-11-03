// functions/api/promo/claim.js — POST /api/promo/claim: hand ONE Google Play
// promo code to one visitor (proposal qapps_free_codes, decision د).
//
//   body: {app, rid, token, src, lang, page}
//   →    {status: "ok", code} | "empty" | "ended" | "limit" | "bot" | "busy"
//
// · The code list never reaches the browser: only the one code given here.
// · Two people never get the same code: picking a code and marking it issued
//   is ONE UPDATE … RETURNING statement in the database.
// · One code per device: the page keeps a random request id (rid); asking
//   again with the same rid returns the SAME code, never a new one.
// · Robots: Cloudflare Turnstile (when TURNSTILE_SECRET is set), our pages
//   only, and at most 3 codes a day from one address (salted fingerprint,
//   deleted after 24 hours).
// Env: DB, IP_SALT, TURNSTILE_SECRET (Pages settings), optional ALLOWED_ORIGINS.

import {
  jsonOut, nowIso, sha256hex, fromOurSite, cleanSource, cleanPage, cleanLang,
  deviceOf, browserOf, appBySlug, offerLive, verifyTurnstile, ensurePromoSchema, PROMO_LIMITS,
} from "../../../lib/promo/common.js";

const PLATFORM = "android";

export async function onRequestPost({ request, env }) {
  if (!env.DB || !env.IP_SALT) return jsonOut({ status: "busy", error: "not_configured" }, 503);
  if (!fromOurSite(request, env)) return jsonOut({ status: "busy", error: "origin" }, 403);
  if (Number(request.headers.get("content-length") || 0) > 8000) return jsonOut({ status: "busy" }, 413);

  let data;
  try {
    data = await request.json();
  } catch {
    return jsonOut({ status: "busy", error: "bad_request" }, 400);
  }
  const rid = String(data.rid || "");
  if (!/^[A-Za-z0-9-]{8,64}$/.test(rid)) return jsonOut({ status: "busy", error: "bad_request" }, 400);

  const db = env.DB;
  await ensurePromoSchema(db);
  const app = await appBySlug(db, data.app);
  if (!app) return jsonOut({ status: "busy", error: "bad_request" }, 400);

  // Same device asking again → the same code (before any other check, so a
  // reload never costs a second code or a second robot check).
  const mine = await db
    .prepare("SELECT code FROM promo_codes WHERE app_id = ? AND platform = ? AND request_id = ?")
    .bind(app.id, PLATFORM, rid).first();
  if (mine) return jsonOut({ status: "ok", code: mine.code, again: true });

  if (!offerLive(app)) return jsonOut({ status: "ended" });

  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  if (env.TURNSTILE_SECRET) {
    let human = false;
    try {
      human = await verifyTurnstile(env, data.token, ip);
    } catch {
      return jsonOut({ status: "busy", error: "verify_unavailable" }, 503);
    }
    if (!human) return jsonOut({ status: "bot" }, 403);
  }

  const now = Date.now();
  const day = new Date(now).toISOString().slice(0, 10);
  const ipHash = await sha256hex(`${env.IP_SALT}|promo|${ip}|${day}`);
  await db.prepare("DELETE FROM promo_hits WHERE ts < ?").bind(now - 86_400_000).run();
  const hits = await db.prepare("SELECT COUNT(*) AS n FROM promo_hits WHERE ip_hash = ?").bind(ipHash).first();
  if ((hits?.n || 0) >= PROMO_LIMITS.codesPerAddressPerDay) {
    // A double tap whose twin just won a code is not "over the limit".
    const won = await db
      .prepare("SELECT code FROM promo_codes WHERE app_id = ? AND platform = ? AND request_id = ?")
      .bind(app.id, PLATFORM, rid).first();
    if (won) return jsonOut({ status: "ok", code: won.code, again: true });
    return jsonOut({ status: "limit" }, 429);
  }

  const ua = request.headers.get("User-Agent") || "";
  const meta = {
    device: deviceOf(ua),
    browser: browserOf(ua),
    source: cleanSource(data.src),
    lang: cleanLang(data.lang),
    page: cleanPage(data.page),
  };
  const at = nowIso();

  let row = null;
  try {
    row = await db.prepare(
      "UPDATE promo_codes SET status = 'issued', issued_at = ?, request_id = ?, device = ?, browser = ?, source = ?, lang = ?, page = ? " +
      "WHERE id = (SELECT id FROM promo_codes WHERE app_id = ? AND platform = ? AND status = 'available' ORDER BY id LIMIT 1) " +
      "AND status = 'available' RETURNING code"
    ).bind(at, rid, meta.device, meta.browser, meta.source, meta.lang, meta.page, app.id, PLATFORM).first();
  } catch (e) {
    // The same rid won a code in a parallel request a moment ago (unique
    // index on app + platform + request id) → give that one.
    const again = await db
      .prepare("SELECT code FROM promo_codes WHERE app_id = ? AND platform = ? AND request_id = ?")
      .bind(app.id, PLATFORM, rid).first();
    if (again) return jsonOut({ status: "ok", code: again.code, again: true });
    throw e;
  }

  if (!row) return jsonOut({ status: "empty" });

  await db.batch([
    db.prepare("INSERT INTO promo_hits (ip_hash, ts) VALUES (?, ?)").bind(ipHash, now),
    db.prepare(
      "INSERT INTO store_clicks (created_at, app_id, platform, kind, page, device, browser, source, lang) VALUES (?, ?, ?, 'code', ?, ?, ?, ?, ?)"
    ).bind(at, app.id, PLATFORM, meta.page, meta.device, meta.browser, meta.source, meta.lang),
  ]);
  return jsonOut({ status: "ok", code: row.code });
}

export function onRequest() {
  return jsonOut({ status: "busy", error: "method" }, 405);
}
