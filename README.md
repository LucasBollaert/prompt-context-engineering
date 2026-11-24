# Prompt & Context Engineering

**Version candidate 1.6 — documentation et instructions réutilisables, non validées empiriquement sur modèle.**

Un référentiel de Prompt et Context Engineering (v1.6) et trois instructions autonomes pour concevoir et auditer des prompts ponctuels, persistants ou intégrés à des systèmes. Le but est la qualité du résultat réel, la fidélité au besoin et l'efficience, pas l'accumulation de règles.

## Démarrage
1. Configurer `SYSTEM_PROMPT.md` au niveau d'instruction privilégié réellement supporté par l'environnement. Fournir le besoin, le modèle cible, les contraintes et le contexte autorisé. Donner accès en lecture à `referentiel/`, `audit/`, `profils/` et `USER_REQUIREMENTS.md`. Ne pas charger le référentiel entier dans chaque contexte ni utiliser son ancien fichier `14` comme seconde instruction active.
2. Pour un audit indépendant, utiliser **à la place** `AUDIT_CONCEPTION_SYSTEM_PROMPT.md` (qualité et exploitation des capacités) ou `AUDIT_SYSTEM_PROMPT.md` (intégration, interfaces et contrats). Sessions distinctes et sans conclusions antérieures pour le mode aveugle ; cette séparation ne garantit pas l'indépendance statistique. Les audits restent proportionnés.
3. Fournir le prompt exact, les exigences et sources, la cible et les contrats applicables. Arbitrer les constats, conserver les versions et qualifier les résultats requis avant promotion. Les tests de lecteur et de modèle exigent les autorisations appropriées.

## Connaissances et invariants
`referentiel/00_INDEX.md` oriente la consultation. Le registre `referentiel/research/knowledge_registry.yaml` distingue OP, CO, CA, DC et QO et sépare les axes de preuve. Le référentiel v1.6 est conservé sans modification. Les exigences métier validées complètent la recherche ; elles ne prouvent pas une efficacité générale. `audit/INVARIANT_PROPORTION_ARRET.md` formalise la lutte contre la sur-assurance sans supprimer les vérifications indispensables. `profils/MODELE_PROFIL.md` aide à décrire un projet local sans rendre ses conventions universelles.

## Vérifier localement
Python 3 et PyYAML nécessaires pour les scripts du référentiel. Installer les dépendances dans un environnement isolé. Depuis la racine :

```sh
python -m pip install -r requirements.txt
sha256sum -c SHA256SUMS
(cd referentiel && PYTHONDONTWRITEBYTECODE=1 python scripts/run_tests.py)
```

Les tests vérifient la cohérence documentaire et informatique, non la performance des modèles. Les scénarios de `evaluations/` sont proposés, non exécutés sur cible. Le dépôt ne contient ni lanceur d'IA ni intégration à un système réel. Les informations sur les modèles peuvent vieillir : vérifier lorsqu'elles sont décisives.

## Contribuer et versionner
Pour chaque changement : besoin, défaut ou hypothèse, source, modification minimale, validation et limites. Conserver la version antérieure via Git ou un historique de versions ; les instructions actives sont des candidats jusqu'à décision explicite. Ne pas publier de prompts métier, traces, secrets ou archives internes. Pour régénérer les empreintes : `python scripts_manifest.py` depuis la racine.

## Licences
- Code (`referentiel/scripts/`, `scripts_manifest.py`) : Apache License 2.0, voir `LICENSE`.
- Prompts, protocoles, référentiel et documentation : Creative Commons Attribution 4.0 International (CC BY 4.0), voir `LICENSE-docs`.
- © 2026 Lucas Bollaert. Les sources citées restent la propriété de leurs auteurs ; voir `NOTICE`.

Ce dépôt n'apporte aucune validation empirique du dispositif complet ; voir `VERIFICATIONS.md`.

## v1.6
Seul un constat effectivement bloquant impose un cycle de correction ; gravité et preuve ne sont pas confondues. Les prérequis de qualification et règles locales approuvées restent applicables. Le déclassement est traçable sans arbitrage humain systématique. Aucune règle locale n’est imposée.
