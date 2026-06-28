# Gates : Definition of Ready / Definition of Done

Pour chaque colonne du GitHub Project, ce qui doit être vrai pour **entrer** (Ready)
et pour **sortir** (Done). Principe de **non-trou** : la *Done* d'une phase contient
la *Ready* de la suivante → reprise déterministe.

## Critères universels (toute sortie de colonne)

- **U1 — Handoff écrit** : aucune colonne ne se quitte sans note de handoff à jour
  (voir [`handoff.md`](handoff.md)).
- **U2 — CI verte** : dès qu'il y a du code, on ne sort pas sur du rouge
  (`black` + `ruff` + `mypy` + `pytest ≥ 95 %`).

- **U3 — Close au merge** : une issue/carte n'est passée *Done* / fermée qu'**après** le
  merge de sa PR sur `main` — **jamais avant**. (Évite les issues « closes mais non
  livrées » : du code resté sur une branche alors que le tracker dit « terminé ».)

**Dates de roadmap** : à l'entrée en *In progress*, renseigner le champ **Début** de la
carte ; à *Done*, renseigner **Fin**. (Champs Date du Project, alimentent la vue Roadmap.)

## Tableau des gates

| Phase (rôle) | Definition of Ready — *entrer* | Definition of Done — *sortir* (+ U1, U2) |
| --- | --- | --- |
| **Spec** (PO) | CDC présent dans `cahier-des-charges/` ; une US identifiée | US + FEAT créées avec critères d'acceptation ; `docs/specifications/us/*.rst` rédigé ; IDs + `:origin:` attribués |
| **Design** (Architecte) | FEAT a critères d'acceptation + spec RST | Classes identifiées (responsabilités, interfaces, abstraites) ; mapping FEAT→classes ; TASK sub-issues créées (taille sprint) ; note de conception |
| **In progress** (Dev) | TASK « Ready » : lien spec, critères, estimation, classe cible, dans le sprint | TDD : tests miroir (`tests/unit/`) + code typé + docstrings RST `:spec:` ; `make all` vert ; commit `BL-XXX: action` ; PR ouverte |
| **In review** (Relecteur) | PR ouverte, CI verte | Conformité `AGENTS.md` ; critères d'acceptation validés ; couverture ≥ 95 % ; passe de simplification ; **API publique : rupture → bump majeur + note de migration** ; décision approuvé/renvoyé ; déclencheur Sécurité évalué |
| **Security** *(conditionnel)* | Surface sensible touchée **ou** release ; PR approuvée | `bandit` propre (ou risques documentés) ; revue ciblée OWASP ; aucun secret |
| **Done** (Release mgr) | Review (+ Sécurité si déclenchée) passée | Mergé ; SemVer bumpé si release ; `CHANGELOG` à jour ; tag si release ; issue close (`Closes #`) |
| **Triage** *(maintenance)* (Support) | Un signalement/événement existe | Reproduit/qualifié ; bug issue structurée + sévérité ; routé vers backlog ou `In progress` |

## Notes

- **Renvoi de review** : la tâche recule (`In review → In progress`) avec une note de
  handoff expliquant *pourquoi*. Ce n'est pas un échec, c'est le fonctionnement normal.
- **Security** est le seul gate dont la *Ready* est un **déclencheur** (pas l'état de la
  phase précédente) : l'Orchestrateur l'évalue à la sortie de review.
