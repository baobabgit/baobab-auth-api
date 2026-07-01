"""Dépendances FastAPI partagées.

:spec: BL-API-010-002
"""

from baobab_auth_api.infrastructure.app_state import AppState
from baobab_auth_api.security.current_user_dependency import CurrentUserDependency

__all__ = ["AppState", "CurrentUserDependency"]
