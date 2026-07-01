"""Réponse d'inscription.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, EmailStr


class RegisterResponse(BaseModel):
    """Corps de réponse 201 pour l'inscription.

    :param id: Identifiant utilisateur.
    :param auth_subject: Sujet d'authentification stable.
    :param email: Email normalisé.
    """

    id: str
    auth_subject: str
    email: EmailStr
