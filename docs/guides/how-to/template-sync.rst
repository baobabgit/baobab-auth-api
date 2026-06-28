Synchroniser les fichiers infra depuis le template
===================================================

Ce guide explique comment propager les évolutions du template source
(``baobab-python-template``) vers un projet dérivé, **sans écraser le code
ni les métadonnées du projet**.

Prérequis
---------

- ``git`` installé et le dépôt courant propre (aucune modification non commitée).
- Accès réseau au dépôt template (HTTPS public ou SSH pour un dépôt privé).

Principe
--------

Le template est ajouté comme remote ``upstream`` dans le projet dérivé.
Un script ``scripts/sync_from_template.sh`` récupère sélectivement les fichiers
infra (CI, règles IA, outils) depuis ``upstream/main`` et les applique sur une
branche dédiée ``template-sync/YYYY-MM-DD``.

Les fichiers projet ne sont jamais touchés :

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Synchronisé depuis le template
     - Jamais touché (projet)
   * - ``.github/workflows/``
     - ``src/``
   * - ``.github/ISSUE_TEMPLATE/``, ``pull_request_template.md``
     - ``tests/``
   * - ``.github/dependabot.yml``
     - ``docs/specifications/``
   * - ``.cursor/rules/``, ``.codex/rules/``
     - ``docs/ai_workflow/state/``, ``runs/``, ``versions/``
   * - ``AGENTS.md``, ``CLAUDE.md``
     - ``docs/backlog/``, ``docs/contracts/``
   * - ``noxfile.py``, ``Makefile``, ``scripts/``
     - ``README.md``, ``CHANGELOG.md``, ``LICENSE``
   * - ``.pre-commit-config.yaml``, ``.python-version``
     - ``pyproject.toml`` (métadonnées + dépendances)
   * - ``docs/workflow/``, ``docs/ai_workflow/roles/``
     - ``uv.lock``
   * - Guides how-to du template
     - Tutorials et guides propres au projet

Premier usage (configuration du remote)
-----------------------------------------

Si le remote ``upstream`` n'est pas encore configuré, le script le crée
automatiquement. Vous pouvez aussi le faire manuellement :

.. code-block:: bash

   git remote add upstream https://github.com/baobabgit/baobab-python-template.git
   git remote -v   # vérification

Synchronisation courante
-------------------------

1. S'assurer que la branche de travail est propre :

   .. code-block:: bash

      git status   # doit afficher "nothing to commit"

2. Lancer le script :

   .. code-block:: bash

      bash scripts/sync_from_template.sh

   Le script crée la branche ``template-sync/YYYY-MM-DD``, applique les fichiers
   infra et affiche un récapitulatif des modifications.

   Pour utiliser un fork du template ou une URL différente :

   .. code-block:: bash

      bash scripts/sync_from_template.sh https://github.com/OWNER/mon-fork.git

Révisions manuelles
--------------------

Après le script, trois points méritent une vérification humaine.

**Sections** ``[tool.*]`` **de** ``pyproject.toml``

Les configs d'outils (``[tool.black]``, ``[tool.ruff]``, ``[tool.mypy]``,
``[tool.coverage]``, ``[tool.bandit]``) peuvent évoluer dans le template.
Le script ne les touche pas pour éviter d'écraser les ajustements du projet ;
diffez et appliquez manuellement ce qui vous convient :

.. code-block:: bash

   git diff upstream/main -- pyproject.toml

**Index des guides** (``docs/guides/index.rst``)

Si le template a ajouté de nouveaux guides, ils n'apparaîtront pas dans la table
des matières Sphinx sans une entrée dans ``index.rst``. Vérifiez et complétez :

.. code-block:: bash

   git diff upstream/main -- docs/guides/index.rst

**Nouveaux fichiers infra**

Le script synchronise une liste connue de chemins. Si le template a introduit de
nouveaux fichiers infra non couverts, repérez-les ainsi :

.. code-block:: bash

   git diff upstream/main HEAD -- .github/ scripts/ docs/workflow/

Créer la PR
-----------

Une fois les révisions terminées :

.. code-block:: bash

   git commit -m "BL-XXX: sync infra from template YYYY-MM-DD"
   git push -u origin template-sync/YYYY-MM-DD

Ouvrez ensuite une PR vers ``version/vX.Y.Z`` (ou ``main`` si aucune version
n'est en cours). Après merge, supprimez la branche ``template-sync/``.

.. note::
   Si la CI signale des conflits entre les nouvelles règles infra et le code
   existant (par exemple une règle ruff ajoutée dans le template), corrigez le
   code du projet dans un commit séparé sur la même branche avant de merger.

Voir aussi
----------

- :doc:`integration-validation` — valider une intégration inter-librairies
- ``AGENTS.md`` § Git & traçabilité — modèle de branches
- ``docs/workflow/SETUP.md`` — configuration GitHub one-time
