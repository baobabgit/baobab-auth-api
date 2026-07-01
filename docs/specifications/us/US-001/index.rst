US-001 — Authentification HTTP minimale (v0.1.0)
==================================================

Objectif
--------

Exposer une API FastAPI permettant l'inscription, la connexion, le rafraîchissement
de session, la déconnexion, l'identité courante et la publication JWKS.

Features
--------

- FEAT-001.1 — Factory ``create_app`` et configuration
- FEAT-001.2 — Endpoints auth (register, login, refresh, logout, me)
- FEAT-001.3 — JWKS, rôles, permissions et health
