"""Mapper RegisterUserResult → RegisterResponse.

:spec: BL-API-010-003
"""

from baobab_auth_core.application.results.register_user_result import RegisterUserResult

from baobab_auth_api.schemas.register_response import RegisterResponse


class RegisterResponseMapper:
    """Convertit le résultat d'inscription en schéma HTTP."""

    @staticmethod
    def to_response(result: RegisterUserResult) -> RegisterResponse:
        """Mappe le résultat d'inscription.

        :param result: Résultat du cas d'usage ``RegisterUser``.
        :returns: Schéma HTTP 201.
        """
        user = result.user
        return RegisterResponse(
            id=str(user.id),
            auth_subject=str(user.auth_subject),
            email=str(user.email),
        )
