"""Service de readiness applicative.

:spec: BL-API-010-007, FEAT-001.3
"""

from sqlalchemy import text

from baobab_auth_api.infrastructure.app_state import AppState


class ReadinessService:
    """Vérifie la disponibilité des dépendances critiques."""

    def __init__(self, state: AppState) -> None:
        """Injecte l'état applicatif.

        :param state: Infrastructure câblée.
        """
        self._state = state

    def is_live(self) -> bool:
        """Indique si le processus répond (sans dépendance externe).

        :returns: Toujours ``True`` si le processus tourne.
        """
        return True

    def is_ready(self) -> bool:
        """Vérifie la base de données et la présence de clés JWKS.

        :returns: ``True`` si DB joignable et JWKS non vide.
        """
        if not self._state.jwks_provider.jwks().keys:
            return False
        try:
            with self._state.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except OSError:
            return False
        except Exception:
            return False
        return True
