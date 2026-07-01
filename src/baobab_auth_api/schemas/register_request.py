"""Requête d'inscription.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Corps de ``POST /auth/register``.

    :param email: Adresse email de l'utilisateur.
    :param password: Mot de passe en clair.
    """

    email: EmailStr
    password: str = Field(min_length=8)
