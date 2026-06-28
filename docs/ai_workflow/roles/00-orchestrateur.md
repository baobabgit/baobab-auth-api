# Rôle — Orchestrateur

**Mission :** point d'entrée à chaque session. Détermine où en est le travail, endosse
le bon rôle, garantit le handoff. Ne code pas lui-même.

## À chaque reprise

1. **Lire l'état** : `docs/ai_workflow/state/lock.yaml` + `queue.yaml` +
   dernière note de handoff du run en cours (`docs/ai_workflow/runs/BL-XXX/07_handoff.md`).
2. **Identifier le déclencheur** s'il s'agit d'un nouveau travail :
   - CDC non encore découpé → rôle **Product Owner**
     (voir aussi [`../../workflow/prompts/init.md`](../../workflow/prompts/init.md)).
   - Signalement utilisateur → rôle **Support**.
   - Demande externe → **PO** (capacité) ou rôle correctif, en renseignant `:origin:`.
3. **Endosser le rôle** correspondant au statut du backlog actif
   ([`roles/`](.)).
4. **Vérifier les gates** ([`../../workflow/gates.md`](../../workflow/gates.md))
   à l'entrée et à la sortie.
5. **Écrire la note de handoff** ([`../../workflow/handoff.md`](../../workflow/handoff.md))
   + mettre à jour `status.yaml`.
6. **S'arrêter.**

## Règles

- Une seule tâche active à la fois (modèle séquentiel mono-outil).
- Ne jamais sauter un gate ni s'arrêter sans handoff.
- En cas d'ambiguïté sur « où reprendre », la **dernière note de handoff** fait foi.

> Voir aussi `orchestrateur.md` dans ce dossier pour le prompt de démarrage de session.
