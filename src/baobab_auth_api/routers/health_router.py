"""Router health et readiness.

:spec: BL-API-010-007, FEAT-001.3
"""

from fastapi import APIRouter, Response, status

from baobab_auth_api.services.readiness_service import ReadinessService


class HealthRouter:
    """Routes ``/health`` et ``/ready``."""

    def __init__(self, readiness_service: ReadinessService) -> None:
        """Injecte le service de readiness.

        :param readiness_service: Vérifications de disponibilité.
        """
        self._readiness = readiness_service
        self._router = APIRouter(tags=["Health"])
        self._router.add_api_route("/health", self.health, methods=["GET"])
        self._router.add_api_route("/ready", self.ready, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        """Expose le router FastAPI.

        :returns: Router configuré.
        """
        return self._router

    def health(self) -> dict[str, str]:
        """Liveness probe sans dépendance externe.

        :returns: Statut ``ok``.
        """
        return {"status": "ok"}

    def ready(self) -> Response:
        """Readiness probe avec vérification DB et JWKS.

        :returns: 200 si prêt, 503 sinon.
        """
        if self._readiness.is_ready():
            return Response(
                content='{"status":"ready"}',
                media_type="application/json",
                status_code=status.HTTP_200_OK,
            )
        return Response(
            content='{"status":"not_ready"}',
            media_type="application/json",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
