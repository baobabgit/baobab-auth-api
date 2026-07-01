# Index — Cahiers des charges versionnés `baobab-auth-api`

Cet index récapitule les fichiers générés pour l’implémentation progressive de `baobab-auth-api`.

| Version API | Jalon | Dépendances directes à valider |
|---|---|---|
| `v0.1.0` | Socle API FastAPI, authentification minimale et contrats publics | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.1.1`, `baobab-auth-security v0.1.1` |
| `v0.2.0` | Sessions, refresh token rotation et readiness robuste | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.2.0`, `baobab-auth-security v0.2.0` |
| `v0.3.0` | RBAC HTTP, autorisation applicative et contrats rôles/permissions | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.3.0`, `baobab-auth-security v0.2.0` |
| `v0.4.0` | Audit, lockout, erreurs non divulgantes et durcissement sécurité HTTP | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.4.0`, `baobab-auth-security v0.3.0` |
| `v0.5.0` | JWKS avancé, rotation de clés et validation cryptographique contractuelle | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.5.0`, `baobab-auth-security v0.4.0` |
| `v0.6.0` | Endpoints d’administration sécurisée utilisateurs et sessions | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.6.0`, `baobab-auth-security v0.4.0` |
| `v0.7.0` | Contrats client, intégration APIs consommatrices et compatibilité OpenAPI | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.6.0`, `baobab-auth-security v0.5.0` |
| `v0.8.0` | Exploitation, observabilité, rate limiting et préparation service Docker | `baobab-auth-core v0.4.0`, `baobab-auth-database v0.7.0`, `baobab-auth-security v0.5.0` |
| `v0.9.0` | Release candidate, non-régression globale et gel des contrats publics | `baobab-auth-core v0.4.0 à v0.9.x`, `baobab-auth-database v0.9.0`, `baobab-auth-security v0.9.0` |
| `v1.0.0` | Version stable, compatibilité inter-briques validée et API publique figée | `baobab-auth-core v1.0.0`, `baobab-auth-database v1.0.0`, `baobab-auth-security v1.0.0` |
