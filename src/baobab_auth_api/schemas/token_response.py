"""Réponse token OAuth2-like.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Corps de réponse login/refresh.

    :param access_token: JWT d'accès.
    :param refresh_token: Token de rafraîchissement.
    :param token_type: Type de token (``bearer``).
    :param expires_in: TTL access token en secondes.
    """

    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer")
    expires_in: int
