Comment ajouter une nouvelle classe
===================================

Objectif : ajouter une classe en respectant les règles du projet.

#. **Créer le fichier de la classe** (1 classe = 1 fichier), nommé d'après la
   classe en ``snake_case`` : ``src/example_package/ma_classe.py`` pour
   ``class MaClasse``.

#. **Annoter et documenter** : type hints complets et docstring RST avec le
   champ ``:spec:`` pointant vers la Feature concernée (ex. ``:spec: FEAT-002.1``).

#. **Créer le test miroir** : ``tests/example_package/test_ma_classe.py`` avec
   une classe ``TestMaClasse``. Pour une classe **abstraite**, définir une
   **classe concrète de test** dans ce fichier.

#. **Exporter si public** : ajouter la classe à ``__all__`` dans ``__init__.py``.

#. **Vérifier** ::

      ruff check . && mypy && pytest

#. **Committer** avec un message conforme ::

      feat(FEAT-002.1): ajouter MaClasse
