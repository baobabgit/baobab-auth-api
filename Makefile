# Commandes standard du projet — toutes les exécutions passent par uv.
.DEFAULT_GOAL := help

.PHONY: help install quality test build traceability all clean new-version new-backlog

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Installe l'environnement de dev + hooks pre-commit
	uv sync
	uv run pre-commit install --hook-type commit-msg
	uv run pre-commit install

quality: ## Formatage (black), lint (ruff), typage (mypy), sécurité (bandit)
	uv run black --check src tests
	uv run ruff check src tests
	uv run mypy src
	uv run bandit -r src -c pyproject.toml

test: ## Tests + couverture ≥ 95 %
	uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95

build: ## Construit le package et vérifie la distribution
	uv build
	uv run twine check dist/*

traceability: ## Vérifie la traçabilité besoin → backlog → run
	uv run python scripts/check_traceability.py

new-version: ## Crée le squelette d'une version  (VERSION=vX.Y.Z)
	@test -n "$(VERSION)" || (echo "Usage: make new-version VERSION=vX.Y.Z" && exit 1)
	uv run python scripts/scaffold.py new-version $(VERSION)

new-backlog: ## Crée le squelette d'un backlog  (BL=BL-001 TITLE="Description")
	@test -n "$(BL)" || (echo 'Usage: make new-backlog BL=BL-001 TITLE="Description"' && exit 1)
	uv run python scripts/scaffold.py new-backlog $(BL) "$(TITLE)"

all: quality test build traceability ## Exécute quality + test + build + traçabilité

clean: ## Nettoie les caches et artefacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov coverage.xml .coverage dist/ docs/_build docs/api/_autosummary
