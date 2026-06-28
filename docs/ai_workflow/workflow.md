# Workflow IA — Mode stable séquentiel

> Un seul outil de développement assisté peut travailler sur le projet à un instant donné.

## Étapes du workflow

```
1.  Dépôt du cahier des charges
2.  Analyse fonctionnelle
3.  Architecture
4.  Découpage US / Features / Backlogs
5.  Priorisation
6.  Sélection du prochain backlog
7.  Création de la branche backlog (depuis version/vX.Y.Z)
8.  Verrouillage du projet (lock.yaml)
9.  Implémentation
10. Tests unitaires
11. Contrôles qualité (make all)
12. Revue QA
13. Revue technique
14. Corrections éventuelles
15. Merge vers version/vX.Y.Z
16. Validation interne de version (INTERNAL_VALIDATED)
17. Validation d'intégration via git-ref (INTEGRATION_PENDING → INTEGRATION_VALIDATED)
18. Merge version/vX.Y.Z → main
19. Tag vX.Y.Z sur main
20. Release GitHub automatique
21. Publication PyPI automatique
```

### Détail de l'étape 17 — Validation d'intégration (git-ref directe)

La validation inter-librairies ne passe pas par TestPyPI. Le mécanisme retenu est la
**référence git directe** sur la branche `version/vX.Y.Z`.

**Producteur** :
1. Passer `version.yaml` à `INTEGRATION_PENDING`.
2. Mettre à jour `compatibility_matrix.yaml` : ajouter les consommateurs avec `status: PENDING`,
   `integration_method: git_ref`, `ref: version/vX.Y.Z`.
3. Notifier chaque consommateur.

**Consommateur** (dans son propre dépôt) :
1. Remplacer la dépendance dans `pyproject.toml` :
   ```toml
   [dependency-groups]
   dev = [
     "example-package @ git+https://github.com/OWNER/REPO.git@version/vX.Y.Z",
   ]
   ```
2. `uv sync` puis `make all` (ou `uv run pytest tests/integration/ tests/contracts/`).
3. Reporter le résultat dans la `compatibility_matrix.yaml` du producteur :
   - `status: PASSED` ou `status: FAILED`
   - Ajouter le rapport dans `docs/integrations/reports/<producteur>-<version>__<consommateur>.md`
4. Une fois la release PyPI publiée : revenir à `"example-package>=X.Y.Z"` dans `pyproject.toml`.

**Producteur** (après retour de tous les consommateurs requis) :
1. Vérifier que tous les consommateurs déclarés ont `status: PASSED`.
2. Passer `version.yaml` à `INTEGRATION_VALIDATED`.

## Modèle de branches

```
main
└── version/v0.1.0
    └── bl/001-implement-greeter
```

## Structure d'un run

```
docs/ai_workflow/runs/BL-XXX/
├── 00_assignment.md      # Backlog assigné + rôle
├── 01_context.md         # Contexte au démarrage
├── 02_role_prompt.md     # Prompt de rôle utilisé
├── 03_expected_outputs.md # Sorties attendues
├── 04_worklog.md         # Journal de travail
├── 05_tests_report.md    # Rapport de tests
├── 06_review.md          # Rapport de revue
├── 07_handoff.md         # Note de passation
├── 08_recovery.md        # Note de recovery (si verrou orphelin)
└── status.yaml           # État courant du run
```

## Procédure de recovery

En cas de verrou expiré sans handoff :

1. Lire `status.yaml` du run interrompu.
2. Lire `git status` et `git diff`.
3. Identifier les fichiers modifiés.
4. Exécuter `make all` (ou `uv run pytest`).
5. Produire `08_recovery.md` avec le diagnostic.
6. Reprendre ou demander correction.
7. Créer un nouveau verrou avec une nouvelle expiration.

## Statuts de run

```
TODO → READY → ASSIGNED → IN_PROGRESS
  → PAUSED_USAGE_EXHAUSTED
  → RECOVERY_IN_PROGRESS
  → READY_FOR_QA → QA_PASSED
  → READY_FOR_REVIEW → CHANGES_REQUESTED (retour à IN_PROGRESS)
  → TECH_REVIEW_PASSED → MERGED
  → NO_GO
```

## Statuts de version

```
PLANNED → IN_DEVELOPMENT → INTERNAL_VALIDATED
  → INTEGRATION_PENDING → INTEGRATION_VALIDATED
  → RELEASE_READY → RELEASED
```

## Rôles

Voir `docs/ai_workflow/roles/` pour le détail de chaque rôle.
Une même personne ou un même outil peut jouer plusieurs rôles successivement,
jamais simultanément.

| Rôle                  | Responsabilité principale                         |
|-----------------------|--------------------------------------------------|
| Orchestrateur         | Initialise, priorise, affecte, contrôle le lock  |
| Analyste fonctionnel  | Exigences vérifiables, critères d'acceptation    |
| Architecte Python     | Architecture, ADR, contrats publics              |
| Découpeur backlog     | US / Features / Backlogs atomiques               |
| Développeur Python    | Implémentation, tests, qualité, handoff          |
| Ingénieur QA          | Vérification tests, couverture, non-régression   |
| Reviewer technique    | Relecture code, architecture, périmètre          |
| Release manager       | Tag, release GitHub, publication PyPI            |
