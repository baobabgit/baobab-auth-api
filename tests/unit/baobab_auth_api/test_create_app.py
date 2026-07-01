"""Tests create_app options."""

from baobab_auth_api.app import create_app
from baobab_auth_api.config import AuthApiSettings


class TestCreateAppOptions:
    def test_FEAT_001_1_cors_middleware_when_origins_set(self) -> None:
        settings = AuthApiSettings(cors_origins=["http://localhost:3000"])
        app = create_app(settings)
        middleware_names = [m.cls.__name__ for m in app.user_middleware]
        assert "CORSMiddleware" in middleware_names
