"""Requête de connexion.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Corps de ``POST /auth/login``.

    :param email: Adresse email.
    :param password: Mot de passe.
    """

    email: EmailStr
    password: str = Field(min_length=1)
