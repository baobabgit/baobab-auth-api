"""Tests gestionnaires d'erreurs.

:spec: BL-API-010-002
"""

import pytest
from baobab_auth_core.exceptions.auth import InvalidCredentialsError
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.exceptions.validation import WeakPasswordError
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from baobab_auth_api.error_handlers import ErrorHandlerRegistry
from baobab_auth_api.exceptions.api_http_error import ApiHttpError


class TestErrorHandlerRegistry:
    @staticmethod
    def _app_with_route(exc: Exception) -> FastAPI:
        app = FastAPI()
        ErrorHandlerRegistry.register(app)

        @app.get("/boom")
        def boom() -> None:
            raise exc

        return app

    @pytest.mark.asyncio
    async def test_FEAT_001_2_invalid_credentials_handler(self) -> None:
        app = self._app_with_route(InvalidCredentialsError("x"))
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://t") as client:
            response = await client.get("/boom")
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "invalid_credentials"

    @pytest.mark.asyncio
    async def test_FEAT_001_2_forbidden_handler(self) -> None:
        app = self._app_with_route(ForbiddenError("denied"))
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://t") as client:
            response = await client.get("/boom")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_FEAT_001_2_not_found_handler(self) -> None:
        app = self._app_with_route(UserNotFoundError("missing"))
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://t") as client:
            response = await client.get("/boom")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_FEAT_001_2_validation_handler(self) -> None:
        app = self._app_with_route(WeakPasswordError("weak"))
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://t") as client:
            response = await client.get("/boom")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_FEAT_001_2_api_http_error_handler(self) -> None:
        app = self._app_with_route(ApiHttpError("custom", "msg", 418))
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://t") as client:
            response = await client.get("/boom")
        assert response.status_code == 418
