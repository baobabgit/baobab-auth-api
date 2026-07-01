"""Gestionnaire de cycle de vie FastAPI.

:spec: BL-API-010-002, FEAT-001.1
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from baobab_auth_api.infrastructure.app_state import AppState


class AppLifespan:
    """Libère les ressources au shutdown de l'application."""

    def __init__(self, state: AppState) -> None:
        """Mémorise l'état à disposer.

        :param state: État applicatif initialisé à la création.
        """
        self._state = state

    @asynccontextmanager
    async def lifespan(self, _app: FastAPI) -> AsyncIterator[None]:
        """Conserve l'état actif puis dispose le moteur SQLAlchemy.

        :param _app: Application FastAPI.
        :yields: Contrôle pendant la durée de vie du processus.
        """
        try:
            yield
        finally:
            self._state.engine.dispose()
