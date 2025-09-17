from __future__ import annotations

from fastapi import FastAPI

from apps.api.config import settings


def build_app() -> FastAPI:
    app = FastAPI(title=settings.api.app_name, version="0.1.0")

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = build_app()
