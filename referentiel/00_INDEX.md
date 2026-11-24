# Référentiel de Prompt & Context Engineering — Index

**Version :** 1.6 — **Date :** 24 novembre 2026. Historique : v1.0 (23 nov.) → v1.1 (contre‑expertise, `15`) → v1.2 (observations résiduelles, `16`) → v1.3 (troisième contre‑expertise, `17`) → v1.4 (recherche sur le cadrage motivationnel, `research/R01`) → v1.5 (verdicts bornés, densité des contraintes, registre des connaissances, `research/R03`) → v1.6 (preuves du problème et de la solution séparées, validateur strict du registre, consultation sélective, `research/R04`) ; résumé dans `CHANGELOG.md`.
**Périmètre modèles :** Claude (Fable 5.2 / Mythos 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5, Claude Code), OpenAI (GPT‑6.2 Astra / Sol, ChatGPT, Codex / gpt‑5.3‑codex), modèles de raisonnement, modèles légers, modèles locaux, agents outillés.

---

## 1. À qui sert ce référentiel

| Lecteur | Point d'entrée | Usage |
|---|---|---|
| Humain qui écrit un prompt ponctuel | `01`, puis `11` | Principes, puis gabarit adapté |
| Humain qui configure un agent (Claude Code, Codex) | `04`, `06`, `07`, `11` §CLAUDE.md/AGENTS.md | Mécanismes natifs, autonomie, garde‑fous |
| Équipe qui industrialise des prompts | `05`, `12`, `rules.yaml` | Coût, évaluation, règles exploitables par machine |
| IA « prompt engineer » | `14` (instruction persistante), `rules.yaml` (référence) | Génération / optimisation / audit de prompts |

`14_AI_PROMPT_ENGINEER_INSTRUCTIONS.md` est autosuffisant pour les invariants : une IA peut l'utiliser comme system prompt. Ses particularités de modèles sont datées et à vérifier quand la mission en dépend. Les autres fichiers servent de référence à la demande.

## 2. Carte des fichiers

