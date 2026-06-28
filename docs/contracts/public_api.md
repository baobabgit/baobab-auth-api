# Contrat — API publique

> Ce fichier documente les symboles exportés dans `__all__` de ce package.
> Toute modification incompatible d'un symbole public déclenche un bump SemVer majeur.

## Symboles exportés

<!-- Documenter ici chaque classe, fonction ou constante publique. -->

| Symbole | Type | Module | Spec |
|---------|------|--------|------|
| `Greeter` | Classe | `example_package.greeter` | FEAT-001.1 |
| `Repository` | Classe abstraite | `example_package.repository` | FEAT-001.2 |

## Règle de rupture de contrat

- Suppression d'un symbole public → **MAJOR bump**
- Changement de signature incompatible → **MAJOR bump**
- Ajout d'un paramètre obligatoire → **MAJOR bump**
- Ajout d'un symbole → **MINOR bump**
- Correction de comportement sans rupture → **PATCH bump**
