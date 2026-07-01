"""Tests imports publics dependencies."""

from baobab_auth_api import dependencies


class TestDependenciesModule:
    def test_FEAT_001_1_exports(self) -> None:
        assert dependencies.AppState is not None
        assert dependencies.CurrentUserDependency is not None
