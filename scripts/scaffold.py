#!/usr/bin/env python3
"""Générateur de squelettes pour versions et backlogs.

Usage :
  python scripts/scaffold.py new-version v0.1.0
  python scripts/scaffold.py new-backlog BL-001 "Description courte"

Crée les fichiers et dossiers nécessaires pour démarrer une version ou un backlog.
N'écrit jamais par-dessus un fichier existant.
Affiche le snippet YAML à ajouter manuellement dans queue.yaml.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

_AI_WORKFLOW = ROOT / "docs" / "ai_workflow"
_BACKLOG_DIR = ROOT / "docs" / "backlog" / "backlogs"
_MIN_ARGC = 3
_ARGC_WITH_TITLE = 4

_RUN_FILES = [
    "00_assignment.md",
    "01_context.md",
    "02_role_prompt.md",
    "03_expected_outputs.md",
    "04_worklog.md",
    "05_tests_report.md",
    "06_review.md",
    "07_handoff.md",
]


def _write(path: Path, content: str) -> None:
    """Create *path* with *content*, skipping if file already exists.

    :param path: Target file path.
    :param content: File content to write.
    """
    if path.exists():
        print(f"  ⚠ déjà présent, ignoré : {path.relative_to(ROOT)}", file=sys.stderr)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path.relative_to(ROOT)}")


def new_version(version: str) -> int:
    """Scaffold a new version directory with all required template files.

    :param version: Version string, e.g. 'v0.1.0'.
    :returns: 0 on success.
    """
    version_dir = _AI_WORKFLOW / "versions" / version
    print(f"▶ Création de la version {version}")

    _write(
        version_dir / "version.yaml",
        dedent(f"""\
            version: {version}
            status: PLANNED
            created_at: {TODAY}
            released_at: null
            # Statuts : PLANNED → IN_DEVELOPMENT → INTERNAL_VALIDATED
            #           → INTEGRATION_PENDING → INTEGRATION_VALIDATED
            #           → RELEASE_READY → RELEASED
        """),
    )

    _write(
        version_dir / "scope.md",
        dedent(f"""\
            # Périmètre — {version}

            ## Objectif

            <!-- Décrire l'objectif principal de cette version. -->

            ## Backlogs inclus

            | ID | Titre | Priorité |
            |----|-------|---------|
            |    |       |         |

            ## Backlogs reportés

            <!-- Lister les backlogs renvoyés à une version ultérieure. -->
        """),
    )

    _write(
        version_dir / "validation.md",
        dedent(f"""\
            # Validation interne — {version}

            ## Critères

            - [ ] Tous les backlogs mergés sur `version/{version}`
            - [ ] `make all` passe (qualité + tests ≥ 95 % + build)
            - [ ] `make traceability` passe sans erreur
            - [ ] CHANGELOG.md à jour
            - [ ] Badges README cohérents

            ## Résultat

            Status : PENDING
        """),
    )

    _write(
        version_dir / "integration_matrix.yaml",
        dedent("""\
            # Matrice de compatibilité inter-librairies
            validated_consumers: []
            # Exemple :
            # - name: baobab-example-consumer
            #   version: v2.0.0
            #   status: PENDING   # PENDING | PASSED | FAILED
            #   integration_method: git_ref
            #   ref: version/v0.1.0
        """),
    )

    _write(
        version_dir / "release_report.md",
        dedent(f"""\
            # Rapport de release — {version}

            Date : (à remplir)
            Tag : {version}

            ## Artefacts

            - [ ] sdist
            - [ ] wheel
            - [ ] Release GitHub

            ## Notes

            <!-- Résumé des changements, breaking changes, migration. -->
        """),
    )

    print(
        f"\nMettez à jour docs/ai_workflow/state/queue.yaml :\n"
        f"  version_active: {version}"
    )
    return 0


def new_backlog(bl_id: str, title: str) -> int:
    """Scaffold a new backlog with fiche, run directory, and all run files.

    :param bl_id: Backlog identifier, e.g. 'BL-001'.
    :param title: Short description of the backlog.
    :returns: 0 on success.
    """
    print(f"▶ Création du backlog {bl_id}")
    run_dir = _AI_WORKFLOW / "runs" / bl_id

    _write(
        _BACKLOG_DIR / f"{bl_id}.md",
        dedent(f"""\
            # {bl_id} — {title}

            :version_target: vX.Y.Z
            :priority: P1
            :depends_on: []

            ## Contexte

            <!-- Pourquoi ce backlog ? Quel problème résout-il ? -->

            ## FEAT liées

            - FEAT-XXX.1 — Description

            ## Critères d'acceptation

            - [ ] Critère 1
            - [ ] Critère 2

            ## Definition of Done

            - [ ] Code POO, 1 classe/fichier, type hints complets
            - [ ] black + ruff + mypy passent
            - [ ] Tests miroir, couverture ≥ 95 %
            - [ ] Docstrings RST à jour
            - [ ] Commit `{bl_id}: ...` + PR fusionnée sur version/vX.Y.Z
            - [ ] `make traceability` passe sans erreur
        """),
    )

    _write(
        run_dir / "status.yaml",
        dedent(f"""\
            id: {bl_id}
            title: "{title}"
            status: TODO
            # Statuts : TODO → READY → IN_PROGRESS → DONE | BLOCKED
            step: null
            role: null
            started_at: null
            completed_at: null
            last_heartbeat_at: null
        """),
    )

    for name in _RUN_FILES:
        label = name[3:].replace("_", " ").replace(".md", "").title()
        _write(run_dir / name, f"# {label} — {bl_id}\n\n")

    print(
        f"\nAjoutez à docs/ai_workflow/state/queue.yaml :\n"
        f"  - id: {bl_id}\n"
        f'    title: "{title}"\n'
        f"    version_target: vX.Y.Z\n"
        f"    priority: P1\n"
        f"    status: TODO\n"
        f"    depends_on: []"
    )
    return 0


def main() -> int:
    """Dispatch to new-version or new-backlog scaffold command.

    :returns: 0 on success, 1 on usage error.
    """
    if len(sys.argv) < _MIN_ARGC:
        print(
            "Usage:\n"
            "  scripts/scaffold.py new-version v0.1.0\n"
            '  scripts/scaffold.py new-backlog BL-001 "Description"',
            file=sys.stderr,
        )
        return 1

    command = sys.argv[1]

    if command == "new-version":
        return new_version(sys.argv[2])

    if command == "new-backlog":
        bl_id = sys.argv[2]
        title = sys.argv[3] if len(sys.argv) >= _ARGC_WITH_TITLE else bl_id
        return new_backlog(bl_id, title)

    print(f"Commande inconnue : {command!r}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
