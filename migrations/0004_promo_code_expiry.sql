-- 0004_promo_code_expiry.sql — store expiry per promo code (2026-11-16).
-- App Store one-time offer codes end on a fixed date; after promo_codes.expires_at
-- (UTC ISO text in the same form as new Date().toISOString(), e.g. 2026-12-30T21:00:00.000Z — compared as text; NULL = no expiry) the site stops giving the code and stops
-- counting it as left (lib/promo/common.js NOT_EXPIRED). ADDITIVE ONLY.
--   npx wrangler d1 execute qapps-feedback --remote --file migrations/0004_promo_code_expiry.sql
-- Set a batch's expiry by hand, e.g. (stop at the start of 31 Dec Saudi time):
--   UPDATE promo_codes SET expires_at = '2026-12-30T21:00:00.000Z' WHERE platform = 'ios' AND note = '…';

ALTER TABLE promo_codes ADD COLUMN expires_at TEXT;
