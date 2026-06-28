# Example Package

[![Integration](https://github.com/your-org/your-repo/actions/workflows/integration.yml/badge.svg)](https://github.com/your-org/your-repo/actions/workflows/integration.yml)
[![Release](https://github.com/your-org/your-repo/actions/workflows/release.yml/badge.svg)](https://github.com/your-org/your-repo/actions/workflows/release.yml)
[![PyPI version](https://img.shields.io/pypi/v/example-package.svg)](https://pypi.org/project/example-package/)
[![Python versions](https://img.shields.io/pypi/pyversions/example-package.svg)](https://pypi.org/project/example-package/)
<!-- Badge Read the Docs : à réactiver une fois l'hébergement de doc configuré.
[![Documentation Status](https://readthedocs.org/projects/your-repo/badge/?version=latest)](https://your-repo.readthedocs.io/en/latest/)
-->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

> Template de projet Python orienté objet, pensé pour être développé par **plusieurs outils**
> (Claude Code, Cursor, Codex) qui partagent un **jeu de règles unique** via `AGENTS.md`.

> ℹ️ Remplacez `your-org/your-repo`, `example-package` et le package `example_package`
> par les valeurs de votre projet (badges, `pyproject.toml`, dossiers `src/` et `tests/`).

## Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Stack technique](#stack-technique)
- [Architecture](#architecture)
- [Structure du projet](#structure-du-projet)
- [Démarrage rapide](#démarrage-rapide)
- [Configuration](#configuration)
- [Sécurité](#sécurité)
- [Contribuer](#contribuer)
- [Et après ?](#et-après-)
- [Licence](#licence)
- [Remerciements](#remerciements)
- [Auteur](#auteur)

## À propos

Ce dépôt est un **template de développement**. Il fixe des règles claires
(orienté objet, 1 classe par fichier, typage strict, tests ≥ 95 %, doc RST) et
les rend applicables par **trois assistants IA** via une source unique de vérité
(`AGENTS.md`). Objectif : produire un code homogène **sans rappeler les règles à
chaque prompt**.

## Fonctionnalités

- 🤖 **Règles multi-IA unifiées** : `AGENTS.md` (source unique) lu par Codex,
  importé par `CLAUDE.md`, reflété dans `.cursor/rules/`.
- 🧱 **Conventions POO strictes** : 1 classe = 1 fichier, tests en arborescence miroir.
- ✅ **Qualité garantie** : `ruff` + `mypy` strict + `pytest` (couverture ≥ 95 %),
  doublés de `pre-commit` et d'une CI GitHub Actions.
- 📚 **Documentation Sphinx/RST** : spécifications (US/FEAT), API (autodoc), guides (Diátaxis).
- 🗂️ **Traçabilité** besoin → code → test via les identifiants `US / FEAT / TASK`.

## Stack technique

| Domaine        | Outil                                  |
| -------------- | -------------------------------------- |
| Langage        | Python ≥ 3.13                          |
| Environnement  | `uv` + lockfile `uv.lock`              |
| Format         | `black`                                |
| Lint           | `ruff`                                 |
| Typage         | `mypy` (strict)                        |
| Sécurité       | `bandit`                               |
| Tests          | `pytest` + `pytest-cov` (≥ 95 %)      |
| Documentation  | `sphinx` (+ `furo`), reStructuredText  |
| Config         | `pydantic-settings`                    |
| CI / Hooks     | GitHub Actions, `pre-commit`           |

## Architecture

Deux axes orthogonaux structurent le projet :

- **Le « quoi »** : `Cahier des charges → US → FEAT → Task` (arbre de besoin).
- **Le « quand »** : sprints (champ *Iteration* de GitHub Projects).

```
Besoin (docs/specifications, RST)
   └─ US-001 ──► Issue ─┐
        └─ FEAT-001.1 ──► sub-issue ─┐  ◄── code (src/) + tests (tests/, miroir)
             └─ TASK-001.1.1 ──► sub-issue ──► sprint (Iteration)
```

## Structure du projet

```
.
├── AGENTS.md              # Règles de dev — SOURCE UNIQUE DE VÉRITÉ
├── CLAUDE.md             # Adaptateur Claude Code (importe AGENTS.md)
├── .cursor/rules/        # Adaptateur Cursor (reflète AGENTS.md)
├── src/example_package/  # Code (1 classe par fichier)
├── tests/unit/example_package/ # Tests en miroir de src/
├── docs/                 # Sphinx : specifications/ · api/ · guides/
│   └── workflow/         # Process multi-IA : rôles, gates, handoff, prompts
├── .github/              # CI + templates d'issues (US/FEAT/Task) + PR
├── pyproject.toml        # Config unique (projet, ruff, mypy, pytest, coverage)
├── .pre-commit-config.yaml
└── Makefile              # Commandes standard (install, lint, type, test, docs)
```

## Démarrage rapide

```bash
# 1. Cloner
git clone https://github.com/your-org/your-repo.git
cd your-repo

# 2. Installer l'environnement + les hooks (via uv)
make install

# 3. Vérifier (qualité + tests ≥ 95 % + build)
make all
```

Prérequis : [uv](https://docs.astral.sh/uv/) installé (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

## Configuration

La configuration passe par des **variables d'environnement** validées via
`pydantic-settings`. Copiez le modèle et renseignez vos valeurs :

```bash
cp .env.example .env
```

| Variable    | Description                      | Défaut        |
| ----------- | -------------------------------- | ------------- |
| `APP_ENV`   | Environnement applicatif         | `development` |
| `LOG_LEVEL` | Niveau de journalisation         | `INFO`        |

## Sécurité

- **Aucun secret** dans le code ni dans Git : `.env` est gitignoré ; seul
  `.env.example` (sans valeurs) est versionné.
- Le hook `detect-private-key` et `pre-commit` bloquent les fuites évidentes.
- Analyse `bandit` (SAST) + Dependabot alerts (vulns des dépendances).
- Signalez toute vulnérabilité en privé (voir [`SECURITY.md`](SECURITY.md)) plutôt
  que via une issue publique.

## Contribuer

Les règles de développement sont décrites dans [`AGENTS.md`](AGENTS.md) et le
processus dans [`docs/ai_workflow/workflow.md`](docs/ai_workflow/workflow.md).
En résumé : branche `bl/XXX-description` depuis `version/vX.Y.Z`,
commit `BL-XXX: action`, PR verte (qualité + tests ≥ 95 % + build).

## Intégration inter-librairies

Les contrats publics sont dans [`docs/contracts/`](docs/contracts/).
La matrice de compatibilité est dans
[`docs/integrations/compatibility_matrix.yaml`](docs/integrations/compatibility_matrix.yaml).
Le workflow `integration.yml` valide automatiquement les intégrations déclarées.

## Et après ?

- [ ] Brancher le dépôt sur GitHub Projects (US / FEAT / Task + sprints).
- [ ] Publier la documentation (Read the Docs).
- [ ] Configurer les environments GitHub (`pypi`) pour le Trusted Publishing.
- [ ] Renseigner la matrice de compatibilité si la librairie dépend d'autres packages.

## Licence

Distribué sous licence **MIT**. Voir [`LICENSE`](LICENSE).

