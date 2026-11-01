// workers/digest/src/index.js — the owner's daily email of new website messages.
//
// Why a separate Worker: the site runs on Cloudflare Pages, and Pages Functions
// cannot run on a schedule. This Worker has a Cron Trigger (wrangler.toml), reads
// the same D1 database as /functions/api/feedback.js, and emails a summary of the
// last 24 hours through Cloudflare Email Routing (send_email binding).
//
// Nothing is sent on a day with no new messages. The recipient comes from the
// DIGEST_TO secret (never in this public file); it must be a verified destination
// address in Email Routing, or Cloudflare refuses to deliver.

import { EmailMessage } from "cloudflare:email";

const SITE = "https://qeuapps.com";
const LOOKBACK_MS = 24 * 60 * 60 * 1000;
const MAX_LISTED = 30;   // longer days list the first 30 and link to the dashboard
const SNIPPET = 400;     // characters of each message shown in the email

const APP_AR = {
  docmatic: "DocMatic",
  vault: "خزنة الضمانات",
  "countdown-keeper": "كم مضى وكم بقي",
  "new-app": "فكرة لتطبيق جديد",
  general: "الموقع / رأي عام",
};
const TYPE_AR = {
  message: "رسالة أو سؤال",
  improve: "اقتراح تحسين",
  feature: "فكرة ميزة جديدة",
  problem: "مشكلة واجهتني",
};

export default {
  async scheduled(_event, env, ctx) {
    ctx.waitUntil(sendDigest(env));
  },
};

export async function sendDigest(env, now = new Date()) {
  if (!env.DB || !env.EMAIL || !env.DIGEST_TO) {
    console.log("digest: not configured (DB, EMAIL or DIGEST_TO missing)");
    return { sent: false, reason: "not_configured" };
  }
  const since = new Date(now.getTime() - LOOKBACK_MS).toISOString();
  const [rows, total, open] = await env.DB.batch([
    env.DB.prepare(
      "SELECT id, created_at, app, type, body, name, contact, flagged FROM messages " +
      "WHERE created_at >= ? ORDER BY created_at ASC LIMIT ?"
    ).bind(since, MAX_LISTED),
    env.DB.prepare("SELECT COUNT(*) AS n FROM messages WHERE created_at >= ?").bind(since),
    env.DB.prepare("SELECT COUNT(*) AS n FROM messages WHERE status = 'new'"),
  ]);
  const list = rows.results;
  const count = total.results[0]?.n || 0;
  const waiting = open.results[0]?.n || 0;
  if (!count) {
    console.log("digest: nothing new");
    return { sent: false, reason: "nothing_new" };
  }

  const subject = `كيو آبز: ${countAr(count)} من الموقع`;
  const from = env.DIGEST_FROM || "digest@qeuapps.com";
  const raw = buildMime({
    from, fromName: "Q Apps", to: env.DIGEST_TO, subject,
    text: renderText(list, count, waiting),
    html: renderHtml(list, count, waiting),
  });
  await env.EMAIL.send(new EmailMessage(from, env.DIGEST_TO, raw));
  console.log(`digest: sent ${count} message(s)`);
  return { sent: true, count };
}

// ---------- content ----------

function riyadhTime(iso) {
  try {
    return new Date(iso).toLocaleString("ar-SA-u-ca-gregory-nu-latn", {
      timeZone: "Asia/Riyadh", day: "numeric", month: "long", hour: "numeric", minute: "2-digit",
    });
  } catch {
    return iso;
  }
}

// Arabic number agreement: 1 / 2 / 3–10 / 11+.
function countAr(n) {
  if (n === 1) return "رسالة جديدة واحدة";
  if (n === 2) return "رسالتان جديدتان";
  if (n <= 10) return `${n} رسائل جديدة`;
  return `${n} رسالة جديدة`;
}
function moreAr(n) {
  return n === 1 ? "ورسالة أخرى" : n === 2 ? "ورسالتان أخريان" : n <= 10 ? `و${n} رسائل أخرى` : `و${n} رسالة أخرى`;
}

function cut(s) {
  s = String(s || "").trim();
  return s.length > SNIPPET ? s.slice(0, SNIPPET) + "…" : s;
}

