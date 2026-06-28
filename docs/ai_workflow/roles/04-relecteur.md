# Rôle — Relecteur / QA

**Mission :** revue indépendante de la PR. Idéalement, une **autre IA** que celle qui a codé.
**Boucle :** construction · **Colonne :** In review

## Definition of Ready

- PR ouverte, CI verte.

## Actions

- Vérifier la **conformité à `AGENTS.md`** (POO, 1 classe/fichier, typage, docstrings RST).
- **Valider les critères d'acceptation** de la FEAT.
- Confirmer la **couverture ≥ 95 %** et la qualité (passe de simplification).
- **Contrat d'API** : si `__all__` change de façon incompatible → exiger **bump majeur**
  + entrée `CHANGELOG` « BREAKING » + note de migration.
- **Évaluer le déclencheur Sécurité** (surface sensible ou release ?).
- Décider : **approuver** ou **renvoyer** (`In review -> In progress` avec raison).

## Definition of Done

- Décision prise ; si approuvé, déclencheur Sécurité tranché.

## Handoff

- `status: In review -> Security` (si déclenché) ou `In review -> Done`,
  ou renvoi `In review -> In progress`.
- Rôle suivant : **Sécurité**, **Release Manager**, ou **Développeur** (renvoi).
