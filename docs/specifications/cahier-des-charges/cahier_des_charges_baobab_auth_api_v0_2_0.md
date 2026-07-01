# Cahier des charges — `baobab-auth-api` — v0.2.0

**Projet :** `baobab-auth-api`  
**Version cible :** `v0.2.0`  
**Titre :** Sessions, refresh token rotation et readiness robuste  
**Destination :** IA de développement  
**Format :** Markdown  
**Statut :** cahier des charges versionné  

---

## 1. Objectif de la version

Rendre le cycle de session fiable, auditable et testable. L’API doit pouvoir gérer la rotation des refresh tokens, refuser les sessions expirées ou révoquées et garantir une atomicité stricte entre token, session et audit.

---

## Références projet et contraintes transverses

Le projet `baobab-auth-api` est la brique HTTP FastAPI de l’écosystème `baobab-auth`. Elle expose les routes d’authentification, orchestre les librairies `baobab-auth-core`, `baobab-auth-database` et `baobab-auth-security`, et doit rester indépendante des applications métiers telles que Riftbound, Altered ou toute autre API consommatrice.

Le découpage cible de l’écosystème est le suivant :

```text
baobab-auth-core      -> logique métier pure, entités, policies, ports, cas d’usage
baobab-auth-database  -> SQLAlchemy, repositories, Unit of Work, migrations, persistance
baobab-auth-security  -> hash mot de passe, JWT, refresh tokens, JWKS, rotation de clés
baobab-auth-api       -> FastAPI, routes, schémas HTTP, erreurs HTTP, OpenAPI
baobab-auth-client    -> client Python et dépendances FastAPI côté API consommatrice
baobab-auth-admin     -> CLI d’administration technique
baobab-auth-service   -> assemblage Docker et déploiement
```

`baobab-auth-api` doit être empaquetée comme librairie Python importable et exécutable comme application FastAPI :

```python
from baobab_auth_api import create_app

app = create_app()
```

Le serveur ne doit pas être démarré directement par le package. Le démarrage s’effectue par `uvicorn`, un conteneur Docker ou une brique d’assemblage.

Contraintes de développement obligatoires pour toutes les versions :

- Python `>=3.11` ;
- structure `src/` ;
- fichier `py.typed` ;
- FastAPI et Pydantic v2 ;
- code typé strictement ;
- `ruff` pour format/lint ;
- `mypy` sans erreur bloquante ;
- `pytest` et `pytest-asyncio` ;
- couverture minimale `>=90 %` ;
- logs sans mot de passe, access token complet, refresh token brut, clé privée ou secret ;
- aucun modèle SQLAlchemy dans `baobab-auth-api` ;
- aucun algorithme cryptographique réimplémenté dans `baobab-auth-api` ;
- aucune logique métier Riftbound, Altered ou application consommatrice ;
- réponses d’erreur standardisées ;
- documentation Markdown maintenue à chaque version.

---

## 2. Versions des librairies dépendantes à valider

Les dépendances directes de `baobab-auth-api` sont `baobab-auth-core`, `baobab-auth-database` et `baobab-auth-security`. La version `v0.2.0` de l’API doit valider explicitement les versions suivantes avant d’être considérée comme terminée.

| Librairie dépendante directe | Version à valider | Pourquoi cette validation est obligatoire |
|---|---:|---|
| `baobab-auth-core` | `v0.4.0` | Revalider `SessionPolicy`, entité `Session`, ports de session, `TokenClaims`, événements `SESSION_REFRESHED`, `LOGOUT`, `ALL_SESSIONS_REVOKED` si disponibles. |
| `baobab-auth-database` | `v0.2.0` | Valider persistance complète des sessions, recherche par refresh token id/hash, révocation, expiration, transactions atomiques. |
| `baobab-auth-security` | `v0.2.0` | Valider refresh tokens opaques, hash refresh token, `TokenId`, `SessionId`, validation de révocation et mappers core/security. |

### Briques aval ou connexes à valider sans les traiter comme dépendances directes

| Brique | Version / statut à valider | Contrat attendu |
|---|---:|---|
| `baobab-auth-client` | `v0.1.0` | Valider login/refresh/logout/me/jwks/health avec client HTTP async. |

Règle de poursuite : une librairie dépendante ne doit pas poursuivre vers son jalon suivant si l’intégration prévue avec `baobab-auth-api` `v0.2.0` échoue sur un contrat bloquant.

---

## Architecture cible du package

Arborescence attendue :

