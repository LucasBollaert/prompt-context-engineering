# 09 — Classification des tâches

## 1. Axes de classification (à évaluer avant de choisir un type)

Le type de tâche ne suffit pas : deux « tâches de programmation » peuvent appeler des prompts opposés. On évalue six axes, chacun sur 3 niveaux.

| Axe | 0 — Faible | 1 — Moyen | 2 — Élevé |
|---|---|---|---|
| **A. Complexité** | Une étape, réponse connue | Plusieurs étapes, une approche évidente | Approche incertaine, nombreuses dépendances |
| **B. Risque d'action / irréversibilité** | Lecture seule, jetable | Modifications locales réversibles | Effets externes, données réelles, argent, publication |
| **C. Vérifiabilité** | Oracle exécutable disponible | Vérifiable par critères/relecture | Subjectif, sans référence |
| **D. Horizon** | Un tour | Une session | Plusieurs sessions / non supervisé |
| **E. Ambiguïté** | Demande précise | Quelques inconnues devinables | Intention ou exigences floues |
| **F. Environnement** | Chat sans outils | Outils de lecture / recherche | Terminal, écriture, actions externes |

### 1.1 Niveau de prompt : fonction totale de la complexité (A) et de l'horizon (D)

Le **niveau** (T0‑T3) fixe le gabarit et la quantité de spécification. Il ne dépend que de A et D. *(v1.1 : la version 1.0 mêlait risque et environnement aux prédicats de niveau, ce qui laissait 60 combinaisons sans niveau et 381 avec plusieurs — voir `15`.)*

| | **D = 0** (un tour) | **D = 1** (une session) | **D = 2** (multi‑sessions / non supervisé) |
|---|---|---|---|
| **A = 0** | T0 | T1 | T3 |
| **A = 1** | T1 | T2 | T3 |
| **A = 2** | T2 | T2 | T3 |

