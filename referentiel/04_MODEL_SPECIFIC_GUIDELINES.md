# 04 — Recommandations par modèle et par environnement

**Volatilité : élevée.** État au 23 novembre 2026. Revalider à chaque nouvelle version (procédure : `13` §7). Avant de s'appuyer sur une particularité ci‑dessous, vérifier qu'elle s'applique à la cible réelle (modèle exact, client, mode, date) [R-CAP-001].

## 1. Distinguer le modèle de son environnement

| Couche | Ce qu'elle détermine | Exemples |
|---|---|---|
| **Modèle** | Littéralité, verbosité par défaut, propension à agir, à déléguer, à vérifier ; formats appris (patch, outils) | Fable 5.2 parle peu entre les appels d'outils ; GPT‑6.2 Astra demande plus souvent une clarification |
| **Paramètres d'API** | Profondeur de raisonnement, longueur, format | `effort`, `reasoning.effort`, `max_tokens`, structured outputs |
| **Harnais / environnement** | Outils, permissions, mémoire, compaction, sous‑agents, hooks, system prompt sous‑jacent | Claude Code, Codex CLI, ChatGPT, claude.ai, votre propre agent |
| **Instructions persistantes** | Conventions du projet | CLAUDE.md, AGENTS.md, instructions de projet |
| **Prompt de tâche** | La tâche | Votre message |

Conséquence : un même texte se comporte différemment selon la couche qui l'entoure. Dans Claude Code ou Codex, un **long system prompt est déjà présent** ; votre prompt de tâche doit compléter, pas répéter. Diagnostiquer un problème commence par identifier la couche responsable (souvent : paramètre d'effort ou permissions, pas formulation).

## 2. Claude via API (Anthropic)

**Modèles actuels** : Claude Fable 5.2 / Mythos 5.2 (sommet de gamme ; Mythos réservé aux organisations vérifiées pour certaines capacités), Opus 5.5, Sonnet 5.5, Haiku 5.5. [DOC]

| Thème | Recommandation | Preuve |
|---|---|---|
| Raisonnement | Thinking adaptatif ; régler `effort` (défaut `high` sur Fable 5.2). `budget_tokens` → erreur 400 sur 4.7+ | [DOC] |
| Balayage d'effort | Refaire à chaque version ; `xhigh` seulement si gain mesuré ; `max` pour plafonds ou problèmes ouverts | [OFF] |
| Prefill | Non supporté sur 4.6+ (erreur 400) | [DOC] |
| Historique | Ajout seul ; ne pas modifier tours passés, `system` ou `tools` en cours de conversation (blocs de thinking invalidés, erreur 400 de contrôle de préfixe sur Fable 5.2) | [DOC] |
| Ton | Pas de MAJUSCULES ni « CRITICAL » ; raisons plutôt qu'injonctions ; « never » est absolu | [OFF] |
| Long contexte | Documents en haut, balisés (`<document><source><document_content>`), question à la fin, citer d'abord | [OFF] |
| Parallélisme | Bloc `<use_parallel_tool_calls>` | [OFF] |
| Fin de tâche (Fable 5.2) | Consigne « Finishing work » : ~moitié moins de sessions inachevées, ~+30 % de tokens de sortie | [EMP fournisseur] |
| Propriété du code (Fable 5.2) | « You are the owner and long-term maintainer… » : consolidation ~75 % vs <10 %, mais +70‑80 % de tokens et changements non demandés ; **ne pas utiliser** si l'utilisateur veut des changements minimaux | [EMP fournisseur] |
| Progression (Fable 5.2) | Le modèle écrit peu de texte visible entre outils ; activer `thinking.display: "updates"` ou ajouter une consigne de mise à jour | [DOC]/[OFF] |
| Rapport final (Fable 5.2) | Consigne « Write for an intelligent but low-context reader » | [OFF] |
| Prudence cumulée (Fable 5.2) | Purger mémoires et notes ; nommer les étapes sans approbation ; préciser les exceptions | [OFF] |
| Verbosité (Opus 5) | Réponses longues par défaut ; `effort` ne contrôle pas la longueur → demander la concision | [OFF] |
| Sous‑agents (Opus 4.6, Opus 5) | Tendance à sur‑déléguer ; bloc de cadrage officiel | [OFF] |
| Haiku 5.5 | Page dédiée : effort, recherche, JSON avec vos outils, arrêt précoce, vérification du code | [DOC] |
| Refus | `stop_reason: "refusal"` avec catégorie (`cyber`, `bio`, `reasoning_extraction`…) ; ne pas demander le raisonnement dans la réponse | [DOC] |
| Cache | Écriture 5 min = 1,25× ; 1 h = 2× ; lecture = 0,1× (multiplicateur réduit annoncé pour Fable sur la page de prix) ; préfixe outils → system → messages | [DOC] |

