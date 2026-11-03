-- 0002_message_source.sql — mark messages sent from inside an app.
-- ADDITIVE ONLY: four nullable columns; existing rows are untouched.
-- The API adds these itself on first use (lib/feedback/common.js → upgrade);
-- this file is the same SQL, for reference or manual setup:
--   npx wrangler d1 execute qapps-feedback --remote --file migrations/0002_message_source.sql
ALTER TABLE messages ADD COLUMN source TEXT;       -- app | web
ALTER TABLE messages ADD COLUMN platform TEXT;     -- ios | android
ALTER TABLE messages ADD COLUMN app_version TEXT;  -- e.g. 1.0.4+15
ALTER TABLE messages ADD COLUMN user_lang TEXT;    -- visitor's real language, e.g. ja
CREATE INDEX IF NOT EXISTS idx_messages_source ON messages(source);