| Fichier | Contenu | Questions auxquelles il répond |
|---|---|---|
| `01_CORE_PRINCIPLES.md` | 13 principes fondamentaux | Qu'est‑ce qui reste vrai quel que soit le modèle ? |
| `02_PROMPT_STRUCTURE.md` | Composants, ordre, formats | Que mettre dans un prompt, dans quel ordre, sous quelle forme ? |
| `03_ADVANCED_TECHNIQUES.md` | 31 techniques, fiche en 10 points | Quelle technique, quand, à quel coût, avec quel niveau de preuve ? |
| `04_MODEL_SPECIFIC_GUIDELINES.md` | Comparatif modèles / environnements | Qu'est‑ce qui change entre Claude, Claude Code, GPT, Codex, petits modèles, modèles locaux ? |
| `05_CONTEXT_AND_COST_OPTIMIZATION.md` | Contexte, tokens, cache, quotas | Comment minimiser le coût **total** d'un résultat satisfaisant ? |
| `06_AUTONOMY_AND_REASONING.md` | Équilibre contrôle / autonomie | Comment laisser le modèle penser sans le laisser dériver ? |
| `07_RELIABILITY_AND_SECURITY.md` | Risques, mitigations, mécanismes externes | Que peut garantir un prompt, et que doit garantir l'infrastructure ? |
| `08_ANTI_PATTERNS.md` | 26 anti‑patterns | Qu'est‑ce qui dégrade les résultats et par quoi le remplacer ? |
| `09_TASK_CLASSIFICATION.md` | Taxonomie de 20 types de tâches + axes | Quel type de prompt pour quel type de tâche ? |
| `10_PROMPT_GENERATION_PROTOCOL.md` | Méthode en 15 étapes | Comment transformer une demande floue en prompt optimisé ? |
| `11_PROMPT_TEMPLATES.md` | Gabarits réutilisables | Par quoi commencer, concrètement ? |
| `12_EVALUATION_PROTOCOL.md` | Protocole expérimental | Comment prouver qu'une formulation est meilleure ? |
| `13_SOURCES_AND_EVIDENCE.md` | Sources, niveaux de preuve, maintenance | D'où vient chaque recommandation, et comment mettre le référentiel à jour ? |
| `14_AI_PROMPT_ENGINEER_INSTRUCTIONS.md` | Instruction persistante concise | Que doit faire une IA qui génère des prompts ? |
| `rules.yaml` | 82 règles atomiques (80 actives, 2 obsolètes conservées) — **source canonique** | Version machine des recommandations (IDs stables, conflits, preuves, volatilité, date de vérification) |
| `rules.json` | Dérivé de `rules.yaml` par le script — ne pas éditer | Même contenu pour les outils JSON |
| `scripts/build_rules.py` | Validateur + générateur | Vérifie syntaxe, clés dupliquées, schéma, types, dates, énumérations, références ; régénère `rules.json` et vérifie l'équivalence |
| `scripts/classification.py` | Référence exécutable de `09` §1 | Niveau, modules, voie rapide |
| `scripts/run_tests.py` | Suite de tests locaux (structure, concordance, présence lexicale — pas la cohérence sémantique) | 35 tests négatifs du validateur, cas de référence de classification et entrées hors domaine (`tests/classification_cases.yaml`), concordance 09/10/14, présence des invariants de 14, références croisées |
| `tests/semantic_review_cases.md` | 14 cas de revue sémantique **manuelle** | Ce que les tests automatiques ne voient pas : contradictions, provenance, fidélité, enjeu informationnel |
| `research/R01_CADRAGE_MOTIVATIONNEL.md` | Dossier de recherche (**hors référentiel établi**) | Effets réels des formulations émotionnelles, motivationnelles, de pression et d'échec honnête ; taxonomie, sources, protocole de pilote, arbitrage de R‑TONE‑003 |
| `research/R02_CARTOGRAPHIE_INDEPENDANTE.md` | Dossier de recherche (**hors référentiel établi**) | Cartographie des mécanismes indépendante du référentiel, angles morts, pistes X1 à X7 ; verdicts corrigés par R03 §2.2 |
| `research/R03_ARBITRAGE_ET_NOUVEAUX_AXES.md` | Arbitrage du retour sur v1.4, R01, R02 | Vocabulaire de verdict, erratum, protocole motivationnel révisé (P0), dix nouveaux axes, organisation en cinq niveaux, décision v1.5 |
| `research/knowledge_registry.yaml` | Registre des connaissances (validé par `scripts/registry.py`) | 49 entrées classées OP / CO / CA / DC / QO, avec quatre axes de preuve (phénomène, mécanisme, intervention, transfert), base des entrées OP et déclencheurs de consultation (table dans `10`, étape 8) |
| `research/R04_EXPLOITATION_ET_SELECTION.md` | Arbitrage du retour sur v1.5 et R03 | Consultation sélective, validateur strict, preuve du problème vs de la solution, typologie des contraintes, EmotionRL, combinaison C dans P0, sélection contextuelle des techniques |
| `scripts/registry.py` | Validateur du registre | Chargeur strict partagé avec `build_rules.py`, vocabulaires de référence dans le code, cohérence niveau × preuve |
| `17_THIRD_REVIEW_ARBITRATION.md` | Arbitrage de la troisième contre‑expertise | V12‑001 à 016, présupposés du référentiel, vérifications |
| `16_FINAL_REVIEW_AND_ARBITRATION.md` | Arbitrage final et auto‑relecture | Observations V11, nouvelles constatations, vérifications, maturité |
| `CHANGELOG.md` | Historique synthétique | Modifications par version |
| `15_REVIEW_ARBITRATION.md` | Registre d'arbitrage de la contre‑expertise | Quels constats ont été acceptés, nuancés ou rejetés, et ce qui a changé |

