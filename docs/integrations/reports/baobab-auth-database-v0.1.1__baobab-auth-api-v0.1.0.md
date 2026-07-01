# Rapport d'intégration — baobab-auth-database v0.1.1 → baobab-auth-api v0.1.0

Date : 2026-07-01  
Statut : **PASSED**

## Périmètre validé

- SqlAlchemyAuthUnitOfWork, AuthCatalogBootstrap, repositories
- Persistance SQLite fichier (tests API)

## Note

Adaptateur timezone API (`SessionRepositoryTimezoneAdapter`) requis pour SQLite
(datetimes naïfs vs UTC aware du core).

## Résultat

Tests API register/login/refresh/logout/me passés.
