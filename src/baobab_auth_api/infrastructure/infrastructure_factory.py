"""Fabrique d'infrastructure production (database + security).

:spec: BL-API-010-002, ADR-0001
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_database import (
    AuthCatalogBootstrap,
    SqlAlchemyAuthUnitOfWork,
    SqlAlchemyEngineFactory,
    SqlAlchemySessionFactory,
)
from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_security import (
    Argon2PasswordHasher,
    CorePasswordHasherAdapter,
    CoreTokenProviderAdapter,
    InMemoryKeyProvider,
    JwtDecoder,
    JwtEncoder,
    JwtTokenProvider,
    JwtValidator,
    KeyGenerator,
    LocalJwksProvider,
    SystemClock,
)

from baobab_auth_api.config import AuthApiSettings
from baobab_auth_api.infrastructure.app_state import AppState
from baobab_auth_api.infrastructure.reentrant_unit_of_work import ReentrantUnitOfWork
from baobab_auth_api.infrastructure.timezone_aware_unit_of_work import (
    TimezoneAwareUnitOfWork,
)
from baobab_auth_api.infrastructure.uuid_id_generator import UuidIdGenerator


class InfrastructureFactory:
    """Assemble l'état applicatif à partir des settings injectés."""

    @staticmethod
    def build(settings: AuthApiSettings) -> AppState:
        """Construit l'infrastructure complète.

        :param settings: Configuration API.
        :returns: État applicatif prêt pour le lifespan.
        """
        db_settings = settings.database_settings()
        sec_settings = settings.security_settings()

        engine = SqlAlchemyEngineFactory(db_settings).create()
        AuthOrmBase.metadata.create_all(engine)
        session_factory = SqlAlchemySessionFactory(db_settings, engine=engine)
        AuthCatalogBootstrap(session_factory, catalog=DefaultAuthCatalog()).run()

        clock = SystemClock()
        key_pair = KeyGenerator(clock).generate(kid="primary")
        key_provider = InMemoryKeyProvider((key_pair,))
        jwks_provider = LocalJwksProvider(key_provider)

        issuer = sec_settings.issuer or "baobab-auth"
        audience = sec_settings.audience or "baobab-api"
        jwt_provider = JwtTokenProvider(
            JwtEncoder(key_pair.private_key, key_pair.kid),
            JwtDecoder(key_provider.public_key_for_kid),
            JwtValidator(clock, issuer=issuer, audience=audience),
            clock,
            issuer=issuer,
            audience=audience,
        )

        password_hasher = CorePasswordHasherAdapter(
            Argon2PasswordHasher(sec_settings.password_policy())
        )
        token_provider = CoreTokenProviderAdapter(
            jwt_provider,
            access_ttl_seconds=sec_settings.access_ttl_seconds,
            refresh_ttl_seconds=sec_settings.refresh_ttl_seconds,
        )

        return AppState(
            settings=settings,
            uow_factory=lambda: ReentrantUnitOfWork(
                TimezoneAwareUnitOfWork(
                    SqlAlchemyAuthUnitOfWork(session_factory),
                ),
            ),
            password_hasher=password_hasher,
            token_provider=token_provider,
            id_generator=UuidIdGenerator(),
            clock=clock,
            jwks_provider=jwks_provider,
            engine=engine,
        )
