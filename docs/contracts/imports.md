# Contrat — Imports publics

> Imports garantis stables pour les consommateurs de ce package.

## Imports garantis

```python
from example_package import Greeter, Repository
from example_package.greeter import Greeter
from example_package.repository import Repository
```

## Imports internes (non garantis)

Les sous-modules non exportés dans `__all__` sont considérés comme internes
et peuvent changer sans bump majeur.
