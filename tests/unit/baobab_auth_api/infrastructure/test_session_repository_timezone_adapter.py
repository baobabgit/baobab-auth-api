"""Tests adaptateur timezone sessions.

:spec: BL-API-010-005
"""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId

from baobab_auth_api.infrastructure.session_repository_timezone_adapter import (
    SessionRepositoryTimezoneAdapter,
)


class TestSessionRepositoryTimezoneAdapter:
    def _session(self) -> Session:
        return Session(
            id=SessionId("s1"),
            user_id=UserId("u1"),
            refresh_token_id=TokenId("r1"),
            status=SessionStatus.ACTIVE,
            created_at=datetime(2026, 1, 1),
            expires_at=datetime(2026, 2, 1),
            revoked_at=None,
            last_used_at=None,
        )

    def test_FEAT_001_2_normalizes_naive_datetimes(self) -> None:
        inner = MagicMock()
        inner.get_by_id.return_value = self._session()
        adapter = SessionRepositoryTimezoneAdapter(inner)
        session = adapter.get_by_id(SessionId("s1"))
        assert session is not None
        assert session.expires_at.tzinfo == UTC

    def test_FEAT_001_2_delete_delegates(self) -> None:
        inner = MagicMock()
        adapter = SessionRepositoryTimezoneAdapter(inner)
        adapter.delete(SessionId("s1"))
        inner.delete.assert_called_once()
