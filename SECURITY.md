# Politique de sécurité

## Signaler une vulnérabilité

Ne créez **pas** d'issue publique pour une faille de sécurité.

Utilisez la fonction **GitHub Security Advisories** (onglet *Security* → *Report a
vulnerability*) du dépôt, ou contactez le mainteneur en privé. Nous visons un premier
retour sous **72 heures**.

Merci d'inclure : description, étapes de reproduction, impact estimé, version concernée.

## Versions supportées

| Version | Supportée |
| ------- | --------- |
| `0.x`   | ✅ (développement) |

## Mesures en place

- Secrets hors du dépôt : `.env` gitignoré, hook `detect-private-key`.
- Analyse statique **`bandit`** (résultats publiés en **SARIF** dans l'onglet *Security*)
  et audit des dépendances **`uv audit`** (pre-commit + CI).
- **SBOM** CycloneDX attaché à chaque Release.
- Mises à jour automatisées des dépendances via **Dependabot**.
- Passe de revue **Sécurité** conditionnelle avant fusion/release (voir
  `docs/ai_workflow/roles/05-securite.md`).
