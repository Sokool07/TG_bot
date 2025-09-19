FROM ghcr.io/astral-sh/uv:0.5-python3.13-alpine

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/usr/src/app/.venv/bin:$PATH"

WORKDIR /usr/src/app

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --group bot --no-group admin --no-group dev \
    && uv add requests \
    && pybabel compile -d ./bot/locales \
    && adduser -D appuser \
    && chown -R appuser:appuser .

USER appuser

# Timeweb Cloud ожидает приложение на порту 8080
EXPOSE 8080

# Добавляем healthcheck для мониторинга
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

CMD ["python", "-m", "bot"]
