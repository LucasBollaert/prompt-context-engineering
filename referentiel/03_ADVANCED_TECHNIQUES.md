# 03 — Techniques avancées

Chaque fiche suit le même plan en 10 points : **Fonctionnement · Objectif réel · Conditions · Bénéfices démontrés · Limites · Coût · Risques · Pertinence moderne · À éviter quand · Exemple.**

Pertinence moderne : ★★★ = levier majeur aujourd'hui ; ★★ = utile en contexte ; ★ = marginal ; ⊘ = obsolète ou nuisible sur les modèles récents.

Ne pas lire cette liste comme un menu à combiner : la plupart des tâches n'ont besoin que de T‑01, T‑10 et d'un oracle (T‑18).

## Index

| # | Technique | ★ | # | Technique | ★ |
|---|---|---|---|---|---|
| T‑01 | Zero‑shot bien spécifié | ★★★ | T‑16 | Contraintes déclaratives et invariants | ★★★ |
| T‑02 | Few‑shot / exemples | ★★ | T‑17 | Structured outputs (schéma) | ★★★ |
| T‑03 | Décomposition | ★★ | T‑18 | Validation par tests / oracles | ★★★ |
| T‑04 | Planification avant exécution | ★★ | T‑19 | Audit indépendant (relecteur frais) | ★★★ |
| T‑05 | Rôle / persona | ★ | T‑20 | Délégation et orchestration multi‑agents | ★★ |
| T‑06 | Chain‑of‑thought manuel | ⊘/★ | T‑21 | Instructions persistantes (CLAUDE.md, AGENTS.md) | ★★★ |
| T‑07 | Raisonnement natif et réglage d'effort | ★★★ | T‑22 | Skills / chargement progressif | ★★★ |
| T‑08 | Self‑consistency / vote | ★ | T‑23 | Hooks et contrôles déterministes | ★★★ |
| T‑09 | Self‑critique / auto‑vérification | ★★ | T‑24 | Mémoire externe et notes structurées | ★★ |
| T‑10 | Explication des raisons (motivation) | ★★★ | T‑25 | Compaction et nettoyage de contexte | ★★ |
| T‑11 | Citer avant de répondre (ancrage) | ★★ | T‑26 | Spec‑first / interview | ★★ |
| T‑12 | Recherche et vérification multi‑sources | ★★ | T‑27 | Metaprompting / optimisation de prompt | ★★ |
| T‑13 | Tool use, function calling, conception d'outils | ★★★ | T‑28 | LLM‑as‑judge | ★★ |
| T‑14 | ReAct (et boucle agentique native) | ★ (pattern) | T‑29 | Best‑of‑N avec vérificateur | ★★ |
| T‑15 | RAG et récupération juste‑à‑temps | ★★ | T‑30 | Checkpoints / retour arrière | ★★ |
| T‑15b | Prompt chaining | ★★ | | | |

---

### T‑01 — Zero‑shot bien spécifié
1. **Fonctionnement** : une instruction sans exemple, contenant objectif, contexte nécessaire, critères et format.
2. **Objectif** : obtenir le résultat avec le minimum de tokens et de biais.
3. **Conditions** : modèle capable ; tâche descriptible en mots.
4. **Bénéfices** : [OFF] tous les fournisseurs en font le point de départ ; « golden rule » Anthropic : un collègue peu informé doit comprendre le prompt.
5. **Limites** : style ou format très particulier difficile à décrire.
6. **Coût** : minimal.
7. **Risques** : sous‑spécification (le modèle littéral fait le minimum).
8. **Pertinence** : ★★★.
9. **Éviter** : quand le format attendu est plus facile à montrer qu'à décrire.
10. **Exemple** : « Réécris cette fonction pour qu'elle soit O(n) au lieu de O(n²). Garde la signature. Ajoute un test qui prouve l'équivalence sur 1 000 entrées aléatoires. »

### T‑02 — Few‑shot / exemples
1. **Fonctionnement** : fournir des paires entrée → sortie attendue, balisées (`<example>`).
2. **Objectif** : transmettre format, style, granularité, frontière de classification.
3. **Conditions** : format/style difficile à décrire ; classification ; extraction ; petits modèles.
4. **Bénéfices** : [EMP] Brown et al. 2020 (GPT‑3) ; [OFF] Anthropic : 3 à 5 exemples pertinents, diversifiés, structurés.
5. **Limites** : effet de sur‑imitation ; l'ordre et la distribution des étiquettes biaisent (Zhao et al. 2021 [EMP]).
6. **Coût** : tokens × exemples, mais cacheables.
7. **Risques** : copie de détails de surface ; réduction de diversité ; fuite d'informations d'exemple dans la sortie.
8. **Pertinence** : ★★ (moins nécessaire pour la compréhension, toujours efficace pour la forme).
9. **Éviter** : tâches de raisonnement ouvert où un exemple ancrerait une seule approche ; quand une description suffit.
10. **Exemple** : 4 exemples de tickets → `{catégorie, urgence}` couvrant les cas limites (ticket vide, ticket multi‑sujet), ordre mélangé.

