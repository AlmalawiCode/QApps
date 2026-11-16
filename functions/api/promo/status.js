// functions/api/promo/status.js — GET /api/promo/status?app=vault
// Is the free offer on for this app, and how many Google Play / App Store codes
// are left? Apple: either one-per-visitor offer codes (apple.codes) or one
// shared offer link (apple.url).
// Read by the offer section on the app page and by the campaign page, so the
// owner can switch the offer off (or change the App Store link) from the
// dashboard without a rebuild. Public and harmless: no code, no visitor data.

import { jsonOut, ensurePromoSchema, appBySlug, offerLive, nowIso, NOT_EXPIRED } from "../../../lib/promo/common.js";

export async function onRequestGet({ request, env }) {
  if (!env.DB) return jsonOut({ ok: false, error: "not_configured" }, 503);
  const db = env.DB;
  await ensurePromoSchema(db);
  const app = await appBySlug(db, new URL(request.url).searchParams.get("app"));
  if (!app) return jsonOut({ ok: false, error: "unknown_app" }, 404);

  const rows = await db.prepare(
    `SELECT platform, COUNT(*) AS total, SUM(status = 'available' AND ${NOT_EXPIRED}) AS left, MAX(expires_at) AS ends FROM promo_codes WHERE app_id = ? AND status != 'void' GROUP BY platform`
  ).bind(nowIso(), app.id).all();
  const by = (p) => rows.results.find((r) => r.platform === p) || {};
  const c = by("android"), ic = by("ios");
  const live = offerLive(app);
  const left = c.left || 0;
  const iosLeft = ic.left || 0;
  const iosCodes = live && !!app.apple_offer_on && iosLeft > 0;
  // One-time offer codes open the App Store redeem sheet with the code filled in.
  const appleId = (String(app.apple_store_url || "").match(/id(\d{6,12})/) || [])[1];
  return jsonOut({
    ok: true,
    active: live,
    ends_at: app.offer_ends_at || null,
    android: { on: live && left > 0, total: c.total || 0, left },
    apple: {
      on: live && !!app.apple_offer_on && (iosCodes || !!app.apple_offer_url),
      url: live && app.apple_offer_on && !iosCodes ? app.apple_offer_url : null,
      codes: iosCodes,
      total: ic.total || 0,
      left: iosLeft,
      // when the codes stop working (store expiry); the page then hides a saved code
      codes_end: ic.ends || null,
      redeem: appleId ? `https://apps.apple.com/redeem?ctx=offercodes&id=${appleId}&code=` : null,
    },
    stores: { apple: app.apple_store_url, play: app.play_store_url },
  }, 200, "public, max-age=30");
}

export function onRequest() {
  return jsonOut({ ok: false, error: "method" }, 405);
}