## 3. Claude Code

**Nature** : harnais agentique (terminal, IDE, desktop, web) avec un system prompt propre, des outils de fichiers et de shell, et des mécanismes de contrôle.

| Mécanisme | Usage | À éviter |
|---|---|---|
| **CLAUDE.md** (utilisateur `~/.claude/`, projet, sous‑dossiers ; imports `@path`) | Commandes non devinables, style divergent des défauts, tests, étiquette du dépôt, décisions d'architecture, pièges | Ce que le code révèle, conventions standards, docs d'API, contenu changeant, tutoriels, description fichier par fichier |
| **Skills** (`.claude/skills/<nom>/SKILL.md`) | Savoir‑faire utile parfois ; workflows invoqués (`/nom`) | Règles permanentes |
| **Hooks** (`settings.json`) | Ce qui doit arriver à chaque fois : formatage, blocage d'écriture, contrôle de fin (`Stop`) | Jugement subjectif |
| **Sous‑agents** (`.claude/agents/*.md`, outils et modèle propres) | Exploration lourde en lecture, revue à contexte frais, sécurité | Tâches simples, couplées |
| **Plan mode** | Approche incertaine, multi‑fichiers | Diff descriptible en une phrase |
| **`/goal`** | Condition de fin réévaluée par un évaluateur séparé après chaque tour | Objectifs non vérifiables |
| **Permissions** : auto mode (classifieur qui bloque escalade de périmètre, infrastructure inconnue, actions pilotées par contenu hostile), listes d'autorisation, sandbox OS, `dontAsk` en non‑interactif | Calibrer l'autonomie techniquement | Tout autoriser avant de comprendre le workflow |
| **Contexte** : `/clear`, `/compact <consignes>`, `/rewind` (résumer depuis/jusqu'à), `/btw`, `/context` | Gestion active | Sessions « fourre‑tout » |
| **Parallélisme** : worktrees, `/batch` (5 à 30 sous‑agents), `claude -p` en boucle, agent view | Migrations, fan‑out | Fichiers partagés sans isolation |
| **Revue** : `/code-review`, sous‑agent adversarial | Avant de considérer une tâche finie | Appliquer chaque remarque (sur‑ingénierie) |

Règles clés [OFF] : donner une vérification exécutable ; exiger des preuves ; après deux corrections ratées, `/clear` et meilleur prompt ; si une règle de CLAUDE.md est ignorée, le fichier est probablement trop long ; emphase (« IMPORTANT ») sur **une seule** ligne réellement ignorée, jamais sur beaucoup.

Note historique : le billet de blog d'avril 2025 (aujourd'hui non maintenu) conseillait l'emphase « IMPORTANT / YOU MUST » plus largement ; la documentation actuelle restreint cet usage. [OBS partiel]

## 4. Claude conversationnel (claude.ai, apps)

