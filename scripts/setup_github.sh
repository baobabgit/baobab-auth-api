#!/usr/bin/env bash
# Configuration GitHub one-time d'un projet généré depuis le template.
# Idempotent. À lancer après création du repo (cf. docs/workflow/SETUP.md).
# Prérequis : gh authentifié avec les scopes repo + project
#   gh auth refresh -s project
#
# Usage : scripts/setup_github.sh [owner/repo]
#   (sans argument, déduit le repo courant via gh)
set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
echo "▶ Configuration de ${REPO}"

echo "• Labels"
gh label create "type:us"       -c 0e8a16 -d "User Story" -R "$REPO" --force
gh label create "type:feat"     -c 1d76db -d "Feature"    -R "$REPO" --force
gh label create "type:task"     -c 5319e7 -d "Task"       -R "$REPO" --force
gh label create "priority:high" -c d93f0b -R "$REPO" --force
gh label create "priority:med"  -c fbca04 -R "$REPO" --force
gh label create "priority:low"  -c c2e0c6 -R "$REPO" --force
gh label create "dependencies"  -c 0366d6 -R "$REPO" --force

echo "• Protection de branche (ruleset : CI verte requise, sans approbation de PR)"
# Indisponible sur repo privé en plan Free → on tolère le 403.
if gh api --method POST "repos/${REPO}/rulesets" --input - >/dev/null 2>&1 <<'JSON'
{
  "name": "main-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          {"context": "Qualité + Typage + Sécurité"},
          {"context": "Tests + couverture ≥ 95 %"},
          {"context": "Traçabilité (specs → backlog → runs)"},
          {"context": "Build package"}
        ]
      }
    }
  ]
}
JSON
then
  echo "  ✓ ruleset actif"
else
  echo "  ⚠ ruleset non créé (repo privé en plan Free ?) → rendre public ou passer Pro/Team."
fi

echo "• Environnements de publication"
gh api --method PUT "repos/${REPO}/environments/pypi"     >/dev/null 2>&1 && echo "  ✓ pypi"     || echo "  ⚠ pypi non créé (plan ?)"
gh api --method PUT "repos/${REPO}/environments/testpypi" >/dev/null 2>&1 && echo "  ✓ testpypi" || echo "  ⚠ testpypi non créé (plan ?)"

echo "✔ Terminé."
echo "  Restent manuels : GitHub Project (gh project create) et Trusted Publishing (UI PyPI/TestPyPI)."
echo "  Adapte les contextes du ruleset si tu modifies la matrice CI (versions Python)."
