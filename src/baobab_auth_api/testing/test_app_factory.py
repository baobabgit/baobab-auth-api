"""Fabrique d'application pour les tests.

:spec: BL-API-010-008, FEAT-001.1
"""

import os
from pathlib import Path

from fastapi import FastAPI

from baobab_auth_api.app import create_app
from baobab_auth_api.config import AuthApiSettings


class TestAppFactory:
    """Construit une application configurée pour les tests."""

    @staticmethod
    def create(db_path: Path | None = None) -> FastAPI:
        """Crée une app avec SQLite fichier ou mémoire.

        :param db_path: Chemin SQLite optionnel (persistance inter-requêtes).
        :returns: Application FastAPI prête pour ``httpx.AsyncClient``.
        """
        if db_path is not None:
            url = f"sqlite:///{db_path.as_posix()}"
        else:
            url = "sqlite:///:memory:"
        os.environ["AUTH_DB_DATABASE_URL"] = url
        os.environ["BAOBAB_SECURITY_ARGON2_TIME_COST"] = "1"
        os.environ["BAOBAB_SECURITY_ARGON2_MEMORY_COST"] = "8192"
        os.environ["BAOBAB_SECURITY_ARGON2_PARALLELISM"] = "1"
        settings = AuthApiSettings()
        return create_app(settings)

    @staticmethod
    def memory_settings() -> AuthApiSettings:
        """Retourne des settings SQLite mémoire.

        :returns: Configuration de test.
        """
        os.environ["AUTH_DB_DATABASE_URL"] = "sqlite:///:memory:"
        return AuthApiSettings()
