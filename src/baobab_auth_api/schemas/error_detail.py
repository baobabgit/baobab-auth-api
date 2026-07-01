"""Détail d'erreur public.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Corps d'une erreur publique.

    :param code: Code machine stable.
    :param message: Message lisible sans secret.
    """

    code: str = Field(examples=["invalid_credentials"])
    message: str = Field(examples=["Invalid credentials"])
