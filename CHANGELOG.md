# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

- `scripts/sync_from_template.sh` : script de synchronisation sélective des
  fichiers infra (CI, règles IA, outils) depuis le template source vers un projet
  dérivé, sans toucher au code ni aux métadonnées du projet.
- `docs/guides/how-to/template-sync.rst` : guide RST décrivant la procédure de
  synchronisation depuis le template (remote upstream, script, révisions manuelles).
- `docs/ai_workflow/roles/orchestrateur.md` : prompt prêt à coller pour le rôle
  orchestrateur — gère la reprise de session, le verrou et les quatre cas possibles
  au démarrage.
- `.cursor/rules/00-global-workflow.mdc` : règle Cursor `alwaysApply: true` pour
  le ritual de démarrage de session et la gestion du verrou.
- Ritual de démarrage de session obligatoire dans `AGENTS.md` : lecture de
  `lock.yaml` → `queue.yaml` → `status.yaml` → `07_handoff.md`, annonce de l'état,
  pose du verrou avant toute modification.

### Modifié

- `ci.yml` : ajout de `uv audit` comme gate bloquant de vulnérabilités des
  dépendances (après Bandit), sans `continue-on-error`.
- `scripts/setup_github.sh` : contextes du ruleset mis à jour pour correspondre
  aux noms de jobs CI actuels (`Qualité + Typage + Sécurité`,
  `Tests + couverture ≥ 95 %`, `Build package`).
- `docs/guides/index.rst` : ajout des entrées `integration-validation` et
  `template-sync` dans le toctree how-to.

### Corrigé

- `README.md` : seuil de couverture 90 % → 95 %, chemin de tests
  `tests/example_package/` → `tests/unit/example_package/`, référence pip-audit
  supprimée.
- `docs/workflow/SETUP.md` : noms de jobs dans le JSON du ruleset corrigés pour
  correspondre à la CI fusionnée.
- `noxfile.py` : violation E501 corrigée (ligne bandit découpée).
- `scripts/check_no_ai_attribution.py` : violations E501, PTH123 (`open()` →
  `Path.read_text()`), PLR2004 (constante `_MIN_ARGS` au lieu de valeur magique).

### Modifié (évolution du template — nouveau cahier des charges)

- **Gestionnaire de dépendances** : migration de `pip`/`venv` vers `uv` ; `uv.lock`
  versionné pour des builds reproductibles ; `.python-version` figée à `3.13`.
- **Python minimum** : `>=3.11` → `>=3.13` ; CI et mypy mis à jour en conséquence.
- **Couverture minimale** : `90 %` → `95 %` dans `pyproject.toml`, `Makefile`, CI et
  hook `pre-commit`.
- **Formatage + lint séparés** : `ruff format` remplacé par `black` (format) ; `ruff`
  conservé pour le lint uniquement. Pre-commit mis à jour (hook `black` ajouté, hook
  `ruff-format` supprimé).
- **Trois workflows CI** : `ci.yml` restructuré (jobs `quality`, `typing`, `security`,
  `tests`, `commit-policy`, `build` via `uv`) ; `integration.yml` créé (déclenché sur
  les PR vers `version/**`, conditionnel selon `integration_required`) ; `release.yml`
  simplifié (ne réexécute pas la CI, vérifie tag + CHANGELOG, publie via Trusted
  Publishing OIDC).
- **Modèle Git à 3 niveaux** : `main → version/vX.Y.Z → bl/XXX` (suppression des
  branches `us/` et `feat/` qui étaient des branches Git — désormais regroupements
  logiques dans les `status.yaml`).
- **Versionnage statique** : `hatch-vcs` supprimé ; version `0.1.0` déclarée
  statiquement dans `pyproject.toml`.
- **SemVer sans borne supérieure** : le template accompagne une librairie de `v0.1.0`
  vers `v1.0.0` et au-delà.
- **AGENTS.md** refonte complète : ajout des sections uv, tests `tests/unit/`,
  modèle Git 3 niveaux, verrou, recovery, versions, intégrations, SemVer.
- **CLAUDE.md** : références mises à jour (`tests/unit/`, `make all`, verrou, règle
  anti-attribution).
- `.cursor/rules/000-core.mdc` : aligné sur les nouvelles règles.
- `Makefile` : cibles `quality`, `test`, `build`, `all` via `uv run`.
- `noxfile.py` : sessions `quality`, `tests`, `build`, `all` créées.

### Ajouté