```text
baobab-auth-api/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── src/
│   └── baobab_auth_api/
│       ├── __init__.py
│       ├── py.typed
│       ├── main.py
│       ├── app.py
│       ├── config.py
│       ├── dependencies.py
│       ├── exceptions.py
│       ├── error_handlers.py
│       ├── lifespan.py
│       ├── openapi.py
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── jwks.py
│       │   ├── roles.py
│       │   ├── permissions.py
│       │   ├── sessions.py
│       │   ├── audit.py
│       │   ├── admin_users.py
│       │   └── health.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── tokens.py
│       │   ├── users.py
│       │   ├── roles.py
│       │   ├── permissions.py
│       │   ├── sessions.py
│       │   ├── audit.py
│       │   ├── jwks.py
│       │   └── errors.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── auth_service.py
│       │   ├── current_user_service.py
│       │   ├── session_service.py
│       │   ├── role_service.py
│       │   ├── permission_service.py
│       │   ├── audit_service.py
│       │   └── admin_user_service.py
│       ├── security/
│       │   ├── __init__.py
│       │   ├── bearer.py
│       │   ├── current_user.py
│       │   └── authorization.py
│       └── testing/
│           ├── __init__.py
│           ├── app.py
│           ├── factories.py
│           └── fixtures.py
├── tests/
│   ├── unit/
│   ├── api/
│   ├── integration/
│   └── contract/
└── docs/
    ├── configuration.md
    ├── endpoints.md
    ├── security.md
    ├── openapi.md
    ├── integration.md
    └── deployment.md
```

Les modules peuvent être créés progressivement. Un module non utilisé à une version donnée ne doit pas contenir de code mort complexe ; il peut être absent tant que la documentation de version le signale clairement.

---

## 3. Périmètre fonctionnel inclus

- Rotation systématique du refresh token à chaque refresh.
- Stockage uniquement du hash du refresh token.
- Révocation de l’ancien refresh token après rotation.
- Création et mise à jour `last_used_at` des sessions.
- Endpoint `GET /auth/sessions/me` listant les sessions courantes de l’utilisateur.
- Vérification stricte `sid`, `jti`, `sub`, expiration et statut de session sur `/auth/me`.
- Readiness enrichie : base accessible, migrations attendues appliquées, clé active disponible.

## 4. Endpoints concernés

- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /auth/me`
- `GET /auth/sessions/me`
- `GET /health`
- `GET /ready`

Les endpoints non listés pour cette version ne doivent pas être développés sauf s’ils sont nécessaires comme dépendances techniques privées. Dans ce cas, ils doivent rester non publics, non documentés comme API stable et couverts par tests internes.

---

## Contrats HTTP transverses

### `POST /auth/login`

Requête :

```json
{
  "email": "user@example.com",
  "password": "secret"
}
```

Réponse nominale :

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 900
}
```

Règles :

- ne jamais distinguer publiquement email inconnu et mauvais mot de passe ;
- ne jamais logger le mot de passe ;
- produire un audit de succès ou d’échec selon le cas ;
- créer ou mettre à jour une session selon la version cible.

### Claims JWT minimales

```json
{
  "sub": "auth_subject",
  "iss": "baobab-auth",
  "aud": "baobab-api",
  "exp": 1780000000,
  "iat": 1779999000,
  "jti": "token-id",
  "sid": "session-id",
  "email": "user@example.com",
  "username": "patrick",
  "roles": ["USER"],
  "permissions": ["auth:user:read"]
}
```

Règles :

- `sub` représente l’identité stable publique, pas un secret ;
- `jti` représente l’identifiant du token ;
- `sid` représente l’identifiant de session quand le token est lié à une session ;
- `roles` et `permissions` sont résolus par core/API/database, pas recalculés par security ;
- les dates doivent être UTC aware côté objets Python ;
- l’algorithme et le `kid` doivent permettre la validation via JWKS.

### `GET /auth/jwks`

Réponse attendue :

```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "key-id",
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "..."
    }
  ]
}
```

Interdictions :

- aucune clé privée ;
- aucun secret ;
- aucun refresh token ;
- aucune donnée utilisateur.

### Format d’erreur public

```json
{
  "error": {
    "code": "invalid_credentials",
    "message": "Invalid credentials"
  }
}
```

Les codes publics doivent être documentés et stables. Les détails techniques peuvent être loggés uniquement s’ils ne contiennent aucun secret.

---

## 5. Backlog détaillé pour l’IA de développement

### BL-API-020-001 — Durcir le modèle de session côté API

**Objectif :** Définir les DTO session, la résolution session/token et les erreurs session expirée/révoquée.

**Critères d’acceptation :**

- le comportement est implémenté ;
- les erreurs sont gérées ;
- les tests unitaires et/ou d’intégration couvrent le cas nominal et les cas d’échec ;
- la documentation de version est mise à jour ;
- aucun secret n’est exposé.

### BL-API-020-002 — Implémenter refresh rotation

**Objectif :** À chaque refresh : vérifier hash, charger session, refuser si expirée/révoquée, générer nouveau token pair, persister nouveau hash, révoquer ancien jeton.

**Critères d’acceptation :**

