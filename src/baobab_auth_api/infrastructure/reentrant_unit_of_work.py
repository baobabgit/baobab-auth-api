"""Unit of Work réentrant pour les cas d'usage core.

Les cas d'usage ouvrent ``with uow:`` en interne ; ce wrapper évite
l'ouverture d'une seconde session SQLAlchemy lorsque l'appelant a déjà
entré le contexte.

:spec: BL-API-010-004, ADR-0001
"""

from types import TracebackType
from typing import Self

from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.permission_repository import PermissionRepository
from baobab_auth_core.ports.role_repository import RoleRepository
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.user_repository import UserRepository

from baobab_auth_api.infrastructure.auth_unit_of_work import AuthUnitOfWork


class ReentrantUnitOfWork:
    """Proxy réentrant autour d'une :class:`AuthUnitOfWork` concrète."""

    def __init__(self, inner: AuthUnitOfWork) -> None:
        """Enveloppe une UoW existante.

        :param inner: Unité de travail déléguée.
        """
        self._inner = inner
        self._depth = 0

    def __enter__(self) -> Self:
        """Entre dans le contexte une seule fois réellement.

        :returns: Le proxy actif.
        """
        self._depth += 1
        if self._depth == 1:
            self._inner.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Sort du contexte lorsque la profondeur retombe à zéro.

        :param exc_type: Type d'exception éventuelle.
        :param exc_val: Valeur d'exception éventuelle.
        :param exc_tb: Traceback éventuel.
        :returns: Résultat de l'``__exit__`` interne.
        """
        self._depth -= 1
        if self._depth == 0:
            return self._inner.__exit__(exc_type, exc_val, exc_tb)
        return None

    def commit(self) -> None:
        """Valide la transaction déléguée."""
        self._inner.commit()

    def rollback(self) -> None:
        """Annule la transaction déléguée."""
        self._inner.rollback()

    @property
    def users(self) -> UserRepository:
        """Repository utilisateurs délégué."""
        return self._inner.users

    @property
    def sessions(self) -> SessionRepository:
        """Repository sessions délégué."""
        return self._inner.sessions

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
