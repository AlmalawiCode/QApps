// functions/api/admin/promo.js — the owner's free-codes & downloads dashboard
// API (/admin/promo/; proposal qapps_free_codes, decision و). Cloudflare
// Access only (lib/feedback/access.js): no valid token → 401, no data.
//
// GET  ?view=summary[&days=30]           apps + code counts + download statistic
// GET  ?view=codes&app=&status=&offset=  the codes of one app (newest issued first)
// GET  ?view=csv&app=                    every code of one app as CSV
// POST {action:"add", app, codes}        paste codes (any separators); duplicates ignored
// POST {action:"void"|"restore", id}     take a never-issued code out / back
// POST {action:"release", id}            put an issued (test / unused) code back
// POST {action:"offer", app, offer_active, apple_offer_on, apple_offer_url,
//       apple_offer_limit, offer_ends_at} switch the offer, edit the App Store link

import { adminEmail } from "../../../lib/feedback/access.js";
import { jsonOut, nowIso, ensurePromoSchema, appBySlug, CODE_STATUSES } from "../../../lib/promo/common.js";

const PAGE = 100;

async function guard(request, env) {
  if (!env.DB) return jsonOut({ ok: false, error: "not_configured" }, 503);
  let who = null;
  try {
    who = await adminEmail(request, env);
  } catch {
    who = null;
  }
  if (!who) return jsonOut({ ok: false, error: "unauthorized" }, 401);
  await ensurePromoSchema(env.DB);
  return null;
}

