"""Service applicatif d'authentification.

:spec: BL-API-010-004, BL-API-010-005, FEAT-001.2
"""

from baobab_auth_core import (
    AuthenticateUser,
    Logout,
    RefreshSession,
    RegisterUser,
)
from baobab_auth_core.application.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from baobab_auth_core.application.commands.logout_command import LogoutCommand
from baobab_auth_core.application.commands.refresh_session_command import (
    RefreshSessionCommand,
)
from baobab_auth_core.application.commands.register_user_command import (
    RegisterUserCommand,
)
from baobab_auth_core.application.results.authenticate_user_result import (
    AuthenticateUserResult,
)
from baobab_auth_core.application.results.refresh_session_result import (
    RefreshSessionResult,
)
from baobab_auth_core.application.results.register_user_result import RegisterUserResult
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.session_id import SessionId

from baobab_auth_api.infrastructure.app_state import AppState


class AuthService:
    """Orchestre les cas d'usage d'authentification du core."""

    def __init__(self, state: AppState) -> None:
        """Injecte l'état applicatif.

        :param state: Infrastructure câblée.
        """
        self._state = state

    def register(
        self,
        email: str,
        password: str,
        ip_address: str | None,
        user_agent: str | None,
    ) -> RegisterUserResult:
        """Inscrit un nouvel utilisateur.

        :param email: Email brut.
        :param password: Mot de passe brut.
        :param ip_address: IP client pour audit.
        :param user_agent: User-Agent pour audit.
        :returns: Résultat d'inscription.
        """
        with self._state.uow_factory() as uow:
            use_case = RegisterUser(
                users=uow.users,
                audit=uow.audit,
                password_hasher=self._state.password_hasher,
                id_generator=self._state.id_generator,
                clock=self._state.clock,
                uow=uow,
            )
            command = RegisterUserCommand(
                email=email,
                password=password,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return use_case.execute(command)

    def login(
        self,
        email: str,
        password: str,
        ip_address: str | None,
        user_agent: str | None,
    ) -> AuthenticateUserResult:
        """Authentifie un utilisateur.

        :param email: Email brut.
        :param password: Mot de passe brut.
        :param ip_address: IP client pour audit.
        :param user_agent: User-Agent pour audit.
        :returns: Résultat avec tokens.
        """
        with self._state.uow_factory() as uow:
            use_case = AuthenticateUser(
                users=uow.users,
                sessions=uow.sessions,
                audit=uow.audit,
                password_hasher=self._state.password_hasher,
                token_provider=self._state.token_provider,
                id_generator=self._state.id_generator,
                clock=self._state.clock,
                uow=uow,
            )
            command = AuthenticateUserCommand(
                email=email,
                password=password,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return use_case.execute(command)

    def refresh(
        self,
        refresh_token: str,
        ip_address: str | None,
        user_agent: str | None,
    ) -> RefreshSessionResult:
        """Rafraîchit une session active.

        :param refresh_token: Token de rafraîchissement brut.
        :param ip_address: IP client pour audit.
        :param user_agent: User-Agent pour audit.
        :returns: Nouvelle paire de tokens.
        """
        with self._state.uow_factory() as uow:
            use_case = RefreshSession(
                sessions=uow.sessions,
                users=uow.users,
                audit=uow.audit,
                token_provider=self._state.token_provider,
                id_generator=self._state.id_generator,
                clock=self._state.clock,
                uow=uow,
            )
            command = RefreshSessionCommand(
                refresh_token=refresh_token,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return use_case.execute(command)

    def logout(self, session_id: str, actor_subject: str) -> None:
        """Déconnecte la session courante.

        :param session_id: Identifiant de session (claim ``sid``).
        :param actor_subject: Sujet du porteur (claim ``sub``).
        """
        with self._state.uow_factory() as uow:
            use_case = Logout(
                sessions=uow.sessions,
                users=uow.users,
                audit=uow.audit,
                id_generator=self._state.id_generator,
                clock=self._state.clock,
                uow=uow,
            )
            command = LogoutCommand(
                session_id=SessionId(session_id),
                actor_subject=AuthSubject(actor_subject),
            )
            use_case.execute(command)
