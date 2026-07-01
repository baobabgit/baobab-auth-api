"""Unit of Work décorée avec normalisation timezone SQLite.

:spec: BL-API-010-005, ADR-0001
"""

from typing import Self

from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.permission_repository import PermissionRepository
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.user_repository import UserRepository

from baobab_auth_api.infrastructure.auth_unit_of_work import AuthUnitOfWork
from baobab_auth_api.infrastructure.session_repository_timezone_adapter import (
    SessionRepositoryTimezoneAdapter,
)


class TimezoneAwareUnitOfWork:
    """Proxy UoW remplaçant le repository sessions par l'adaptateur timezone."""

    def __init__(self, inner: AuthUnitOfWork) -> None:
        """Enveloppe une UoW SQLAlchemy.

        :param inner: Unité de travail concrète.
        """
        self._inner = inner
        self._sessions: SessionRepositoryTimezoneAdapter | None = None

    def __enter__(self) -> Self:
        """Ouvre le contexte de l'UoW interne.

        :returns: Proxy actif.
        """
        self._inner.__enter__()
        self._sessions = SessionRepositoryTimezoneAdapter(self._inner.sessions)
        return self

    def __exit__(self, *args: object) -> bool | None:
        """Ferme le contexte interne.

        :param args: Arguments de contexte.
        :returns: Résultat de l'``__exit__`` interne.
        """
        self._sessions = None
        return self._inner.__exit__(*args)  # type: ignore[arg-type]

    def commit(self) -> None:
        """Valide la transaction."""
        self._inner.commit()

    def rollback(self) -> None:
        """Annule la transaction."""
        self._inner.rollback()

    @property
    def users(self) -> UserRepository:
        """Repository utilisateurs délégué."""
        return self._inner.users

    @property
    def sessions(self) -> SessionRepository:
        """Repository sessions avec normalisation timezone."""
        if self._sessions is None:
            return SessionRepositoryTimezoneAdapter(self._inner.sessions)
        return self._sessions

    @property
    def audit(self) -> AuditRepository:
        """Repository audit délégué."""
        return self._inner.audit

    @property
    def roles(self) -> RoleRepository:
        """Repository rôles délégué."""
        return self._inner.roles

    @property
    def permissions(self) -> PermissionRepository:
        """Repository permissions délégué."""
        return self._inner.permissions