function renderText(list, count, waiting) {
  const lines = [`وصلت ${countAr(count)} خلال آخر 24 ساعة.`, ""];
  for (const m of list) {
    lines.push(`— ${APP_AR[m.app] || m.app} · ${TYPE_AR[m.type] || m.type} · ${riyadhTime(m.created_at)}${m.flagged ? " · ⚠ مشبوهة" : ""}`);
    lines.push(cut(m.body));
    if (m.name || m.contact) lines.push([m.name, m.contact].filter(Boolean).join(" · "));
    lines.push("");
  }
  if (count > list.length) lines.push(`${moreAr(count - list.length)} في لوحة الرسائل.`, "");
  lines.push(`رسائل بحالة «جديدة» تنتظرك: ${waiting}`);
  lines.push(`افتح لوحة الرسائل: ${SITE}/admin/`);
  return lines.join("\n");
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

function renderHtml(list, count, waiting) {
  const items = list.map((m) => `
    <tr><td style="padding:14px 16px;border-bottom:1px solid #e3ecec">
      <div style="font-size:13px;color:#0f766e;font-weight:bold">${esc(APP_AR[m.app] || m.app)} · ${esc(TYPE_AR[m.type] || m.type)}
        <span style="color:#6b7f7f;font-weight:normal"> · ${esc(riyadhTime(m.created_at))}</span>
        ${m.flagged ? '<span style="color:#b45309"> · ⚠ مشبوهة</span>' : ""}</div>
      <div dir="auto" style="margin-top:6px;font-size:15px;line-height:1.7;color:#1f2d2d;white-space:pre-wrap">${esc(cut(m.body))}</div>
      ${m.name || m.contact ? `<div style="margin-top:6px;font-size:13px;color:#6b7f7f">${esc([m.name, m.contact].filter(Boolean).join(" · "))}</div>` : ""}
    </td></tr>`).join("");
  const more = count > list.length
    ? `<p style="margin:12px 0 0;color:#6b7f7f">${moreAr(count - list.length)} في لوحة الرسائل.</p>` : "";
  return `<!DOCTYPE html><html lang="ar" dir="rtl"><body style="margin:0;background:#f4f8f8;font-family:Tahoma,Arial,sans-serif">
  <div style="max-width:640px;margin:0 auto;padding:24px 16px" dir="rtl">
    <h1 style="font-size:20px;color:#0f766e;margin:0 0 6px">رسائل جديدة من الموقع</h1>
    <p style="margin:0 0 16px;color:#1f2d2d">وصلت <b>${countAr(count)}</b> خلال آخر 24 ساعة.</p>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#fff;border:1px solid #e3ecec;border-radius:12px;border-collapse:separate">${items}</table>
    ${more}
    <p style="margin:18px 0 0;color:#1f2d2d">رسائل بحالة «جديدة» تنتظرك: <b>${waiting}</b></p>
    <p style="margin:18px 0 0"><a href="${SITE}/admin/" style="display:inline-block;background:#0f766e;color:#fff;text-decoration:none;padding:10px 18px;border-radius:10px">افتح لوحة الرسائل</a></p>
    <p style="margin:24px 0 0;font-size:12px;color:#8a9b9b">ملخص يومي آلي من qeuapps.com — يُرسل فقط في الأيام التي فيها رسائل جديدة.</p>
  </div></body></html>`;
}

// ---------- MIME (send_email takes a raw RFC 5322 message) ----------

function b64(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}
function wrap76(s) {
  return s.replace(/.{1,76}/g, "$&\r\n").trimEnd();
}
function encWord(s) {
  return `=?UTF-8?B?${b64(s)}?=`;
}

export function buildMime({ from, fromName, to, subject, text, html }) {
  const boundary = "qapps-" + crypto.randomUUID();
  const domain = from.split("@")[1] || "qeuapps.com";
  return [
    `From: ${encWord(fromName)} <${from}>`,
    `To: <${to}>`,
    `Subject: ${encWord(subject)}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@${domain}>`,
    "MIME-Version: 1.0",
    `Content-Type: multipart/alternative; boundary="${boundary}"`,
    "",
    `--${boundary}`,
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "",
    wrap76(b64(text)),
    `--${boundary}`,
    "Content-Type: text/html; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
    "",
    wrap76(b64(html)),
    `--${boundary}--`,
    "",
  ].join("\r\n");
}
