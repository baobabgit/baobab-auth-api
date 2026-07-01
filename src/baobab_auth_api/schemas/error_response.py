"""Enveloppe d'erreur HTTP standard.

:spec: BL-API-010-003, FEAT-001.2
"""

from pydantic import BaseModel

from baobab_auth_api.schemas.error_detail import ErrorDetail


class ErrorResponse(BaseModel):
    """Réponse d'erreur publique ``{error: {code, message}}``.

    :param error: Détail de l'erreur.
    """

    error: ErrorDetail
