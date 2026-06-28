# Contrat — Compatibilité

> Politiques de compatibilité et de dépréciation de ce package.

## Versionnage sémantique (SemVer)

Ce package suit [SemVer](https://semver.org/lang/fr/) sans borne supérieure :

- **MAJOR** : rupture de l'API publique (changement incompatible).
- **MINOR** : ajout rétrocompatible de fonctionnalités.
- **PATCH** : correction de bugs rétrocompatible.

## Phase de maturation (v0.x.y)

Tant que la version majeure est `0`, l'API publique peut évoluer entre
versions mineures. À partir de `v1.0.0`, les règles SemVer standard s'appliquent.

## Politique de dépréciation

1. Annoncer la dépréciation dans `CHANGELOG.md` et via `DeprecationWarning`.
2. Maintenir le symbole déprécié pendant au moins une version mineure.
3. Supprimer lors du prochain bump majeur.
