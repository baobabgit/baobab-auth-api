# Contribuer

Merci de contribuer ! Les **règles de développement** font foi dans
[`AGENTS.md`](AGENTS.md) (source unique partagée par Claude Code, Cursor et Codex).
Ce document décrit le **processus**.

## Mise en place

```bash
# Prérequis : uv installé (https://docs.astral.sh/uv/)
make install
```

Cette commande installe l'environnement via `uv sync` et active les hooks `pre-commit`
(y compris le hook `commit-msg` anti-attribution IA).

## Cycle de contribution

1. **Prendre un backlog** dans `docs/ai_workflow/state/queue.yaml` ou via GitHub Issues.
2. **Vérifier le verrou** : `docs/ai_workflow/state/lock.yaml` doit être `locked: false`.
3. **Créer la branche backlog** depuis `version/vX.Y.Z` :
   ```bash
   git checkout version/vX.Y.Z
   git checkout -b bl/XXX-description-courte
   ```
4. **Créer le dossier de run** : `docs/ai_workflow/runs/BL-XXX/`.
5. **Développer** en respectant `AGENTS.md` :
   - 1 classe = 1 fichier ; type hints complets ; docstrings RST avec `:spec:`.
   - Test miroir obligatoire (`tests/unit/.../test_*.py`) ; classe abstraite testée
     via une classe concrète de test.
6. **Vérifier** :
   ```bash
   make all    # qualité (black + ruff + mypy + bandit) + tests ≥ 95 % + build
   ```
7. **Committer** au format `BL-XXX: action courte et explicite` :
   ```
   BL-012: implement user repository
   ```
   — **Jamais** de mention d'outil, `Co-authored-by:` ou signature d'assistant.
8. **Ouvrir une PR** vers `version/vX.Y.Z` en utilisant le template fourni.
9. Attendre la **CI verte** (`ci.yml`) puis obtenir `QA_PASSED` et `TECH_REVIEW_PASSED`.

## Definition of Done

Voir la section *Definition of Done* dans [`AGENTS.md`](AGENTS.md).

Une tâche n'est close que si :

1. Code POO, 1 classe/fichier, type hints complets.
2. `black`, `ruff` et `mypy` strict passent.
3. Tests présents en miroir (`tests/unit/`), couverture ≥ 95 %.
4. Docstrings RST + guide mis à jour si le comportement public change.
5. Commit conforme (`BL-XXX: action`), PR fusionnée sur `version/vX.Y.Z`.
