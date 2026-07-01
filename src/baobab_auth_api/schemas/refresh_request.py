"""Requête de rafraîchissement de session.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, Field


class RefreshRequest(BaseModel):
    """Corps de ``POST /auth/refresh``.

    :param refresh_token: Token de rafraîchissement.
    """

    refresh_token: str = Field(min_length=1)
