# AGENTS.md — Règles de développement (source unique de vérité)

> Ce fichier est **la** source des règles pour **toutes** les IA de développement
> (Codex le lit nativement ; `CLAUDE.md` l'importe ; `.cursor/rules/000-core.mdc` le reflète).
> Toute modification de règle se fait **ici**, jamais en double.

---

## Langage & conception

- Langage : **Python ≥ 3.13**, **orienté objet**. Respect de **SOLID**, composition > héritage.
- **1 classe = 1 fichier.** Le module porte le nom de la classe en `snake_case`
  (`class FactureClient` → `facture_client.py`).
  - *Dérogation* : une **hiérarchie d'exceptions** (classes courtes) peut être regroupée
    dans un sous-package `exceptions/` organisé **par catégorie** (un fichier par famille).
- Pas de logique exécutable au niveau module ; tout passe par des classes/méthodes.

## Librairie consommable (contrat d'API)

- Le livrable est une **librairie réutilisable**, susceptible d'être intégrée dans un
  projet parent. Ce qui est exporté dans `__all__` est un **contrat**.
- Rupture du contrat (suppression/modification incompatible d'un symbole public) →
  **bump SemVer majeur** + entrée `CHANGELOG` « BREAKING » + note de migration.
- Aucune hypothèse sur l'hôte : pas d'état global, config **injectée** (`pydantic-settings`).
  Ce dépôt *expose*, il ne *dépend jamais* d'un projet parent.

## PEP 8 & PEP 20

- Respect de **PEP 8** (style) et de **PEP 20** (Zen of Python : explicite, simple, lisible).
- **En cas de conflit entre PEP 8 et PEP 20, la PEP 8 prime.**

## Typage & style

- **Type hints obligatoires** sur toutes les signatures (paramètres et retours).
- Format : **`black`** (line-length 88). Lint : **`ruff`** (lint uniquement, pas format).
  Vérification de types : **`mypy`** (mode strict).
- **Docstrings en reStructuredText (RST)** sur tout élément public
  (champs `:param:`, `:returns:`, `:raises:`, et `:spec: <ID>` pour la traçabilité).

## Tests

- Framework : **`pytest`**, structure **AAA** (Arrange / Act / Assert), tests déterministes.
- **Arborescence miroir** : `src/<pkg>/a/b/c.py` ⇒ `tests/unit/<pkg>/a/b/test_c.py`.
- **Une classe testée = une classe de test** (`class FactureClient` ⇒ `class TestFactureClient`).
- **Classe abstraite** : testée via une **classe concrète de test** définie dans le fichier de test.
- Nom de test porteur de l'ID spec : `def test_FEAT_001_1_cas_nominal(...)`.
- **Couverture ≥ 95 %**, imposée par `--cov-fail-under=95` (voir `pyproject.toml`).
- Les tests d'intégration vont dans `tests/integration/`, les tests de contrat dans
  `tests/contracts/`, les fixtures partagées dans `tests/fixtures/`.

## Documentation

- **Sphinx** + **RST**. La doc API est générée par **`autodoc`** depuis les docstrings.
- Dossier **`docs/guides/` obligatoire**, organisé selon **Diátaxis** :
  `tutorials/` (apprendre) et `how-to/` (résoudre un problème précis).
- **`README.md`** : porte **tous les badges** CI (ci, integration, release) et les sections
  minimales : installation, usage, qualité, tests, release, intégration, licence.

## Arborescence (layout `src/`)

```
.
├── src/<package>/        # code (1 classe par fichier)
├── tests/
│   ├── unit/<package>/   # tests unitaires en miroir de src/
│   ├── integration/      # tests d'intégration inter-librairies
│   ├── contracts/        # tests de contrat des API publiques
│   └── fixtures/         # fixtures partagées
├── docs/
│   ├── specifications/   # cahier des charges : US / FEAT (RST, stable)
│   ├── ai_workflow/      # workflow IA : state/, runs/, versions/, roles/
│   ├── backlog/          # user_stories/, features/, backlogs/
│   ├── contracts/        # contrats publics de la librairie
│   ├── integrations/     # matrices de compatibilité + rapports
│   ├── architecture/adr/ # Architecture Decision Records
│   ├── api/              # doc API (autodoc)
│   └── guides/           # tutorials/ + how-to/  (OBLIGATOIRE)
├── pyproject.toml        # config unique (projet, black, ruff, mypy, pytest, coverage)
├── uv.lock               # lockfile reproductible (versionné)
├── .python-version       # version Python figée (3.13)
├── .pre-commit-config.yaml
├── noxfile.py
└── .github/              # CI (ci.yml, integration.yml, release.yml) + PR template
```

## Gestion des dépendances avec `uv`

- **`uv`** est le gestionnaire d'environnement et de dépendances.
- Les dépendances sont déclarées dans `pyproject.toml` sous `[dependency-groups]`.
- Le fichier **`uv.lock`** est **versionné** (builds reproductibles).
- L'interpréteur est figé par **`.python-version`** (`3.13`).
- Commandes courantes :
  - `uv sync` — installe l'environnement depuis uv.lock
  - `uv sync --frozen` — en CI (échoue si le lock n'est pas à jour)
  - `uv add <paquet>` — ajoute une dépendance et met à jour le lock
  - `uv run <commande>` — exécute dans l'environnement uv
  - `uv build` — construit le package

## Standards qualité obligatoires

Commandes (toutes via `uv run`) :

```bash
# Qualité
uv run black --check src tests
uv run ruff check src tests
uv run mypy src
uv run bandit -r src -c pyproject.toml

# Tests
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95

# Build
uv build
uv run twine check dist/*
```

Cible unique : `make all` (ou `uv run nox -s all`).

Sont bloquants : erreur black, erreur ruff, erreur mypy, warning non corrigé,
couverture < 95 %, alerte bandit non triée, build invalide, distribution invalide,
badge CI en échec, intégration inter-librairie en échec.

## Sécurité

- **Aucun secret** dans le code ou Git. Variables via `.env` (gitignoré) + `.env.example` versionné.
- Chargement/validation de la config via **`pydantic-settings`**.

## Git & traçabilité

### Modèle de branches (3 niveaux)

```
main
└── version/vX.Y.Z
    └── bl/XXX-description
```

- `main` — code stable uniquement, porte les tags de release.
- `version/vX.Y.Z` — tout le travail d'une version ; créée depuis `main`.
- `bl/XXX-description` — implémentation atomique d'un backlog ; créée depuis
  `version/vX.Y.Z`, mergée vers `version/vX.Y.Z` par PR après CI verte.
- Les User Stories (`US-XXX`) et Features (`FEAT-XXX`) sont des **regroupements logiques**
  portés dans les backlogs et les `status.yaml` ; **ce ne sont pas des branches Git**.
- Une seule branche `bl/` peut être active (non mergée) à la fois.
- Merges toujours ascendants : `bl/` → `version/` → `main`.
- Aucun commit direct sur `main`. Aucun tag si la version n'est pas `RELEASE_READY`.

### Messages de commit

Format obligatoire : `BL-XXX: action courte et explicite`

Exemples corrects :
```
BL-012: implement user repository
BL-013: add user repository unit tests
BL-014: document public user service
```

**Interdictions absolues** (contrôlées par le hook `no-ai-attribution`) :
- mentionner un outil (Cursor, Claude, Codex…)
- mentionner une génération automatique
- ajouter un trailer `Co-authored-by:`
- ajouter une signature d'assistant

### Conventional Commits & chaîne d'ID

Format alternatif pour les commits hors BL (refacto, CI, docs) :
`feat(FEAT-001.1): export PDF de la facture`

Chaîne propagée partout : **US-001** → **FEAT-001.1** → **TASK-001.1.1**
(titres d'issues, branches bl/, commits, noms de tests, docstrings `:spec:`).

**SemVer** pour les versions, sans borne supérieure :
- `MAJOR` : rupture de l'API publique ;
- `MINOR` : ajout rétrocompatible ;
- `PATCH` : correction rétrocompatible.

**Fermeture au merge** : une issue ne se ferme qu'après le merge de sa PR sur `main`.

## Interdiction de mention contributive des outils

**Aucun outil de développement assisté ne doit être mentionné comme contributeur,
auteur, co-auteur, mainteneur ou générateur du projet.**

Cette règle s'applique partout :
- `README.md`, `CHANGELOG.md`, documentation projet
- messages de commit, descriptions de PR, notes de release
- métadonnées `pyproject.toml`, fichiers `AUTHORS` ou `CONTRIBUTORS`
- commentaires de code, docstrings, rapports de revue ou de release
- logs de workflow conservés dans le dépôt

Un hook `pre-commit` de type `commit-msg` (`no-ai-attribution`) **rejette automatiquement**
tout commit dont le message contient une formulation interdite.
Ce contrôle est également rejoué en CI (job `commit-policy` dans `ci.yml`).

## Démarrage de session (ritual obligatoire)

**À faire en tout premier, avant toute modification de fichier :**

1. **Lire `docs/ai_workflow/state/lock.yaml`**
   - `locked: true` + `expires_at` futur → stop. Un autre outil est actif.
   - `locked: true` + `expires_at` dépassé → verrou orphelin → suivre la procédure de recovery.
   - `locked: false` → continuer.

2. **Lire `docs/ai_workflow/state/queue.yaml`** — identifier le backlog actif (`status: IN_PROGRESS`)
   ou le prochain à démarrer (`status: READY`).

3. **Lire `docs/ai_workflow/runs/BL-XXX/status.yaml`** du run en cours
   — connaître l'étape atteinte et le rôle en cours.

4. **Lire `docs/ai_workflow/runs/BL-XXX/07_handoff.md`** — note de passation
   laissée par la session précédente.

5. **Annoncer** : état du verrou, backlog concerné, dernière étape accomplie, prochaine action.
   Puis poser le verrou (`locked: true`, `expires_at: +2h`) et démarrer.

Ce ritual s'applique que la session reprenne un travail interrompu ou démarre un nouveau backlog.

## Gestion du verrou de travail

Un seul outil peut travailler à un instant donné. Le verrou est géré via :

```
docs/ai_workflow/state/lock.yaml
```

Règles :
- `locked: false` → un outil peut démarrer.
- `locked: true` + `expires_at` dans le futur → aucun autre outil ne modifie le projet.
- `locked: true` + `expires_at` dépassé → verrou orphelin → procédure de recovery.
- Tout outil actif met à jour `last_heartbeat_at` et `expires_at` régulièrement.

En cas de verrou orphelin, produire `docs/ai_workflow/runs/<BL-ID>/08_recovery.md`
(voir `docs/ai_workflow/workflow.md` pour le détail de la procédure).

## Gestion des versions

Chaque version possède un dossier `docs/ai_workflow/versions/vX.Y.Z/` contenant :
`version.yaml`, `scope.md`, `validation.md`, `integration_matrix.yaml`, `release_report.md`.

Statuts : `PLANNED` → `IN_DEVELOPMENT` → `INTERNAL_VALIDATED` → `INTEGRATION_PENDING`
→ `INTEGRATION_VALIDATED` → `RELEASE_READY` → `RELEASED`.

Une version est `RELEASE_READY` uniquement si : tous les backlogs sont mergés, black +
ruff + mypy + bandit passent, couverture ≥ 95 %, build valide, twine check valide,
changelog à jour, badges README cohérents, intégrations obligatoires validées.

## Gestion inter-librairies

Les contrats publics sont dans `docs/contracts/`. La matrice de compatibilité est dans
`docs/integrations/compatibility_matrix.yaml`. Les rapports d'intégration sont dans
`docs/integrations/reports/`.

### Mécanisme d'intégration : git-ref directe

La validation inter-librairies se fait via **référence git directe** sur la branche
`version/vX.Y.Z` — aucune publication sur TestPyPI n'est requise.

**Côté producteur** (cette librairie) :
1. Atteindre `INTERNAL_VALIDATED` (`bl/` tous mergés, CI verte sur `version/`).
2. Déclarer les consommateurs à valider dans `compatibility_matrix.yaml` (`status: PENDING`).
3. Communiquer la branche aux consommateurs : `version/vX.Y.Z`.

**Côté consommateur** (librairie qui dépend de ce package) :
1. Remplacer la dépendance stable par la git-ref dans `pyproject.toml` :
   ```
   "example-package @ git+https://github.com/OWNER/REPO.git@version/vX.Y.Z"
   ```
2. Exécuter `uv sync` puis `make all` (ou `uv run pytest tests/integration/`).
3. Reporter le résultat (`PASSED` / `FAILED`) dans la `compatibility_matrix.yaml`
   du producteur et produire un rapport dans `docs/integrations/reports/`.
4. Revenir à la dépendance PyPI une fois la release publiée.

Une version est `INTEGRATION_VALIDATED` si : validation interne réussie, dépendances
compatibles, librairies consommatrices requises ont validé l'intégration (`status: PASSED`),
rapports d'intégration présents, matrices de compatibilité à jour.

## Workflow

Le processus de dev (rôles, états, handoff, prompts) est décrit dans
**`docs/ai_workflow/workflow.md`**. L'IA endosse un rôle à la fois, de façon
séquentielle, et reprend via la note de handoff + le `status.yaml` du run courant.

Format des fichiers : instructions opérationnelles en **Markdown** ; documentation
du projet (specifications, API, guides) en **reStructuredText**.

## Definition of Done (une tâche n'est close que si)

1. Code POO, 1 classe/fichier, type hints complets.
2. `black`, `ruff` (lint) et `mypy` strict passent.
3. Tests présents en miroir (`tests/unit/`), couverture ≥ 95 %.
4. Docstrings RST + guide mis à jour si le comportement public change.
5. Commit conforme (BL-XXX: + sans attribution IA), PR fusionnée sur `version/vX.Y.Z`.
6. Cahier des charges (`docs/specifications/`) déposé, User Stories et FEATs dérivées.
7. Fiche backlog `docs/backlog/backlogs/BL-XXX.md` renseignée avec la FEAT référencée.
8. Dossier run `docs/ai_workflow/runs/BL-XXX/` matérialisé, `status.yaml` à jour.
9. Toute décision d'architecture structurante couverte par un ADR (`docs/architecture/adr/`).
10. `make traceability` passe sans erreur.
