"""Claims d'authentification extraites du Bearer token.

:spec: BL-API-010-005
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BearerClaims:
    """Claims minimales extraites d'un access token valide.

    :param subject: Claim ``sub``.
    :param session_id: Claim ``sid`` (optionnel).
    """

    subject: str
    session_id: str | None
