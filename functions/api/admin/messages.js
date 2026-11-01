// functions/api/admin/messages.js — the owner's dashboard API (/admin/).
//   GET  /api/admin/messages?app=&type=&status=&q=&offset=  → messages + counts
//   POST /api/admin/messages {id, status?, note?}           → update one message
// Every request must pass Cloudflare Access (lib/feedback/access.js); without
// a valid Access token the answer is 401 and no data leaves the database.

import { APPS, TYPES, STATUSES, json, ensureSchema, nowIso } from "../../../lib/feedback/common.js";
import { adminEmail } from "../../../lib/feedback/access.js";

const PAGE = 50;

async function guard(request, env) {
  if (!env.DB) return json({ ok: false, error: "not_configured" }, 503);
  let who = null;
  try {
    who = await adminEmail(request, env);
  } catch {
    who = null;
  }
  if (!who) return json({ ok: false, error: "unauthorized" }, 401);
  await ensureSchema(env.DB);
  return null;
}

export async function onRequestGet({ request, env }) {
  const denied = await guard(request, env);
  if (denied) return denied;
  const db = env.DB;
  const u = new URL(request.url);
  const app = u.searchParams.get("app") || "";
  const type = u.searchParams.get("type") || "";
  const status = u.searchParams.get("status") || "";
  const q = (u.searchParams.get("q") || "").trim().slice(0, 100);
  const offset = Math.max(0, Number(u.searchParams.get("offset")) || 0);

  const where = [];
  const args = [];
  if (APPS.includes(app)) { where.push("app = ?"); args.push(app); }
  if (TYPES.includes(type)) { where.push("type = ?"); args.push(type); }
  if (STATUSES.includes(status)) { where.push("status = ?"); args.push(status); }
  else { where.push("status != 'archived'"); }
  if (q) {
    where.push("(body LIKE ? OR name LIKE ? OR contact LIKE ? OR note LIKE ?)");
    const like = `%${q.replace(/[%_]/g, "")}%`;
    args.push(like, like, like, like);
  }
  const w = where.length ? "WHERE " + where.join(" AND ") : "";

  const weekAgo = new Date(Date.now() - 7 * 86_400_000).toISOString();
  const [rows, total, byStatus, byApp, week] = await db.batch([
    db.prepare(`SELECT * FROM messages ${w} ORDER BY created_at DESC LIMIT ${PAGE} OFFSET ?`).bind(...args, offset),
    db.prepare(`SELECT COUNT(*) AS n FROM messages ${w}`).bind(...args),
    db.prepare("SELECT status, COUNT(*) AS n FROM messages GROUP BY status"),
    db.prepare("SELECT app, COUNT(*) AS n FROM messages WHERE status != 'archived' GROUP BY app"),
    db.prepare("SELECT type, COUNT(*) AS n FROM messages WHERE created_at >= ? GROUP BY type").bind(weekAgo),
  ]);
  return json({
    ok: true,
    messages: rows.results,
    total: total.results[0]?.n || 0,
    page: PAGE,
    offset,
    counts: {
      status: Object.fromEntries(byStatus.results.map((r) => [r.status, r.n])),
      app: Object.fromEntries(byApp.results.map((r) => [r.app, r.n])),
      week: Object.fromEntries(week.results.map((r) => [r.type, r.n])),
    },
  });
}

export async function onRequestPost({ request, env }) {
  const denied = await guard(request, env);
  if (denied) return denied;
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: "bad_request" }, 400);
  }
  const id = Number(data.id);
  if (!Number.isInteger(id) || id <= 0) return json({ ok: false, error: "bad_request" }, 400);
  const sets = [];
  const args = [];
  if (data.status !== undefined) {
    if (!STATUSES.includes(data.status)) return json({ ok: false, error: "bad_request" }, 400);
    sets.push("status = ?"); args.push(data.status);
  }
  if (data.note !== undefined) {
    sets.push("note = ?"); args.push(String(data.note).slice(0, 2000));
  }
  if (!sets.length) return json({ ok: false, error: "bad_request" }, 400);
  sets.push("updated_at = ?"); args.push(nowIso());
  const r = await env.DB.prepare(`UPDATE messages SET ${sets.join(", ")} WHERE id = ?`).bind(...args, id).run();
  return json({ ok: true, changed: r.meta?.changes ?? 0 });
}

export function onRequest() {
  return json({ ok: false, error: "method" }, 405);
}
