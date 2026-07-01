# baobab-auth-api

[![CI](https://github.com/baobabgit/baobab-auth-api/actions/workflows/ci.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-api/actions/workflows/ci.yml)
[![Integration](https://github.com/baobabgit/baobab-auth-api/actions/workflows/integration.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-api/actions/workflows/integration.yml)
[![Release](https://github.com/baobabgit/baobab-auth-api/actions/workflows/release.yml/badge.svg)](https://github.com/baobabgit/baobab-auth-api/actions/workflows/release.yml)
[![PyPI version](https://img.shields.io/pypi/v/baobab-auth-api.svg)](https://pypi.org/project/baobab-auth-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/baobab-auth-api.svg)](https://pypi.org/project/baobab-auth-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

API FastAPI d'authentification de l'écosystème **Baobab Auth**. Elle expose les routes
HTTP (inscription, connexion, refresh, logout, profil, JWKS, catalogue RBAC) et
orchestre les librairies [`baobab-auth-core`](https://pypi.org/project/baobab-auth-core/),
[`baobab-auth-database`](https://pypi.org/project/baobab-auth-database/) et
[`baobab-auth-security`](https://pypi.org/project/baobab-auth-security/).

## Fonctionnalités (v0.1.0)

- Inscription, connexion, refresh et déconnexion
- Endpoint `/me` (profil authentifié)
- Exposition JWKS pour validation des tokens côté consommateur
- Catalogue lecture seule des rôles et permissions
- Health (`/health`) et readiness (`/ready`)
- Factory `create_app()` importable comme librairie

## Démarrage rapide

```bash
git clone https://github.com/baobabgit/baobab-auth-api.git
cd baobab-auth-api
uv sync
cp .env.example .env
uv run uvicorn baobab_auth_api.main:app --reload
```

Qualité complète (format, lint, typage, sécurité, tests ≥ 95 %, build) :

```bash
uv run nox -s all
```

## Usage programmatique

```python
from baobab_auth_api import create_app

app = create_app()
```

Le serveur HTTP est démarré par l'hôte (`uvicorn`, conteneur Docker, etc.) — pas par le package.

## Configuration

Variables d'environnement (voir [`.env.example`](.env.example)) :

| Préfixe | Description |
| --- | --- |
| `AUTH_API_` | Nom, environnement, CORS (`AuthApiSettings`) |
| `AUTH_DB_` | URL base de données, pool SQLAlchemy |
| `BAOBAB_SECURITY_` | TTL tokens, Argon2, émetteur JWT |

## Architecture

Couche HTTP fine au-dessus du domaine :

```text
baobab-auth-core      → cas d'usage, entités, ports
baobab-auth-database  → persistance SQLAlchemy, Unit of Work
baobab-auth-security  → hash, JWT, JWKS
baobab-auth-api       → FastAPI, schémas HTTP, orchestration
```

Décision structurante : [`docs/architecture/adr/0001-api-layered-architecture.md`](docs/architecture/adr/0001-api-layered-architecture.md).

## Intégration inter-librairies

Matrice : [`docs/integrations/compatibility_matrix.yaml`](docs/integrations/compatibility_matrix.yaml).

| Dépendance | Version validée | Statut |
| --- | --- | --- |
| baobab-auth-core | 0.5.1 | PASSED |
| baobab-auth-database | 0.1.1 | PASSED |
| baobab-auth-security | 0.1.1 | PASSED |

## Contribuer

Règles : [`AGENTS.md`](AGENTS.md). Workflow : [`docs/ai_workflow/workflow.md`](docs/ai_workflow/workflow.md).
Branche `bl/XXX-description` depuis `version/vX.Y.Z`, commit `BL-XXX: action`.

## Licence

MIT — voir [`LICENSE`](LICENSE).