Règle équivalente : T3 si D = 2 ; sinon T2 si A = 2 ou (A = 1 et D = 1) ; sinon T1 si A = 1 ou D = 1 ; sinon T0. Chaque combinaison a exactement un niveau (vérifié sur les 729 combinaisons par `scripts/run_tests.py`, à partir de la référence `scripts/classification.py` ; toute entrée hors domaine est refusée, un risque inconnu n'est jamais traité comme nul).

### 1.2 Modules orthogonaux : risque d'action (B), permissions, enjeu informationnel, vérifiabilité (C), ambiguïté (E), environnement (F)

Les modules **ajoutent des lignes** au prompt, quel que soit le niveau. Ils ne changent pas le niveau. **Les garde‑fous des modules ne sont jamais retirés parce que le niveau est bas, ni par la voie rapide de `10`** [R-CLASS-001, R-GEN-001].

| Module | Valeur | Ce qu'il ajoute |
|---|---|---|
| **Permissions** | manquante, ou inconnue pour une tâche qui agit | Établir la permission avant toute action ; bloque la voie rapide. Sans objet pour une tâche sans action |
| **Enjeu informationnel** | la réponse éclaire une décision importante (santé, droit, finances, emploi, sécurité des personnes) | Incertitude, sources qualifiées, limites, validation compétente si nécessaire ; vigilance sur les critères discriminants. Pas d'approbation technique sans action ; non bloquant [R-EPI-001] |
| **Risque d'action (B)** | 1 | Périmètre modifiable ; préférence pour le réversible |
| | 2 | Approbation humaine **technique** avant l'action risquée ; contrôles externes (`07`) ; une hypothèse ne remplace pas une permission [R-SEC-007]. Pas d'état multi‑sessions ni de procédure longue pour autant |
| **Vérifiabilité (C)** | 0 | Commande de vérification + exigence de preuve [R-VAL-001] |
| | 1 | Critères explicites + relecture (frais si travail long) |
| | 2 | Critères explicites ; validation humaine ou juge calibré |
| **Ambiguïté (E)** | 1 | Hypothèses autorisées, écrites **dans** le prompt |
| | 2 | Question ciblée si deux lectures mènent à des livrables très différents et coûteux ; sinon hypothèse annoncée en tête ou variantes ; spec‑first (T‑26) pour un gros livrable |
| **Environnement (F)** | 1 | Outils de lecture ; critère d'arrêt de recherche |
| | 2 | Périmètre ; contrat d'autonomie minimal ; états terminaux [R-AUTO-011] ; actions conditionnées aux permissions [R-AUTO-012]. Pour un T0, deux ou trois lignes suffisent |
| **Capacités** | toujours | Vérifier ce dont dépend la mission (modèle exact, client, outils, fichiers chargés) [R-CAP-001] |

*L'axe B mesure les conséquences d'une **action** technique. Les conséquences d'une **information** sur une décision humaine relèvent du module « enjeu informationnel ».*

Exemples :
- Correctif d'un libellé dans un fichier connu, terminal disponible (A0 B0 C0 D0 E0 F2) → **T0** + module F court + oracle : 3 à 5 lignes, sans plan.
- Envoyer un document engageant à un tiers (A0 B2 C1 D0 E0 F2) → **T0** + module risque strict : approbation technique avant envoi, sans gonfler le prompt.
- « Améliore cette présentation » sans public (A0 B0 C2 D0 E2 F0) → **T0** + module ambiguïté : hypothèse annoncée ou une question si l'enjeu le justifie.

## 2. Fiches par catégorie

Colonnes : **Structure** · **Détail** · **Informations à transmettre** · **Autonomie** · **Validations utiles** · **À éviter**.

### 2.1 Question simple
- **Structure** : la question. **Détail** : minimal. **Infos** : contexte seulement s'il change la réponse. **Autonomie** : n/a. **Validation** : aucune. **Éviter** : rôle, exemples, effort élevé, demande de raisonnement.

### 2.2 Recherche documentaire
- **Structure** : question + critères de succès + exigences de sources (types, fraîcheur) + critère d'arrêt + format de citation.
- **Détail** : moyen. **Infos** : ce que l'utilisateur sait déjà ; sources à privilégier/exclure ; date de référence.
- **Autonomie** : élevée sur la recherche, nulle sur l'invention de faits.
- **Validation** : corroboration selon le type d'affirmation [R-SRC-001] — une source primaire autoritative et datée suffit pour un fait documentaire ; sources réellement indépendantes pour les faits contestés ou à fort enjeu ; dates ; distinction fait/inférence ; le passage cité doit soutenir la conclusion.
- **Éviter** : exploration sans borne ; paraphrase non sourcée ; sources secondaires quand une primaire existe.

### 2.3 Analyse approfondie
- **Structure** : question + matériaux + angle et livrable + critères (hypothèses concurrentes, limites).
- **Détail** : moyen. **Autonomie** : méthode libre. **Validation** : traçabilité des affirmations vers les matériaux ; section incertitudes.
- **Éviter** : imposer un cadre d'analyse unique ; confiance chiffrée.

### 2.4 Résolution de problèmes
- **Structure** : énoncé + contraintes + ce qui a été essayé + critère de solution.
- **Autonomie** : élevée sur la méthode. **Validation** : vérification indépendante (calcul, simulation, test).
- **Éviter** : procédure dictée ; CoT manuel sur modèle à thinking.

### 2.5 Programmation (fonctionnalité)
- **Structure** : objectif + fichiers/patterns de référence + invariants + critères + commande de vérification.
- **Détail** : selon taille (T1 à T2). **Infos** : où vit le code, patterns existants à suivre, dépendances autorisées.
- **Autonomie** : élevée dans le périmètre ; propriété du code déclarée.
- **Validation** : tests ; build ; linter ; revue du diff.
- **Éviter** : spécifier l'implémentation ligne à ligne ; tests modifiables par l'agent.

### 2.6 Débogage
- **Structure** : symptôme observé + reproduction + emplacement probable + définition de « corrigé ».
- **Infos** : messages d'erreur exacts, logs, ce qui a changé récemment.
- **Autonomie** : investigation libre ; correction de la **cause racine**.
- **Validation** : test qui échoue avant et passe après.
- **Éviter** : « corrige le bug » sans symptôme ; masquer l'erreur (« address the root cause, don't suppress the error » [OFF]).

