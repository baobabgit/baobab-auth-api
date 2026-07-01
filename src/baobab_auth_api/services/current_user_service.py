"""Service utilisateur courant.

:spec: BL-API-010-005, FEAT-001.2
"""

from baobab_auth_core import GetCurrentUser
from baobab_auth_core.application.queries.get_current_user_query import (
    GetCurrentUserQuery,
)
from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject

from baobab_auth_api.infrastructure.app_state import AppState


class CurrentUserService:
    """Expose l'identité courante avec rôles et permissions."""

    def __init__(self, state: AppState) -> None:
        """Injecte l'état applicatif.

        :param state: Infrastructure câblée.
        """
        self._state = state

    def get_me(self, auth_subject: str) -> AuthenticatedUser:
        """Retourne l'utilisateur authentifié.

        :param auth_subject: Claim ``sub`` du token.
        :returns: Projection publique enrichie RBAC.
        """
        with self._state.uow_factory() as uow:
            authorization = AuthorizationService(
                uow.users,
                uow.roles,
                uow.permissions,
            )
            use_case = GetCurrentUser(uow.users, authorization)
            query = GetCurrentUserQuery(auth_subject=AuthSubject(auth_subject))
            return use_case.execute(query)
