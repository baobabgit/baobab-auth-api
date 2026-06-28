# Workflow de développement multi-IA

> **Format :** les fichiers de `docs/workflow/` sont des **instructions opérationnelles**
> destinées aux IA (comme `AGENTS.md`) → en Markdown. La **documentation du projet**
> (specifications, API, guides) reste en **reStructuredText**.

Ce dossier décrit *comment* on construit le projet : une **machine à états** jouée par
une seule IA à la fois, qui enchaîne des **rôles** de façon séquentielle. D'une phase à
l'autre, on peut changer d'IA : chacune reprend grâce à la **note de handoff** + l'état du
dépôt et du GitHub Project.

## Les trois points d'entrée du travail

| Source | Boucle | Rôle d'entrée |
| --- | --- | --- |
| Cahier des charges (`docs/specifications/cahier-des-charges/`) | Construction | Product Owner |
| Signalement utilisateur | Maintenance | Support |
| Demande d'un projet/sous-projet externe | Construction ou Maintenance | PO ou Mainteneur (champ `:origin:`) |

## Les deux boucles

```
CONSTRUCTION  : PO → Architecte → Développeur → Relecteur → [Sécurité] → Release
MAINTENANCE   : Support → Mainteneur → [Sécurité] → Release   (dormante en v1)
```

## Les colonnes du GitHub Project (= phases)

```
Spec → Design → In progress → In review → Security(conditionnel) → Done
                      ▲                                                │
                      └──────────────  renvoi de review  ◄────────────┘
```

## La boucle d'orchestration (à chaque reprise)

```
lire le statut de la tâche active (colonne du Project + dernière note de handoff)
   → endosser le rôle de cette colonne (docs/workflow/roles/)
   → exécuter l'action en respectant AGENTS.md
   → vérifier la Definition of Done (docs/workflow/gates.md)
   → écrire la note de handoff (docs/workflow/handoff.md) + mettre à jour le statut
   → s'arrêter
```

## Stratégie de branches

- **v1 (séquentiel, défaut)** : **trunk-based**. Branches courtes `feat/<ID>-slug` →
  PR → `main`. La hiérarchie US/FEAT/TASK vit dans le **tracker** (sub-issues, labels,
  milestones), pas dans des branches longues. `main` reste toujours vert et livrable.
- **v2 (concurrence)** : modèle **imbriqué** `TASK → FEAT → US → main` (branches
  d'intégration par US/FEAT) pour isoler des agents travaillant en parallèle. Réservé à
  la v2, où l'isolation paie réellement.
- **Protection** : ruleset sur `main` exigeant la **CI verte** (lint, type, security,
  test) ; **pas d'approbation de PR** (modèle solo : une IA ne peut pas s'auto-approuver).
  Disponible gratuitement sur repo **public** ou plan Pro/Team (cf. `SETUP.md`).

## Contenu

- [`roles/`](roles/) — un persona par rôle (mission, gates, actions).
- [`gates.md`](gates.md) — Definition of Ready / Done par transition de colonne.
- [`handoff.md`](handoff.md) — format de la note de handoff (reprise sans perte).
- [`prompts/init.md`](prompts/init.md) — prompt de **bootstrap** (une seule fois).
- [`prompts/orchestration.md`](prompts/orchestration.md) — prompt **récurrent**.
- [`SETUP.md`](SETUP.md) — configuration GitHub one-time (template, labels, Project,
  branch protection, environnements, Trusted Publishing).
