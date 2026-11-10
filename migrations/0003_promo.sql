-- 0003_promo.sql — free full-version offer from the website (Google Play
-- promo codes + App Store offer link + download statistic).
-- ADDITIVE ONLY: new tables; the messages tables are untouched.
-- The API creates these itself on first use (lib/promo/common.js); this file
-- is the same SQL, for reference or manual setup:
--   npx wrangler d1 execute qapps-feedback --remote --file migrations/0003_promo.sql
-- The codes are NOT here (this repo is public): add them from /admin/promo/.

CREATE TABLE IF NOT EXISTS apps (
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
 );

CREATE TABLE IF NOT EXISTS promo_codes (
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
 );

CREATE INDEX IF NOT EXISTS idx_promo_pick ON promo_codes(app_id, platform, status, id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_promo_request ON promo_codes(app_id, platform, request_id);

CREATE INDEX IF NOT EXISTS idx_promo_issued ON promo_codes(issued_at);

CREATE TABLE IF NOT EXISTS promo_hits (ip_hash TEXT NOT NULL, ts INTEGER NOT NULL);

CREATE INDEX IF NOT EXISTS idx_promo_hits ON promo_hits(ip_hash, ts);

CREATE TABLE IF NOT EXISTS store_clicks (
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
 );

CREATE INDEX IF NOT EXISTS idx_clicks_created ON store_clicks(created_at);

CREATE INDEX IF NOT EXISTS idx_clicks_app ON store_clicks(app_id, created_at);

INSERT OR IGNORE INTO apps (id, slug, name_ar, name_en, apple_store_url, play_store_url,
     apple_offer_url, apple_offer_limit, apple_offer_on, offer_active) VALUES
   (1, 'vault', 'خزنة الضمانات', 'Vault — Warranty Manager',
    'https://apps.apple.com/app/id6773164894',
    'https://play.google.com/store/apps/details?id=com.vault.warranty',
    'https://apps.apple.com/redeem?ctx=offercodes&id=6773164894&code=FREE500', 500, 1, 1),
   (2, 'countdown-keeper', 'كم مضى وكم بقي', 'Countdown Keeper',
    'https://apps.apple.com/app/id6806348941',
    'https://play.google.com/store/apps/details?id=com.eventcounter.countdown', NULL, NULL, 1, 0),
   (3, 'docmatic', 'DocMatic', 'DocMatic', NULL, NULL, NULL, NULL, 1, 0);

-- Countdown Keeper reached Google Play on 2026-11-10 (for a database seeded before that).
UPDATE apps SET play_store_url = 'https://play.google.com/store/apps/details?id=com.eventcounter.countdown'
 WHERE slug = 'countdown-keeper' AND play_store_url IS NULL;
