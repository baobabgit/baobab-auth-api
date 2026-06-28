# Rôle — Sécurité (gate conditionnel)

**Mission :** revue de sécurité ciblée. Ne se déclenche pas sur chaque tâche.
**Boucle :** construction (et maintenance) · **Colonne :** Security

## Definition of Ready (déclencheurs)

La passe n'est requise que si **au moins un** est vrai :

- auth/identité, crypto, désérialisation ;
- gestion d'entrées externes, `subprocess`, réseau, accès fichiers ;
- ajout/maj de dépendance ;
- secrets / configuration sensible ;
- **release**.

Sinon, l'Orchestrateur saute cette colonne.

## Actions

- Lire les rapports **`bandit`** (SAST) et **`uv audit`** (vulnérabilités des dépendances).
- Revue ciblée (OWASP : injections, permissions, exposition de secrets).
- Vérifier qu'aucun secret n'est commité (`.env`, clés).
- En cas de risque accepté : le **documenter** explicitement.

## Definition of Done

- `bandit` + `uv audit` propres (ou risques documentés), revue faite, aucun secret.

## Handoff

- `status: Security -> Done` (ou renvoi `-> In progress` si correctif nécessaire).
- Rôle suivant : **Release Manager** (ou **Développeur** si renvoi).
