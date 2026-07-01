"""Router JWKS public.

:spec: BL-API-010-006, FEAT-001.3
"""

from fastapi import APIRouter

from baobab_auth_api.infrastructure.app_state import AppState
from baobab_auth_api.schemas.jwks_response import JwksResponse


class JwksRouter:
    """Route ``GET /auth/jwks``."""

    def __init__(self, state: AppState) -> None:
        """Injecte l'état applicatif.

        :param state: État avec ``jwks_provider``.
        """
        self._state = state
        self._router = APIRouter(prefix="/auth", tags=["JWKS"])
        self._router.add_api_route("/jwks", self.jwks, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        """Expose le router FastAPI.

        :returns: Router configuré.
        """
        return self._router

    def jwks(self) -> JwksResponse:
        """Retourne les clés publiques JWKS.

        :returns: Document JWKS sans clé privée.
        """
        document = self._state.jwks_provider.jwks().to_dict()
        keys = document.get("keys", [])
        return JwksResponse(keys=list(keys))
