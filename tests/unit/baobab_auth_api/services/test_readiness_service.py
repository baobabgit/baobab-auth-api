"""Tests readiness service.

:spec: BL-API-010-007
"""

from unittest.mock import MagicMock

from baobab_auth_api.services.readiness_service import ReadinessService


class TestReadinessService:
    def test_FEAT_001_3_is_live_always_true(self) -> None:
        state = MagicMock()
        service = ReadinessService(state)
        assert service.is_live() is True

    def test_FEAT_001_3_is_ready_false_without_jwks(self) -> None:
        state = MagicMock()
        state.jwks_provider.jwks.return_value.keys = []
        service = ReadinessService(state)
        assert service.is_ready() is False

    def test_FEAT_001_3_is_ready_false_on_db_error(self) -> None:
        state = MagicMock()
        state.jwks_provider.jwks.return_value.keys = ["k1"]
        state.engine.connect.side_effect = OSError("db down")
        service = ReadinessService(state)
        assert service.is_ready() is False
