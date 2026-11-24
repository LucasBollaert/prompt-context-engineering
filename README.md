# Prompt & Context Engineering

[![Tests](https://github.com/LucasBollaert/prompt-context-engineering/actions/workflows/tests.yml/badge.svg)](https://github.com/LucasBollaert/prompt-context-engineering/actions/workflows/tests.yml)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE)
[![Contenus: CC BY 4.0](https://img.shields.io/badge/contenus-CC%20BY%204.0-lightgrey.svg)](LICENSE-docs)

> **English summary.** A French-language knowledge base on prompt and context engineering: evidence-graded rules, research notes and a knowledge registry. It comes with three ready-to-use system prompts: a prompt designer, a design auditor and an integration auditor. Paste `SYSTEM_PROMPT.md` as the system prompt (or custom instructions) of a capable model, describe what you need, and get a prompt tailored to your target model, with assumptions and checks listed separately. Code is Apache-2.0; prompts and documentation are CC BY 4.0. Only structural tests are provided: the full setup has not been validated empirically.

Un référentiel de Prompt et Context Engineering et trois instructions prêtes à l'emploi pour **concevoir, auditer et faire évoluer des prompts** : ponctuels, persistants ou intégrés à un système. Le but est la qualité du résultat réel, la fidélité au besoin et l'efficience, pas l'accumulation de règles.

**Licences** : le code est sous Apache‑2.0 (`LICENSE`) ; les prompts, protocoles, le référentiel et la documentation sont sous CC BY 4.0 (`LICENSE-docs`). Voir [Licences](#licences).

## À quoi sert ce dépôt
- **Écrire un bon prompt** pour Claude, GPT, Codex, un modèle léger ou un agent, adapté à la cible, au contexte et au risque. Ou s'entendre dire qu'aucune reformulation n'est utile.
- **Auditer un prompt existant** : sa qualité de conception, ou sa compatibilité avec le système qui le lit.
- **Choisir les techniques selon leurs preuves** : ce qui est établi, conditionnel, expérimental ou déconseillé, avec les sources.

## Démarrage rapide
1. Copiez le contenu de [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md).
2. Collez‑le comme instruction système d'un modèle capable : prompt système d'API, instructions d'un projet, instructions personnalisées.
3. Décrivez votre besoin, votre modèle cible et vos contraintes. Par exemple :
   ```text
   Cible : Claude Code, sur un dépôt Python existant.
   Besoin : un prompt pour corriger un bug qui déconnecte les utilisateurs après 5 minutes,
   sans modifier l'API publique.
   Contexte : tests pytest disponibles ; pas de droit de push.
   ```
4. Vous recevez un prompt prêt à copier, ainsi que, séparément, les paramètres recommandés, les hypothèses et les contrôles à garantir hors du prompt.

**Pour de meilleurs résultats**, donnez au modèle un accès en lecture aux dossiers `referentiel/`, `audit/` et `profils/` : fichiers d'un projet, agent avec accès au disque. Sans cet accès, le prompt fonctionne seul et signale ce qu'il n'a pas pu consulter.

## Les trois rôles
Chaque rôle s'utilise dans **sa propre session** : on ne charge jamais deux instructions ensemble.

| Fichier | Rôle | Quand l'utiliser |
|---|---|---|
| [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md) | Concepteur | Créer, adapter, comparer ou faire évoluer un prompt |
| [`AUDIT_CONCEPTION_SYSTEM_PROMPT.md`](AUDIT_CONCEPTION_SYSTEM_PROMPT.md) | Auditeur de conception | Juger la qualité d'un prompt : nécessité, intention, capacités de la cible, contraintes, contexte, coût |
| [`AUDIT_SYSTEM_PROMPT.md`](AUDIT_SYSTEM_PROMPT.md) | Auditeur d'intégration | Vérifier qu'un prompt fonctionne dans le système qui le lit : contrats, variables, formats, permissions |

Pour un audit, ouvrez une nouvelle session avec l'auditeur choisi et fournissez le prompt exact, le besoin d'origine et la cible (dossier d'entrée : [`audit/CONTROLE_PROMPTS.md`](audit/CONTROLE_PROMPTS.md)). En mode aveugle, ne transmettez pas les conclusions d'un autre audit. Les deux audits ne sont pas obligatoires : un prompt simple n'en demande aucun.

## Principes
- **Les techniques sont choisies, pas empilées.** Chaque connaissance du registre a un niveau : **OP** opérationnel (appliqué quand ses conditions sont réunies), **CO** conditionnel, **CA** candidat à tester, **DC** déconseillé dans des conditions précises, **QO** question ouverte. Un candidat n'est jamais présenté comme un gain acquis.
- **Proportion et arrêt** ([`audit/INVARIANT_PROPORTION_ARRET.md`](audit/INVARIANT_PROPORTION_ARRET.md)). Seul un défaut bloquant établi impose une correction. Les améliorations facultatives et la simple prudence ne relancent pas de cycle. Les vérifications indispensables et les risques de sécurité réels ne sont jamais escamotés.
- **Liberté de méthode pour la cible** : une finalité vraie et des critères précis, plutôt qu'une procédure imposée.
- **Honnêteté** : distinguer fait vérifié, hypothèse et inconnu. Ne jamais prétendre avoir testé ce qui ne l'a pas été.

## Organisation du dépôt
```text
SYSTEM_PROMPT.md                    concepteur de prompts
AUDIT_CONCEPTION_SYSTEM_PROMPT.md   auditeur de conception
AUDIT_SYSTEM_PROMPT.md              auditeur d'intégration
audit/                              protocole de contrôle commun, règle de proportion et d'arrêt
evaluations/                        scénarios de contrôle manuels (non exécutés sur modèle)
profils/                            modèle pour décrire votre propre projet (MODELE_PROFIL.md)
referentiel/                        base de connaissances v1.6 (gelée)
  00_INDEX.md                       ← commencer ici
  01 à 13                           principes, structure, techniques, modèles, contexte, sécurité, évaluation, sources
  14                                ancienne instruction, conservée pour l'historique (ne pas charger)
  15 à 17, research/                contre-expertises et dossiers de recherche (provenance des choix)
  rules.yaml / rules.json           règles atomiques avec niveau de preuve
  research/knowledge_registry.yaml  registre des connaissances (OP/CO/CA/DC/QO)
  scripts/, tests/                  validateurs et tests structurels
```
Les dossiers de recherche mentionnent des archives de travail qui ne sont pas incluses dans ce dépôt.

## Limites
- Les tests vérifient la cohérence documentaire et le code, **pas la performance des modèles**. Les scénarios de `evaluations/` sont proposés, non exécutés.
- Les informations sur les modèles datent de novembre 2026 et vieilliront : vérifiez‑les lorsqu'elles sont décisives.
- Le dépôt ne contient ni lanceur d'IA ni intégration à un système réel.

## Vérifier localement
Python 3 et PyYAML sont nécessaires. Depuis la racine, dans un environnement isolé :
```sh
python -m pip install -r requirements.txt
sha256sum -c SHA256SUMS
(cd referentiel && python scripts/run_tests.py && python scripts/registry.py)
```
Sous Windows, `sha256sum` est disponible dans Git Bash ou WSL. Les mêmes contrôles s'exécutent automatiquement à chaque envoi (badge « Tests »).

## Contribuer
Pour chaque proposition, indiquer le besoin, le défaut ou l'hypothèse, la source, la modification minimale, sa validation et ses limites. Les instructions restent des candidates jusqu'à décision explicite. Ne pas soumettre de prompts métier privés, de traces, de secrets ni d'archives internes. Après une modification, régénérer les empreintes avec `python scripts_manifest.py`.

## Licences
- Code (`referentiel/scripts/`, `scripts_manifest.py`) : Apache License 2.0, voir `LICENSE`.
- Prompts, protocoles, référentiel et documentation : Creative Commons Attribution 4.0 International (CC BY 4.0), voir `LICENSE-docs`.
- © 2026 Lucas Bollaert. Les sources citées restent la propriété de leurs auteurs ; voir `NOTICE`.

Ce dépôt n'apporte aucune validation empirique du dispositif complet ; voir `VERIFICATIONS.md`. Historique : [`CHANGELOG.md`](CHANGELOG.md).