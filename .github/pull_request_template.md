## Objectif

<!-- Décrire le but de cette PR et le backlog implémenté. -->

## Backlog lié

- Backlog : `BL-XXX`
- User Story : `US-XXX`
- Feature : `FEAT-XXX`
- Issue : Closes #

## Changements

<!-- Lister les fichiers/classes modifiés et ce qui a changé. -->

## Tests exécutés

```
make all
```

- [ ] `uv run black --check src tests` → vert
- [ ] `uv run ruff check src tests` → vert
- [ ] `uv run mypy src` → vert
- [ ] `uv run bandit -r src -c pyproject.toml` → vert
- [ ] `uv run pytest --cov=src --cov-fail-under=95` → vert

## Résultats qualité

<!-- Coller le résumé de `make all` ou copier les sorties pertinentes. -->

## Couverture

<!-- Indiquer le pourcentage de couverture obtenu (doit être ≥ 95 %). -->

Couverture : X %

## Impact contrat public

- [ ] Aucun symbole public (`__all__`) modifié de façon incompatible.
- [ ] Si rupture de contrat : MAJOR bump + entrée BREAKING dans `CHANGELOG.md` + note de migration.

## Impact intégration

- [ ] `integration_required: false` — aucune validation inter-librairie requise.
- [ ] `integration_required: true` — les tests d'intégration ont été exécutés et sont verts.

## Décision attendue

- [ ] `QA_PASSED`
- [ ] `TECH_REVIEW_PASSED`
- [ ] Prêt à merger vers `version/vX.Y.Z`