- Un system prompt produit long est déjà présent ; le prompt utilisateur se concentre sur la tâche.
- Mécanismes persistants : **projets** (instructions + fichiers de connaissance), **préférences/styles**, **mémoire** (si activée), **skills**.
- Les fichiers de projet sont du contexte permanent : n'y mettre que ce qui sert souvent ; sinon les joindre au besoin.
- Pas d'accès aux paramètres d'effort fins dans tous les plans ; le choix du modèle et du mode de raisonnement est le principal levier.
- Quotas d'abonnement : la consommation dépend de la longueur de la conversation (tout l'historique est relu à chaque tour) → nouvelles conversations pour tâches nouvelles (`05` §9).

## 5. OpenAI via API (GPT‑6.2 et famille GPT‑5.x)

**Modèles actuels documentés** : GPT‑6.2 Astra (`gpt-6.2-astra`, tâches les plus exigeantes) et GPT‑6.2 Sol (`gpt-6.2-sol`, travaux complexes à moindre coût) ; GPT‑6 / 6.1 antérieurs. [DOC]

| Thème | Recommandation | Preuve |
|---|---|---|
| API | Responses API (obligatoire pour l'appel d'outils sur GPT‑6.2 ; persistance du raisonnement entre appels). Sur GPT‑5, Tau‑Bench Retail : 73,9 % → 78,2 % en passant `previous_response_id` | [DOC]/[EMP fournisseur] |
| Effort | Commencer à `medium` ; remplacer `none`/`minimal` par `low` sur GPT‑6.2 | [OFF] |
| Clarification | Astra demande plus souvent une clarification que ses prédécesseurs ; pour les tâches longues, l'autoriser explicitement à supposer et continuer ; outil de question asynchrone | [OFF] |
| Autonomie | Agir sans attendre, persévérer, vérifier, signaler les hypothèses | [OFF] |
| Instructions héritées | Réexaminer « sois concis » (déjà concis par défaut) ; `temperature`, `top_p`, `logprobs` non pris en charge | [DOC] |
| Ordre | `instructions` ajouté après `input` ; instructions stables dans un message `developer` en tête | [DOC] |
| Cache | Préfixe inchangé ; modifier l'historique peut faire perdre les éléments de raisonnement. GPT‑5.6+ : écritures payantes (1,25× à TTL 30 min, 2,5× à 12 h), lectures 0,1× (0,05× sur GPT‑6.2 Astra/Sol), seuil 1 024 tokens, breakpoints implicites ou explicites (`05` §9.2) | [DOC] S-O10 |
| Contradictions | Les modèles très fidèles dépensent du raisonnement pour concilier des règles contradictoires → relire et résoudre | [OFF] (GPT‑5) |
| Markdown | Par défaut peu de Markdown via API ; le demander explicitement ; réinjecter tous les 3‑5 messages dans les longues conversations | [OFF] (GPT‑5) |
| Metaprompting | Demander au modèle des modifications minimales de son prompt | [OFF] |

## 6. Codex (CLI, IDE, app, cloud)

**Codex (produit) ≠ `gpt-5.3-codex` (modèle API).** OpenAI recommande de commencer par **GPT‑6.2 Sol** pour la plupart des tâches dans Codex, et GPT‑6.2 Astra pour les projets complexes ; la disponibilité varie selon le produit et la version [DOC, S-O9]. `gpt-5.3-codex` reste le modèle orienté code documenté dans l'API (Responses API ; effort `low`/`medium`/`high`/`xhigh`) [DOC, S-O3, S-O11]. **Les consignes ci‑dessous marquées « 5.3 » ne s'appliquent qu'à ce modèle** ; pour Codex avec GPT‑6.2, suivre §5.

