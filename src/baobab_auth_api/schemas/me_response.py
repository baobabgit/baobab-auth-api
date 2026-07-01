"""Réponse identité courante.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, EmailStr


class MeResponse(BaseModel):
    """Corps de ``GET /auth/me``.

    :param id: Identifiant utilisateur.
    :param auth_subject: Sujet stable.
    :param email: Email normalisé.
    :param roles: Rôles assignés.
    :param permissions: Permissions agrégées.
    """

    id: str
    auth_subject: str
    email: EmailStr
    roles: list[str]
    permissions: list[str]
