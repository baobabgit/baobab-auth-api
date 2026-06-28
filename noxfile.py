"""Nox sessions — délègue à uv pour un environnement reproductible."""

from __future__ import annotations

import nox

nox.options.default_venv_backend = "none"


@nox.session
def quality(session: nox.Session) -> None:
    """Formatage (black), lint (ruff), typage (mypy), sécurité (bandit)."""
    session.run("uv", "run", "black", "--check", "src", "tests", external=True)
    session.run("uv", "run", "ruff", "check", "src", "tests", external=True)
    session.run("uv", "run", "mypy", "src", external=True)
    session.run(
        "uv", "run", "bandit", "-r", "src", "-c", "pyproject.toml", external=True
    )


@nox.session
def tests(session: nox.Session) -> None:
    """Tests pytest + couverture ≥ 95 %."""
    session.run(
        "uv",
        "run",
        "pytest",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=95",
        external=True,
    )


@nox.session
def build(session: nox.Session) -> None:
    """Construit le package et vérifie la distribution."""
    session.run("uv", "build", external=True)
    session.run("uv", "run", "twine", "check", "dist/*", external=True)


@nox.session
def traceability(session: nox.Session) -> None:
    """Vérifie la chaîne de traçabilité besoin → backlog → run."""
    session.run(
        "uv", "run", "python", "scripts/check_traceability.py", external=True
    )


@nox.session(name="all")
def all_checks(session: nox.Session) -> None:
    """Exécute quality + tests + build + traçabilité (validation complète)."""
    quality(session)
    tests(session)
    build(session)
    traceability(session)
