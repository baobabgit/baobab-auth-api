"""Mapper TokenPair → TokenResponse.

:spec: BL-API-010-003
"""

from baobab_auth_core.application.results.token_pair import TokenPair

from baobab_auth_api.schemas.token_response import TokenResponse


class TokenResponseMapper:
    """Convertit un :class:`TokenPair` core en schéma HTTP."""

    @staticmethod
    def to_response(tokens: TokenPair) -> TokenResponse:
        """Mappe la paire de tokens.

        :param tokens: Paire émise par le core.
        :returns: Schéma HTTP ``token_type=bearer``.
        """
        return TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type.lower(),
            expires_in=tokens.expires_in,
        )
