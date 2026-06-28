# Note de handoff

Garantit la **reprise sans perte** par n'importe quelle IA. Elle ne capture que
**l'état volatil irrécupérable** — pas ce qui est déjà dans `git`, le GitHub Project,
les specs RST ou `AGENTS.md`.

## Où

Un **commentaire sur l'issue de la tâche**, en **append-only** (le plus récent fait foi).
Fallback `HANDOFF.md` à la racine **uniquement** en mode 100 % hors-ligne sans GitHub.

## Format

```markdown
## HANDOFF
task: TASK-001.1.1            # ancre tout (FEAT-001.1 / US-001)
ia: claude                   # qui vient d'agir (claude|cursor|codex)
role_done: Développeur       # rôle joué ce tour
status: In progress -> In review   # transition de colonne effectuée
branch: feat/FEAT-001.1-salutations
commit: a1b2c3d              # dernier commit (point de reprise du code)
verify: make check           # commande pour valider l'état de départ
---
**Fait ce tour-ci :** tests TDD + classe Greeter, couverture 100 %.
**Prochaine action :** relire la PR vs critères d'acceptation de FEAT-001.1.
**Décisions & pourquoi :** registre via paramètre `formal=` (et non 2 méthodes) — garde 1 classe simple.
**Blocages / questions :** aucun.
```

## Pourquoi chaque champ

| Champ | Perte évitée |
| --- | --- |
| `task` | l'ancrage : sur quoi on reprend |
| `role_done` + `status` | la position dans la machine à états → quel rôle ensuite |
| `branch` + `commit` | le point de reprise exact du code |
| `verify` | confirmer que l'état de départ est sain |
| **Fait** | le delta : éviter de relire tout l'historique |
| **Prochaine action** | le champ le plus important : quoi faire ensuite |
| **Décisions & pourquoi** | empêche une autre IA de rejouer/annuler un choix délibéré |
| **Blocages** | empêche la perte silencieuse d'un problème connu |

## Discipline (non négociable)

1. **On ne s'arrête jamais sans écrire la note** (condition de sortie de tout rôle, U1).
2. **Test du démarrage à froid** : la note est complète si une IA qui n'a *que* la note
   + le repo peut reprendre sans poser de question. Sinon, il manque un champ.

## Cas limites

- **Bootstrap** : 1ʳᵉ note posée après la phase 0 (`role_done: PO`, `status: -> Spec`).
- **Clôture** : dernière note `status: In review -> Done`, `Prochaine action : aucune
  (tâche close)`, puis `Closes #`.