| Mécanisme | Recommandation | Preuve |
|---|---|---|
| **AGENTS.md** : global `~/.codex/AGENTS.md` (ou `AGENTS.override.md`), puis de la racine du dépôt jusqu'au répertoire courant, un fichier par niveau, limite de taille par défaut (32 KiB) ; le plus spécifique l'emporte ; les instructions de l'utilisateur dans le chat priment sur AGENTS.md pour les préférences et conventions, sans lever les restrictions système/développeur ni les permissions techniques. Le chargement dépend du répertoire de lancement : ne pas supposer qu'un fichier est lu sans l'avoir vérifié [S-O12] | Court et précis ; commandes de build/test/lint ; structure ; conventions ; contraintes ; définition de « terminé » ; ajouter une règle seulement quand une erreur se répète ; renvoyer vers des fichiers par sujet si le fichier grossit | [OFF]/[DOC] |
| **Starter prompt officiel** | Partir du prompt recommandé et ajouter des compléments ciblés | [OFF] |
| **Outils** | `apply_patch` officiel (format d'entraînement) ; `shell_command` ; `update_plan` ; outils dédiés aux noms précis ; sorties tronquées ~10k tokens | [OFF] |
| **Préambules et plans (5.3)** | `phase` est une **métadonnée des items assistant** (`commentary` / `final_answer`), pas une consigne : l'intégration doit la conserver lors du replay de l'historique, sinon les performances se dégradent fortement. Si l'intégration la préserve, des préambules demandés par le prompt sont pris en charge ; sinon, retirer du prompt les demandes de plan initial, de préambules et de statut (risque d'arrêt brusque). Le client Codex gère ce champ lui‑même ; une intégration API maison doit le faire. Plus largement, le guide de raisonnement d'OpenAI demande, pour tout replay sans réponses stockées, de conserver chaque élément de sortie (raisonnement chiffré, phase de l'assistant) dans l'ordre d'origine — la consigne ne se limite donc pas à 5.3 [S-O13]. Distinguer : plan soumis à approbation (plan mode), outil de plan (`update_plan`), récit du plan dans le texte | [DOC]/[OFF] S-O11 |
| **Autonomie** | Agir avec hypothèses raisonnables ; mener de bout en bout (implémentation, tests, explication) ; éviter les boucles de relecture sans progrès ; pour les évaluations, mode non interactif | [OFF] |
| **Compaction** | `/responses/compact` ; réinjecter la liste compactée (`encrypted_content`) | [DOC] |
| **Plans longs** | PLANS.md / plans d'exécution | [OFF] |
| **Config** | `config.toml` : modèle, effort, sandbox, politique d'approbation, profils, MCP | [DOC] |
| **Skills** | `SKILL.md` dans `.agents/skills/` | [DOC] |
| **Erreurs fréquentes listées par OpenAI** | Surcharger le prompt de règles durables au lieu d'AGENTS.md ; ne pas fournir les commandes de test ; sauter la planification sur tâches complexes ; donner l'accès complet avant de comprendre le workflow ; plusieurs threads sur les mêmes fichiers sans worktree ; un thread par projet au lieu d'un par tâche | [OFF] |

## 7. ChatGPT conversationnel

- Mécanismes persistants : instructions personnalisées, mémoire, projets, GPTs.
- Le guide grand public d'OpenAI (2026) privilégie peu de blocs : décrire le résultat voulu, le public, le contexte utile, et n'attacher que les sources qui changent la réponse. [OFF, rapporté par presse spécialisée]
- Les remarques de §5 sur la clarification et la concision s'appliquent quand le modèle sous‑jacent est GPT‑6.x. [HYP]

## 8. Modèles de raisonnement avancé (tous fournisseurs)

- **Ne pas** prescrire le raisonnement ; régler l'effort ; donner objectifs et critères.
- Donner le **contexte** (le raisonnement ne compense pas une information absente).
- Attention à la sur‑réflexion sur tâches simples → baisser l'effort plutôt qu'écrire « réfléchis moins » (sans effet à `medium`+ chez Claude Fable 5.2 [OFF]).
- Préserver le raisonnement entre appels (Responses API ; blocs de thinking inchangés chez Claude).
- Few‑shot : utile pour la forme ; peut contraindre inutilement la méthode. [HYP]

