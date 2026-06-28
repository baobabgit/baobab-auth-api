Valider une intégration inter-librairies (git-ref directe)
===========================================================

Ce guide explique comment valider qu'une nouvelle version d'une librairie
est compatible avec ses consommateurs **avant** de la publier sur PyPI.
Le mécanisme retenu est la **référence git directe** sur la branche
``version/vX.Y.Z`` — aucune publication intermédiaire n'est requise.

Prérequis
---------

- La branche ``version/vX.Y.Z`` du producteur est ``INTERNAL_VALIDATED``
  (tous les ``bl/`` mergés, CI verte).
- Les dépôts consommateurs sont accessibles en lecture (dépôts privés : token
  ou deploy key configuré côté ``uv`` / ``git``).

Étapes côté producteur
-----------------------

1. Déclarer les consommateurs dans ``compatibility_matrix.yaml`` :

   .. code-block:: yaml

      validated_consumers:
        - name: baobab-api
          version: v2.1.0          # version du consommateur testée
          status: PENDING
          integration_method: git_ref
          ref: version/v1.2.0      # branche producteur testée

2. Passer ``version.yaml`` à ``INTEGRATION_PENDING``.

3. Notifier chaque consommateur (canal d'équipe, issue GitHub, etc.) avec
   la branche à référencer : ``version/v1.2.0``.

Étapes côté consommateur
-------------------------

Dans le dépôt du consommateur :

1. **Remplacer** la dépendance stable par la git-ref dans ``pyproject.toml`` :

   .. code-block:: toml

      [dependency-groups]
      dev = [
        "example-package @ git+https://github.com/OWNER/REPO.git@version/v1.2.0",
      ]

   .. note::
      ``uv`` supporte nativement les URL ``git+https://``. Pour un dépôt
      privé, assurez-vous que ``git`` a accès (SSH ou HTTPS avec token).

2. **Synchroniser** l'environnement :

   .. code-block:: bash

      uv sync

3. **Exécuter** la suite d'intégration :

   .. code-block:: bash

      uv run pytest tests/integration/ tests/contracts/ -v

4. **Reporter le résultat** dans ``compatibility_matrix.yaml`` du producteur
   (via PR ou communication directe) :

   .. code-block:: yaml

      - name: baobab-api
        status: PASSED      # ou FAILED
        integration_method: git_ref
        ref: version/v1.2.0
        report: docs/integrations/reports/example-package-v1.2.0__baobab-api-v2.1.0.md

5. **Créer le rapport** ``docs/integrations/reports/<producteur>-<version>__<consommateur>.md``
   (résumé : version testée, commandes, résultats, date).

6. Après la release PyPI du producteur, **revenir** à la dépendance stable :

   .. code-block:: toml

      [dependency-groups]
      dev = [
        "example-package>=1.2.0",
      ]

Étapes finales côté producteur
--------------------------------

1. Vérifier que tous les consommateurs requis ont ``status: PASSED``.
2. Passer ``version.yaml`` à ``INTEGRATION_VALIDATED``.
3. Continuer vers ``RELEASE_READY`` → tag → publication PyPI.

Cas d'échec (``status: FAILED``)
----------------------------------

Si un consommateur signale un échec :

- Analyser le rapport d'erreur fourni par le consommateur.
- Créer un nouveau ``bl/`` correctif sur ``version/vX.Y.Z``.
- Une fois corrigé et mergé, recommencer la notification du consommateur.
- Ne pas bumper la version : la correction reste sur ``version/vX.Y.Z``.

Voir aussi
----------

- :doc:`ajouter-une-classe` — conventions OOP du projet
- ``docs/contracts/`` — contrats publics de la librairie
- ``docs/integrations/compatibility_matrix.yaml`` — matrice de compatibilité
- ``AGENTS.md`` § Gestion inter-librairies — règles normatives
