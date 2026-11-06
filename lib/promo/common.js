// lib/promo/common.js — shared rules for the free full-version offer handed out
// by the website itself (proposal: proposals/qapps_free_codes_proposal_ar.html,
// approved 2026-11-04). Used by /functions/api/promo/* and
// /functions/api/admin/promo.js. Lives outside /functions so it is not a route.
//
// Three tables, in the same D1 database as the messages (binding DB):
//   apps         one row per app: store links, the App Store offer link, on/off
//   promo_codes  the Google Play promo codes, each mapped to its app; a code
//                someone took is "issued" (✗) with when / device / source
//   store_clicks the download statistic: one row per tap on a store button
// Plus promo_hits: a salted, daily-changing fingerprint of the address per code
// request (rate limit only), deleted after 24 hours.
//
// The codes themselves are never in this public repo: they are loaded into the
// database from the dashboard (/admin/promo/) or with wrangler (README).

export const PLATFORMS = ["ios", "android"];
export const CODE_STATUSES = ["available", "issued", "void"];
// visit = the campaign page was opened; download = a tap on "App Store" /
// "Google Play"; redeem = a tap on "activate the offer" (Apple link or the
// Play redeem link with the code); code = a code was handed out; copy = the
// code was copied; youtube = a tap on the «Tutorials on YouTube» button
// (the app comes from the page, there is no store link to match).
export const CLICK_KINDS = ["visit", "download", "redeem", "code", "copy", "youtube"];

export const PROMO_LIMITS = {
  codesPerAddressPerDay: 3, // a family on one network can still get one each
  clicksPerDay: 20000,      // whole-site cap on statistic rows (env CLICK_CAP overrides)
};

export const DEFAULT_ORIGINS = ["https://qeuapps.com", "https://www.qeuapps.com"];

