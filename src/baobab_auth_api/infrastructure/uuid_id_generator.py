"""Générateur d'identifiants UUID pour la production.

:spec: BL-API-010-001
"""

from uuid import uuid4


class UuidIdGenerator:
    """Produit des identifiants UUID v4 sous forme de chaîne."""

    def generate(self) -> str:
        """Génère un identifiant unique.

        :returns: UUID v4 sérialisé.
        """
        return str(uuid4())
