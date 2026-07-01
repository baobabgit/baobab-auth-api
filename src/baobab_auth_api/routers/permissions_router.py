"""Router catalogue des permissions.

:spec: BL-API-010-006, FEAT-001.3
"""

from fastapi import APIRouter

from baobab_auth_api.schemas.permission_response import PermissionResponse
from baobab_auth_api.services.rbac_service import RbacService


class PermissionsRouter:
    """Route ``GET /auth/permissions``."""

    def __init__(self, rbac_service: RbacService) -> None:
        """Injecte le service RBAC.

        :param rbac_service: Service catalogue.
        """
        self._rbac = rbac_service
        self._router = APIRouter(prefix="/auth", tags=["Permissions"])
        self._router.add_api_route(
            "/permissions",
            self.list_permissions,
            methods=["GET"],
        )

    @property
    def router(self) -> APIRouter:
        """Expose le router FastAPI.

        :returns: Router configuré.
        """
        return self._router

    def list_permissions(self) -> list[PermissionResponse]:
        """Liste les permissions du catalogue.

        :returns: Permissions atomiques connues.
        """
        return [
            PermissionResponse(
                name=str(permission.name),
                resource=permission.resource,
                action=permission.action,
                description=permission.description,
            )
            for permission in self._rbac.list_permissions()
        ]
