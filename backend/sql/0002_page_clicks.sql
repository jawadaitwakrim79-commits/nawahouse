-- ─────────────────────────────────────────────────────────────────────────────
-- Nawa House — admin dashboard migration
-- Run this directly against your Postgres database if you prefer not to use
-- Alembic:
--
--   psql "$DATABASE_URL" -f backend/sql/0002_page_clicks.sql
--
-- Idempotent: safe to re-run.
-- ─────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS page_clicks (
  id              BIGSERIAL PRIMARY KEY,
  session_id      TEXT        NOT NULL,
  path            TEXT        NOT NULL,
  referrer        TEXT,
  utm_source      TEXT,
  utm_medium      TEXT,
  utm_campaign    TEXT,
  fbclid          TEXT,
  ttclid          TEXT,
  sc_click_id     TEXT,
  client_ip       TEXT,
  user_agent      TEXT,
  country_code    TEXT,
  is_vpn          BOOLEAN     NOT NULL DEFAULT FALSE,
  is_valid_ksa    BOOLEAN     NOT NULL DEFAULT FALSE,
  intel_source    TEXT,
  risk_score      INTEGER,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS page_clicks_session_idx    ON page_clicks (session_id);
CREATE INDEX IF NOT EXISTS page_clicks_ip_idx         ON page_clicks (client_ip);
CREATE INDEX IF NOT EXISTS page_clicks_country_idx    ON page_clicks (country_code);
CREATE INDEX IF NOT EXISTS page_clicks_valid_ksa_idx  ON page_clicks (is_valid_ksa);
CREATE INDEX IF NOT EXISTS page_clicks_created_idx    ON page_clicks (created_at);