function csvCell(v) {
  const s = v == null ? "" : String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export async function onRequestGet({ request, env }) {
  const denied = await guard(request, env);
  if (denied) return denied;
  const db = env.DB;
  const u = new URL(request.url);
  const view = u.searchParams.get("view") || "summary";

  if (view === "codes" || view === "csv") {
    const app = await appBySlug(db, u.searchParams.get("app"));
    if (!app) return jsonOut({ ok: false, error: "unknown_app" }, 404);
    if (view === "csv") {
      const all = await db.prepare(
        "SELECT code, status, platform, added_at, issued_at, device, browser, source, lang, page, request_id, note FROM promo_codes WHERE app_id = ? ORDER BY id"
      ).bind(app.id).all();
      const cols = ["code", "status", "platform", "added_at", "issued_at", "device", "browser", "source", "lang", "page", "request_id", "note"];
      const text = "﻿" + [cols.join(",")].concat(all.results.map((r) => cols.map((c) => csvCell(r[c])).join(","))).join("\n") + "\n";
      return new Response(text, {
        headers: {
          "content-type": "text/csv; charset=utf-8",
          "content-disposition": `attachment; filename="${app.slug}-codes-${nowIso().slice(0, 10)}.csv"`,
          "cache-control": "no-store",
        },
      });
    }
    const status = u.searchParams.get("status") || "issued";
    const offset = Math.max(0, Number(u.searchParams.get("offset")) || 0);
    const where = CODE_STATUSES.includes(status) ? "AND status = ?" : "";
    const args = CODE_STATUSES.includes(status) ? [app.id, status] : [app.id];
    const [rows, total] = await db.batch([
      db.prepare(`SELECT id, code, status, platform, added_at, issued_at, device, browser, source, lang, page FROM promo_codes WHERE app_id = ? ${where} ORDER BY issued_at DESC, id ASC LIMIT ${PAGE} OFFSET ?`).bind(...args, offset),
      db.prepare(`SELECT COUNT(*) AS n FROM promo_codes WHERE app_id = ? ${where}`).bind(...args),
    ]);
    return jsonOut({ ok: true, codes: rows.results, total: total.results[0]?.n || 0, page: PAGE, offset });
  }

  // summary
  const days = Math.min(90, Math.max(1, Number(u.searchParams.get("days")) || 30));
  const since = new Date(Date.now() - days * 86_400_000).toISOString();
  const day1 = new Date(Date.now() - 86_400_000).toISOString();
  const day7 = new Date(Date.now() - 7 * 86_400_000).toISOString();
  const [apps, codes, recent, byDay, bySource, byDevice, byPage, totals] = await db.batch([
    db.prepare("SELECT * FROM apps ORDER BY id"),
    db.prepare("SELECT app_id, platform, status, COUNT(*) AS n FROM promo_codes GROUP BY app_id, platform, status"),
    db.prepare("SELECT app_id, SUM(issued_at >= ?) AS d1, SUM(issued_at >= ?) AS d7 FROM promo_codes WHERE status = 'issued' GROUP BY app_id").bind(day1, day7),
    db.prepare("SELECT substr(created_at, 1, 10) AS day, app_id, platform, kind, COUNT(*) AS n FROM store_clicks WHERE created_at >= ? GROUP BY day, app_id, platform, kind ORDER BY day").bind(since),
    db.prepare("SELECT app_id, source, kind, COUNT(*) AS n FROM store_clicks WHERE created_at >= ? GROUP BY app_id, source, kind").bind(since),
    db.prepare("SELECT app_id, device, kind, COUNT(*) AS n FROM store_clicks WHERE created_at >= ? GROUP BY app_id, device, kind").bind(since),
    db.prepare("SELECT app_id, page, kind, COUNT(*) AS n FROM store_clicks WHERE created_at >= ? GROUP BY app_id, page, kind").bind(since),
    db.prepare("SELECT app_id, platform, kind, SUM(created_at >= ?) AS d1, SUM(created_at >= ?) AS d7, COUNT(*) AS all_time FROM store_clicks GROUP BY app_id, platform, kind").bind(day1, day7),
  ]);
  return jsonOut({
    ok: true,
    days,
    apps: apps.results,
    codes: codes.results,
    recent: recent.results,
    clicks: { byDay: byDay.results, bySource: bySource.results, byDevice: byDevice.results, byPage: byPage.results, totals: totals.results },
  });
}

export async function onRequestPost({ request, env }) {
  const denied = await guard(request, env);
  if (denied) return denied;
  const db = env.DB;
  let data;
  try {
    data = await request.json();
  } catch {
    return jsonOut({ ok: false, error: "bad_request" }, 400);
  }

  if (data.action === "add") {
    const app = await appBySlug(db, data.app);
    if (!app) return jsonOut({ ok: false, error: "unknown_app" }, 404);
    const platform = data.platform === "ios" ? "ios" : "android";
    // Play promo codes are long upper-case letters and digits (23 today);
    // take every such token from whatever was pasted (one per line, CSV,
    // spaces…). A digit is required so CSV headers ("AssignedAt") never count.
    const found = (String(data.codes || "").toUpperCase().match(/\b[A-Z0-9]{12,40}\b/g) || []).filter((c) => /\d/.test(c));
    const codes = [...new Set(found)].slice(0, 5000);
    if (!codes.length) return jsonOut({ ok: false, error: "no_codes" }, 400);
    const at = nowIso();
    let added = 0;
    for (let i = 0; i < codes.length; i += 50) {
      const res = await db.batch(codes.slice(i, i + 50).map((c) =>
        db.prepare("INSERT OR IGNORE INTO promo_codes (app_id, platform, code, status, added_at) VALUES (?, ?, ?, 'available', ?)").bind(app.id, platform, c, at)));
      added += res.reduce((s, r) => s + (r.meta?.changes || 0), 0);
    }
    return jsonOut({ ok: true, found: codes.length, added, duplicates: codes.length - added });
  }

  if (data.action === "void" || data.action === "restore") {
    const id = Number(data.id);
    if (!Number.isInteger(id) || id <= 0) return jsonOut({ ok: false, error: "bad_request" }, 400);
    // Only a code that was never given to anyone can change.
    const r = data.action === "void"
      ? await db.prepare("UPDATE promo_codes SET status = 'void' WHERE id = ? AND status = 'available'").bind(id).run()
      : await db.prepare("UPDATE promo_codes SET status = 'available' WHERE id = ? AND status = 'void' AND issued_at IS NULL").bind(id).run();
    return jsonOut({ ok: true, changed: r.meta?.changes ?? 0 });
  }

  if (data.action === "release") {
    // Give an issued code back (the owner's own test, or a code that was
    // never used). Only for codes NOT redeemed in Google Play: a redeemed
    // code put back would reach the next visitor dead.
    const id = Number(data.id);
    if (!Number.isInteger(id) || id <= 0) return jsonOut({ ok: false, error: "bad_request" }, 400);
    const row = await db.prepare("SELECT app_id, issued_at FROM promo_codes WHERE id = ? AND status = 'issued'").bind(id).first();
    if (!row) return jsonOut({ ok: true, changed: 0 });
    const ms = Date.parse(row.issued_at);
    const [r] = await db.batch([
      db.prepare(
        "UPDATE promo_codes SET status = 'available', issued_at = NULL, request_id = NULL, device = NULL, browser = NULL, source = NULL, lang = NULL, page = NULL WHERE id = ? AND status = 'issued'"
      ).bind(id),
      // The claim row in the download statistic (same timestamp as issued_at).
      db.prepare(
        "DELETE FROM store_clicks WHERE id = (SELECT id FROM store_clicks WHERE app_id = ? AND kind = 'code' AND created_at = ? LIMIT 1)"
      ).bind(row.app_id, row.issued_at),
      // The matching use of the 3-a-day limit (written in the same instant).
      db.prepare(
        "DELETE FROM promo_hits WHERE rowid = (SELECT rowid FROM promo_hits WHERE ABS(ts - ?) < 5000 ORDER BY ABS(ts - ?) LIMIT 1)"
      ).bind(ms || 0, ms || 0),
    ]);
    return jsonOut({ ok: true, changed: r.meta?.changes ?? 0 });
  }

  if (data.action === "offer") {
    const app = await appBySlug(db, data.app);
    if (!app) return jsonOut({ ok: false, error: "unknown_app" }, 404);
    const sets = [];
    const args = [];
    if (data.offer_active !== undefined) { sets.push("offer_active = ?"); args.push(data.offer_active ? 1 : 0); }
    if (data.apple_offer_on !== undefined) { sets.push("apple_offer_on = ?"); args.push(data.apple_offer_on ? 1 : 0); }
    if (data.apple_offer_url !== undefined) {
      const url = String(data.apple_offer_url || "").trim();
      if (url && !/^https:\/\/apps\.apple\.com\//.test(url)) return jsonOut({ ok: false, error: "apple_url" }, 400);
      sets.push("apple_offer_url = ?"); args.push(url || null);
    }
    if (data.apple_offer_limit !== undefined) {
      const n = Number(data.apple_offer_limit);
      sets.push("apple_offer_limit = ?"); args.push(Number.isInteger(n) && n > 0 ? n : null);
    }
    if (data.offer_ends_at !== undefined) {
      const s = String(data.offer_ends_at || "").trim();
      if (s && isNaN(new Date(s))) return jsonOut({ ok: false, error: "date" }, 400);
      sets.push("offer_ends_at = ?"); args.push(s ? new Date(s).toISOString() : null);
    }
    if (!sets.length) return jsonOut({ ok: false, error: "bad_request" }, 400);
    sets.push("updated_at = ?"); args.push(nowIso());
    await db.prepare(`UPDATE apps SET ${sets.join(", ")} WHERE id = ?`).bind(...args, app.id).run();
    return jsonOut({ ok: true });
  }

  return jsonOut({ ok: false, error: "bad_request" }, 400);
}

export function onRequest() {
  return jsonOut({ ok: false, error: "method" }, 405);
}
