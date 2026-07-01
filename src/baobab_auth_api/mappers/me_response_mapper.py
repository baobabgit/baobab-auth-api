"""Mapper AuthenticatedUser → MeResponse.

:spec: BL-API-010-003
"""

from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser

from baobab_auth_api.schemas.me_response import MeResponse


class MeResponseMapper:
    """Convertit un :class:`AuthenticatedUser` en schéma HTTP."""

    @staticmethod
    def to_response(user: AuthenticatedUser) -> MeResponse:
        """Mappe l'utilisateur courant.

        :param user: DTO core sans secret.
        :returns: Schéma ``/auth/me``.
        """
        return MeResponse(
            id=str(user.id),
            auth_subject=str(user.auth_subject),
            email=str(user.email),
            roles=[str(role) for role in user.role_names],
            permissions=[str(perm) for perm in user.permissions],
        )
