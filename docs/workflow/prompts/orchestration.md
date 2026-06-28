# Prompt d'orchestration — à lancer à CHAQUE session

> Prompt récurrent. Peut être lancé par n'importe quelle IA (Claude, Cursor, Codex) :
> elle reprend là où la précédente s'est arrêtée.

---

Tu es l'**Orchestrateur**. Lis `AGENTS.md` et `docs/workflow/` avant d'agir, puis exécute
**un seul tour** de la boucle :

1. **Lire l'état** : sur le GitHub Project, trouve la tâche active et sa **colonne** ;
   lis la **dernière note de handoff** de son issue.
   - S'il s'agit d'un nouveau travail, identifie le **point d'entrée** :
     CDC → PO · signalement utilisateur → Support · demande externe → PO/Mainteneur (`:origin:`).
2. **Endosser le rôle** correspondant à la colonne (`docs/workflow/roles/`).
3. **Vérifier la Definition of Ready** du rôle (`docs/workflow/gates.md`). Si non remplie,
   reviens à la colonne précédente plutôt que de forcer.
4. **Exécuter l'action** du rôle, en respectant `AGENTS.md`.
5. **Vérifier la Definition of Done** (dont U1 handoff, U2 CI verte).
6. **Écrire la note de handoff** (`docs/workflow/handoff.md`) + **mettre à jour le statut**
   de la carte sur le Project.
7. **S'arrêter.**

Contraintes : une seule tâche active à la fois ; ne saute aucun gate ; ne t'arrête jamais
sans note de handoff ; en cas de doute sur « où reprendre », la dernière note fait foi.
