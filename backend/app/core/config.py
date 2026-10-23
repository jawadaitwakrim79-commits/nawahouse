from __future__ import annotations

import re
from pydantic_settings import BaseSettings, SettingsConfigDict


def _normalize_db_url(raw: str) -> str:
    """Convert postgres:// / postgresql:// to postgresql+asyncpg://, strip sslmode."""
    url = re.sub(r"^postgres(ql)?://", "postgresql+asyncpg://", raw)
    # Remove ?sslmode=... or &sslmode=...
    url = re.sub(r"[?&]sslmode=[^&]*", "", url)
    url = url.rstrip("?&")
    return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://nawahouse:nawahouse@localhost:5432/nawahouse"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return _normalize_db_url(self.DATABASE_URL)

    # CORS
    CORS_ORIGINS: str = "https://nawahouse.shop"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    PUBLIC_SITE_URL: str = "https://nawahouse.shop"

    # Sheet
    SHEET_WEBHOOK_URL: str = ""
    SHEET_WEBHOOK_SECRET: str = ""

    # Meta
    META_PIXEL_ID: str = ""
    META_CAPI_ACCESS_TOKEN: str = ""
    META_TEST_EVENT_CODE: str = ""

    # TikTok
    TIKTOK_PIXEL_CODE: str = ""
    TIKTOK_ACCESS_TOKEN: str = ""
    TIKTOK_TEST_EVENT_CODE: str = ""

    # Snap
    SNAP_PIXEL_ID: str = ""
    SNAP_CAPI_ACCESS_TOKEN: str = ""
    SNAP_TEST_EVENT_CODE: str = ""

    # ── Admin dashboard ──
    # Either ADMIN_TOKEN, or both ADMIN_USERNAME and ADMIN_PASSWORD.
    # The token is read from the environment only. It is never given a default.
    ADMIN_TOKEN: str = ""
    ADMIN_USERNAME: str = ""
    ADMIN_PASSWORD: str = ""

    # ── IP intelligence ──
    # MaxMind GeoIP2 — local MMDB file path.
    # Default matches the Docker image path (backend/data/ → COPY . . → /app/data/).
    MAXMIND_DB_PATH: str = "/app/data/GeoLite2-Country.mmdb"
    # Fallback: MaxMind Web Services (minFraud / GeoIP2 Precision) credentials.
    MAXMIND_ACCOUNT_ID: str = ""
    MAXMIND_LICENSE_KEY: str = ""

    # VPN / proxy detection — second provider. One of: "ipqualityscore",
    # "proxycheck", "ipinfo", or empty to disable. The API key below is
    # scoped to whichever provider is selected.
    VPN_PROVIDER: str = ""
    VPN_API_KEY: str = ""

    # Dashboard click metrics. Order creation always requires country SA
    # and does not consult this flag.
    STRICT_KSA_ONLY: bool = True


settings = Settings()
