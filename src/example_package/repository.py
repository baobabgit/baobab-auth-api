"""Module ``repository`` : une classe abstraite d'exemple."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Dépôt abstrait d'éléments identifiés par un entier.

    Sert d'exemple pour la règle « tester une classe abstraite via une
    classe concrète de test » (voir ``tests/example_package/test_repository.py``).

    :spec: FEAT-001.2
    """

    @abstractmethod
    def get(self, item_id: int) -> str:
        """Récupère un élément par son identifiant.

        :param item_id: identifiant de l'élément.
        :returns: la représentation de l'élément.
        :raises KeyError: si l'élément n'existe pas.
        """
        raise NotImplementedError

    def describe(self) -> str:
        """Décrit le dépôt (méthode concrète, donc testable directement).

        :returns: une description lisible du type de dépôt.
        """
        return f"Dépôt {type(self).__name__}"
