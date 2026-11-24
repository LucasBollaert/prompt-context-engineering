# 05 — Optimisation du contexte et des ressources

## 1. Comptabilité du coût [R-COST-001, R-COST-002]

Deux grandeurs à ne pas mélanger : le **coût réalisé** d'une exécution (mesuré après coup) et le **coût espéré** d'une stratégie (estimé avant de choisir).

### 1.1 Coût réalisé d'une exécution (compteurs non chevauchants)

```
Coût_monétaire = Σ_requêtes [ in_non_caché × p_in + in_écriture_cache × p_w + in_lecture_cache × p_r
                              + out_facturé × p_out ]          # out_facturé inclut en général le raisonnement
               + coût_outils (exécution, recherche, API tierces)
Temps_humain   = rédaction + clarification + vérification + correction     (en minutes)
Coût_total     = Coût_monétaire + Temps_humain × valeur_horaire_explicite
```

Conventions :
- **Ne pas additionner raisonnement et sortie** si le fournisseur facture déjà le raisonnement dans les tokens de sortie (cas général chez Anthropic et OpenAI ; `max_output_tokens` couvre raisonnement et texte visible chez OpenAI). Lire les champs de l'objet `usage` plutôt que reconstruire.
- **Ne pas compter deux fois le cache** : chez OpenAI (GPT‑5.6+), les tarifs d'écriture et de lecture sont des tarifs **totaux** — chaque token est facturé à un seul tarif [DOC, S-O10].
- **Prix versionnés** : noter le modèle, la date et le TTL du cache ; utiliser le **taux de hit observé**, pas le taux supposé.
- **Valoriser le temps humain explicitement** (valeur horaire déclarée) et rapporter aussi les composantes brutes (tokens, minutes), car la valorisation est discutable.
- **Coût par succès** = Coût_total cumulé / nombre de résultats acceptés (indéfini si aucun succès : le rapporter tel quel).
- **Quotas d'abonnement** : à mesurer séparément (§14) ; ne pas les convertir en prix par token.

### 1.2 Coût espéré d'une stratégie (avant exécution)

```
E[Coût_total] ≈ coût_d'une_tentative + P(échec) × E[coût_de_reprise] + coût_de_génération_du_prompt
```

Le dernier terme est souvent oublié : un intermédiaire qui reformule la demande (`10`, `14`) coûte au moins un appel et parfois une clarification. Son gain n'est **pas démontré** ; il se mesure contre une baseline directe (`12` §5.0).