## 9. Modèles légers (Haiku, mini, petits modèles spécialisés)

*« Léger » décrit un coût ou une taille, pas une capacité : régler la structure sur la capacité **observée** sur vos tâches [R-MODEL-003].*

| Différence probable | Ajustement | Preuve |
|---|---|---|
| Moins d'inférence implicite | Instructions plus explicites, exemples | [HYP] cohérent avec pratiques fournisseurs |
| Arrêt précoce plus fréquent | Conditions de fin explicites | [OFF] (Haiku 5.5 : section « arrêt précoce ») |
| Bons en tâches bornées à fort volume | Classification, extraction, sous‑agents `low` | [OFF] |
| Plus sensibles au format | Schémas, structured outputs | [HYP] |

Stratégie : petit modèle + schéma + validation déterministe + escalade vers un grand modèle en cas d'échec de validation (routage par cascade). [HYP, pratique courante]

## 10. Modèles locaux (open weights)

*« Local » décrit un mode de déploiement, pas une capacité : certains modèles locaux ont un raisonnement natif. Les ajustements ci‑dessous dépendent du modèle réel.*

| Particularité | Conséquence | Preuve |
|---|---|---|
| Gabarit de chat spécifique (balises système/utilisateur) | Utiliser le template officiel du modèle ; un mauvais template dégrade fortement | [DOC] (cartes de modèles) |
| Fenêtre effective souvent plus courte que l'annoncée | Contexte minimal, RAG | [EMP] RULER (Hsieh et al. 2024) : longueur effective souvent inférieure à la longueur annoncée |
| Raisonnement natif variable | CoT manuel parfois utile (T‑06) | [EMP] |
| Pas toujours de function calling fiable | Décodage contraint par grammaire (GBNF, JSON schema) | [DOC] |
| Quantification | Peut dégrader suivi d'instructions et long contexte | [EMP] variable |
| Coût marginal ≈ 0, latence matérielle | Self‑consistency et best‑of‑N redeviennent abordables | [HYP] |

## 11. Agents avec terminal / environnement d'exécution (générique)

- Le levier principal est l'**environnement**, pas la formulation : outils, permissions, sandbox, commandes de vérification documentées.
- Démarrage prescrit d'une session : `pwd`, lecture des fichiers d'état, `git log`, test de base. [OFF]
- Interdire de contourner les contrôles (`--no-verify`) et de supprimer des fichiers non reconnus ; confirmer les actions destructives. [OFF]
- Les modèles récents découvrent très bien l'état à partir du système de fichiers : une nouvelle fenêtre avec démarrage prescrit vaut souvent mieux qu'une compaction. [OFF]

## 12. Tableau comparatif des mécanismes persistants

| Besoin | Claude Code | Codex | claude.ai | ChatGPT | API |
|---|---|---|---|---|---|
| Conventions de projet | CLAUDE.md | AGENTS.md | Instructions de projet | Projet / instructions | System / developer |
| Savoir‑faire à la demande | Skills | Skills | Skills | GPTs / projets | Outils + récupération |
| Règle garantie | Hooks, permissions | Sandbox, approbations, config | — (limité) | — (limité) | Code du harnais |
| Isolation de contexte | Sous‑agents | Sous‑agents / threads | — | — | Appels séparés |
| État long | Fichiers, git, `/goal` | PLANS.md, fichiers, compaction | Mémoire | Mémoire | Fichiers / BDD |

## 13. Erreurs transversales fréquentes

1. Porter un prompt « anti‑paresse » d'un ancien modèle vers un modèle récent → sur‑déclenchement.
2. Copier le balayage d'effort d'une version précédente.
3. Corriger par le texte un problème de permissions ou d'outils.
4. Répéter dans le prompt de tâche ce que le harnais ou AGENTS.md dit déjà.
5. Modifier l'historique (cache perdu, raisonnement invalidé, erreurs 400).
6. Croire qu'une recommandation d'un fournisseur vaut pour l'autre.
