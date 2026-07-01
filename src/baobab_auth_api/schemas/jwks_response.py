"""Réponse JWKS publique.

:spec: BL-API-010-003, FEAT-001.3
"""

from typing import Any

from pydantic import BaseModel


class JwksResponse(BaseModel):
    """Corps de ``GET /auth/jwks``.

    :param keys: Clés publiques JWK.
    """

    keys: list[dict[str, Any]]
