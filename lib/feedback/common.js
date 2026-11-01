// lib/feedback/common.js — shared rules for the website's "Contact & suggest"
// channel (proposal: /proposals/qapps_feedback_proposal_ar.html, approved
// 2026-11-01). Used by the Pages Functions in /functions/api/.
//
// Why here and not in /functions: every file under /functions becomes a
// route; shared code lives outside and is bundled in by the build.
// No secrets in this file (it is public like the rest of the repo); secrets
// come from the Pages environment (see README → "Contact & suggest").

export const APPS = ["docmatic", "vault", "countdown-keeper", "new-app", "general"];
export const TYPES = ["message", "improve", "feature", "problem"];
export const STATUSES = ["new", "review", "done", "archived"];
export const LANGS = ["ar", "en"];

export const LIMITS = {
  minText: 10,
  maxText: 2000,
  maxName: 80,
  maxContact: 120,
  perHour: 5,      // messages from one visitor in an hour
  perDay: 10,      // … and in a day
  dailyCap: 300,   // messages for the whole site in a day (env DAILY_CAP overrides)
  minMillis: 2000, // faster than this after opening the page = a robot
  maxLinks: 2,     // more links than this marks the message "suspicious"
};

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex",
    },
  });
}

export async function sha256hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// The tables are created on first use, so setting up the site needs only a
// D1 database bound as DB — no migration step. Same SQL as
// /migrations/0001_feedback.sql (kept for reference and manual setup).
const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS messages (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     created_at TEXT NOT NULL,
     app TEXT NOT NULL,
     type TEXT NOT NULL,
     body TEXT NOT NULL,
     name TEXT,
     contact TEXT,
     lang TEXT,
     status TEXT NOT NULL DEFAULT 'new',
     note TEXT,
     flagged INTEGER NOT NULL DEFAULT 0,
     updated_at TEXT
   )`,
  `CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at)`,
  `CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status)`,
  `CREATE TABLE IF NOT EXISTS rate_hits (ip_hash TEXT NOT NULL, ts INTEGER NOT NULL)`,
  `CREATE INDEX IF NOT EXISTS idx_rate_hits ON rate_hits(ip_hash, ts)`,
];

let schemaReady = null;
export function ensureSchema(db) {
  if (!schemaReady) {
    schemaReady = db.batch(SCHEMA.map((s) => db.prepare(s))).catch((e) => {
      schemaReady = null; // try again on the next request
      throw e;
    });
  }
  return schemaReady;
}

export function nowIso() {
  return new Date().toISOString();
}
