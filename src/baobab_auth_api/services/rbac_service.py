"""Service catalogue RBAC.

:spec: BL-API-010-006, FEAT-001.3
"""

from baobab_auth_core import ListPermissions, ListRoles
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role

from baobab_auth_api.infrastructure.app_state import AppState


class RbacService:
    """Liste les rôles et permissions du catalogue."""

    def __init__(self, state: AppState) -> None:
        """Injecte l'état applicatif.

        :param state: Infrastructure câblée.
        """
        self._state = state

    def list_roles(self) -> tuple[Role, ...]:
        """Retourne tous les rôles connus.

        :returns: Tuple de rôles.
        """
        with self._state.uow_factory() as uow:
            return ListRoles(uow.roles).execute()

    def list_permissions(self) -> tuple[Permission, ...]:
        """Retourne toutes les permissions connues.

        :returns: Tuple de permissions.
        """
        with self._state.uow_factory() as uow:
            return ListPermissions(uow.permissions).execute()
