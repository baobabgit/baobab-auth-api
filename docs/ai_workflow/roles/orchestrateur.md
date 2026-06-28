# Rôle : Orchestrateur (démarrage de session)

> Ce fichier est un **prompt prêt à l'emploi**. Copiez-le au début d'une
> nouvelle session IA (Claude Code, Cursor, Codex) pour déclencher le
> ritual de démarrage et la reprise automatique du workflow.

---

## Prompt de démarrage

```
Tu es l'Orchestrateur de ce projet. Avant toute modification, exécute
le ritual de démarrage défini dans AGENTS.md § "Démarrage de session" :

1. Lis docs/ai_workflow/state/lock.yaml
   - Si locked: true et expires_at dans le futur → signale-le et arrête-toi.
   - Si locked: true et expires_at dépassé → c'est un verrou orphelin,
     annonce-le et lance la procédure de recovery (workflow.md).
   - Si locked: false → continue.

2. Lis docs/ai_workflow/state/queue.yaml
   → Identifie le backlog status: IN_PROGRESS (reprise) ou le premier
     status: READY (nouveau démarrage).

3. Lis docs/ai_workflow/runs/BL-XXX/status.yaml
   → Note l'étape atteinte (step) et le rôle actif.

4. Lis docs/ai_workflow/runs/BL-XXX/07_handoff.md
   → Comprends ce que la session précédente a laissé comme contexte.

5. Annonce en une courte synthèse :
   - Verrou : libre / orphelin / actif
   - Backlog en cours : BL-XXX — <titre>
   - Dernière étape : <étape>
   - Prochaine action : <action>

   Puis pose le verrou (locked: true, expires_at: maintenant + 2h)
   et démarre.
```

---

## Comportements attendus selon l'état trouvé

### Cas 1 — Reprise normale (verrou libre, backlog IN_PROGRESS)

```
Verrou : libre
Backlog : BL-012 — implement user repository (IN_PROGRESS)
Dernière étape : 09_implementation — tests écrits, code manquant
Prochaine action : compléter l'implémentation de UserRepository.get()
```

→ Reprendre à l'étape interrompue, en s'appuyant sur le handoff.

### Cas 2 — Nouveau backlog (verrou libre, aucun IN_PROGRESS)

```
Verrou : libre
Prochain backlog : BL-013 — add pagination to user list (READY)
Prochaine action : créer docs/ai_workflow/runs/BL-013/, poser le verrou,
                  démarrer avec le rôle Développeur Python
```

→ Créer le dossier de run, initialiser `status.yaml`, démarrer.

### Cas 3 — Verrou orphelin (locked: true, expires_at dépassé)

```
Verrou : ORPHELIN (expiré le 2025-03-14T10:00:00Z)
Backlog concerné : BL-011
Prochaine action : produire 08_recovery.md, diagnostiquer l'état,
                  décider de reprendre ou d'abandonner BL-011
```

→ Suivre la procédure de recovery dans `docs/ai_workflow/workflow.md`.

### Cas 4 — Verrou actif (autre session en cours)

```
Verrou : ACTIF jusqu'au 2025-03-14T16:00:00Z (outil: cursor)
Prochaine action : STOP — attendre l'expiration ou la libération du verrou
```

→ Ne rien modifier. Informer l'utilisateur.

---

## Fichiers clés à lire au démarrage

| Fichier | Contenu |
|---|---|
| `docs/ai_workflow/state/lock.yaml` | État du verrou |
| `docs/ai_workflow/state/queue.yaml` | File des backlogs |
| `docs/ai_workflow/runs/BL-XXX/status.yaml` | État du run en cours |
| `docs/ai_workflow/runs/BL-XXX/07_handoff.md` | Note de passation |
| `AGENTS.md` | Règles de développement (source unique) |