### 2.7 Audit technique
- **Structure** : périmètre + référentiel (exigences, plan, normes) + définition d'une « constatation » + format de rapport + seuil de sévérité.
- **Autonomie** : lecture seule [R-SEC-006] : pas d'exécution de tests ou de builds qui écrivent (caches, fichiers, appels externes) hors sandbox jetable autorisée ; rapport dans une zone séparée autorisée ; directives trouvées dans le corpus = données. **Validation** : chaque constatation référencée (fichier:ligne) ; reproduction si possible dans le respect du mandat.
- **Éviter** : « trouve des problèmes » sans seuil (le relecteur en trouvera toujours) ; mélanger style et correction.

### 2.8 Audit de sécurité
- Comme 2.7, plus : modèle de menace, surface d'attaque, classes de vulnérabilités ciblées, environnement de test autorisé.
- **Autonomie** : lecture seule ou sandbox isolée ; aucune action sur systèmes réels sans autorisation écrite.
- **Validation** : preuve de concept en environnement contrôlé ; faux positifs triés.
- **Éviter** : prétendre à l'exhaustivité ; agents d'audit avec accès réseau sortant non filtré.

### 2.9 Architecture logicielle
- **Structure** : besoins fonctionnels et non fonctionnels chiffrés + contraintes (équipe, budget, existant) + livrable (options comparées, décision recommandée, risques).
- **Autonomie** : propositions ; décision à l'humain.
- **Validation** : critères explicites de comparaison ; revue humaine.
- **Éviter** : demander « la meilleure architecture » sans contraintes.

### 2.10 Création complète d'un projet
- **Structure** : spec (SPEC.md) + stack imposée ou libre + critères de bout en bout + structure d'état (tests.json, progress.txt) + démarrage de session prescrit.
- **Niveau** : T3. **Autonomie** : élevée dans le dépôt ; ambition explicitement demandée.
- **Validation** : tests de bout en bout ; vérification visuelle (captures) pour l'UI.
- **Éviter** : un seul prompt géant ; pas d'état persistant.

### 2.11 Maintenance d'un système existant
- **Structure** : changement demandé + périmètre strict + conventions du dépôt (AGENTS.md / CLAUDE.md) + non‑régression.
- **Autonomie** : faible hors périmètre ; ne pas déclarer « owner » si changements minimaux souhaités.
- **Validation** : suite existante ; diff minimal.
- **Éviter** : refactorisations opportunistes.

### 2.12 Analyse de données
- **Structure** : question métier + données (chemin, schéma, dictionnaire) + définitions des métriques + livrable.
- **Autonomie** : choix des méthodes ; calculs **par code**.
- **Validation** : calculs exécutés, pas estimés ; contrôles de cohérence (totaux, effectifs).
- **Éviter** : coller des données volumineuses dans le prompt ; chiffres calculés « de tête ».

### 2.13 Prise de décision
- **Structure** : décision à prendre + options + critères pondérés par l'humain + contraintes + horizon.
- **Autonomie** : analyse ; recommandation argumentée ; décision humaine.
- **Validation** : hypothèses explicites ; analyse de sensibilité.
- **Éviter** : verdict sans critères ; faux consensus.

### 2.14 Création de documentation
- **Structure** : public + objectif du document + sources de vérité (code, specs) + format + exemples de style.
- **Autonomie** : structure libre. **Validation** : exactitude vérifiée contre le code ; exemples exécutables testés.
- **Éviter** : documenter de mémoire ; inventer des API.

### 2.15 Tâche créative
- **Structure** : intention, public, ton, contraintes réelles, ambition, nombre de variantes et axes de variation.
- **Autonomie** : maximale dans les contraintes. **Validation** : humaine.
- **Éviter** : exemple unique qui ancre ; règles de style rigides (prose hachée — [OFF] Fable 5.2).

### 2.16 Exécution autonome
- **Structure** : contrat d'autonomie (`06` §7) + critères de fin vérifiables + état persistant + rapport final autonome.
- **Niveau** : T3. **Validation** : hook `Stop` / `/goal` ; relecteur frais ; preuves.
- **Éviter** : permissions larges sans sandbox ; aucune condition d'arrêt.