- `scripts/check_no_ai_attribution.py` : hook `commit-msg` et outil CI rejetant toute
  attribution interdite dans les messages de commit.
- `.codex/rules/default.rules` : règles Codex (`uv run *` autorisé, `rm -rf` interdit,
  `git push`/`git tag` à confirmer).
- `.python-version` : fixe Python 3.13 pour uv et les outils.
- `uv.lock` : lockfile reproductible.
- `noxfile.py` : sessions qualité/tests/build.
- `docs/ai_workflow/` : structure complète (workflow.md, state/lock.yaml,
  state/queue.yaml, state/dependency_graph.yaml, runs/, roles/, versions/, priorities/).
- `docs/backlog/` : structure (user_stories/, features/, backlogs/).
- `docs/contracts/` : contrats publics (public_api.md, imports.md, exceptions.md,
  models.md, services.md, compatibility.md).
- `docs/integrations/` : compatibility_matrix.yaml + reports/.
- `docs/architecture/adr/` : dossier pour les Architecture Decision Records.
- `tests/unit/` : les tests exemple déplacés depuis `tests/example_package/`.
- `tests/integration/`, `tests/contracts/`, `tests/fixtures/` : nouveaux dossiers.
- `.github/workflows/integration.yml` : workflow d'intégration inter-librairies.
- Badges README : `integration` et `release` ajoutés ; badges simplifiés à 3 workflows.

### Supprimé

- `pip-audit` : retiré des dépendances de dev (non mentionné dans le nouveau CDC).
- Version dérivée du tag git (`hatch-vcs`) : remplacée par versionnage statique.

### Modifié (suite changelog existant)
- Retours du premier dogfood : `init.md` pointe vers `SETUP.md`, étape d'adaptation des
  métadonnées au CDC, réécriture de l'intro README à l'étape PO, décision explicite sur les
  placeholders, et badge Read the Docs neutralisé par défaut.
- Règle « 1 classe = 1 fichier » : dérogation documentée pour les hiérarchies d'exceptions
  (sous-package `exceptions/` par catégorie).
- `scripts/setup_github.sh` : configuration GitHub idempotente (labels, ruleset de
  protection, environnements), tolérante au plan, câblée dans le bootstrap. `SETUP.md` §4
  corrigé (pas d'approbation de PR en mode solo ; protection indisponible en privé/Free).
- Roadmap : champs Date `Début`/`Fin` du Project (gratuits), renseignés aux transitions
  (In progress → Début, Done → Fin) ; documenté dans `gates.md` et le bootstrap.
- Ruff : règle `D401` (imperative mood, heuristique anglaise) désactivée — inadaptée aux
  docstrings françaises.
- Stratégie de branches documentée : trunk-based en v1, modèle imbriqué
  `TASK→FEAT→US→main` réservé à la v2 concurrence.
- Règle « fermeture au merge » (U3) : une issue ne se ferme qu'après le merge de sa PR
  sur `main` — évite les issues « closes mais non livrées » (incident dogfood).

### Ajouté
- Structure initiale du template (règles multi-IA, docs Sphinx, CI, exemples).
- Workflow multi-IA : `docs/workflow/` (rôles, gates, handoff, prompts init/orchestration).
- Sécurité de base : `bandit`, `pip-audit`, Dependabot, `SECURITY.md`.
- Dossier d'intake `docs/specifications/cahier-des-charges/` et champ `:origin:`.
- Contrat d'API publique (`__all__`) avec règle de bump majeur sur rupture.
- CI réorganisée en jobs (lint, type, security, docs, test matriciel) avec concurrency.
- Pipeline de release `release.yml` : tag `v*` → PyPI public (OIDC) + Release GitHub.
- Version dérivée du tag git via `hatch-vcs` (le tag est l'unique source de version).
- Snapshots CI : Bandit en SARIF (onglet Security), job `build` de validation packaging,
  artefacts couverture HTML + JUnit + doc HTML.
- SBOM CycloneDX (via `pip-audit`) attaché aux Releases.
- Durcissement release : TestPyPI sur pré-releases (`vX.Y.Zrc1`), attestation de
  provenance (supply chain), upload SARIF tolérant (repo privé sans GHAS).
- `docs/workflow/SETUP.md` : checklist de configuration GitHub one-time (commandes `gh`).

## [0.1.0] - 2026-06-18

### Ajouté
- Squelette du projet : `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`.
- Exemples `Greeter` (classe concrète) et `Repository` (classe abstraite) + tests miroir.
