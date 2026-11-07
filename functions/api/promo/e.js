// functions/api/promo/e.js — POST /api/promo/e: one row of the download
// statistic (proposal qapps_free_codes, decision ه): a tap on "App Store" /
// "Google Play" / "YouTube" / "activate the offer" / "copy", or a page opened
// (visit = first page of a browser session = one visitor; view = a further page).
//
//   body (JSON, sent as text/plain by sendBeacon):
//     {app?, href?, platform?, kind, page, src, lang}
//   The app comes from `app` (slug) or from the store link `href`.
//
// A tap is not an install: real installs are in Play Console / App Store
// Connect. No address, cookie or name is stored — app, platform, kind, page,
// device and browser (from the User-Agent), source (?utm_source) and language.
// The short opaque path ("e") keeps content blockers from dropping it.

import {
  jsonOut, nowIso, fromOurSite, cleanSource, cleanPage, cleanLang, deviceOf, browserOf,
  appBySlug, appByStoreLink, ensurePromoSchema, CLICK_KINDS, PLATFORMS, PROMO_LIMITS, isBot,
} from "../../../lib/promo/common.js";

const done = () => new Response(null, { status: 204, headers: { "cache-control": "no-store" } });

export async function onRequestPost({ request, env }) {
  if (!env.DB) return done();
  if (!fromOurSite(request, env)) return jsonOut({ ok: false, error: "origin" }, 403);
  if (Number(request.headers.get("content-length") || 0) > 4000) return done();

  let data;
  try {
    data = JSON.parse(await request.text());
  } catch {
    return done();
  }
  const kind = CLICK_KINDS.includes(data.kind) ? data.kind : null;
  if (!kind) return done();

  const ua = request.headers.get("User-Agent") || "";
  const pageLoad = kind === "visit" || kind === "view";
  if (pageLoad && isBot(ua)) return done();

  const db = env.DB;
  await ensurePromoSchema(db);
  let app = null;
  let platform = PLATFORMS.includes(data.platform) ? data.platform : null;
  if (data.href) {
    const hit = await appByStoreLink(db, data.href);
    if (hit) { app = hit.app; platform = platform || hit.platform; }
  }
  if (!app && data.app) app = await appBySlug(db, data.app);
  // A page without an app (home, /apps/, /privacy/…) still counts as a visit.
  if (!app && !pageLoad) return done();

  const now = nowIso();
  const cap = Number(env.CLICK_CAP) || PROMO_LIMITS.clicksPerDay;
  const today = await db.prepare("SELECT COUNT(*) AS n FROM store_clicks WHERE created_at >= ?")
    .bind(now.slice(0, 10) + "T00:00:00.000Z").first();
  if ((today?.n || 0) >= cap) return done();

  await db.prepare(
    "INSERT INTO store_clicks (created_at, app_id, platform, kind, page, device, browser, source, lang) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
  ).bind(now, app ? app.id : null, platform, kind, cleanPage(data.page), deviceOf(ua), browserOf(ua), cleanSource(data.src), cleanLang(data.lang)).run();
  return done();
}

export function onRequest() {
  return jsonOut({ ok: false, error: "method" }, 405);
}
