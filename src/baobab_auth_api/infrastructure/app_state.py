"""État applicatif partagé (lifespan FastAPI).

:spec: BL-API-010-002, ADR-0001
"""

from collections.abc import Callable
from dataclasses import dataclass

from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.password_hasher import PasswordHasher
from baobab_auth_core.ports.token_provider import TokenProvider
from baobab_auth_security import LocalJwksProvider
from sqlalchemy.engine import Engine

from baobab_auth_api.config import AuthApiSettings
from baobab_auth_api.infrastructure.reentrant_unit_of_work import ReentrantUnitOfWork


@dataclass(frozen=True)
class AppState:
    """Conteneur d'état initialisé au démarrage de l'application.

    :param settings: Configuration API.
    :param uow_factory: Fabrique d'unités de travail.
    :param password_hasher: Port de hachage mot de passe.
    :param token_provider: Port d'émission et validation de tokens.
    :param id_generator: Générateur d'identifiants.
    :param clock: Horloge injectée.
    :param jwks_provider: Fournisseur JWKS public.
    :param engine: Moteur SQLAlchemy pour readiness.
    :spec: ADR-0001
    """

    settings: AuthApiSettings
    uow_factory: Callable[[], ReentrantUnitOfWork]
    password_hasher: PasswordHasher
    token_provider: TokenProvider
    id_generator: IdGenerator
    clock: Clock
    jwks_provider: LocalJwksProvider
    engine: Engine
