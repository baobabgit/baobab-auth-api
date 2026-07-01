"""Factory FastAPI ``create_app``.

:spec: BL-API-010-001, BL-API-010-002, FEAT-001.1
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from baobab_auth_api.config import AuthApiSettings
from baobab_auth_api.error_handlers import ErrorHandlerRegistry
from baobab_auth_api.infrastructure.app_state import AppState
from baobab_auth_api.infrastructure.infrastructure_factory import InfrastructureFactory
from baobab_auth_api.lifespan import AppLifespan
from baobab_auth_api.openapi import OpenApiConfigurator
from baobab_auth_api.routers.auth_router import AuthRouter
from baobab_auth_api.routers.health_router import HealthRouter
from baobab_auth_api.routers.jwks_router import JwksRouter
from baobab_auth_api.routers.permissions_router import PermissionsRouter
from baobab_auth_api.routers.roles_router import RolesRouter
from baobab_auth_api.services.auth_service import AuthService
from baobab_auth_api.services.current_user_service import CurrentUserService
from baobab_auth_api.services.rbac_service import RbacService
from baobab_auth_api.services.readiness_service import ReadinessService


class AppRouterRegistry:
    """Branche les routers une fois l'infrastructure initialisée."""

    @staticmethod
    def register(app: FastAPI, state: AppState) -> None:
        """Inclut tous les routers sur *app*.

        :param app: Application FastAPI.
        :param state: État applicatif câblé.
        """
        auth_service = AuthService(state)
        current_user_service = CurrentUserService(state)
        rbac_service = RbacService(state)
        readiness_service = ReadinessService(state)

        app.include_router(AuthRouter(auth_service, current_user_service).router)
        app.include_router(JwksRouter(state).router)
        app.include_router(RolesRouter(rbac_service).router)
        app.include_router(PermissionsRouter(rbac_service).router)
        app.include_router(HealthRouter(readiness_service).router)


def create_app(settings: AuthApiSettings | None = None) -> FastAPI:
    """Crée l'application FastAPI configurée.

    :param settings: Configuration injectée ; défaut depuis l'environnement.
    :returns: Application prête pour uvicorn ou tests ASGI.
    :spec: FEAT-001.1
    """
    resolved = settings or AuthApiSettings()
    state = InfrastructureFactory.build(resolved)
    app = FastAPI(lifespan=AppLifespan(state).lifespan)
    app.state.app_state = state

    OpenApiConfigurator.apply(app, resolved.app_name)
    ErrorHandlerRegistry.register(app)
    AppRouterRegistry.register(app, state)

    if resolved.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=resolved.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return app
