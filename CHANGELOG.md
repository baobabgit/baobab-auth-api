# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

## [0.1.0] - 2026-07-01

### Ajouté

- Package `baobab-auth-api` : factory `create_app()`, configuration injectée (`AuthApiSettings`).
- Endpoints auth : `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`,
  `POST /auth/logout`, `GET /auth/me`.
- Endpoints JWKS et catalogue RBAC : `GET /.well-known/jwks.json`, `GET /roles`,
  `GET /permissions`.
- Health et readiness : `GET /health`, `GET /ready`.
- Intégration PyPI : `baobab-auth-core` 0.5.1, `baobab-auth-database` 0.1.1,
  `baobab-auth-security` 0.1.1 (matrice compatibilité PASSED).
- Tests API et unitaires (30 tests, couverture ≥ 96 %).
- ADR-0001 : architecture en couches HTTP / services / infrastructure.

### Supprimé

- Template `example_package` et tests associés.
