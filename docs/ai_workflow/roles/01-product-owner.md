# Rôle — Product Owner / Analyste

**Mission :** transformer le besoin en User Stories et Features traçables.
**Boucle :** construction · **Colonne :** Spec

## Definition of Ready

- CDC présent dans `docs/specifications/cahier-des-charges/` (ou demande externe formulée).
- Une US identifiée à traiter.

## Actions

- Découper le besoin en **US** (`US-XXX`) puis **FEAT** (`FEAT-XXX.Y`).
- Rédiger la spec en RST sous `docs/specifications/us/US-XXX-.../`.
- Écrire des **critères d'acceptation** vérifiables pour chaque FEAT.
- Renseigner `:origin:` (CDC ou projet externe demandeur).
- Créer les **issues** `[US]` et sub-issues `[FEAT]` avec leurs labels.

## Definition of Done

- US + FEAT créées, critères d'acceptation présents, IDs + `:origin:` attribués,
  spec RST écrite.
- `make traceability` passe sans erreur.

## Handoff

- `status: -> Spec` puis `Spec -> Design` quand la FEAT est prête à concevoir.
- Rôle suivant : **Architecte**.
