"""Module ``greeter`` : une classe concrète d'exemple (1 classe = 1 fichier)."""


class Greeter:
    """Produit des salutations pour une personne donnée.

    Classe concrète servant d'exemple aux conventions du template :
    type hints complets, docstring RST et traçabilité spec.

    :spec: FEAT-001.1
    """

    def __init__(self, name: str) -> None:
        """Initialise le salueur.

        :param name: nom de la personne à saluer (non vide).
        :raises ValueError: si ``name`` est vide ou composé d'espaces.
        """
        if not name.strip():
            raise ValueError("name ne doit pas être vide")
        self._name = name.strip()

    @property
    def name(self) -> str:
        """Renvoie le nom enregistré.

        :returns: le nom de la personne.
        """
        return self._name

    def greet(self, *, formal: bool = False) -> str:
        """Construit une salutation.

        :param formal: utilise un registre formel si ``True``.
        :returns: la salutation complète.
        """
        salutation = "Bonjour" if formal else "Salut"
        return f"{salutation}, {self._name} !"
