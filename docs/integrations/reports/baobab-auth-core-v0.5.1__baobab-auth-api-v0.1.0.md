# Rapport d'intégration — baobab-auth-core v0.5.1 → baobab-auth-api v0.1.0

Date : 2026-07-01  
Statut : **PASSED**

## Périmètre validé

- Cas d'usage RegisterUser, AuthenticateUser, RefreshSession, Logout, GetCurrentUser
- ListRoles, ListPermissions
- Ports PasswordHasher, TokenProvider, UnitOfWork

## Commandes

```bash
uv sync
uv run pytest tests/api/ tests/unit/ --cov=src --cov-fail-under=95
```

## Résultat

30 tests passés, couverture 96 %.
