"""Enregistrement des gestionnaires d'erreurs FastAPI.

:spec: BL-API-010-002, FEAT-001.2
"""

from baobab_auth_core.exceptions.auth import (
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
)
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.exceptions.session import (
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
)
from baobab_auth_core.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from baobab_auth_core.exceptions.validation import (
    InvalidEmailError,
    ValidationError,
    WeakPasswordError,
)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from baobab_auth_api.exceptions.api_http_error import ApiHttpError
from baobab_auth_api.schemas.error_detail import ErrorDetail
from baobab_auth_api.schemas.error_response import ErrorResponse


class ErrorHandlerRegistry:
    """Enregistre les handlers d'erreurs sur une application FastAPI."""

    @staticmethod
    def register(app: FastAPI) -> None:
        """Branche tous les handlers sur *app*.

        :param app: Application FastAPI cible.
        """
        app.add_exception_handler(ApiHttpError, ErrorHandlerRegistry._api_http_error)
        app.add_exception_handler(
            InvalidCredentialsError,
            ErrorHandlerRegistry._invalid_credentials,
        )
        app.add_exception_handler(
            UserAlreadyExistsError,
            ErrorHandlerRegistry._conflict,
        )
        app.add_exception_handler(
            TokenInvalidError,
            ErrorHandlerRegistry._unauthorized,
        )
        app.add_exception_handler(
            TokenExpiredError,
            ErrorHandlerRegistry._unauthorized,
        )
        app.add_exception_handler(ForbiddenError, ErrorHandlerRegistry._forbidden)
        app.add_exception_handler(
            SessionNotFoundError,
            ErrorHandlerRegistry._unauthorized,
        )
        app.add_exception_handler(
            SessionRevokedError,
            ErrorHandlerRegistry._unauthorized,
        )
        app.add_exception_handler(
            SessionExpiredError,
            ErrorHandlerRegistry._unauthorized,
        )
        app.add_exception_handler(UserNotFoundError, ErrorHandlerRegistry._not_found)
        app.add_exception_handler(ValidationError, ErrorHandlerRegistry._bad_request)
        app.add_exception_handler(InvalidEmailError, ErrorHandlerRegistry._bad_request)
        app.add_exception_handler(WeakPasswordError, ErrorHandlerRegistry._bad_request)

    @staticmethod
    async def _api_http_error(_request: Request, exc: Exception) -> JSONResponse:
        """Convertit une :class:`ApiHttpError` en JSON.

        :param _request: Requête HTTP.
        :param exc: Erreur applicative.
        :returns: Réponse JSON standardisée.
        """
        if not isinstance(exc, ApiHttpError):
            return ErrorHandlerRegistry._json("internal_error", "Internal error", 500)
        return ErrorHandlerRegistry._json(exc.code, exc.message, exc.status_code)

    @staticmethod
    async def _invalid_credentials(
        _request: Request,
        _exc: Exception,
    ) -> JSONResponse:
        """Réponse générique pour identifiants invalides.

        :param _request: Requête HTTP.
        :param _exc: Erreur domaine.
        :returns: Réponse 401.
        """
        return ErrorHandlerRegistry._json(
            "invalid_credentials",
            "Invalid credentials",
            401,
        )

    @staticmethod
    async def _conflict(_request: Request, exc: Exception) -> JSONResponse:
        """Réponse 409 pour conflit d'inscription.

        :param _request: Requête HTTP.
        :param exc: Erreur domaine.
        :returns: Réponse 409.
        """
        return ErrorHandlerRegistry._json("conflict", str(exc), 409)

    @staticmethod
    async def _unauthorized(_request: Request, _exc: Exception) -> JSONResponse:
        """Réponse 401 générique.

        :param _request: Requête HTTP.
        :param _exc: Erreur domaine.
        :returns: Réponse 401.
        """
        return ErrorHandlerRegistry._json("unauthorized", "Unauthorized", 401)

    @staticmethod
    async def _forbidden(_request: Request, exc: Exception) -> JSONResponse:
        """Réponse 403.

        :param _request: Requête HTTP.
        :param exc: Erreur domaine.
        :returns: Réponse 403.
        """
        return ErrorHandlerRegistry._json("forbidden", str(exc), 403)

    @staticmethod
    async def _not_found(_request: Request, exc: Exception) -> JSONResponse:
        """Réponse 404.

        :param _request: Requête HTTP.
        :param exc: Erreur domaine.
        :returns: Réponse 404.
        """
        return ErrorHandlerRegistry._json("not_found", str(exc), 404)

    @staticmethod
    async def _bad_request(_request: Request, exc: Exception) -> JSONResponse:
        """Réponse 400 pour validation.

        :param _request: Requête HTTP.
        :param exc: Erreur domaine.
        :returns: Réponse 400.
        """
        return ErrorHandlerRegistry._json("validation_error", str(exc), 400)

    @staticmethod
    def _json(code: str, message: str, status: int) -> JSONResponse:
        """Construit une réponse d'erreur standard.

        :param code: Code machine.
        :param message: Message public.
        :param status: Code HTTP.
        :returns: Réponse JSON.
        """
        body = ErrorResponse(error=ErrorDetail(code=code, message=message))
        return JSONResponse(status_code=status, content=body.model_dump())
