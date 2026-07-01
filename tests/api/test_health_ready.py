"""Tests health router readiness 503."""

import pytest
from httpx import AsyncClient


class TestHealthReadyFailure:
    @pytest.mark.asyncio
    async def test_BL_API_010_007_ready_503_sans_jwks(
        self,
        client: AsyncClient,
    ) -> None:
        """Ready renvoie 503 si JWKS vide."""
        state = client._transport.app.state.app_state  # type: ignore[attr-defined]
        original = state.jwks_provider.jwks
        state.jwks_provider.jwks = lambda: type("J", (), {"keys": []})()
        try:
            response = await client.get("/ready")
            assert response.status_code == 503
        finally:
            state.jwks_provider.jwks = original
