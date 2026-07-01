"""Configuration de l'API FastAPI.

:spec: BL-API-010-001, FEAT-001.1
"""

from baobab_auth_database import AuthDatabaseSettings
from baobab_auth_security import SecuritySettings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthApiSettings(BaseSettings):
    """Paramètres applicatifs injectés par variables d'environnement.

    :param app_name: Nom affiché dans OpenAPI.
    :param app_env: Environnement (development, staging, production).
    :param log_level: Niveau de journalisation.
    :param cors_origins: Origines CORS autorisées.
    :spec: FEAT-001.1
    """

    model_config = SettingsConfigDict(
        env_prefix="AUTH_API_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="baobab-auth-api")
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    cors_origins: list[str] = Field(default_factory=list)

    def database_settings(self) -> AuthDatabaseSettings:
        """Construit la configuration database.

        :returns: Paramètres ``baobab-auth-database``.
        """
        return AuthDatabaseSettings()

    def security_settings(self) -> SecuritySettings:
        """Construit la configuration security.

        :returns: Paramètres ``baobab-auth-security``.
        """
        return SecuritySettings()