## 3. Légende des niveaux de preuve (utilisée partout)

Dans `rules.yaml`, seuls DOC, OFF, EMP et HYP sont des **types de preuve** (champ `evidence`). CTR et OBS décrivent la **transférabilité** et le **cycle de vie** : ils y sont portés par les champs `transfer` (`general`, `provider_specific`, `contested`), `status` et `notes`. Dans le Markdown, les étiquettes [CTR] et [OBS] restent utilisées avec ce sens.

| Code | Signification | Exemple |
|---|---|---|
| **[DOC]** | Fait documenté (comportement d'API, prix, fonctionnalité) | Lecture du cache facturée 0,1× l'entrée de base |
| **[OFF]** | Recommandation officielle d'un fournisseur, sans protocole publié | « Mettez la question à la fin des longs documents » |
| **[EMP]** | Résultat empirique publié (article, rapport technique, test chiffré d'un fournisseur — non indépendant, non répliqué sauf mention) | Dégradation avec la longueur du contexte (Chroma, 2025) |
| **[HYP]** | Hypothèse plausible, peu ou pas démontrée | « Une structure XML aide davantage les petits modèles » |
| **[CTR]** | Pratique controversée ou fortement dépendante du modèle | Attribution d'un rôle d'expert pour gagner en exactitude |
| **[OBS]** | Pratique obsolète ou contre‑productive sur les modèles récents | Prefill de la réponse (refusé par l'API sur Claude 4.6+) |

Règle de lecture : une recommandation [OFF] d'un fournisseur vaut pour **ses** modèles à **la date indiquée**. Elle n'est pas transférable sans test.

## 4. Modifications apportées à la structure demandée

1. **`rules.yaml` comme source canonique**, `rules.json` dérivé par `scripts/build_rules.py` : YAML tolère les commentaires et reste lisible. Les codes sont des chaînes entre guillemets : non cité, `OFF` est lu comme booléen par les parseurs YAML 1.1 (défaut corrigé en v1.1). Le catalogue est conçu pour une **sélection assistée par IA** avec filtres structurés, pas comme moteur de décision déterministe (`rules.yaml` → `meta.selection_semantics`).
2. **Méthode de mise à jour intégrée à `13`** plutôt qu'un fichier séparé : la maintenance dépend directement de la traçabilité des sources ; les séparer créerait une redondance.
3. **Context engineering traité dans `05`** et non dans `03` : c'est une discipline transversale, pas une technique ponctuelle. `03` y renvoie.
4. **Pas de fichier « glossaire »** : les termes sont définis à leur première occurrence ; un glossaire dupliquerait.

## 5. Limites déclarées

- **Aucune expérience n'a été exécutée** pour produire ce référentiel, ni pour sa contre‑expertise. En particulier, le gain du protocole de génération (`10`, `14`) face à une demande directe n'est pas démontré (`12` §5.0). Les chiffres cités proviennent des sources listées dans `13`. Le protocole de `12` décrit comment les vérifier sur vos tâches.
- Les recommandations spécifiques aux modèles (`04`) sont **volatiles** : elles changent à chaque version. Elles sont datées et doivent être revalidées (voir `13` §7).
- Certaines sources n'ont pu être consultées qu'à travers des extraits ; `13` indique le statut de vérification de chacune.

## 6. Parcours recommandés

- **« J'ai 5 minutes »** → `01` §Résumé, puis le gabarit T1 de `11`.
- **« Je configure Claude Code ou Codex »** → `04` §3 et §6, `06` §4, `07` §3, gabarits CLAUDE.md / AGENTS.md de `11`.
- **« Mes agents coûtent trop cher »** → `05` en entier, puis `08` AP‑01, AP‑08, AP‑09, AP‑19, AP‑20.
- **« Je construis une IA qui écrit des prompts »** → `14`, `10`, `rules.yaml`, `12` (§5.0 d'abord : mesurer contre une demande directe).
