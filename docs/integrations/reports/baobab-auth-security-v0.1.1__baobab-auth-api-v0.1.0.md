# Rapport d'intégration — baobab-auth-security v0.1.1 → baobab-auth-api v0.1.0

Date : 2026-07-01  
Statut : **PASSED**

## Périmètre validé

- CorePasswordHasherAdapter, CoreTokenProviderAdapter
- LocalJwksProvider, JWT RS256
- Émission et validation access/refresh tokens

## Résultat

JWKS sans clé privée, login/refresh/me validés en tests API.
