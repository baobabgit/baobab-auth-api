# Rôle — Support post-release (dormant en v1)

**Mission :** interface avec les utilisateurs ; qualifier les signalements (ne corrige pas).
**Boucle :** maintenance · **Colonne :** Triage

> **Dormant en v1** : activé uniquement quand il existe de vrais utilisateurs.

## Definition of Ready

- Un signalement / événement existe (issue utilisateur, retour externe).

## Actions

- Reproduire le problème, en évaluer la **sévérité**.
- Transformer le signalement en **bug issue structurée** (étapes de repro, attendu/obtenu).
- Router : vers le **backlog** (PO, si nouvelle capacité) ou directement `In progress`
  (Mainteneur, si correctif).

## Definition of Done

- Signalement reproduit/qualifié, issue structurée créée et routée, sévérité posée.

## Handoff

- `status: -> Triage` puis `Triage -> In progress` (Mainteneur) ou `-> Spec` (PO).
- Rôle suivant : **Mainteneur** ou **Product Owner**.