### 1.3 Conséquences (sous hypothèses)
1. **Le contexte est retraité à chaque tour** tant qu'il reste dans l'historique : à plein tarif sans cache, au tarif lecture si le préfixe est stable et le cache actif, et plus du tout après compaction ou réinitialisation.
2. **La probabilité d'échec peut dominer.** Exemple illustratif, à recalculer avec vos prix : si une reprise coûte nettement plus que 500 tokens d'entrée (cas typique dès qu'elle implique un humain), un ajout de 500 tokens qui fait passer la réussite de 60 % à 85 % est rentable. Ce n'est pas vrai si la reprise est automatique et bon marché.
3. **Le temps humain est le coût caché.** Une question coûte un aller‑retour humain ; une mauvaise hypothèse coûte une reprise.

## 2. Longueur optimale selon la tâche

Aucune longueur « optimale » universelle n'est démontrée. Les ordres de grandeur ci‑dessous sont des **heuristiques** [HYP] cohérentes avec les recommandations officielles.

| Type de tâche | Prompt de tâche typique | Ce qui doit y être |
|---|---|---|
| Question simple | 1‑3 phrases | La question + contrainte de format si nécessaire |
| Transformation bornée (traduire, reformuler, extraire) | 3‑10 lignes + données | Objectif, public, format, exemples si format rare |
| Tâche de code ciblée | 3‑15 lignes | Fichiers, symptôme, critère « corrigé », commande de test |
| Fonctionnalité multi‑fichiers | 15‑60 lignes ou une SPEC.md | Objectif, périmètre, invariants, critères, vérification de bout en bout |
| Exécution autonome longue | Spec + contrat d'autonomie + état | Conditions d'arrêt, permissions, état persistant, rapport |
| System prompt de produit | Variable ; chaque ligne justifiée | Comportements non par défaut uniquement |

### Quand un prompt détaillé est préférable
- Le modèle **ne peut pas** deviner l'information (préférences, contexte métier, contraintes cachées).
- L'erreur est coûteuse ou irréversible.
- La tâche sera **répétée** (production) : le coût de rédaction est amorti.
- Modèle léger ou local.
- Travail non supervisé : pas de correction en cours de route possible.

### Quand un prompt court sur un modèle performant fait mieux
- Tâche exploratoire où l'on veut voir l'interprétation du modèle ([OFF] Claude Code : un prompt vague peut faire émerger ce qu'on n'aurait pas pensé à demander).
- Le modèle a accès aux informations (code, docs) et sait les chercher : lui dire **où**, pas **quoi**.
- La méthode prescrite serait moins bonne que la sienne.
- Correction rapide et réversible.

## 3. Densité informationnelle

- **Une idée par phrase**, vocabulaire constant (même mot pour la même chose).
- Préférer les **identifiants légers** (chemins, noms de symboles, requêtes) au contenu intégral : le modèle charge à la demande ([OFF] Anthropic, récupération juste‑à‑temps).
- Supprimer : politesse, généralités (« écris du code propre »), conventions que le modèle connaît, descriptions de ce qu'il peut lire.
- Garder : raisons, exceptions, pièges non évidents.

## 4. Redondance : utile ou inutile

| Redondance | Verdict | Justification |
|---|---|---|
| Répéter une règle critique en fin de contexte très long | Utile | Effet de récence ; [OFF] question à la fin des longs documents |
| Réinjecter une consigne de format toutes les 3‑5 interventions dans une longue conversation | Utile | [OFF] OpenAI (Markdown) |
| Répéter la même règle 3 fois dans un system prompt court | Inutile/nuisible | Sur‑pondération → sur‑application |
| Dupliquer dans le prompt de tâche ce qui est dans CLAUDE.md / AGENTS.md | Inutile | Déjà en contexte ; risque de divergence |
| Exemples qui illustrent la même chose | Inutile | Sur‑imitation sans gain d'information |
| Critères d'acceptation + test qui les vérifie | Utile | Le texte guide, le test garantit |

## 5. Dilution, position, saturation

- **Dégradation avec la longueur** : [EMP] Chroma 2025 (18 modèles, tâche constante, longueur variable) — performance de moins en moins fiable ; distracteurs sémantiquement proches particulièrement nocifs. [EMP] NoLiMa (2025) : chute marquée quand la récupération ne peut pas s'appuyer sur des correspondances littérales. [EMP] RULER (2024) : longueur effective < longueur annoncée.
- **Position** : [EMP] *Lost in the Middle* (2023) — courbe en U (début et fin mieux exploités). Les modèles récents sont plus robustes, mais la recommandation officielle reste : documents en haut, question à la fin. [OFF]
- **Saturation agentique** : [OFF] Claude Code — quand la fenêtre se remplit, le modèle « oublie » des instructions et commet plus d'erreurs. Indicateurs : règles de CLAUDE.md ignorées, questions déjà répondues, retours à des approches abandonnées.

## 6. Sélection dynamique du contexte

Ordre de préférence :
1. **Ne rien charger** si le modèle peut chercher lui‑même (outils de recherche, `grep`, MCP).
2. **Pointeurs** (chemins, URLs, IDs) + consigne de lire au besoin.
3. **Chargement progressif** : skills (description toujours chargée, contenu à la demande).
4. **Récupération sémantique** (RAG) pour gros corpus non structurés.
5. **Injection complète** seulement si tout le document sert.

Outils : peu nombreux, non ambigus, réponses concises, pagination/filtrage par défaut ([OFF] Anthropic, *Writing tools for agents* ; [OFF] Codex : tronquer ~10k tokens en gardant début et fin). Ne tronquer que si le contenu intégral reste accessible (pagination, fichier, relecture ciblée) : sinon la troncature peut supprimer la seule preuve utile.

## 7. Compression du contexte

| Technique | Quand | Risque | Mitigation |
|---|---|---|---|
| **`/clear` + nouveau prompt** | Tâches non liées ; après deux corrections ratées | Perte d'apprentissages | Incorporer ce qui a été appris dans le nouveau prompt |
| **Compaction** (auto, `/compact <focus>`, `/responses/compact`) | Même tâche, contexte plein | Oubli de contraintes | Instruire ce qu'il faut préserver (fichiers modifiés, commandes de test, décisions) |
| **Résumé partiel** (`/rewind` → résumer depuis/jusqu'à) | Une partie de l'historique est du bruit | — | — |
| **Effacement des vieux résultats d'outils** | Agents longs | Re‑lecture nécessaire | Garder les identifiants (chemins) |
| **Notes externes** (progress.txt, tests.json, git) | Multi‑sessions | Notes périmées | Purge régulière |
| **Nouvelle fenêtre + démarrage prescrit** | Long horizon | — | [OFF] Anthropic : souvent préférable à la compaction |
| **Sous‑agents** | Exploration lourde | Résumé incomplet | Format de retour imposé, chemins et preuves |

## 8. Documents volumineux

1. Se demander si le document doit être **lu entièrement** ou **interrogé**.
2. Si interrogé : outils de recherche ou RAG ; sinon découpage avec chevauchement et synthèse hiérarchique (map‑reduce).
3. Si lu entièrement : en tête de prompt, balisé avec source et métadonnées, question à la fin, citer avant de répondre.
4. Préférer les formats texte extraits (Markdown) aux binaires quand la mise en page n'importe pas ; garder le PDF quand tableaux ou figures portent le sens. [HYP]
5. Plusieurs documents : `<documents><document index="n"><source>…</source><document_content>…</document_content></document></documents>`. [OFF]

## 9. Réutilisation du contexte et prompt caching

### 9.1 Faits (Anthropic) [DOC]
- Le cache porte sur le **préfixe complet** : outils, puis system, puis messages, jusqu'au point de cache.
- Écriture 5 minutes : 1,25× le prix d'entrée ; écriture 1 heure : 2× ; lecture : 0,1× (multiplicateur inférieur indiqué pour Claude Fable sur la page de prix).
- Rentabilité : dès **une** lecture pour le cache 5 min, **deux** lectures pour le cache 1 h.
- Les multiplicateurs se cumulent avec la remise Batch et la résidence des données.
- Cache automatique disponible en plus des points de cache explicites.
- Sur Fable 5.2, changer l'effort en cours de conversation via l'effort par message (bêta) préserve le cache.

### 9.2 Faits (OpenAI) [DOC, S-O10, vérifié nov. 2026]
- Cache par préfixe, activé par défaut sur les modèles compatibles ; tout le préfixe rendu doit correspondre.
- **GPT‑5.6 et ultérieurs** : écritures **payantes** — 1,25× le tarif d'entrée pour un TTL de 30 min (défaut), 2,5× pour 12 h (Responses API uniquement) ; ce sont des tarifs totaux, pas une surcharge. Lectures à 0,1× sur la plupart des modèles, 0,05× sur GPT‑6.2 Astra, GPT‑6.2 Sol, GPT‑6.1 Sol et GPT‑6.1 Terra. Seuil minimal : 1 024 tokens d'entrée visibles. Breakpoints implicites (défaut) ou explicites (`prompt_cache_options.mode`, jusqu'à quatre écritures par requête ; pas de breakpoint sur `instructions`).
- **Modèles antérieurs** : pas de frais d'écriture ; rétention `in_memory` ou `24h` ; breakpoints implicites seulement.
- Exemple officiel (30 min, lecture 0,1×) : une écriture + une lecture = 1,35× le coût sans cache pour deux requêtes (contre 2×) ; une écriture + neuf lectures = 2,15× (contre 10×). Une écriture jamais relue coûte **plus** que sans cache.
- Instructions stables en tête (message `developer`) ; modifier l'historique peut faire perdre les éléments de raisonnement.

### 9.3 Règles de conception
- **Stable en haut, variable en bas** : outils et instructions permanentes figés ; date, nom d'utilisateur, données de la requête en fin.
- **Ne pas** insérer d'horodatage ou d'identifiant variable dans le system prompt.
- **Ne pas** réordonner les outils entre requêtes.
- Grouper les requêtes qui partagent un préfixe dans la fenêtre de validité.
- Mesurer : `cache_read_input_tokens` / `cache_creation_input_tokens` dans l'objet `usage`.

## 10. Instructions permanentes vs temporaires

| Permanentes | Temporaires |
|---|---|
| Conventions, commandes, architecture, politique d'autonomie, sécurité | Tâche, données, critères spécifiques, état courant |
| CLAUDE.md, AGENTS.md, system prompt, skills | Message de tâche, fichiers d'état, issue |
| Changent rarement ; revues comme du code | Jetables |
| Cacheables | Non cacheables (en fin de préfixe) |

Un contenu temporaire placé dans un fichier permanent devient une règle fantôme ; c'est la source principale de « prudence cumulée » ([OFF] Fable 5.2).

## 11. Transmission entre agents

- **Brief descendant** (orchestrateur → sous‑agent) : objectif, ce qui est déjà connu, périmètre, outils à utiliser, format et taille de retour, critère d'arrêt. [OFF] Anthropic : un brief vague provoque duplication et lacunes.
- **Retour ascendant** : résumé condensé (Anthropic indique typiquement 1 000 à 2 000 tokens pour un sous‑agent qui a exploré beaucoup plus [OFF, *Effective context engineering*]), avec **preuves** (chemins, lignes, URLs, sorties de commandes).
- **Artefacts plutôt que messages** : écrire les résultats volumineux dans des fichiers et transmettre le chemin (évite le « téléphone arabe ») [OFF] Anthropic (système de recherche) — **si** l'orchestrateur peut lire cet espace (fichiers partagés, permissions, durée de vie). Sinon : résumé + références vérifiables. Pour une donnée courte, le retour en texte est préférable.
- **Coût** : les sous‑agents peuvent représenter une grande part du coût d'une session ; vérifier leur modèle par défaut ; une description d'outil de délégation explicitant ce coût a environ divisé par deux le nombre de sous‑agents lancés (test Anthropic, Fable 5.2). [EMP fournisseur]

## 12. Coût des validations et relectures

| Validation | Coût | Valeur | Recommandation |
|---|---|---|---|
| Test / build / linter | Faible (exécution) | Très élevée | Toujours quand disponible |
| Contrôle déterministe (schéma, regex, présence de citation) | Très faible | Élevée pour la forme | Toujours pour sorties machine |
| Auto‑vérification par critères | Faible à moyen | Moyenne, faible sans signal externe | Si pas d'oracle ; éviter sur modèles qui vérifient déjà |
| Relecteur à contexte frais | Moyen | Élevée pour travail long | Travail autonome ou à fort enjeu |
| Multiples relecteurs / vote | Élevé | Décroissante | Rarement justifié |
| Humain | Le plus cher | Indispensable pour l'irréversible | Concentrer sur les décisions, pas la forme |

Règle : une validation n'est rentable que si P(détecte une erreur) × coût_de_l'erreur > coût_de_la_validation.

## 13. Nombre d'interactions et coût réel de la clarification

- **Coût d'une question** = latence humaine + interruption + tour supplémentaire (relecture du contexte). En exécution non supervisée, une question **bloque tout**.
- **Coût d'une mauvaise hypothèse** = travail perdu × P(hypothèse fausse) + coût de détection.
- **Règle de décision** : questionner si P(hypothèse fausse) × coût_reprise > coût_question **et** qu'aucune hypothèse sûre (réversible, documentée) n'existe.
- **Questions groupées** : une seule fois, toutes les questions bloquantes, avec options et valeurs par défaut.
- **Questions asynchrones** : poser et continuer le travail indépendant ([OFF] OpenAI GPT‑6.2, Anthropic Fable 5.2).
- **Relances précises** : « Oui, lance la migration sur staging » plutôt que « go » ([OFF] Fable 5.2).

## 14. Quotas d'abonnement vs facturation API

| Dimension | Abonnement (claude.ai, ChatGPT, Claude Code / Codex inclus dans un plan) | API |
|---|---|---|
| Unité | Quota d'usage sur fenêtres de temps (limites de messages / de calcul selon le plan) | Prix par token (entrée, sortie, cache), remise Batch (≈ 50 % chez les deux fournisseurs [DOC]) |
| Ce qui consomme | Longueur de conversation, taille des fichiers, effort / modèle choisi, sous‑agents | Idem, facturé à l'unité |
| Levier principal | Conversations courtes et ciblées ; `/clear` ; modèle adapté ; éviter les sous‑agents inutiles | Cache, batch, routage de modèle, effort, troncature des outils |
| Visibilité | Faible (indicateurs d'usage) | Totale (`usage`) |
| Cache | Géré par le produit, opaque | Contrôlable |

Les montants et limites exacts des plans changent fréquemment : consulter la page de support du fournisseur à la date d'usage. [DOC, volatil]

## 15. Check‑list de réduction de coût (ordre d'impact typique)

1. Bon modèle et bon effort (le plus gros levier ; ne pas surpayer les tâches simples).
2. Oracle de vérification (réduit les tours de correction).
3. Contexte minimal + pointeurs + skills.
4. Préfixe stable et cache.
5. `/clear` entre tâches ; nouvelle session plutôt que corrections empilées.
6. Sous‑agents seulement pour exploration parallèle et lourde.
7. Sorties d'outils tronquées et filtrées.
8. Batch pour le non‑interactif.
9. Retirer les budgets de tokens affichés et les consignes héritées inutiles.
