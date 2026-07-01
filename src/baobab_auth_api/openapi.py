"""Personnalisation OpenAPI.

:spec: BL-API-010-002, FEAT-001.1
"""

from fastapi import FastAPI


class OpenApiConfigurator:
    """Configure les métadonnées OpenAPI de l'application."""

    @staticmethod
    def apply(app: FastAPI, title: str) -> None:
        """Applique le titre et la description OpenAPI.

        :param app: Application FastAPI.
        :param title: Titre documenté.
        """
        app.title = title
        app.description = (
            "API d'authentification Baobab Auth — inscription, connexion, "
            "tokens, JWKS et catalogue RBAC."
        )
        app.version = "0.1.0"
