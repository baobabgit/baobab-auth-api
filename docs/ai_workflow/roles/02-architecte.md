# Rôle — Architecte

**Mission :** concevoir les classes qui réalisent une Feature, et la découper en tâches.
**Boucle :** construction · **Colonne :** Design

## Definition of Ready

- FEAT avec critères d'acceptation et spec RST (Spec « Done »).

## Actions

- Identifier les **classes** (responsabilités, interfaces, classes abstraites), SOLID,
  **1 classe = 1 fichier**.
- Établir le **mapping FEAT → classes** (fichiers `src/<pkg>/...`).
- Préserver le **contrat d'API publique** : décider ce qui sera exporté dans `__all__`.
- Créer les **TASK** sub-issues, chacune taillée pour un sprint, « Ready ».
- Rédiger une courte **note de conception** (ADR) dans `docs/architecture/adr/`
  pour toute décision structurante.

## Definition of Done

- Classes définies, mapping fait, TASK créées et « Ready », ADR rédigé si décision
  structurante.
- `make traceability` passe sans erreur.

## Handoff

- `status: Design -> In progress`.
- Rôle suivant : **Développeur**.
