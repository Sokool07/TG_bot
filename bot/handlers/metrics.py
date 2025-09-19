import prometheus_client
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response


class MetricsView(web.View):
    def __init__(
        self,
        request: Request,
        registry: prometheus_client.CollectorRegistry = prometheus_client.REGISTRY,
    ) -> None:
        self._request = request
        self.registry = registry

    async def get(self) -> Response:
        response = Response(body=prometheus_client.generate_latest(self.registry))
        response.content_type = prometheus_client.CONTENT_TYPE_LATEST
        return response


class HealthView(web.View):
    """Health check endpoint для мониторинга состояния бота"""
    
    async def get(self) -> Response:
        return web.json_response({
            "status": "healthy",
            "service": "telegram-bot",
            "version": "2.4.0"
        })
