"""Dépendance FastAPI pour l'utilisateur courant.

:spec: BL-API-010-005
"""

from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from baobab_auth_api.exceptions.api_http_error import ApiHttpError
from baobab_auth_api.infrastructure.app_state import AppState
from baobab_auth_api.security.bearer_claims import BearerClaims

_bearer_scheme = HTTPBearer(auto_error=False)


class CurrentUserDependency:
    """Extrait et valide le Bearer token depuis la requête."""

    @staticmethod
    def get_state(request: Request) -> AppState:
        """Retourne l'état applicatif depuis ``app.state``.

        :param request: Requête HTTP courante.
        :returns: État initialisé au lifespan.
        """
        state: AppState = request.app.state.app_state
        return state

    @staticmethod
    def get_bearer_claims(
        request: Request,
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(_bearer_scheme),
        ],
    ) -> BearerClaims:
        """Valide le token Bearer et retourne les claims utiles.

        :param request: Requête HTTP.
        :param credentials: En-tête Authorization.
        :returns: Claims ``sub`` et ``sid``.
        :raises ApiHttpError: Si le token est absent ou invalide.
        """
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise ApiHttpError("unauthorized", "Unauthorized", 401)
        state = CurrentUserDependency.get_state(request)
        try:
            payload = state.token_provider.verify_access_token(credentials.credentials)
        except Exception as exc:
            raise ApiHttpError("unauthorized", "Unauthorized", 401) from exc
        subject = payload.get("sub")
        if not subject:
            raise ApiHttpError("unauthorized", "Unauthorized", 401)
        sid = payload.get("sid")
        return BearerClaims(subject=str(subject), session_id=str(sid) if sid else None)
