# Configuration GitHub (one-time)

Étapes de configuration non versionnables dans le repo, à faire **une fois** après
création du projet. Remplace `OWNER/REPO` par les valeurs réelles.

> Prérequis : `gh auth login` puis `gh auth refresh -s project` (scope Projects).

## 1. Marquer le dépôt comme template (sur le repo template uniquement)

```bash
gh api -X PATCH repos/OWNER/REPO -F is_template=true
```

Créer un projet à partir du template :

```bash
gh repo create OWNER/mon-projet --template OWNER/templates --private --clone
```

## 2. Labels (US / FEAT / Task + priorités)

```bash
gh label create "type:us"        -c "#0e8a16" -d "User Story"   -R OWNER/REPO
gh label create "type:feat"      -c "#1d76db" -d "Feature"      -R OWNER/REPO
gh label create "type:task"      -c "#5319e7" -d "Task"         -R OWNER/REPO
gh label create "priority:high"  -c "#d93f0b" -R OWNER/REPO
gh label create "priority:med"   -c "#fbca04" -R OWNER/REPO
gh label create "priority:low"   -c "#c2e0c6" -R OWNER/REPO
gh label create "dependencies"   -c "#0366d6" -R OWNER/REPO
```

## 3. GitHub Project (board + colonnes + sprints)

```bash
gh project create --owner OWNER --title "Mon projet"
```

Puis, dans l'UI du Project (ou via `gh project field-create`) :

- champ **Status** avec les options : `Spec`, `Design`, `In progress`, `In review`,
  `Security`, `Done` (+ `Triage` pour la maintenance) ;
- champ **Iteration** (sprints) ;
- champs `Priority`, `Estimate`.

## 4. Branch protection (applique le gate « U2 : CI verte »)

> ⚠️ **Modèle solo / mono-IA** : n'exige **pas** d'approbation de PR — une IA ne peut pas
> approuver sa propre PR, cela bloquerait tout merge. On exige uniquement la **CI verte** ;
> le rôle Relecteur est porté par le workflow, pas par GitHub.
>
> ⚠️ **Plan** : branch protection et rulesets sont **indisponibles sur repo privé en plan
> Free** (HTTP 403). → rendre le repo **public** ou passer **Pro/Team**.

Le plus simple : exécuter [`scripts/setup_github.sh`](../../scripts/setup_github.sh)
(labels + ruleset + environnements, idempotent, tolérant au plan). Sinon, manuellement
via un **ruleset** exigeant la CI verte :

```bash
gh api --method POST repos/OWNER/REPO/rulesets --input - <<'JSON'
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
```

## 5. Environnements de publication

```bash
gh api -X PUT repos/OWNER/REPO/environments/pypi
gh api -X PUT repos/OWNER/REPO/environments/testpypi
```

(Optionnel : exiger une approbation manuelle avant publication via l'UI de l'environnement.)

## 6. Trusted Publishing (UI PyPI / TestPyPI — pas de `gh`)

Sur **pypi.org** et **test.pypi.org** → *Your projects* → *Publishing* → *Add a pending
publisher* :

- Owner : `OWNER`
- Repository : `REPO`
- Workflow : `release.yml`
- Environment : `pypi` (et `testpypi` côté TestPyPI)

Aucun token à stocker : la publication se fait par OIDC.

## 7. Quota CI — suspension et réactivation

Sur un dépôt privé, les minutes GitHub Actions sont limitées. En cas de quota épuisé,
la CI peut être suspendue sans toucher au code, via une **variable de dépôt**.

### Suspendre la CI

```
GitHub → Settings → Secrets and variables → Actions → Variables → New repository variable
  Name  : CI_ENABLED
  Value : false
```

Effet immédiat : tous les jobs de `ci.yml` sont sautés (`skipped`). Les PRs restent
ouvrables et les commits continuent de s'empiler ; aucun job ne consomme de minutes.

### Réactiver la CI

Deux options (au choix) :
- Remettre `CI_ENABLED = true` (ou supprimer la variable) ;
- Puis lancer un run manuel : **Actions → CI → Run workflow**.

### Règle de merge pendant la suspension

Si le ruleset exige la CI verte, le merge est bloqué tant que les jobs sont en `skipped`.
Options :
- Désactiver temporairement le ruleset via `gh api` ou l'UI ;
- Ou attendre la réinitialisation du quota, réactiver la CI et obtenir un run vert.

> La variable `CI_ENABLED` n'est **pas** versionnée : elle vit uniquement dans
> les paramètres du dépôt GitHub, sans laisser de trace dans le code.

## 8. Sécurité (Code Scanning)

- **Repo public** : l'upload SARIF (Bandit) alimente l'onglet *Security* sans config.
- **Repo privé** : nécessite **GitHub Advanced Security**. Sans GHAS, l'étape d'upload
  SARIF est tolérée (`continue-on-error`) ; le gate Bandit/pip-audit reste actif.
- Vérifier que **Dependabot alerts** est activé (Settings → Code security).
```
