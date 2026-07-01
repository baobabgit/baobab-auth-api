"""Tests module main."""

import baobab_auth_api.main as main_module


class TestMainModule:
    def test_FEAT_001_1_main_exposes_app(self) -> None:
        assert main_module.app is not None