const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS apps (
     id INTEGER PRIMARY KEY,
     slug TEXT NOT NULL UNIQUE,
     name_ar TEXT,
     name_en TEXT,
     apple_store_url TEXT,
     play_store_url TEXT,
     apple_offer_url TEXT,
     apple_offer_limit INTEGER,
     apple_offer_on INTEGER NOT NULL DEFAULT 1,
     offer_active INTEGER NOT NULL DEFAULT 0,
     offer_ends_at TEXT,
     updated_at TEXT
   )`,
  `CREATE TABLE IF NOT EXISTS promo_codes (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     app_id INTEGER NOT NULL REFERENCES apps(id),
     platform TEXT NOT NULL DEFAULT 'android',
     code TEXT NOT NULL UNIQUE,
     status TEXT NOT NULL DEFAULT 'available',
     added_at TEXT NOT NULL,
     issued_at TEXT,
     request_id TEXT,
     device TEXT,
     browser TEXT,
     source TEXT,
     lang TEXT,
     page TEXT,
     note TEXT
   )`,
  `CREATE INDEX IF NOT EXISTS idx_promo_pick ON promo_codes(app_id, platform, status, id)`,
  `CREATE UNIQUE INDEX IF NOT EXISTS idx_promo_request ON promo_codes(app_id, platform, request_id)`,
  `CREATE INDEX IF NOT EXISTS idx_promo_issued ON promo_codes(issued_at)`,
  `CREATE TABLE IF NOT EXISTS promo_hits (ip_hash TEXT NOT NULL, ts INTEGER NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS idx_promo_hits ON promo_hits(ip_hash, ts)`,
  `CREATE TABLE IF NOT EXISTS store_clicks (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     created_at TEXT NOT NULL,
     app_id INTEGER REFERENCES apps(id),
     platform TEXT,
     kind TEXT NOT NULL,
     page TEXT,
     device TEXT,
     browser TEXT,
     source TEXT,
     lang TEXT
   )`,
  `CREATE INDEX IF NOT EXISTS idx_clicks_created ON store_clicks(created_at)`,
  `CREATE INDEX IF NOT EXISTS idx_clicks_app ON store_clicks(app_id, created_at)`,
  // The apps, once. INSERT OR IGNORE never overwrites what the owner changes
  // later from the dashboard.
  `INSERT OR IGNORE INTO apps (id, slug, name_ar, name_en, apple_store_url, play_store_url,
       apple_offer_url, apple_offer_limit, apple_offer_on, offer_active) VALUES
     (1, 'vault', 'خزنة الضمانات', 'Vault — Warranty Manager',
      'https://apps.apple.com/app/id6773164894',
      'https://play.google.com/store/apps/details?id=com.vault.warranty',
      'https://apps.apple.com/redeem?ctx=offercodes&id=6773164894&code=FREE500', 500, 1, 1),
     (2, 'countdown-keeper', 'كم مضى وكم بقي', 'Countdown Keeper',
      'https://apps.apple.com/app/id6806348941', NULL, NULL, NULL, 1, 0),
     (3, 'docmatic', 'DocMatic', 'DocMatic', NULL, NULL, NULL, NULL, 1, 0)`,
];

let ready = null;
/** Creates the tables on first use (same SQL as migrations/0003_promo.sql). */
export function ensurePromoSchema(db) {
  if (!ready) {
    ready = db.batch(SCHEMA.map((s) => db.prepare(s))).catch((e) => {
      ready = null;
      throw e;
    });
  }
  return ready;
}

export function jsonOut(data, status = 200, cache = "no-store") {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": cache,
      "x-robots-tag": "noindex",
    },
  });
}

export function nowIso() {
  return new Date().toISOString();
}

export async function sha256hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

/** Only from our own pages (Origin, or Referer when a browser sends no Origin). */
export function fromOurSite(request, env) {
  const extra = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const allowed = extra.length ? extra : DEFAULT_ORIGINS;
  const origin = request.headers.get("Origin");
  if (origin) return allowed.includes(origin);
  const ref = request.headers.get("Referer") || "";
  return allowed.some((o) => ref === o || ref.startsWith(o + "/"));
}

/** Campaign source from ?utm_source= (same rules as the campaign page). */
export function cleanSource(raw) {
  let s = String(raw == null ? "" : raw).trim().toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 24);
  if (!s) return "direct";
  if (s === "twitter") return "x";
  return s;
}

export function cleanPage(raw) {
  const s = String(raw || "").slice(0, 80);
  return /^\/[A-Za-z0-9/_-]*$/.test(s) ? s : null;
}

export function cleanLang(raw) {
  return /^[a-z]{2}$/.test(raw || "") ? raw : null;
}

/** Short device / browser names from the User-Agent (nothing is stored raw). */
export function deviceOf(ua) {
  ua = ua || "";
  if (/iPad/.test(ua)) return "ipad";
  if (/iPhone|iPod/.test(ua)) return "iphone";
  if (/Android/.test(ua)) {
    if (/SM-|SAMSUNG|Samsung/.test(ua)) return "samsung";
    return /Mobile/.test(ua) ? "android" : "android_tablet";
  }
  if (/Macintosh/.test(ua)) return "mac";
  if (/Windows/.test(ua)) return "windows";
  if (/Linux|CrOS/.test(ua)) return "linux";
  return "other";
}

export function browserOf(ua) {
  ua = ua || "";
  if (/Instagram/.test(ua)) return "instagram";
  if (/Snapchat/.test(ua)) return "snapchat";
  if (/BytedanceWebview|musical_ly|TikTok/i.test(ua)) return "tiktok";
  if (/FBAN|FBAV|FB_IAB/.test(ua)) return "facebook";
  if (/Twitter/.test(ua)) return "x";
  if (/WhatsApp/.test(ua)) return "whatsapp";
  if (/SamsungBrowser/.test(ua)) return "samsung";
  if (/EdgA?\/|EdgiOS/.test(ua)) return "edge";
  if (/OPR\/|Opera/.test(ua)) return "opera";
  if (/Firefox\/|FxiOS/.test(ua)) return "firefox";
  if (/CriOS|Chrome\//.test(ua)) return "chrome";
  if (/Safari\//.test(ua)) return "safari";
  return "other";
}

export async function appBySlug(db, slug) {
  if (!/^[a-z0-9-]{1,40}$/.test(slug || "")) return null;
  return db.prepare("SELECT * FROM apps WHERE slug = ?").bind(slug).first();
}

/** Which app a store link belongs to (App Store id… or Play ?id=package). */
export async function appByStoreLink(db, href) {
  const s = String(href || "");
  let m = s.match(/apps\.apple\.com\/.*?id(\d{6,12})/);
  if (m) {
    const r = await db.prepare("SELECT * FROM apps WHERE apple_store_url LIKE ?").bind(`%id${m[1]}%`).first();
    return r ? { app: r, platform: "ios" } : null;
  }
  m = s.match(/play\.google\.com\/.*[?&]id=([A-Za-z0-9._]{3,100})/);
  if (m) {
    const r = await db.prepare("SELECT * FROM apps WHERE play_store_url LIKE ?").bind(`%id=${m[1]}%`).first();
    return r ? { app: r, platform: "android" } : null;
  }
  return null;
}

/** Is the offer on right now? (switched on, and its end date not passed) */
export function offerLive(app, now = new Date()) {
  if (!app || !app.offer_active) return false;
  if (app.offer_ends_at && new Date(app.offer_ends_at) <= now) return false;
  return true;
}

export async function verifyTurnstile(env, token, ip) {
  const form = new FormData();
  form.append("secret", env.TURNSTILE_SECRET);
  form.append("response", String(token || "").slice(0, 4096));
  form.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
  const v = await r.json();
  return !!v.success;
}
