// functions/api/promo/status.js — GET /api/promo/status?app=vault
// Is the free offer on for this app, and how many Google Play codes are left?
// Read by the offer section on the app page and by the campaign page, so the
// owner can switch the offer off (or change the App Store link) from the
// dashboard without a rebuild. Public and harmless: no code, no visitor data.

import { jsonOut, ensurePromoSchema, appBySlug, offerLive } from "../../../lib/promo/common.js";

export async function onRequestGet({ request, env }) {
  if (!env.DB) return jsonOut({ ok: false, error: "not_configured" }, 503);
  const db = env.DB;
  await ensurePromoSchema(db);
  const app = await appBySlug(db, new URL(request.url).searchParams.get("app"));
  if (!app) return jsonOut({ ok: false, error: "unknown_app" }, 404);

  const c = await db.prepare(
    "SELECT COUNT(*) AS total, SUM(status = 'available') AS left FROM promo_codes WHERE app_id = ? AND platform = 'android' AND status != 'void'"
  ).bind(app.id).first();
  const live = offerLive(app);
  const left = c?.left || 0;
  return jsonOut({
    ok: true,
    active: live,
    ends_at: app.offer_ends_at || null,
    android: { on: live && left > 0, total: c?.total || 0, left },
    apple: { on: live && !!app.apple_offer_on && !!app.apple_offer_url, url: live && app.apple_offer_on ? app.apple_offer_url : null },
    stores: { apple: app.apple_store_url, play: app.play_store_url },
  }, 200, "public, max-age=30");
}

export function onRequest() {
  return jsonOut({ ok: false, error: "method" }, 405);
}
