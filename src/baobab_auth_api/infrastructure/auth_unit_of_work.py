"""Protocole UoW auth exposant les repositories requis par l'API.

:spec: ADR-0001
"""

from types import TracebackType
from typing import Protocol, Self

from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.permission_repository import PermissionRepository
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.user_repository import UserRepository


class AuthUnitOfWork(Protocol):
    """Unité de travail avec repositories auth."""

    def __enter__(self) -> Self:
        """Ouvre le contexte transactionnel."""
        ...  # pragma: no cover

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Ferme le contexte transactionnel."""
        ...  # pragma: no cover

    def commit(self) -> None:
        """Valide la transaction."""
        ...  # pragma: no cover

    def rollback(self) -> None:
        """Annule la transaction."""
        ...  # pragma: no cover

    @property
    def users(self) -> UserRepository:
        """Repository utilisateurs."""
        ...  # pragma: no cover

    @property
    def sessions(self) -> SessionRepository:
        """Repository sessions."""
        ...  # pragma: no cover

    @property
    def audit(self) -> AuditRepository:
        """Repository audit."""
        ...  # pragma: no cover

    @property
    def roles(self) -> RoleRepository:
        """Repository rôles."""
        ...  # pragma: no cover

    @property
    def permissions(self) -> PermissionRepository:
        """Repository permissions."""
        ...  # pragma: no cover
