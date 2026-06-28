@AGENTS.md

## Spécifique à Claude Code

Les règles de développement complètes vivent dans `AGENTS.md` (source unique de vérité,
partagée avec Codex et Cursor). Ne les duplique pas ici.

- Avant de modifier des fichiers sous `src/`, vérifie qu'une **classe de test miroir** existe
  dans `tests/unit/` (même chemin, fichier `test_<module>.py`) ou crée-la.
- Pour une **classe abstraite**, écris une **classe concrète de test** dans le fichier de test.
- N'ajoute jamais une 2ᵉ classe dans un fichier existant : **1 classe = 1 fichier**.
- Lance `make all` (qualité + tests ≥ 95 % + build) avant de proposer un commit.
- Ne jamais modifier le projet si le verrou `docs/ai_workflow/state/lock.yaml` est actif
  et non expiré.
- Ne jamais mentionner cet outil comme contributeur, auteur ou co-auteur dans un commit,
  une PR, un commentaire de code ou tout fichier versionné.
