"""Router HTTP authentification.

:spec: BL-API-010-004, BL-API-010-005, FEAT-001.2
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from baobab_auth_api.mappers.me_response_mapper import MeResponseMapper
from baobab_auth_api.mappers.register_response_mapper import RegisterResponseMapper
from baobab_auth_api.mappers.token_response_mapper import TokenResponseMapper
from baobab_auth_api.schemas.login_request import LoginRequest
from baobab_auth_api.schemas.me_response import MeResponse
from baobab_auth_api.schemas.refresh_request import RefreshRequest
from baobab_auth_api.schemas.register_request import RegisterRequest
from baobab_auth_api.schemas.register_response import RegisterResponse
from baobab_auth_api.schemas.token_response import TokenResponse
from baobab_auth_api.security.bearer_claims import BearerClaims
from baobab_auth_api.security.current_user_dependency import CurrentUserDependency
from baobab_auth_api.services.auth_service import AuthService
from baobab_auth_api.services.current_user_service import CurrentUserService


class AuthRouter:
    """Routes ``/auth/*`` pour register, login, refresh, logout et me."""

    def __init__(
        self,
        auth_service: AuthService,
        current_user_service: CurrentUserService,
    ) -> None:
        """Initialise le router avec les services injectés.

        :param auth_service: Service d'authentification.
        :param current_user_service: Service identité courante.
        """
        self._auth = auth_service
        self._current_user = current_user_service
        self._router = APIRouter(prefix="/auth", tags=["Auth"])
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        """Expose le router FastAPI.

        :returns: Router configuré.
        """
        return self._router

    def _register_routes(self) -> None:
        """Enregistre les handlers HTTP."""
        self._router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            response_model=RegisterResponse,
            status_code=status.HTTP_201_CREATED,
        )
        self._router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=TokenResponse,
        )
        self._router.add_api_route(
            "/refresh",
            self.refresh,
            methods=["POST"],
            response_model=TokenResponse,
        )
        self._router.add_api_route(
            "/logout",
            self.logout,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self._router.add_api_route(
            "/me",
            self.me,
            methods=["GET"],
            response_model=MeResponse,
        )

    def register(
        self,
        body: RegisterRequest,
        request: Request,
    ) -> RegisterResponse:
        """Inscrit un nouvel utilisateur.

        :param body: Données d'inscription.
        :param request: Requête HTTP (IP, User-Agent).
        :returns: Utilisateur créé.
        """
        result = self._auth.register(
            email=str(body.email),
            password=body.password,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        return RegisterResponseMapper.to_response(result)

    def login(self, body: LoginRequest, request: Request) -> TokenResponse:
        """Authentifie un utilisateur.

        :param body: Identifiants.
        :param request: Requête HTTP.
        :returns: Paire de tokens.
        """
        result = self._auth.login(
            email=str(body.email),
            password=body.password,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        return TokenResponseMapper.to_response(result.tokens)

    def refresh(self, body: RefreshRequest, request: Request) -> TokenResponse:
        """Rafraîchit une session.

        :param body: Refresh token.
        :param request: Requête HTTP.
        :returns: Nouvelle paire de tokens.
        """
        result = self._auth.refresh(
            refresh_token=body.refresh_token,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        return TokenResponseMapper.to_response(result.tokens)

    def logout(
        self,
        claims: Annotated[
            BearerClaims, Depends(CurrentUserDependency.get_bearer_claims)
        ],
    ) -> Response:
        """Déconnecte la session du porteur.

        :param claims: Claims extraites du Bearer token.
        :returns: Réponse 204 sans corps.
        """
        if claims.session_id is not None:
            self._auth.logout(claims.session_id, claims.subject)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    def me(
        self,
        claims: Annotated[
            BearerClaims, Depends(CurrentUserDependency.get_bearer_claims)
        ],
    ) -> MeResponse:
        """Retourne l'identité courante.

        :param claims: Claims extraites du Bearer token.
        :returns: Profil utilisateur avec RBAC.
        """
        user = self._current_user.get_me(claims.subject)
        return MeResponseMapper.to_response(user)
