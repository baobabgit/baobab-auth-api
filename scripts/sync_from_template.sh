#!/usr/bin/env bash
# Synchronise les fichiers infra (CI, règles, outils) depuis le template source.
# Ne touche pas au code, aux tests, aux specs ni aux métadonnées du projet.
#
# Usage : scripts/sync_from_template.sh [URL-du-template]
#   Par défaut : https://github.com/baobabgit/baobab-python-template.git
#
# Prérequis : git propre (pas de modifications non commitées).
set -euo pipefail

TEMPLATE_URL="${1:-https://github.com/baobabgit/baobab-python-template.git}"
SYNC_DATE=$(date +%Y-%m-%d)
BRANCH="template-sync/${SYNC_DATE}"

# Fichiers et dossiers infra à synchroniser depuis le template.
# Le code projet (src/, tests/, docs/specifications/, ...) n'est jamais touché.
INFRA_PATHS=(
    ".github/workflows"
    ".github/ISSUE_TEMPLATE"
    ".github/pull_request_template.md"
    ".github/dependabot.yml"
    ".cursor/rules"
    ".codex/rules"
    "AGENTS.md"
    "CLAUDE.md"
    "noxfile.py"
    "Makefile"
    "scripts/check_no_ai_attribution.py"
    "scripts/setup_github.sh"
    "scripts/sync_from_template.sh"
    ".pre-commit-config.yaml"
    ".python-version"
    "docs/workflow"
    "docs/ai_workflow/workflow.md"
    "docs/ai_workflow/roles"
    "docs/guides/tutorials/premiers-pas.rst"
    "docs/guides/how-to/ajouter-une-classe.rst"
    "docs/guides/how-to/integration-validation.rst"
    "docs/guides/how-to/template-sync.rst"
)

sync_path() {
    local path="$1"
    if git checkout upstream/main -- "${path}" 2>/dev/null; then
        echo "  ok  ${path}"
    else
        echo "  --  ${path} (absent dans upstream, ignoré)"
    fi
}

# ── Vérifications préalables ──────────────────────────────────────────────────

if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "ERREUR : exécuter depuis un dépôt git." >&2
    exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERREUR : modifications non commitées — commite ou stash d'abord." >&2
    exit 1
fi

if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
    echo "ERREUR : la branche '${BRANCH}' existe déjà." >&2
    echo "  Supprime-la (git branch -d ${BRANCH}) ou patiente jusqu'à demain." >&2
    exit 1
fi

# ── Remote upstream ───────────────────────────────────────────────────────────

if git remote get-url upstream >/dev/null 2>&1; then
    CURRENT_URL=$(git remote get-url upstream)
    echo "▶ Remote 'upstream' : ${CURRENT_URL}"
    if [[ "${CURRENT_URL}" != "${TEMPLATE_URL}" ]]; then
        echo "  ⚠ URL différente de ${TEMPLATE_URL}"
        echo "  Pour corriger : git remote set-url upstream ${TEMPLATE_URL}"
    fi
else
    echo "▶ Ajout du remote 'upstream' → ${TEMPLATE_URL}"
    git remote add upstream "${TEMPLATE_URL}"
fi

# ── Fetch + branche ───────────────────────────────────────────────────────────

echo "▶ Fetch upstream/main …"
git fetch upstream main --quiet

echo "▶ Création de la branche ${BRANCH}"
git checkout -b "${BRANCH}" --quiet

# ── Synchronisation ───────────────────────────────────────────────────────────

echo "▶ Synchronisation des fichiers infra :"
for path in "${INFRA_PATHS[@]}"; do
    sync_path "${path}"
done

# ── Récapitulatif ─────────────────────────────────────────────────────────────

CHANGED=$(git diff --cached --name-only | wc -l | tr -d ' ')

if [[ "${CHANGED}" -eq 0 ]]; then
    echo ""
    echo "Aucune modification — le projet est déjà à jour avec le template."
    git checkout - --quiet
    git branch -d "${BRANCH}" --quiet
    exit 0
fi

echo ""
echo "▶ Fichiers modifiés (${CHANGED}) :"
git diff --cached --name-only | sed 's/^/    /'

echo ""
echo "──────────────────────────────────────────────────────────────────────"
echo "Révisions manuelles recommandées avant commit :"
echo ""
echo "  1. Sections [tool.*] de pyproject.toml :"
echo "       git diff upstream/main -- pyproject.toml"
echo ""
echo "  2. docs/guides/index.rst (entrées tutorials / how-to) :"
echo "       git diff upstream/main -- docs/guides/index.rst"
echo ""
echo "  3. Nouveaux fichiers infra éventuels non couverts par ce script :"
echo "       git diff upstream/main HEAD -- .github/ scripts/ docs/workflow/"
echo ""
echo "Quand tout est vérifié :"
echo "  git commit -m 'BL-XXX: sync infra from template ${SYNC_DATE}'"
echo "  git push -u origin ${BRANCH}"
echo "  Ouvrir une PR vers version/vX.Y.Z (ou main)."
echo "──────────────────────────────────────────────────────────────────────"
