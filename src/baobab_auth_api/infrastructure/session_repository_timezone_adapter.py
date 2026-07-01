"""Adaptateur normalisant les datetimes SQLite en UTC aware.

:spec: BL-API-010-005, ADR-0001
"""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.ports.session_repository import SessionRepository


class SessionRepositoryTimezoneAdapter:
    """Décorateur de :class:`SessionRepository` corrigeant les datetimes naïfs."""

    def __init__(self, inner: SessionRepository) -> None:
        """Enveloppe un repository SQLAlchemy.

        :param inner: Repository délégué.
        """
        self._inner = inner

    def get_by_id(self, session_id: SessionId) -> Session | None:
        """Récupère une session par identifiant.

        :param session_id: Identifiant de session.
        :returns: Session normalisée ou ``None``.
        """
        return self._normalize(self._inner.get_by_id(session_id))

    def get_by_refresh_token_id(self, refresh_token_id: TokenId) -> Session | None:
        """Récupère une session par refresh token id.

        :param refresh_token_id: Identifiant du refresh token.
        :returns: Session normalisée ou ``None``.
        """
        return self._normalize(
            self._inner.get_by_refresh_token_id(refresh_token_id),
        )

    def get_active_by_user(self, user_id: UserId) -> list[Session]:
        """Liste les sessions actives d'un utilisateur.

        :param user_id: Identifiant utilisateur.
        :returns: Sessions normalisées.
        """
        return [
            normalized
            for session in self._inner.get_active_by_user(user_id)
            if (normalized := self._normalize(session)) is not None
        ]

    def save(self, session: Session) -> None:
        """Sauvegarde une session.

        :param session: Entité à persister.
        """
        self._inner.save(session)

    def delete(self, session_id: SessionId) -> None:
        """Supprime une session.

        :param session_id: Identifiant à supprimer.
        """
        self._inner.delete(session_id)

    @staticmethod
    def _normalize(session: Session | None) -> Session | None:
        """Force les champs datetime en UTC aware.

        :param session: Session lue depuis SQLite.
        :returns: Session corrigée ou ``None``.
        """
        if session is None:
            return None
        session.created_at = SessionRepositoryTimezoneAdapter._ensure_utc(
            session.created_at,
        )
        session.expires_at = SessionRepositoryTimezoneAdapter._ensure_utc(
            session.expires_at,
        )
        session.revoked_at = SessionRepositoryTimezoneAdapter._ensure_utc_optional(
            session.revoked_at,
        )
        session.last_used_at = SessionRepositoryTimezoneAdapter._ensure_utc_optional(
            session.last_used_at,
        )
        return session

    @staticmethod
    def _ensure_utc(value: datetime) -> datetime:
        """Convertit un datetime naïf en UTC aware.

        :param value: Valeur source.
        :returns: Datetime UTC aware.
        """
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value

    @staticmethod
    def _ensure_utc_optional(value: datetime | None) -> datetime | None:
        """Convertit un datetime optionnel en UTC aware.

        :param value: Valeur source ou ``None``.
        :returns: Datetime UTC aware ou ``None``.
        """
        if value is None:
            return None
        return SessionRepositoryTimezoneAdapter._ensure_utc(value)
