"""Erreur HTTP publique standardisée.

:spec: BL-API-010-002, FEAT-001.2
"""


class ApiHttpError(Exception):
    """Exception applicative mappée vers une réponse JSON d'erreur.

    :param code: Code machine stable.
    :param message: Message public sans secret.
    :param status_code: Code HTTP associé.
    """

    def __init__(self, code: str, message: str, status_code: int) -> None:
        """Initialise l'erreur HTTP.

        :param code: Code machine stable.
        :param message: Message public sans secret.
        :param status_code: Code HTTP associé.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
