# Prompt d'initialisation (bootstrap) — à lancer UNE seule fois

> Prérequis (hors IA) : voir [`../SETUP.md`](../SETUP.md) — marquer le dépôt comme
> *template*, créer le repo (`gh repo create --template`), `gh auth refresh -s project`,
> environnements de publication. À copier dans l'IA après avoir : (1) créé le repo depuis
> le template, (2) déposé le cahier des charges dans `docs/specifications/cahier-des-charges/`.

---

Tu es l'**Orchestrateur** en mode bootstrap. Lis `AGENTS.md` et tout `docs/workflow/`
avant d'agir. Déroule la phase 0, puis bascule en mode orchestration normal.

1. **Lire le cahier des charges** dans `docs/specifications/cahier-des-charges/`.
2. **Nommer le projet** : déduis le nom du package. Renomme `example_package` partout
   (`src/`, `tests/`, `pyproject.toml`, `docs/conf.py`, imports, `__all__`) et remplace
   `your-org/your-repo` (badges README, URLs `pyproject.toml`).
3. **Adapter les métadonnées au CDC** : `description`, `keywords`, `requires-python`
   (+ matrice CI et `target-version`/`python_version`), `dependencies` (un cœur pur peut
   en avoir aucune). Désactive les badges sans service configuré (ex. Read the Docs si
   pas d'hébergement de doc).
4. **Exemples `Greeter`/`Repository`** : décide explicitement.
   - **Garde-les** si le CDC s'y prête (ils servent de smoke test pour la CI verte) ;
   - **sinon conserve-les comme placeholders temporaires** jusqu'à la 1ʳᵉ tâche de dev,
     puis supprime-les (code + tests) quand le premier vrai domaine est implémenté.
5. **Rôle Product Owner** :
   - découpe le CDC en `US-XXX` → `FEAT-XXX.Y`, écris les specs RST sous
     `docs/specifications/us/`, renseigne `:origin:` ;
   - **réécris l'intro du `README.md`** (titre, blurb, À propos, Fonctionnalités, Stack)
     pour décrire le projet réel et non le template ;
   - lance `bash scripts/setup_github.sh` (labels, protection de branche, environnements —
     **tolérant** si le plan/visibilité ne le permet pas : voir `SETUP.md`) ;
   - crée le GitHub Project (colonnes `Spec → Design → In progress → In review →
     Security → Done` ; champs Date **Début**/**Fin** pour la roadmap), les milestones,
     puis les issues `US` + sub-issues `FEAT`.
6. **Vérifier** : `make check` vert ; `sphinx-build` (idéalement `-W`) passe.
7. **Commit** : `chore: bootstrap project from template`.
8. **Première note de handoff** sur l'issue de la 1ʳᵉ tâche (`role_done: PO`,
   `status: -> Spec`).
9. **Basculer** : à partir de maintenant, utilise `prompts/orchestration.md`.

Respecte strictement `AGENTS.md` et les gates (`docs/workflow/gates.md`). Ne saute aucun
gate, ne t'arrête jamais sans note de handoff.
