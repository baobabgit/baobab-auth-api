"""Tests API authentification bout en bout.

:spec: BL-API-010-008, FEAT-001.2
"""

import pytest
from httpx import AsyncClient


class TestAuthApiFlow:
    """Scénarios obligatoires du cahier des charges v0.1.0."""

    @pytest.mark.asyncio
    async def test_BL_API_010_008_register_nominal_201(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Register nominal -> 201."""
        response = await client.post(
            "/auth/register",
            json={"email": "user@example.com", "password": strong_password},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "user@example.com"
        assert "auth_subject" in body

    @pytest.mark.asyncio
    async def test_BL_API_010_008_register_email_existant_409(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Register email existant -> 409."""
        payload = {"email": "dup@example.com", "password": strong_password}
        await client.post("/auth/register", json=payload)
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "conflict"

    @pytest.mark.asyncio
    async def test_BL_API_010_008_login_nominal_200(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Login nominal -> 200 avec tokens."""
        email = "login@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": strong_password},
        )
        response = await client.post(
            "/auth/login",
            json={"email": email, "password": strong_password},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["token_type"] == "bearer"
        assert body["access_token"]
        assert body["refresh_token"]
        assert body["expires_in"] > 0

    @pytest.mark.asyncio
    async def test_BL_API_010_008_login_invalid_password_401(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Login mot de passe invalide -> 401 générique."""
        email = "badpass@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": strong_password},
        )
        response = await client.post(
            "/auth/login",
            json={"email": email, "password": "WrongPass1!"},
        )
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "invalid_credentials"

    @pytest.mark.asyncio
    async def test_BL_API_010_008_refresh_nominal_200(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Refresh nominal -> 200."""
        email = "refresh@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": strong_password},
        )
        login = await client.post(
            "/auth/login",
            json={"email": email, "password": strong_password},
        )
        refresh_token = login.json()["refresh_token"]
        response = await client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        assert response.json()["access_token"]

    @pytest.mark.asyncio
    async def test_BL_API_010_008_logout_nominal_204(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Logout nominal -> 204."""
        email = "logout@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": strong_password},
        )
        login = await client.post(
            "/auth/login",
            json={"email": email, "password": strong_password},
        )
        access_token = login.json()["access_token"]
        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_BL_API_010_008_me_sans_token_401(
        self,
        client: AsyncClient,
    ) -> None:
        """Me sans token -> 401."""
        response = await client.get("/auth/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_BL_API_010_008_me_avec_token_200(
        self,
        client: AsyncClient,
        strong_password: str,
    ) -> None:
        """Me avec token valide -> 200."""
        email = "me@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": strong_password},
        )
        login = await client.post(
            "/auth/login",
            json={"email": email, "password": strong_password},
        )
        access_token = login.json()["access_token"]
        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["email"] == email
        assert "USER" in body["roles"]

    @pytest.mark.asyncio
    async def test_BL_API_010_008_jwks_sans_cle_privee(
        self,
        client: AsyncClient,
    ) -> None:
        """JWKS ne contient aucune clé privée."""
        response = await client.get("/auth/jwks")
        assert response.status_code == 200
        keys = response.json()["keys"]
        assert len(keys) >= 1
        for key in keys:
            assert "d" not in key
            assert "p" not in key

    @pytest.mark.asyncio
    async def test_BL_API_010_008_roles_permissions_catalogue(
        self,
        client: AsyncClient,
    ) -> None:
        """Roles/permissions reflètent le catalogue core."""
        roles = await client.get("/auth/roles")
        permissions = await client.get("/auth/permissions")
        assert roles.status_code == 200
        assert permissions.status_code == 200
        assert len(roles.json()) >= 1
        assert len(permissions.json()) >= 1

    @pytest.mark.asyncio
    async def test_BL_API_010_008_health_ok(self, client: AsyncClient) -> None:
        """Health renvoie ok."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @pytest.mark.asyncio
    async def test_BL_API_010_008_ready_ok(self, client: AsyncClient) -> None:
        """Ready renvoie 200 quand DB disponible."""
        response = await client.get("/ready")
        assert response.status_code == 200
