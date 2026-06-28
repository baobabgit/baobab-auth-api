"""Tests de Greeter (arborescence miroir de src/example_package/greeter.py)."""

import pytest

from example_package.greeter import Greeter


class TestGreeter:
    """1 classe testée (Greeter) = 1 classe de test (TestGreeter)."""

    def test_FEAT_001_1_greet_informel(self) -> None:
        # Arrange
        greeter = Greeter("Ada")
        # Act
        message = greeter.greet()
        # Assert
        assert message == "Salut, Ada !"

    def test_FEAT_001_1_greet_formel(self) -> None:
        greeter = Greeter("Ada")
        assert greeter.greet(formal=True) == "Bonjour, Ada !"

    def test_FEAT_001_1_name_est_nettoye(self) -> None:
        assert Greeter("  Ada  ").name == "Ada"

    def test_FEAT_001_1_nom_vide_leve_valueerror(self) -> None:
        with pytest.raises(ValueError):
            Greeter("   ")
