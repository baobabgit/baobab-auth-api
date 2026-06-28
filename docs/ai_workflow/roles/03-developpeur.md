# Rôle — Développeur (TDD + tests + docstrings)

**Mission :** implémenter une tâche en TDD, testée et documentée.
**Boucle :** construction · **Colonne :** In progress

## Definition of Ready

- TASK « Ready » : lien spec, critères d'acceptation, estimation, classe cible,
  dans le sprint.

## Actions (ordre TDD)

1. Écrire d'abord les **tests** en arborescence miroir (`tests/unit/<pkg>/.../test_*.py`).
   Classe abstraite → **classe concrète de test** dans le fichier de test.
2. Implémenter la **classe** (1 classe/fichier), type hints complets.
3. Rédiger les **docstrings RST** avec `:spec:` (et `:origin:` si pertinent).
4. Exporter dans `__all__` si l'élément est public.
5. `make all` jusqu'au **vert** (black + ruff + mypy + pytest ≥ 95 % + build +
   traçabilité).
6. Commit `BL-XXX: action courte`, ouvrir la **PR** (`Closes #`).

## Definition of Done

- Tests miroir présents, code typé, docstrings RST, `make all` vert, PR ouverte.

## Handoff

- `status: In progress -> In review`.
- Rôle suivant : **Relecteur**.
