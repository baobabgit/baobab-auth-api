"""Fixtures pytest partagées."""

from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from baobab_auth_api.testing.test_app_factory import TestAppFactory

_STRONG_PASSWORD = "Str0ng!Passw0rd"


@pytest.fixture
def strong_password() -> str:
    """Mot de passe conforme à la politique core.

    :returns: Mot de passe de test.
    """
    return _STRONG_PASSWORD


@pytest.fixture
async def client(tmp_path: Path) -> AsyncIterator[AsyncClient]:
    """Client HTTP async contre une app SQLite fichier.

    :param tmp_path: Répertoire temporaire pytest.
    :yields: Client httpx configuré.
    """
    db_file = tmp_path / "test.db"
    app = TestAppFactory.create(db_file)
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as http_client:
        yield http_client
