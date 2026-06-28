# Contrat — Exceptions publiques

> Exceptions publiques de ce package.

## Exceptions déclarées

| Exception | Module | Déclenchée par |
|-----------|--------|----------------|
| `ValueError` | builtins | `Greeter.__init__` si le nom est vide |
| `KeyError` | builtins | `Repository.get` si l'élément n'existe pas |

## Notes

Les exceptions publiques font partie du contrat API. Tout changement de leur
liste ou de leurs signatures est soumis aux règles SemVer.
