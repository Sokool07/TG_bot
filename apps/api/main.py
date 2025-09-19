from __future__ import annotations
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from apps.api.config import settings

BASE_DIR = Path(__file__).resolve().parents[2]
NOTCOIN_DIST_DIR = BASE_DIR / "webapps" / "notcoin" / "dist"


def build_app() -> FastAPI:
    app = FastAPI(title=settings.api.app_name, version="0.1.0")

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    if NOTCOIN_DIST_DIR.exists():
        logger.info("Mounting NotCoin mini app from %s", NOTCOIN_DIST_DIR)
        app.mount(
            "/notcoin",
            StaticFiles(directory=NOTCOIN_DIST_DIR, html=True),
            name="notcoin-mini-app",
        )
    else:
        logger.warning("NotCoin mini app directory %s not found; static files not mounted", NOTCOIN_DIST_DIR)

    return app


app = build_app()