### T‑03 — Décomposition
1. **Fonctionnement** : découper un problème en sous‑problèmes résolus séparément (dans un même prompt ou en plusieurs appels).
2. **Objectif** : réduire la charge par étape ; rendre les étapes vérifiables ; paralléliser.
3. **Conditions** : sous‑problèmes réellement séparables ; étapes intermédiaires inspectables.
4. **Bénéfices** : [EMP] Least‑to‑most prompting (Zhou et al. 2022) sur généralisation compositionnelle ; [EMP] recherche multi‑agents Anthropic (décomposition en sous‑tâches parallèles).
5. **Limites** : les modèles avancés décomposent déjà nativement ; une décomposition imposée peut être moins bonne que la leur.
6. **Coût** : appels supplémentaires si chaînée.
7. **Risques** : perte de contexte entre parties ; incohérence des sous‑résultats.
8. **Pertinence** : ★★ — surtout utile quand la décomposition **est connue de l'humain et pas du modèle** (connaissance métier), ou pour paralléliser.
9. **Éviter** : tâches fortement couplées (beaucoup de code interdépendant).
10. **Exemple** : migration de 2 000 fichiers → liste dans `files.txt` puis un appel par fichier (docs Claude Code, *fan out*).

### T‑04 — Planification avant exécution
1. **Fonctionnement** : faire produire un plan (lu, éventuellement édité par l'humain) avant toute modification. Natif : *plan mode* (Claude Code), `update_plan` / PLANS.md (Codex).
2. **Objectif** : détecter un mauvais cadrage avant qu'il coûte ; aligner humain et modèle.
3. **Conditions** : approche incertaine ; plusieurs fichiers ; code peu familier ; tâche longue.
4. **Bénéfices** : [OFF] Claude Code : évite de « résoudre le mauvais problème ».
5. **Limites** : surcoût ; inutile si le diff tient en une phrase (règle officielle Claude Code).
6. **Coût** : un tour d'exploration + lecture humaine.
7. **Risques** : plan figé suivi malgré des découvertes contraires ; sur gpt‑5.3‑codex, demander un plan en prompt peut provoquer un arrêt prématuré — utiliser l'outil de plan natif.
8. **Pertinence** : ★★.
9. **Éviter** : corrections triviales ; tâches exploratoires où le plan émerge en faisant.
10. **Exemple** : « En mode plan : lis src/auth, puis propose les fichiers à modifier pour ajouter OAuth Google, le flux de session et les tests. N'écris rien. »

### T‑05 — Rôle / persona
1. **Fonctionnement** : « Tu es [rôle] » dans le system prompt.
2. **Objectif réel** : régler ton, registre, vocabulaire, angle d'analyse — pas l'intelligence.
3. **Conditions** : besoin de ton ou de perspective spécifique (relecteur sécurité, rédacteur juridique).
4. **Bénéfices** : [OFF] Anthropic : une phrase suffit à cadrer ton et comportement. [EMP] Zheng et al. (Findings EMNLP 2024, *When "A Helpful Assistant" Is Not Really Helpful*) : sur 2 410 questions factuelles, ajouter un persona n'améliore pas la performance par rapport à l'absence de persona ; effets nuls ou légèrement négatifs, et le meilleur rôle n'est pas prévisible.
5. **Limites** : aucun gain d'exactitude démontré de façon robuste.
6. **Coût** : négligeable.
7. **Risques** : rôle grandiloquent (« le meilleur expert mondial ») → sur‑confiance, ton pompeux ; rôle qui contredit les contraintes.
8. **Pertinence** : ★ (utile, mais pour le style). [CTR]
9. **Éviter** : comme substitut au contexte réel (le rôle « avocat » ne remplace pas le texte du contrat).
10. **Exemple** : « Tu relis du code pour un service de paiement ; tu privilégies la correction et la sécurité sur le style. »

### T‑06 — Chain‑of‑thought manuel (« réfléchis étape par étape »)
1. **Fonctionnement** : demander d'écrire le raisonnement avant la réponse.
2. **Objectif** : améliorer le raisonnement multi‑étapes.
3. **Conditions** : modèle **sans** raisonnement natif, ou raisonnement natif désactivé.
4. **Bénéfices** : [EMP] Wei et al. 2022 ; Kojima et al. 2022 — gains importants sur arithmétique et logique pour les modèles non entraînés au raisonnement.
5. **Limites** : [EMP] gains faibles voire négatifs sur certaines tâches (Sprague et al. 2024, *To CoT or not to CoT* : bénéfice concentré sur maths/logique symbolique ; Liu et al. 2024, *Mind Your Step* : CoT dégrade certaines tâches où la réflexion verbale nuit aussi aux humains).
6. **Coût** : tokens de sortie ×2 à ×10.
7. **Risques** : sur Claude Fable 5.x, demander au modèle d'écrire son raisonnement dans la réponse déclenche une catégorie de refus `reasoning_extraction` [DOC] ; raisonnement affiché non fidèle au calcul réel (Turpin et al. 2023 [EMP]).
8. **Pertinence** : ⊘ sur modèles à thinking natif ; ★ sur modèles légers/locaux sans raisonnement.
9. **Éviter** : tout modèle à raisonnement natif (utiliser T‑07) ; tâches de classification simple.
10. **Exemple (modèle local sans thinking)** : « Raisonne dans `<scratch>`, puis donne uniquement la réponse finale dans `<answer>`. »

### T‑07 — Raisonnement natif et réglage d'effort
1. **Fonctionnement** : paramètre d'API qui contrôle la profondeur de raisonnement, le nombre d'appels d'outils et la durée : `effort` (Claude : low → max, défaut `high` sur Fable 5.2), `reasoning.effort` (OpenAI : défaut conseillé `medium`).
2. **Objectif** : acheter de la qualité contre des tokens, **sans** modifier le texte du prompt.
3. **Conditions** : modèles de raisonnement.
4. **Bénéfices** : [OFF] Anthropic : l'essentiel du gain est à `high` pour code difficile, recherche, agents ; `xhigh` seulement si un gain est mesuré. [OFF] OpenAI : monter pour tâches complexes, baisser pour tâches simples.
5. **Limites** : à `high` et au‑dessus, le modèle Claude réfléchit même à un « bonjour » ; « réponds sans réfléchir » n'a pas d'effet à `medium`+ → baisser l'effort plutôt que l'écrire.
6. **Coût** : principal poste variable.
7. **Risques** : effort trop bas → arrêt prématuré des longues tâches (Fable 5.2, surtout `low`/`medium`) ; trop haut → sur‑réflexion, sur‑vérification.
8. **Pertinence** : ★★★ (remplace la plupart des techniques de « faire réfléchir » textuelles).
9. **Éviter** : de reprendre le réglage d'une version précédente sans nouveau balayage (recommandation explicite Anthropic).
10. **Exemple** : agent de tri de tickets à `low`, agent de débogage à `high`, sous‑agents de recherche à volume élevé à `low`. `budget_tokens` est [OBS] (erreur 400 sur Claude 4.7+).

### T‑08 — Self‑consistency / vote majoritaire
1. **Fonctionnement** : échantillonner N réponses, retenir la plus fréquente.
2. **Objectif** : réduire la variance sur des réponses à forme fermée.
3. **Conditions** : réponse comparable (nombre, étiquette, choix) ; coût ×N acceptable.
4. **Bénéfices** : [EMP] Wang et al. 2022 : gains notables sur benchmarks de raisonnement avec modèles de l'époque.
5. **Limites** : inapplicable aux sorties ouvertes ; gains réduits avec raisonnement natif long (le modèle explore déjà plusieurs pistes — [HYP]) ; sur les modèles OpenAI récents, `temperature` n'est plus pris en charge, ce qui limite le contrôle de la diversité [DOC].
6. **Coût** : ×N.
7. **Risques** : majorité confiante mais fausse (erreurs corrélées).
8. **Pertinence** : ★ ; préférer T‑29 (best‑of‑N avec vérificateur) quand un oracle existe.
9. **Éviter** : code, rédaction, tâches agentiques.
10. **Exemple** : extraction d'un montant ambigu sur 5 échantillons ; si désaccord → routage humain (l'utile est souvent le **désaccord**, pas le vote).

