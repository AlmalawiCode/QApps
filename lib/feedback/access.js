// lib/feedback/access.js — who may read the messages.
//
// The admin page and its API sit behind Cloudflare Access (a code sent to the
// owner's email). Access adds a signed token (Cf-Access-Jwt-Assertion) to
// every request it lets through. We verify that token ourselves — signature,
// audience, issuer, expiry — so the API stays closed even if the Access rule
// is ever removed or mis-set: no valid token, no data (fails closed).
//
// Env: ACCESS_TEAM_DOMAIN (e.g. "qapps.cloudflareaccess.com"), ACCESS_AUD
// (the Access application's "Application Audience (AUD) Tag"), optional
// ADMIN_EMAILS (comma list). Local testing only: ADMIN_DEV_BYPASS=1 works on
// localhost / 127.0.0.1 and nowhere else.

let certCache = { at: 0, keys: [] };

function b64urlToBytes(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function decodePart(s) {
  return JSON.parse(new TextDecoder().decode(b64urlToBytes(s)));
}

async function accessKeys(team) {
  if (Date.now() - certCache.at < 3600_000 && certCache.keys.length) return certCache.keys;
  const res = await fetch(`https://${team}/cdn-cgi/access/certs`);
  if (!res.ok) throw new Error("access certs " + res.status);
  const data = await res.json();
  certCache = { at: Date.now(), keys: data.keys || [] };
  return certCache.keys;
}

/** Returns the signed-in owner's email, or null if the request is not allowed. */
export async function adminEmail(request, env) {
  const host = new URL(request.url).hostname;
  if (env.ADMIN_DEV_BYPASS === "1" && (host === "localhost" || host === "127.0.0.1")) {
    return "dev@localhost";
  }
  const team = env.ACCESS_TEAM_DOMAIN;
  const aud = env.ACCESS_AUD;
  const token = request.headers.get("Cf-Access-Jwt-Assertion");
  if (!team || !aud || !token) return null;

  const parts = token.split(".");
  if (parts.length !== 3) return null;
  let header, payload;
  try {
    header = decodePart(parts[0]);
    payload = decodePart(parts[1]);
  } catch {
    return null;
  }
  if (header.alg !== "RS256") return null;

  const keys = await accessKeys(team);
  const jwk = keys.find((k) => k.kid === header.kid);
  if (!jwk) return null;
  const key = await crypto.subtle.importKey(
    "jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
  const ok = await crypto.subtle.verify(
    "RSASSA-PKCS1-v1_5", key, b64urlToBytes(parts[2]),
    new TextEncoder().encode(parts[0] + "." + parts[1]));
  if (!ok) return null;

  const now = Math.floor(Date.now() / 1000);
  const auds = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
  if (!auds.includes(aud)) return null;
  if (payload.iss !== `https://${team}`) return null;
  if (!payload.exp || payload.exp < now) return null;

  const allowed = (env.ADMIN_EMAILS || "").split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
  const email = (payload.email || "").toLowerCase();
  if (allowed.length && !allowed.includes(email)) return null;
  return email || "access-user";
}
