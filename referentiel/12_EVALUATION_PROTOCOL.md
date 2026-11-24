# 12 — Protocole d'évaluation des prompts

**Déclaration** : aucune expérience n'a été exécutée pour produire ce référentiel, ni pour sa contre‑expertise. Ce fichier décrit comment en mener. **Le bénéfice du protocole de génération lui‑même (`10`, `14`) n'est pas démontré** : §5.0 décrit comment le mesurer.

## 1. Pourquoi un protocole

- Les sorties sont **stochastiques** : un essai ne prouve rien.
- Les modèles sont **sensibles** à des variations sans changement de sens ([EMP] Sclar et al. 2023).
- L'évaluateur humain est **biaisé** : préférence pour la version qu'il a écrite, pour les réponses longues, pour la dernière vue.
- Les agents **composent** les erreurs : un taux de réussite par étape de 95 % sur 10 étapes donne ~60 % de réussite globale (si indépendance).

## 2. Critères et métriques

| Critère | Métrique opérationnelle | Mesure |
|---|---|---|
| Fidélité à l'intention | % de sorties jugées conformes à l'intention | Juge humain ou LLM calibré, binaire |
| Exactitude | % de faits / résultats corrects | Oracle, référence, vérification de sources |
| Complétude | % des exigences couvertes | Checklist par cas |
| Respect des contraintes | % de cas sans violation | Contrôles déterministes |
| Robustesse aux ambiguïtés | Taux de réussite sur variantes paraphrasées / incomplètes | Jeu de perturbations |
| Capacité d'adaptation | Réussite sur cas hors distribution | Sous‑ensemble dédié |
| Autonomie pertinente | Questions inutiles / cas ; arrêts prématurés ; actions hors périmètre | Analyse des transcripts |
| Reproductibilité | Variance entre essais ; pass^k | k essais par cas |
| Tokens | Entrée, cache, sortie, raisonnement par cas réussi | Objet `usage` |
| Temps | Latence totale par cas | Horodatage |
| Interactions | Tours jusqu'au succès | Transcripts |
| Taux de réussite | pass@1, pass@k, pass^k | Oracle |
| Coût des corrections | Tours et minutes humaines de reprise | Journal |
| Qualité des livrables | Grille par dimension, binaire par critère | Juge calibré + échantillon humain |

**Métrique de synthèse recommandée** : *coût par succès* = coût total (tokens + outils + temps humain valorisé) / nombre de cas réussis. Elle capte l'arbitrage longueur/qualité de `05` §1.