### T‑09 — Self‑critique / auto‑vérification
1. **Fonctionnement** : demander au modèle de vérifier sa réponse selon des critères avant de conclure.
2. **Objectif** : rattraper des erreurs détectables.
3. **Conditions** : critères concrets ; idéalement un signal externe (test, calcul, source).
4. **Bénéfices** : [OFF] Anthropic : « Avant de conclure, vérifie selon [critères] » utile en code et maths. [EMP] Huang et al. 2023 (*LLMs cannot self-correct reasoning yet*) : sans retour externe, l'auto‑correction améliore peu et peut dégrader. [EMP] Self‑Refine (Madaan et al. 2023) : gains sur tâches de génération avec critères explicites.
5. **Limites** : le modèle partage ses propres angles morts.
6. **Coût** : +20 à +100 % de tokens.
7. **Risques** : sur‑vérification (Anthropic : Opus 5 vérifie déjà bien sans consigne ; la consigne peut provoquer une sur‑vérification) ; boucles de relecture sans progrès (OpenAI Codex).
8. **Pertinence** : ★★ avec signal externe ; ★ sans.
9. **Éviter** : quand un oracle exécutable existe (l'utiliser à la place) ; modèles qui vérifient déjà nativement.
10. **Exemple** : « Avant de rendre, recalcule les totaux avec du code et compare‑les au tableau. Signale tout écart. »

### T‑10 — Expliquer les raisons (motivation des contraintes)
1. **Fonctionnement** : accompagner chaque contrainte non évidente de sa raison.
2. **Objectif** : généralisation correcte aux cas non prévus ; arbitrages intelligents.
3. **Conditions** : toute contrainte non évidente.
4. **Bénéfices** : [OFF] Anthropic (exemple synthèse vocale / points de suspension).
5. **Limites** : allonge le prompt.
6. **Coût** : quelques tokens par règle.
7. **Risques** : une raison fausse ou partielle fait mal généraliser.
8. **Pertinence** : ★★★.
9. **Éviter** : raisons évidentes (bruit).
10. **Exemple** : « Ne modifie pas `migrations/`, car ces fichiers sont déjà appliqués en production et toute modification casse le rejeu. Crée une nouvelle migration à la place. »

### T‑11 — Citer avant de répondre (ancrage)
1. **Fonctionnement** : demander d'extraire les passages pertinents (`<quotes>`) puis de répondre en s'y appuyant. Natif : API de citations.
2. **Objectif** : réduire les hallucinations sur documents longs ; rendre la réponse vérifiable.
3. **Conditions** : documents fournis ; questions factuelles.
4. **Bénéfices** : [OFF] Anthropic (contexte long) : ancre la réponse et écarte le bruit.
5. **Limites** : coût de sortie ; ne détecte pas une citation mal interprétée.
6. **Coût** : +citations.
7. **Risques** : citations fabriquées si non vérifiées → vérifier automatiquement la présence littérale (contrôle déterministe) ; ce contrôle ne prouve pas que la citation soutient la conclusion.
8. **Pertinence** : ★★.
9. **Éviter** : synthèse créative ; documents courts.
10. **Exemple** : « Cite mot pour mot les clauses relatives à la résiliation, puis réponds. Si aucune clause ne répond, dis‑le. »

### T‑12 — Recherche et vérification multi‑sources
1. **Fonctionnement** : critères de succès de la recherche + exigence de sources multiples + hypothèses concurrentes + notes.
2. **Objectif** : réponses factuelles à jour et vérifiables.
3. **Conditions** : accès web / documents ; question dont la réponse peut avoir changé.
4. **Bénéfices** : [OFF] Anthropic : critères de succès, vérification multi‑sources, hypothèses concurrentes, suivi de confiance, fichier de notes. Corroboration à proportionner au type d'affirmation : une source primaire autoritative suffit pour un fait documentaire (R-SRC-001).
5. **Limites** : sources SEO de faible qualité ; coût en outils.
6. **Coût** : élevé (outils + lecture).
7. **Risques** : exploration infinie ; injection via pages web (`07`).
8. **Pertinence** : ★★.
9. **Éviter** : faits stables connus du modèle.
10. **Exemple** : « Trouve le prix actuel de X sur la page tarifaire officielle et indique sa date. Si elle est introuvable, cherche deux sources indépendantes et signale tout désaccord. »

### T‑13 — Tool use, function calling et conception d'outils
1. **Fonctionnement** : exposer des outils avec nom, description, schéma ; le modèle les appelle.
2. **Objectif** : accès à l'information et à l'action ; calculs exacts.
3. **Conditions** : besoin d'informations externes, d'actions ou de calculs.
4. **Bénéfices** : [OFF] Anthropic, *Writing effective tools for agents* (2025) : la description d'outil est un prompt ; outils peu nombreux, non ambigus, réponses concises et informatives. [OFF] OpenAI Codex : noms sémantiquement précis (`semantic_search` plutôt que `search`), sortie tronquée (~10k tokens, début et fin conservés), appels parallèles. [OFF] Anthropic : consigne d'appels parallèles → presque 100 % de parallélisation des appels indépendants.
5. **Limites** : trop d'outils → confusion (« si un humain ne sait pas quel outil utiliser, le modèle non plus » — Anthropic, context engineering).
6. **Coût** : définitions d'outils dans chaque requête (cacheables) + résultats.
7. **Risques** : sur‑déclenchement après consignes agressives ; paramètres devinés (« Never use placeholders or guess missing parameters » [OFF]).
8. **Pertinence** : ★★★.
9. **Éviter** : outils redondants ; outils qui renvoient des volumes non filtrés.
10. **Exemple** : remplacer `list_all_users()` par `search_users(query, limit=20)` qui renvoie noms et ID uniquement.

### T‑14 — ReAct et boucle agentique
1. **Fonctionnement** : alterner raisonnement → action (outil) → observation (Yao et al. 2022).
2. **Objectif** : ancrer le raisonnement dans des observations réelles.
3. **Conditions** : agents avec outils.
4. **Bénéfices** : [EMP] Yao et al. 2022 sur QA et environnements interactifs.
5. **Limites** : aujourd'hui **intégré** aux modèles et aux harnais (thinking entrelacé, boucles natives) ; l'écrire en prompt est redondant.
6. **Coût** : —
7. **Risques** : imposer le format « Thought/Action/Observation » textuel à un modèle doté d'outils natifs dégrade l'usage des outils ([HYP] fondée sur le décalage avec le format d'entraînement).
8. **Pertinence** : ★ comme technique de prompt ; ★★★ comme modèle mental.
9. **Éviter** : avec API d'outils natives.
10. **Exemple** : n'écrire que « Utilise les outils pour vérifier avant de conclure ; ne spécule pas sur du code que tu n'as pas ouvert. »

### T‑15 — RAG et récupération juste‑à‑temps
1. **Fonctionnement** : récupérer les passages pertinents (pré‑calculé : embeddings ; ou à la demande : l'agent cherche avec `grep`, `glob`, recherche).
2. **Objectif** : ne mettre en contexte que ce qui sert.
3. **Conditions** : corpus plus grand que la fenêtre utile.
4. **Bénéfices** : [EMP] Lewis et al. 2020 ; [OFF] Anthropic, context engineering : stratégie hybride — quelques données en amont, le reste récupéré juste‑à‑temps via identifiants légers (chemins, requêtes).
5. **Limites** : qualité du retrieval = plafond de la qualité ; fragmentation du sens.
6. **Coût** : infrastructure ; tokens de passages.
7. **Risques** : passages hors sujet mais similaires (distracteurs, dont Chroma montre l'effet négatif) ; injection via documents indexés.
8. **Pertinence** : ★★ ; pour le code, la recherche agentique (`grep`) est souvent préférée par les agents de code ([OFF] Anthropic, Claude Code).
9. **Éviter** : corpus qui tient confortablement en contexte et sert intégralement.
10. **Exemple** : passer à l'agent le chemin des fichiers de spécification et l'instruction de lire ceux qui concernent le module touché.

### T‑15b — Prompt chaining
1. **Fonctionnement** : enchaîner des appels séparés, la sortie de l'un alimentant l'autre.
2. **Objectif** : inspecter les intermédiaires ; imposer un pipeline ; utiliser des modèles différents par étape.
3. **Conditions** : étapes de nature différente ; besoin d'audit intermédiaire ; production à grand volume.
4. **Bénéfices** : [OFF] Anthropic : moins nécessaire avec thinking adaptatif, sauf pour inspecter les intermédiaires ou imposer un pipeline (brouillon → revue → raffinement).
5. **Limites** : perte d'information entre étapes ; latence.
6. **Coût** : somme des appels ; parfois **moins** cher (petits modèles par étape).
7. **Risques** : erreurs propagées sans détection.
8. **Pertinence** : ★★ en production, ★ en interactif.
9. **Éviter** : quand un seul appel avec bon modèle suffit.
10. **Exemple** : extraction (Haiku, schéma JSON) → validation déterministe → rédaction (Sonnet).

### T‑16 — Contraintes déclaratives et invariants
1. **Fonctionnement** : énoncer des propriétés qui doivent rester vraies (« l'API publique ne change pas », « aucun test supprimé ») plutôt que des étapes.
2. **Objectif** : laisser la liberté de méthode tout en bornant le résultat.
3. **Conditions** : tâches agentiques, refactorisations, rédaction réglementée.
4. **Bénéfices** : [OFF] Anthropic : « Il est inacceptable de supprimer ou modifier des tests » ; demander une solution générale plutôt que de coder en dur les cas testés.
5. **Limites** : invariant non vérifié = vœu pieux → l'adosser à un contrôle.
6. **Coût** : faible.
7. **Risques** : invariants trop nombreux → paralysie.
8. **Pertinence** : ★★★.
9. **Éviter** : invariants invérifiables.
10. **Exemple** : « Invariants : la sortie de `cli --help` est identique ; `pytest` passe ; aucun fichier hors de `src/parser/` n'est modifié. »

### T‑17 — Structured outputs (sortie contrainte par schéma)
1. **Fonctionnement** : fournir un schéma JSON à l'API ; décodage contraint.
2. **Objectif** : sortie parseable garantie.
3. **Conditions** : consommation par un programme.
4. **Bénéfices** : [DOC] conformité au schéma garantie par l'API (OpenAI, Anthropic) pour une sortie complète, non refusée, avec un schéma supporté (S-O8, S-A14) ; grammaires pour modèles locaux (llama.cpp GBNF, outlines) [DOC].
5. **Limites** : conformité **syntaxique et de schéma**, pas sémantique ; refus et sorties incomplètes possibles ; tous les schémas ne sont pas supportés. Le consommateur doit traiter ces états (R-VAL-005, gabarit d'extraction de `11`).
6. **Coût** : faible.
7. **Risques** : [CTR] baisse possible de raisonnement si le schéma force la réponse avant la réflexion → mettre un champ de raisonnement en tête, ou utiliser le thinking natif.
8. **Pertinence** : ★★★.
9. **Éviter** : sortie destinée à un humain.
10. **Exemple** : schéma `{decision: enum[approve,reject,escalate], reasons: string[], evidence_ids: string[]}`.

### T‑18 — Validation par tests et oracles
1. **Fonctionnement** : donner au modèle un moyen d'obtenir un signal pass/fail et lui demander d'itérer jusqu'au succès.
2. **Objectif** : remplacer l'auto‑évaluation par une évaluation externe.
3. **Conditions** : résultat vérifiable mécaniquement.
4. **Bénéfices** : [OFF] Claude Code (« la différence entre une session surveillée et une session autonome ») ; [OFF] Codex : fournir les commandes de build/test dans AGENTS.md pour que l'agent vérifie son travail.
5. **Limites** : tests incomplets → faux succès ; tentation de modifier les tests.
6. **Coût** : exécution ; souvent le meilleur rapport qualité/coût.
7. **Risques** : *reward hacking* (codage en dur, tests affaiblis) → invariants T‑16 + revue du diff des tests.
8. **Pertinence** : ★★★.
9. **Éviter** : jamais, quand c'est possible.
10. **Exemple** : « Écris d'abord un test qui reproduit le bug et échoue. Puis corrige. Montre la sortie du test avant et après. »

### T‑19 — Audit indépendant (relecteur à contexte frais)
1. **Fonctionnement** : faire relire le résultat par une instance qui n'a vu que le livrable et les critères.
2. **Objectif** : éviter que le producteur se note lui‑même.
3. **Conditions** : travail long, autonome ou à fort enjeu.
4. **Bénéfices** : [OFF] Claude Code : contexte frais = pas de biais envers le code qu'on vient d'écrire ; pattern Writer/Reviewer.
5. **Limites** : [OFF] un relecteur chargé de trouver des lacunes en trouvera toujours, même si le travail est bon → limiter aux lacunes affectant correction et exigences.
6. **Coût** : un appel supplémentaire (contexte réduit).
7. **Risques** : sur‑ingénierie si chaque remarque est appliquée.
8. **Pertinence** : ★★★.
9. **Éviter** : tâches triviales.
10. **Exemple** : voir gabarit « Relecteur » de `11`.

### T‑20 — Délégation et orchestration multi‑agents
1. **Fonctionnement** : un orchestrateur lance des sous‑agents à contexte séparé, chacun renvoyant un résumé condensé.
2. **Objectif** : paralléliser ; isoler l'exploration ; dépasser la limite d'une fenêtre.
3. **Conditions** : sous‑tâches **indépendantes**, à forte lecture, de valeur suffisante.
4. **Bénéfices** : [EMP fournisseur] Anthropic : système Opus 4 + sous‑agents Sonnet 4 meilleur de 90,2 % qu'Opus 4 seul sur leur évaluation interne de recherche (juin 2025) — résultat non répliqué, propre à la recherche en largeur.
5. **Limites** : [OFF] Anthropic : mauvais choix quand tous les agents doivent partager le même contexte ou ont beaucoup de dépendances (la plupart des tâches de code). Cognition, *Don't Build Multi-Agents* (2025) : décisions implicites divergentes entre agents qui écrivent.
6. **Coût** : dans le système de recherche d'Anthropic, ~15× les tokens d'une interaction de chat (agents simples : ~4×). Ce n'est pas une comparaison à un agent unique à qualité égale : mesurer localement.
7. **Risques** : sur‑délégation (sous‑agent pour un `grep`) ; briefs vagues → duplication ; confiance aveugle dans les résultats des sous‑agents.
8. **Pertinence** : ★★ (fort pour la recherche en largeur ; faible pour l'écriture couplée).
9. **Éviter** : tâches séquentielles, édition d'un seul fichier, besoin de contexte continu (consigne Anthropic officielle).
**Délégation ponctuelle ou architecture** : la décision ponctuelle d'un agent de déléguer pendant une mission relève de son jugement selon les critères ci‑dessus (R-ARCH-002), sans démonstration préalable. Inscrire la délégation dans un fichier persistant, un harnais ou un pipeline la rend permanente : la tester d'abord sur quelques missions et mesurer coût et qualité (R-ARCH-001).
10. **Exemple** : « Lance 3 sous‑agents : (a) usages de `TokenRefresh` dans src/, (b) tests existants d'auth, (c) utilitaires OAuth réutilisables. Chacun renvoie ≤ 15 lignes avec chemins de fichiers. »

### T‑21 — Instructions persistantes (CLAUDE.md, AGENTS.md, system prompts de projet)
1. **Fonctionnement** : fichier lu au début de chaque session.
2. **Objectif** : ne plus répéter commandes, conventions, pièges.
3. **Conditions** : travail récurrent sur un même projet.
4. **Bénéfices** : [OFF] Anthropic et OpenAI : court, précis, mis à jour quand une erreur se répète (Codex : « si Codex fait deux fois la même erreur, demandez une rétrospective et mettez à jour AGENTS.md »).
5. **Limites** : [OFF] un fichier trop long fait ignorer les règles importantes.
6. **Coût** : chargé à chaque session (cacheable).
7. **Risques** : accumulation de prudence obsolète (Fable 5.2) ; contradictions entre niveaux de fichiers.
8. **Pertinence** : ★★★.
9. **Éviter** : y mettre ce que le modèle peut lire dans le code, ou des connaissances utiles seulement parfois (→ skills).
10. **Exemple** : voir gabarits `11`.

### T‑22 — Skills / chargement progressif (progressive disclosure)
1. **Fonctionnement** : dossier `SKILL.md` + ressources ; seul le nom et la description sont chargés en permanence ; le contenu est chargé quand pertinent.
2. **Objectif** : disposer de beaucoup de savoir‑faire sans saturer le contexte.
3. **Conditions** : procédures ou connaissances utiles **parfois**.
4. **Bénéfices** : [OFF] Claude Code : les skills se chargent à la demande « sans alourdir chaque conversation » ; [DOC] Codex prend aussi en charge les skills (`SKILL.md`).
5. **Limites** : déclenchement dépendant de la qualité de la description.
6. **Coût** : très faible au repos.
7. **Risques** : skills tiers non audités (exécutent du code) ; description trop large → déclenchement abusif.
8. **Pertinence** : ★★★.
9. **Éviter** : règles qui doivent s'appliquer **toujours** (→ fichier persistant ou hook).
10. **Exemple** : skill `release-checklist` invoquée manuellement (`disable-model-invocation: true` pour les workflows à effets de bord).

### T‑23 — Hooks et contrôles déterministes
1. **Fonctionnement** : scripts exécutés à des points du cycle de vie (avant/après outil, fin de tour…), capables de bloquer.
2. **Objectif** : garantir ce que le prompt ne peut que demander.
3. **Conditions** : règle qui doit s'appliquer à chaque fois sans exception.
4. **Bénéfices** : [OFF] Claude Code : hooks déterministes vs CLAUDE.md consultatif ; hook `Stop` qui bloque la fin du tour tant qu'un contrôle échoue.
5. **Limites** : ne juge pas le sens ; maintenance de scripts.
6. **Coût** : temps d'exécution des scripts.
7. **Risques** : hook bloquant mal conçu → boucles (il existe un plafond de blocages consécutifs [DOC]).
8. **Pertinence** : ★★★.
9. **Éviter** : pour des préférences de style subjectives.
10. **Exemple** : `PreToolUse` qui refuse toute écriture dans `migrations/` ; `PostToolUse` qui lance le formateur.

### T‑24 — Mémoire externe et notes structurées
1. **Fonctionnement** : l'agent écrit son état hors du contexte (progress.txt, tests.json, git) et le relit.
2. **Objectif** : continuité sur plusieurs fenêtres / sessions.
3. **Conditions** : tâches longues, reprises, compaction.
4. **Bénéfices** : [OFF] Anthropic : JSON pour l'état structuré, texte libre pour les notes, git pour les checkpoints ; une nouvelle fenêtre avec démarrage prescrit est souvent préférable à la compaction.
5. **Limites** : discipline d'écriture.
6. **Coût** : faible.
7. **Risques** : notes obsolètes qui deviennent des règles (prudence cumulée).
8. **Pertinence** : ★★.
9. **Éviter** : tâches courtes.
10. **Exemple** : « Au début de chaque session : `pwd`, lis progress.txt, tests.json et `git log -10`, lance le test d'intégration de base. »

### T‑25 — Compaction et nettoyage du contexte
1. **Fonctionnement** : résumer l'historique (auto‑compaction, `/compact`, `/responses/compact`), effacer les vieux résultats d'outils, ou repartir d'une session propre.
2. **Objectif** : prolonger le travail sans saturer.
3. **Conditions** : sessions longues.
4. **Bénéfices** : [DOC] natif dans Claude Code, Codex, API OpenAI.
5. **Limites** : perte d'information ; résumé qui oublie une contrainte.
6. **Coût** : un appel de résumé.
7. **Risques** : invalidation du cache ; perte des décisions → préciser quoi préserver (« préserve la liste des fichiers modifiés et les commandes de test » [OFF]).
8. **Pertinence** : ★★.
9. **Éviter** : quand `/clear` + bon prompt est plus simple (tâches non liées).
10. **Exemple** : `/compact Concentre-toi sur les changements d'API et les tests restant en échec`.

### T‑26 — Spec‑first / interview
1. **Fonctionnement** : faire interroger l'humain par le modèle, produire une spécification, puis exécuter dans une session neuve.
2. **Objectif** : extraire les exigences implicites avant d'investir.
3. **Conditions** : fonctionnalités larges, ambiguës.
4. **Bénéfices** : [OFF] Claude Code (prompt « Interview me in detail… then write SPEC.md »).
5. **Limites** : temps humain.
6. **Coût** : quelques tours.
7. **Risques** : questions évidentes (à interdire explicitement).
8. **Pertinence** : ★★.
9. **Éviter** : tâches claires.
10. **Exemple** : gabarit « Interview » de `11`.

### T‑27 — Metaprompting et optimisation de prompts
1. **Fonctionnement** : utiliser un modèle pour améliorer un prompt (manuellement : « quelles phrases ajouter/retirer pour obtenir X au lieu de Y ? » ; automatiquement : DSPy, optimiseurs de fournisseurs).
2. **Objectif** : itérer plus vite.
3. **Conditions** : comportement observé vs voulu clairement décrit ; jeu d'évaluation pour valider.
4. **Bénéfices** : [OFF] OpenAI : plusieurs utilisateurs ont déployé en production des révisions obtenues ainsi ; [EMP] DSPy (Khattab et al. 2023), OPRO (Yang et al. 2023).
5. **Limites** : sur‑ajustement au jeu d'évaluation ; prompts optimisés parfois illisibles.
6. **Coût** : appels d'optimisation + évaluations.
7. **Risques** : gonflement du prompt (le modèle ajoute plutôt qu'il ne retire) → demander des modifications **minimales**.
8. **Pertinence** : ★★.
9. **Éviter** : sans évaluation pour trancher.
10. **Exemple** : gabarit OpenAI : prompt + comportement voulu + comportement observé → modifications minimales.

### T‑28 — LLM‑as‑judge
1. **Fonctionnement** : un modèle note des sorties selon une grille.
2. **Objectif** : évaluer à grande échelle ce qui n'a pas d'oracle exact.
3. **Conditions** : grille précise, dimensions isolées, calibrage humain.
4. **Bénéfices** : [EMP] Zheng et al. 2023 (MT‑Bench) : accord avec humains comparable à l'accord inter‑humains sur certaines tâches.
5. **Limites** : [EMP] biais de position, de longueur, d'auto‑préférence.
6. **Coût** : un appel par sortie (× permutations).
7. **Risques** : optimiser pour le juge et non pour l'utilisateur.
8. **Pertinence** : ★★.
9. **Éviter** : quand un test exact existe.
10. **Exemple** : juge binaire par critère, avec option « Inconnu » si preuve insuffisante ([OFF] Anthropic, evals).

### T‑29 — Best‑of‑N avec vérificateur
1. **Fonctionnement** : générer N candidats, sélectionner via un oracle (tests) ou un juge.
2. **Objectif** : convertir du calcul en qualité quand la vérification est moins chère que la génération.
3. **Conditions** : vérificateur fiable.
4. **Bénéfices** : [EMP] approche standard en génération de code (pass@k) ; worktrees concurrents implémentant des approches différentes (pratique Claude Code rapportée).
5. **Limites** : ×N ; vérificateur imparfait.
6. **Coût** : ×N + vérification.
7. **Risques** : sélection du candidat qui « triche » le mieux sur les tests.
8. **Pertinence** : ★★.
9. **Éviter** : sans vérificateur.
10. **Exemple** : 3 worktrees, 3 approches d'optimisation, sélection par benchmark + tests.

### T‑30 — Checkpoints et retour arrière
1. **Fonctionnement** : instantanés de conversation et de code (`/rewind`, git).
2. **Objectif** : rendre l'essai bon marché ; autoriser des tentatives risquées réversibles.
3. **Conditions** : environnement qui les fournit.
4. **Bénéfices** : [OFF] Claude Code : « dire à Claude d'essayer quelque chose de risqué, puis revenir en arrière ».
5. **Limites** : [DOC] les checkpoints ne couvrent pas les effets des commandes Bash ni les systèmes externes.
6. **Coût** : nul.
7. **Risques** : fausse impression de réversibilité pour les effets externes.
8. **Pertinence** : ★★.
9. **Éviter** : de compter dessus pour des actions externes (base de production, API tierce).
10. **Exemple** : travailler dans un worktree git dédié, commit à chaque étape verte.

---

## Techniques à considérer comme obsolètes ou à fort risque

| Technique | Statut | Remplacement |
|---|---|---|
| Prefill de la réponse de l'assistant | [OBS] erreur 400 sur Claude 4.6+ | Instructions de format, structured outputs |
| `budget_tokens` | [OBS] erreur 400 sur Claude 4.7+ | `effort`, `max_tokens` |
| « Think step by step » sur modèle à thinking | [OBS] | Réglage d'effort |
| Demander d'écrire son raisonnement dans la réponse (Claude Fable 5.x) | [OBS] → refus | Lire les blocs `thinking` résumés |
| Consignes anti‑paresse héritées (« sois exhaustif !!! ») | [OBS] → sur‑déclenchement | Critères explicites d'exhaustivité |
| Pourboires, menaces, urgence émotionnelle | [CTR]/[OBS] | Raisons réelles, critères |
| Format ReAct textuel avec outils natifs | [OBS] | Outils natifs |
| `temperature`/`top_p` pour diversité (OpenAI GPT‑6.x) | [DOC] non pris en charge | Variation des prompts, N appels |
| Demander des préambules et un plan en prompt sur `gpt-5.3-codex` quand l'intégration ne conserve pas `phase` | [OFF] à retirer | Outil de plan natif ; ou conserver `phase` au replay (S-O11). Ne s'applique pas à Codex avec d'autres modèles |
