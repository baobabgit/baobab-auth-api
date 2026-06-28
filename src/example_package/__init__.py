"""Package d'exemple du template.

Renommez ``example_package`` par le nom de votre projet (et adaptez
``pyproject.toml`` ainsi que le dossier miroir ``tests/example_package/``).
"""

from example_package.greeter import Greeter
from example_package.repository import Repository

__all__ = ["Greeter", "Repository"]