**pass@k vs pass^k** : pass@k = au moins un succès sur k essais (utile si l'on peut sélectionner) ; pass^k = succès sur les k essais (utile pour la fiabilité en production). [OFF] Anthropic, *Demystifying evals*.

## 3. Construire le jeu d'évaluation

1. **Sources des cas** : échecs réels de production, demandes réelles anonymisées, cas limites connus, cas adverses (injection, ambiguïté, données manquantes).
2. **Taille** : commencer à 20‑50 cas réels vaut mieux que zéro ; viser plusieurs centaines pour détecter des écarts de quelques points ([OFF] Anthropic : commencer petit, sur des échecs réels).
3. **Stratification** : par type de tâche, difficulté, longueur de contexte.
4. **Référence** : pour chaque cas, critère de succès explicite (oracle ou rubrique). Pour mesurer une **capacité**, vérifier que chaque cas est résoluble (un humain compétent réussit), sinon il mesure le bruit.
4b. **Cas où réussir, c'est ne pas exécuter** : pour évaluer le système généraliste, inclure des tâches impossibles avec les permissions, informations ou outils disponibles (API indisponible, document manquant, action interdite) et des demandes dont la bonne issue est une clarification, une abstention ou un refus justifié, à côté de demandes réalisables. Coder séparément : résultat métier obtenu, qualité de la gestion du blocage, respect des contraintes, refus justifié. Une fausse réussite n'est jamais un succès. Ne pas mélanger les dénominateurs de capacité et de sécurité.
4c. **Diversité des formulations** : pour quelques intentions, inclure des paraphrases équivalentes (brève/longue, novice/expert, transcription orale/structurée, autre langue si pertinent), en préservant les contraintes. Les stratifier par intention : ce ne sont pas des cas indépendants. Hypothèse à tester, pas d'a priori sur la meilleure forme ([EMP] Sclar et al. : sensibilité au format).
4d. **Données** : jeux d'évaluation anonymisés ou fictifs ; ne pas y conserver de secrets ni de données personnelles réelles [R-SEC-009].
5. **Séparation** : jeu de développement (pour itérer) et jeu de test réservé (pour valider) ; ne jamais itérer sur le jeu de test.
6. **Évaluer le résultat, pas le chemin** : noter l'état final de l'environnement plutôt que la séquence exacte d'appels ([OFF] Anthropic : ne pas sur‑spécifier le chemin ; distinguer transcript et résultat).

## 4. Correcteurs (graders)

| Type | Quand | Précautions |
|---|---|---|
| Déterministe (tests, regex, schéma, comparaison exacte) | Dès que possible | Couvre‑t‑il vraiment le critère ? Tests contournables ? |
| LLM‑as‑judge | Qualité, fidélité, ton | Une dimension par juge ; binaire ou échelle courte ancrée ; option « inconnu » ; permuter l'ordre en comparaison par paires ; modèle juge différent si possible ; **calibrer** sur 50‑100 cas notés par des humains (accord mesuré) |
| Humain | Calibrage, cas critiques, décision finale | En aveugle (versions anonymisées, ordre aléatoire) ; deux évaluateurs sur un échantillon pour mesurer l'accord |

Biais connus des juges LLM [EMP] (Zheng et al. 2023) : position, longueur, auto‑préférence.

## 5. Plan expérimental

### 5.0 Baseline obligatoire : l'intermédiaire apporte‑t‑il quelque chose ? [R-EVAL-004]
Avant de comparer deux formulations entre elles, établir qu'une formulation vaut mieux que **pas de formulation**. Bras minimaux, sur les mêmes cas, la même cible, le même harnais :
- **A** — la demande humaine brute, envoyée directement ;
- **B** — un prompt minimal (T0/T1 écrit en deux minutes) ;
- **C** — le prompt produit par le protocole complet (`10`) ;
- **D** *(facultatif)* — une version allégée de C.

**Ce que mesure cette comparaison** : l'effet du **workflow** complet (reformulation + clarifications + contexte ou recherches ajoutés), pas celui de la seule reformulation. Pour attribuer un effet à la reformulation, ajouter sur un sous‑échantillon un bras **à information égale** (mêmes clarifications et même contexte fournis à A ou B). Réinitialiser l'environnement entre essais ; randomiser ou contrebalancer l'ordre des bras quand le cache, les quotas, l'heure ou l'état de session peuvent varier. Le correcteur reçoit la **demande originale** et les clarifications validées, pas seulement le prompt produit [R-GEN-002] ; sur les cas ambigus ou importants, contrôler le **diff d'intention** : exigences explicites préservées, interdictions conservées, hypothèses et changements de portée signalés.

Mesurer **de la demande initiale au résultat accepté** : tokens et appels du générateur, recherches, clarifications, exécution, validation et temps humain. Stratifier au moins : T0, code, recherche, tâches à risque, modèle local. Hypothèse de départ (non testée) : l'intermédiaire réduit le coût par succès sur les tâches ambiguës ou agentiques et l'augmente sur les T0. Commencer par un pilote de 20‑30 cas pour détecter les problèmes majeurs ; il est **exploratoire et non conclusif**.

### 5.1 Comparer deux formulations (A/B)
0. **Convention** : Δ = variante − référence (un Δ coût négatif est une économie).
1. **Hypothèse écrite** avant l'essai, avec le **critère de décision** : supériorité (« B améliore le taux de réussite ») ou **non‑infériorité** (« B coûte moins sans perdre plus de *m* points »).
2. **Une seule modification** entre A et B (sinon, ablation).
3. **Mêmes conditions** : modèle et version exacts, effort, outils, environnement, ordre des cas.
   - **Technique ou prompt** : une formulation n'est qu'un échantillon des formulations possibles. Pour conclure sur une **technique**, tester au moins deux paraphrases par bras et rapporter l'écart ; la sensibilité au format est forte et corrèle peu d'un modèle à l'autre (R03 §5.3).
4. **Répétitions** : k ≥ 3 essais par cas et par variante. Les répétitions mesurent la variance **intra‑cas** ; elles ne sont **pas** des cas indépendants. L'unité statistique est le cas.
5. **Appariement** : comparer A et B **sur les mêmes cas**.
6. **Aveugle** : correcteurs sans connaissance de la variante.
7. **Statistiques** :
   - Taux binaires appariés (un essai par cas) : test de McNemar ; la puissance dépend du **nombre de paires discordantes**, pas seulement de n.
   - Avec répétitions : bootstrap **par cas** (rééchantillonner les cas, garder leurs k essais ensemble), ou modèle à effets aléatoires par cas.
   - Coût et coût par succès : bootstrap par cas du ratio, intervalle de confiance à 95 %. Rapporter **séparément** taux de succès et coût par tentative.
   - **Coût par succès indéfini** : il l'est à zéro succès, et un rééchantillonnage peut ne contenir aucun succès même si le bras en compte (3 cas dont 1 réussi : probabilité 8/27 ≈ 30 % qu'un rééchantillonnage n'en contienne aucun). Règle pré‑déclarée : ne pas jeter ces rééchantillonnages, ne pas ajouter de pseudo‑succès ; compter la proportion de rééchantillonnages indéfinis ; au‑delà d'un seuil déclaré (par ex. 5 %), la conclusion sur le coût par succès est **non concluante** et la décision s'appuie sur le taux de succès et le coût par tentative.
   - Rapporter **l'intervalle**, pas seulement la moyenne. Comparaisons multiples : correction (Holm) ou moins de variantes.
8. **Décision (multi‑objectifs, pré‑déclarée)** :
   - **Garde‑fous d'abord** : aucune hausse des violations de sécurité ou de contraintes critiques au‑delà d'un seuil pré‑défini (souvent zéro), vérifiée par tests adverses déterministes plutôt que par une note moyenne de juge.
   - **Supériorité** : adopter si la borne inférieure de l'IC de Δ qualité > 0 et si la borne supérieure de l'IC de Δ coût par succès reste sous la marge de coût déclarée (l'incertitude du coût compte aussi).
   - **Non‑infériorité** [R-EVAL-005] : une variante moins chère est **non inférieure en qualité** si la borne inférieure de l'IC de Δ qualité > −*m* (marge pré‑définie par classe de tâche et métrique). Son **gain de coût** g > 0 n'est établi que si la borne supérieure de l'IC de Δ coût par succès (bootstrap par cas, ratio recalculé à chaque rééchantillonnage) est inférieure à −g, g étant un seuil de gain pratique pré‑déclaré (g = 0 à défaut).
   - **Décisions provisoires** : si la qualité est non inférieure et l'estimation de coût favorable mais que son IC contient zéro, ou si l'essai est un pilote exploratoire, la décision est **provisoire**. Elle est acceptable si le changement est réversible et peu coûteux ; elle est étiquetée comme telle dans la fiche (§8), suivie en production sur les mêmes métriques et réévaluée après un nombre de cas fixé d'avance. Un petit gain de coût n'est jamais présenté comme démontré sur cette base.
   - Sinon : rejeter ou approfondir. Un IC qui contient zéro **ne démontre pas** l'absence d'effet : un IC [−12 ; +3] points est compatible avec une perte de 12 points.

### 5.2 Ordre de grandeur d'échantillon [indicatif]
- Le nombre de cas nécessaire dépend des **paires discordantes** (cas où A et B diffèrent) et de la corrélation entre bras. Le calculer à partir d'un pilote plutôt qu'à partir de taux marginaux.
- Ordre de grandeur, à titre d'illustration : détecter un écart de 10 points autour de 70‑80 % demande en général **plusieurs centaines** de cas indépendants ; 5 points, plus d'un millier. Avec 30 cas, seuls des écarts très importants sont détectables. Une marge de non‑infériorité étroite demande encore plus de cas.
- Vérifier le protocole par **simulation** : un test sans effet réel doit conclure à tort au plus au taux d'erreur choisi ; une dégradation de la taille de la marge doit être détectée avec la puissance visée.

### 5.3 Ablation d'un prompt long
Retirer un bloc à la fois. Le test de suppression ligne par ligne (`10` étape 12) **propose** des candidats ; leur retrait d'un prompt de production n'est décidé que par **non‑infériorité** (§5.1 point 8) et sans hausse des violations. Attention aux blocs qui protègent des cas **rares** : ajouter au jeu des cas qui les déclenchent, sinon l'ablation les jugera inutiles à tort.

### 5.4 Balayage de paramètres
Effort (et modèle) en grille, mêmes cas. Tracer taux de réussite vs coût par succès ; choisir le point le moins coûteux non inférieur au meilleur selon la marge pré‑définie, puis **confirmer ce point sur des cas réservés** (le choix sur le même jeu surestime sa performance) ([OFF] Anthropic : refaire ce balayage à chaque version).

## 6. Distinguer amélioration réelle et perçue

| Piège | Symptôme | Parade |
|---|---|---|
| Variance d'échantillonnage | « Meilleur » sur 1‑3 essais | k répétitions, IC |
| Biais de l'auteur | Préférence pour sa version | Aveugle |
| Biais de longueur | Réponses plus longues jugées meilleures | Critères binaires ; contrôler la longueur |
| Sur‑ajustement | Gain sur jeu de dev, pas sur test | Jeu de test réservé |
| Cas non représentatifs | Gain sur exemples choisis | Cas issus de la production |
| Changement de modèle silencieux | Résultats qui dérivent | Épingler la version ; consigner la date |
| Correcteur trompé | Score monte, qualité non | Lire des transcripts ; audits humains réguliers |
| Reward hacking de l'agent | Tests passent, solution invalide | Variantes impossibles des tâches (spécification et tests en conflit, à la manière d'ImpossibleBench) ; tests cachés ; revue des diffs de tests |
| Conscience d'être évalué | Le modèle se comporte mieux (ou autrement) parce qu'il reconnaît un test | Scénarios réalistes ; ne jamais annoncer faussement une observation ou un enjeu ; comparer à des traces de production |
| Grille qui récompense la supposition | Peu d'abstentions, erreurs confiantes | Noter séparément erreurs et abstentions ; une abstention justifiée vaut mieux qu'une erreur |
| Effet de contexte du harnais | Gain dû à un autre changement | Versionner prompt + harnais + config ensemble |

**Règle** : lire régulièrement des transcripts bruts, échecs **et** succès. Les métriques indiquent *où* regarder, les transcripts expliquent *pourquoi*.

## 7. Cycle de vie

1. **Capacité** : « peut‑on le faire ? » — cas difficiles, faible taux attendu.
2. **Régression** : cas réussis qui doivent le rester ; exécutés à chaque changement de prompt, de modèle ou de harnais ([OFF] Anthropic : les évaluations de capacité « deviennent » des évaluations de régression).
3. **Production** : échantillonnage et revue des sorties réelles ; nouveaux échecs ajoutés au jeu.
4. **Au déploiement seulement** : relever le contexte effectif (instructions héritées, mémoire, outils, permissions, limites, compaction, version réelle) et l'associer au prompt déployé ; un prompt évalué en session vierge peut échouer dans une conversation chargée ou reprise. Prévoir un retour arrière simple et un historique minimal — pas de manifeste obligatoire pour chaque prompt.

## 8. Fiche de résultat (gabarit)

```
Hypothèse et critère (supériorité / non‑infériorité, marge m = …) : […]
Variante A / B : [diff exact]
Modèle / version / effort / harnais : […] — Date : […]
Jeu : [nom, n cas, stratification] — Répétitions : k = […] (unité statistique : le cas)
Baseline directe incluse : [oui/non]
Correcteurs : [types, calibrage : accord humain = …]
Résultats (IC 95 %) :
  Taux de réussite : A = … [..,..] ; B = … [..,..] ; Δ = … [..,..]
  Coût par succès : A = … ; B = … ; Δ = …
  Arrêts prématurés / questions inutiles / violations : …
Analyse qualitative (transcripts) : […]
Décision : adopter (étayée) / adopter (provisoire, réévaluation à […] cas) / rejeter / approfondir — Raison : […]
```
