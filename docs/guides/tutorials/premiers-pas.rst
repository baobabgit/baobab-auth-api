Premiers pas
============

Ce tutoriel met en place l'environnement de développement et lance les tests.

#. **Créer l'environnement virtuel** ::

      python -m venv .venv

#. **Activer l'environnement**

   * Windows (PowerShell) : ``.venv\Scripts\Activate.ps1``
   * Linux / macOS : ``source .venv/bin/activate``

#. **Installer le projet et les outils** ::

      pip install -e ".[dev,docs]"
      pre-commit install

#. **Vérifier que tout passe** ::

      ruff check .
      mypy
      pytest

Vous obtenez une couverture de tests supérieure à 90 % : l'environnement est prêt.
