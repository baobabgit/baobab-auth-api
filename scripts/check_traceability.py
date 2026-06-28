#!/usr/bin/env python3
"""Vérification de la chaîne de traçabilité besoin → backlog → run.

Contrôles effectués :
  1. Cahiers dans specifications/cahier-des-charges/ → US dans specifications/us/.
  2. Chaque BL dans queue.yaml → fiche backlog + ref FEAT + run/status.yaml.
  3. Queue non-vide (entrées actives) → au moins un ADR dans docs/architecture/adr/.
  4. version_active de queue.yaml → dossier dans docs/ai_workflow/versions/.

Retourne 0 si tout passe, 1 sinon.

Branché en pre-push (pre-commit) et en job CI (Traçabilité).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "ERREUR : pyyaml requis — uv add --group dev pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

_SPECS_CDC = ROOT / "docs" / "specifications" / "cahier-des-charges"
_SPECS_US = ROOT / "docs" / "specifications" / "us"
_QUEUE_YAML = ROOT / "docs" / "ai_workflow" / "state" / "queue.yaml"
_BACKLOG_DIR = ROOT / "docs" / "backlog" / "backlogs"
_RUNS_DIR = ROOT / "docs" / "ai_workflow" / "runs"
_VERSIONS_DIR = ROOT / "docs" / "ai_workflow" / "versions"
_ADR_DIR = ROOT / "docs" / "architecture" / "adr"

_PLACEHOLDER = frozenset({".gitkeep"})
_SKIP_NAMES = frozenset({"readme.md", "readme.rst"})
_DOC_SUFFIXES = frozenset({".md", ".rst"})
_FEAT_RE = re.compile(r"FEAT-\d{3}")
_STARTED_STATUSES = frozenset({"IN_PROGRESS", "DONE"})
_REQUIRES_FEAT = frozenset({"READY", "IN_PROGRESS", "DONE"})


def _content_files(directory: Path) -> list[Path]:
    """Return non-placeholder doc files in *directory* (non-recursive).

    :param directory: Directory to scan.
    :returns: List of matching file paths, or empty list if directory absent.
    """
    if not directory.exists():
        return []
    return [
        f
        for f in directory.iterdir()
        if f.is_file()
        and f.name not in _PLACEHOLDER
        and f.suffix in _DOC_SUFFIXES
        and f.name.lower() not in _SKIP_NAMES
    ]


def _subdirs(directory: Path) -> list[Path]:
    """Return non-hidden sub-directories in *directory* (non-recursive).

    :param directory: Directory to scan.
    :returns: List of sub-directory paths, or empty list if directory absent.
    """
    if not directory.exists():
        return []
    return [
        d for d in directory.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]


def _load_queue() -> dict[str, Any]:
    """Return parsed queue.yaml content, or empty dict if file absent.

    :returns: Parsed YAML as a dict.
    """
    if not _QUEUE_YAML.exists():
        return {}
    result: dict[str, Any] = yaml.safe_load(_QUEUE_YAML.read_text()) or {}
    return result


def check_cahiers_have_us(errors: list[str]) -> None:
    """Fail if cahiers exist in cahier-des-charges/ but no US has been derived.

    :param errors: Mutable list to append error messages to.
    """
    cahiers = _content_files(_SPECS_CDC)
    if not cahiers:
        return
    if not _subdirs(_SPECS_US):
        errors.append(
            f"{len(cahiers)} cahier(s) présent(s) dans "
            "specifications/cahier-des-charges/ mais aucune US dans "
            "specifications/us/. Dériver au moins une User Story."
        )


def check_queue_entries(errors: list[str]) -> None:
    """Check each BL in queue.yaml has its fiche, FEAT ref, and run artefacts.

    :param errors: Mutable list to append error messages to.
    """
    data = _load_queue()
    queue: list[dict[str, Any]] = data.get("queue", []) or []

    for entry in queue:
        bl_id: str = entry.get("id", "")
        status: str = entry.get("status", "TODO")
        if not bl_id:
            continue

        fiche = _BACKLOG_DIR / f"{bl_id}.md"
        if not fiche.exists():
            errors.append(
                f"[{bl_id}] fiche manquante : "
                f"docs/backlog/backlogs/{bl_id}.md"
            )
            continue

        if status in _REQUIRES_FEAT and not _FEAT_RE.search(fiche.read_text()):
            errors.append(
                f"[{bl_id}] aucune référence FEAT-XXX dans la fiche "
                f"(statut : {status}). Renseigner la section « FEAT liées »."
            )

        if status in _STARTED_STATUSES:
            run_status = _RUNS_DIR / bl_id / "status.yaml"
            if not run_status.exists():
                errors.append(
                    f"[{bl_id}] statut '{status}' mais "
                    f"docs/ai_workflow/runs/{bl_id}/status.yaml manquant. "
                    f"Créer avec : make new-backlog BL={bl_id}"
                )


def check_adr_present(errors: list[str]) -> None:
    """Fail if active queue entries exist but no ADR is present.

    :param errors: Mutable list to append error messages to.
    """
    data = _load_queue()
    queue: list[dict[str, Any]] = data.get("queue", []) or []
    active = [e for e in queue if e.get("status", "TODO") != "TODO"]
    if not active:
        return
    if not _content_files(_ADR_DIR):
        errors.append(
            "La queue contient des backlogs actifs mais aucun ADR n'est "
            "présent dans docs/architecture/adr/. Toute décision "
            "d'architecture structurante doit être documentée."
        )


def check_version_consistency(errors: list[str]) -> None:
    """Fail if version_active has no matching directory in versions/.

    :param errors: Mutable list to append error messages to.
    """
    data = _load_queue()
    version_active: str | None = data.get("version_active")
    if not version_active:
        return
    if not (_VERSIONS_DIR / version_active).exists():
        errors.append(
            f"version_active='{version_active}' dans queue.yaml mais "
            f"docs/ai_workflow/versions/{version_active}/ est absent. "
            f"Créer avec : make new-version VERSION={version_active}"
        )


def main() -> int:
    """Run all traceability checks and report failures.

    :returns: 0 if all checks pass, 1 if any check fails.
    """
    errors: list[str] = []
    check_cahiers_have_us(errors)
    check_queue_entries(errors)
    check_adr_present(errors)
    check_version_consistency(errors)

    if errors:
        print("Échecs de traçabilité :\n", file=sys.stderr)
        for err in errors:
            print(f"  • {err}", file=sys.stderr)
        print(
            "\nLa chaîne besoin → US/FEAT → backlog → run → ADR"
            " doit être complète.",
            file=sys.stderr,
        )
        return 1

    print("Traçabilité OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
