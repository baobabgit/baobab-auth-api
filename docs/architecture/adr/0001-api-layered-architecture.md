# ADR-0001 — Architecture en couches de baobab-auth-api

**Statut :** accepté  
**Date :** 2026-07-01  
**Version :** v0.1.0

## Contexte

`baobab-auth-api` est la brique HTTP FastAPI de l'écosystème `baobab-auth`. Elle doit
orchestrer `baobab-auth-core`, `baobab-auth-database` et `baobab-auth-security` sans
réimplémenter la logique métier, la persistance ou la cryptographie.

## Décision

Adopter une architecture en quatre couches :

1. **Routers HTTP** — traduction requête/réponse, codes HTTP, validation Pydantic.
2. **Services applicatifs API** — orchestration des cas d'usage core dans une UoW.
3. **Infrastructure** — câblage database, security, générateurs d'ID, état applicatif.
4. **Librairies aval** — core (use cases), database (repositories), security (JWT/JWKS).

Les routes FastAPI sont encapsulées dans des classes (1 classe = 1 fichier) exposant
un `APIRouter`. L'état partagé est porté par `app.state` via un `AppState` initialisé
au lifespan.

## Conséquences

- Aucun modèle SQLAlchemy ni algorithme crypto dans l'API.
- Les tests API utilisent des fakes core + `SecurityTestHarness` ; les tests
  d'intégration utilisent SQLite en mémoire via `baobab-auth-database`.
- Les erreurs domaine sont mappées vers `{error: {code, message}}`.
