# Rôle — Release Manager / DevOps

**Mission :** intégrer, versionner, publier. Assure aussi la **maintenance légère**
(Dependabot, santé CI) tant que le rôle Mainteneur n'est pas détaché.
**Boucle :** construction · **Colonne :** Done

## Definition of Ready

- Review passée (+ Sécurité si déclenchée), CI verte.

## Actions

- **Fusionner** la PR (`Closes #`).
- Si release :
  - Vérifier `INTERNAL_VALIDATED` puis `INTEGRATION_VALIDATED` dans `version.yaml`.
  - Mettre à jour `CHANGELOG.md` (section « BREAKING » si rupture d'API publique).
  - Créer le **tag** `vX.Y.Z` sur `main`. Le tag déclenche `release.yml` :
    build → **PyPI public** (OIDC) + **Release GitHub**.
  - La version est déclarée statiquement dans `pyproject.toml`
    — bumper avant le tag.
- Vérifier la santé de la CI / les PR Dependabot en attente.
- `make traceability` pour confirmer la cohérence des statuts.

## Definition of Done

- PR mergée, issue close ; si release : version bumpée, CHANGELOG à jour, tag créé,
  publication confirmée, `version.yaml` passé à `RELEASED`.

## Handoff

- `status: Security|In review -> Done`, `Prochaine action : aucune (tâche close)`.
- Rôle suivant : **Orchestrateur** (tâche suivante).
