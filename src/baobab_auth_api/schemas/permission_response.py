"""Réponse permission RBAC.

:spec: BL-API-010-003, FEAT-001.3
"""

from pydantic import BaseModel


class PermissionResponse(BaseModel):
    """Projection publique d'une permission.

    :param name: Nom ``scope:resource:action``.
    :param resource: Ressource ciblée.
    :param action: Action autorisée.
    :param description: Description optionnelle.
    """

    name: str
    resource: str
    action: str
    description: str | None