- le comportement est implémenté ;
- les erreurs sont gérées ;
- les tests unitaires et/ou d’intégration couvrent le cas nominal et les cas d’échec ;
- la documentation de version est mise à jour ;
- aucun secret n’est exposé.

### BL-API-020-003 — Implémenter liste des sessions courantes

**Objectif :** Créer `/auth/sessions/me` avec masquage IP/User-Agent si nécessaire et pagination simple.

**Critères d’acceptation :**

- le comportement est implémenté ;
- les erreurs sont gérées ;
- les tests unitaires et/ou d’intégration couvrent le cas nominal et les cas d’échec ;
- la documentation de version est mise à jour ;
- aucun secret n’est exposé.

### BL-API-020-004 — Auditer sessions

**Objectif :** Écrire les événements LOGIN_SUCCESS, SESSION_REFRESHED, LOGOUT, SESSION_REVOKED sans token brut.

**Critères d’acceptation :**

- le comportement est implémenté ;
- les erreurs sont gérées ;
- les tests unitaires et/ou d’intégration couvrent le cas nominal et les cas d’échec ;
- la documentation de version est mise à jour ;
- aucun secret n’est exposé.

### BL-API-020-005 — Readiness avancée

**Objectif :** Contrôler DB, UoW, migrations minimales et présence d’une clé active.

**Critères d’acceptation :**

- le comportement est implémenté ;
- les erreurs sont gérées ;
- les tests unitaires et/ou d’intégration couvrent le cas nominal et les cas d’échec ;
- la documentation de version est mise à jour ;
- aucun secret n’est exposé.

### BL-API-020-006 — Tests d’intégration session

**Objectif :** Tester rotation, replay de refresh token, session expirée, session révoquée, logout idempotent.

**Critères d’acceptation :**

- le comportement est implémenté ;
- les erreurs sont gérées ;
- les tests unitaires et/ou d’intégration couvrent le cas nominal et les cas d’échec ;
- la documentation de version est mise à jour ;
- aucun secret n’est exposé.

---

## 6. Tests obligatoires de cette version

- Un refresh token rejoué après rotation est refusé.
- Un refresh token expiré est refusé.
- Une session révoquée empêche `/auth/me` si la politique impose la vérification de session.
- Logout est idempotent.
- Les audits de session ne contiennent pas de refresh token brut.
- La transaction rollback si la persistance session échoue après émission de token.

En complément, tous les tests de non-régression des versions précédentes doivent continuer à passer.

---

## Qualité, CI et définition de terminé commune

Chaque version doit respecter les contrôles suivants :

```bash
ruff check .
ruff format --check .
mypy src tests
pytest --cov=baobab_auth_api --cov-report=term-missing
```

Critères minimums :

- couverture `>=90 %` ;
- aucun test instable dépendant de l’ordre d’exécution ;
- fixtures explicites ;
- tests unitaires des services ;
- tests API avec `httpx.AsyncClient` ou client de test FastAPI ;
- tests d’intégration database/security dès qu’un comportement dépend d’une vraie persistance ou d’un vrai token ;
- tests contractuels avec `baobab-auth-client` aux versions indiquées ;
- documentation mise à jour ;
- changelog mis à jour ;
- version package mise à jour ;
- aucune dépendance inutilisée ;
- aucune fuite de secret dans les logs, erreurs, réponses JSON ou audits.

---

## 7. Critères d’acceptation globaux

La version `v0.2.0` est acceptée si :

- les dépendances directes indiquées dans la matrice sont installées et validées en intégration ;
- l’API démarre via `create_app()` et via `uvicorn baobab_auth_api.main:app` ;
- les endpoints de la version répondent avec les codes attendus ;
- les schémas OpenAPI sont générés ;
- les erreurs HTTP ne divulguent pas de détail sensible ;
- les logs ne contiennent aucun secret ;
- les audits ne contiennent aucun secret ;
- les transactions database sont atomiques ;
- les tokens sont produits et validés par `baobab-auth-security`, jamais réimplémentés dans l’API ;
- les règles métier restent dans `baobab-auth-core` ;
- les repositories et migrations restent dans `baobab-auth-database` ;
- les tests unitaires, API, intégration et contractuels passent ;
- la documentation et le changelog mentionnent explicitement les versions validées des librairies dépendantes.

---

## 8. Hors périmètre

Sauf mention explicite dans cette version, ne pas implémenter :

- OAuth complet ;
- OIDC discovery complet ;
- MFA ;
- passkeys ;
- reset password par email ;
- envoi d’email ;
- interface web ;
- CLI admin ;
- Docker compose complet ;
- logique métier d’une application consommatrice ;
- modèle ORM directement dans l’API ;
- hash de mot de passe directement dans l’API ;
- génération cryptographique directement dans l’API.

---

## 9. Préparation de la version suivante

La version suivante pourra exploiter pleinement les rôles et permissions pour protéger des routes API d’administration et exposer un contrat RBAC stable.
