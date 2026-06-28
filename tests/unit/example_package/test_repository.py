"""Tests de Repository : exemple de test d'une classe ABSTRAITE.

On teste la classe abstraite en définissant une **classe concrète de test**
(``_ConcreteRepository``) au sein du fichier de test.
"""

from example_package.repository import Repository


class _ConcreteRepository(Repository):
    """Implémentation concrète minimale, dédiée aux tests de Repository."""

    def get(self, item_id: int) -> str:
        return f"item-{item_id}"


class TestRepository:
    """1 classe testée (Repository) = 1 classe de test (TestRepository)."""

    def test_FEAT_001_2_get_via_classe_concrete(self) -> None:
        # Arrange
        repo = _ConcreteRepository()
        # Act
        result = repo.get(42)
        # Assert
        assert result == "item-42"

    def test_FEAT_001_2_describe_methode_concrete(self) -> None:
        repo = _ConcreteRepository()
        assert repo.describe() == "Dépôt _ConcreteRepository"