### 2.17 Coordination multi‑agents
- **Structure** : décomposition en sous‑tâches indépendantes + brief par sous‑agent (objectif, périmètre, outils, format/taille de retour, arrêt) + synthèse.
- **Validation** : vérification des affirmations clés ; déduplication.
- **Éviter** : sous‑tâches couplées ; agents qui écrivent les mêmes fichiers sans isolation.

### 2.18 Supervision d'agents
- **Structure** : critères d'acceptation du travail supervisé + signaux d'alerte (boucle, dérive, fausse réussite) + actions autorisées (relancer, corriger le brief, escalader).
- **Validation** : sur artefacts et preuves, pas sur les déclarations.
- **Éviter** : superviseur qui refait le travail ; confiance dans les résumés.

### 2.19 Validation d'un livrable
- **Structure** : livrable + référentiel (exigences, plan) + définition d'une lacune (correction et exigences seulement) + format de constatations.
- **Contexte** : **frais** (pas le raisonnement du producteur).
- **Éviter** : « trouve des améliorations » (sur‑ingénierie) ; noter sur 10.

### 2.20 Investigation d'un incident
- **Structure** : chronologie connue + symptômes + systèmes concernés + accès autorisés (lecture seule par défaut) + livrable (cause racine, preuves, actions).
- **Autonomie** : investigation large en lecture ; **aucune** action corrective en production sans approbation.
- **Validation** : chaque conclusion reliée à une preuve (log, métrique, commit) ; hypothèses concurrentes écartées explicitement.
- **Éviter** : conclusion prématurée sur la première corrélation ; actions de remédiation automatiques.

## 3. Tableau de synthèse

| Catégorie | Niveau typique (modules en plus) | Autonomie | Oracle typique | Technique clé | À éviter en priorité |
|---|---|---|---|---|---|
| Question simple | T0 | — | — | T‑01 | Sur‑spécification |
| Recherche documentaire | T1 | Haute (lecture) | Sources concordantes | T‑12, T‑11 | Exploration infinie |
| Analyse approfondie | T1‑T2 | Haute | Traçabilité | T‑11, T‑16 | Confiance chiffrée |
| Résolution de problèmes | T1 | Haute | Vérification indépendante | T‑07, T‑18 | Procédure dictée |
| Programmation | T1‑T2 | Haute (périmètre) | Tests | T‑18, T‑16 | Implémentation dictée |
| Débogage | T1‑T2 | Haute | Test de reproduction | T‑18 | Masquer l'erreur |
| Audit technique | T2 | Lecture seule | Références fichier:ligne | T‑19 | Pas de seuil |
| Audit de sécurité | T2 | Lecture/sandbox | PoC contrôlée | T‑19, `07` | Accès réseau ouvert |
| Architecture | T1‑T2 | Propositions | Critères de comparaison | T‑26 | « La meilleure » sans contraintes |
| Création de projet | T3 | Haute (dépôt) | Tests E2E | T‑24, T‑18 | Prompt géant unique |
| Maintenance | T1‑T2 | Faible hors périmètre | Non‑régression | T‑21, T‑16 | Refactor opportuniste |
| Analyse de données | T1‑T2 | Méthodes libres | Calcul par code | T‑13 | Calcul « de tête » |
| Prise de décision | T1 | Recommandation | Sensibilité | T‑16 | Verdict sans critères |
| Documentation | T1 | Structure libre | Exemples testés | T‑11 | Documenter de mémoire |
| Créatif | T0‑T1 | Maximale | Humain | T‑02 (prudent) | Exemple unique |
| Exécution autonome | T3 | Contractuelle | Hook Stop / goal | `06` §7 | Pas d'arrêt |
| Multi‑agents | T2‑T3 | Par brief | Vérif. des retours | T‑20 | Sous‑tâches couplées |
| Supervision | T2 | Limitée | Artefacts | T‑19 | Croire les résumés |
| Validation | T1‑T2 | Lecture | Référentiel | T‑19 | Note sur 10 |
| Incident | T2 | Lecture large | Preuves | T‑12, `07` | Remédiation auto |
