-- 0001_feedback.sql — tables for the website's "Contact & suggest" channel.
-- The API creates these itself on first use (lib/feedback/common.js); this
-- file is the same SQL, for reference or to set up the database by hand:
--   npx wrangler d1 execute qapps-feedback --remote --file migrations/0001_feedback.sql

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,          -- ISO time (UTC)
  app TEXT NOT NULL,                 -- docmatic | vault | countdown-keeper | new-app | general
  type TEXT NOT NULL,                -- message | improve | feature | problem
  body TEXT NOT NULL,
  name TEXT,                         -- optional
  contact TEXT,                      -- optional (email or number, as the visitor wrote it)
  lang TEXT,                         -- page language: ar | en
  status TEXT NOT NULL DEFAULT 'new',-- new | review | done | archived
  note TEXT,                         -- the owner's private note
  flagged INTEGER NOT NULL DEFAULT 0,-- 1 = many links ("suspicious")
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status);

-- Per-visitor rate limit: a salted, daily-changing fingerprint of the
-- address (never the address itself); rows older than 24 hours are deleted.
CREATE TABLE IF NOT EXISTS rate_hits (ip_hash TEXT NOT NULL, ts INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS idx_rate_hits ON rate_hits(ip_hash, ts);
