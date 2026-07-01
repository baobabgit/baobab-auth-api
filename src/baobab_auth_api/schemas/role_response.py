"""Réponse rôle RBAC.

:spec: BL-API-010-003, FEAT-001.3
"""

from pydantic import BaseModel


class RoleResponse(BaseModel):
    """Projection publique d'un rôle.

    :param name: Nom du rôle.
    :param description: Description optionnelle.
    :param permissions: Permissions associées.
    """

    name: str
    description: str | None
    permissions: list[str]
