"""Router catalogue des rôles.

:spec: BL-API-010-006, FEAT-001.3
"""

from fastapi import APIRouter

from baobab_auth_api.schemas.role_response import RoleResponse
from baobab_auth_api.services.rbac_service import RbacService


class RolesRouter:
    """Route ``GET /auth/roles``."""

    def __init__(self, rbac_service: RbacService) -> None:
        """Injecte le service RBAC.

        :param rbac_service: Service catalogue.
        """
        self._rbac = rbac_service
        self._router = APIRouter(prefix="/auth", tags=["Roles"])
        self._router.add_api_route("/roles", self.list_roles, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        """Expose le router FastAPI.

        :returns: Router configuré.
        """
        return self._router

    def list_roles(self) -> list[RoleResponse]:
        """Liste les rôles du catalogue.

        :returns: Rôles avec permissions associées.
        """
        return [
            RoleResponse(
                name=str(role.name),
                description=role.description,
                permissions=[str(p) for p in role.permission_names],
            )
            for role in self._rbac.list_roles()
        ]
