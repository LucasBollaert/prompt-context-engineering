# 15 — Arbitrage de la contre‑expertise (v1.0 → v1.1)

**Objet :** réponse aux 20 constatations de la contre‑expertise indépendante du 24 novembre 2026 (`independent_review/`, source S‑REV). **Date :** 24 novembre 2026.

## 1. Méthode d'arbitrage

1. Chaque constat vérifiable a été **reproduit** avant d'être accepté. C'est le cas du typage YAML, de l'énumération des 729 combinaisons d'axes et des sources OpenAI et Anthropic citées pour les constats 004, 007, 013 et 016.
2. Les constats d'analyse (portée, statistiques, cohérence) ont été jugés sur le texte du référentiel.
3. Pour chaque question d'arbitrage, une décision est prise et justifiée. Aucune n'est renvoyée sans réponse.
4. Ni la revue ni cette réponse n'ont exécuté d'expérience sur des modèles. Les gains attendus des corrections restent **à mesurer**.

## 2. Synthèse

| Décision | Nombre | Constats |
|---|---|---|
| Accepté et corrigé | 17 | 001, 002, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 015, 016, 017, 018, 020 |
| Accepté en partie (le reste est reporté et motivé) | 3 | 003, 014, 019 |
| Rejeté | 0 | — |

La revue est jugée exacte sur tous les points vérifiés. Aucun constat n'a été réfuté. Les reports concernent des chantiers dont le coût n'est pas justifié tant qu'aucun besoin d'automatisation déterministe n'est établi.

## 3. Arbitrage constat par constat

### REVIEW-001 — `OFF` lu comme booléen · **accepté, corrigé**
- **Vérification** : défaut reproduit. Avec PyYAML, la clé `OFF` de `meta` et 50 listes `evidence` contenaient `False`. Le contrôle de la v1.0 ne vérifiait pas les types, d'où le défaut non détecté.
- **Décision** : `rules.yaml` est la **source canonique**. Le fichier doit être lu de façon identique par les parseurs YAML 1.1 et 1.2, ce que garantissent les codes entre guillemets. `rules.json` est dérivé.
- **Changements** :
  - Les codes sont désormais des chaînes.
  - `scripts/build_rules.py` valide les types et les énumérations. Il compare le chargeur standard et un chargeur où tout reste en chaîne, puis génère `rules.json`.
  - Test négatif effectué : un `OFF` non cité fait échouer la construction. La recherche `OFF` renvoie 50 règles.

### REVIEW-002 — Niveaux T0‑T3 ni exclusifs ni exhaustifs · **accepté, corrigé**
- **Vérification** : la répartition 60 / 288 / 324 / 57 sur les 729 combinaisons est reproduite.
- **Décision** : les niveaux sont des **gabarits**, mais leur attribution doit être une fonction totale.
  - Le niveau dépend uniquement de la complexité (A) et de l'horizon (D).
  - Le risque, la vérifiabilité, l'ambiguïté et l'environnement deviennent des **modules** indépendants. Ils ajoutent des lignes au prompt sans changer le niveau.
  - Les garde‑fous ne dépendent jamais du niveau.
- **Changements** : `09` §1 (table A × D, modules, exemples) ; `10` étapes 8‑9 ; `14` étapes 7‑8 ; règle R‑CLASS‑001. Le validateur vérifie que chacune des 729 combinaisons reçoit exactement un niveau.

### REVIEW-003 — Sémantique de sélection absente · **accepté en partie**
- **Décision** : le niveau d'automatisation visé est une **sélection assistée par IA** : des filtres structurés, puis un jugement explicable. Il ne s'agit pas d'un moteur déterministe.
- **Changements** :
  - `meta.selection_semantics` documente le sens de chaque champ. Les conditions sont lues en disjonction, une conjonction s'écrit « ET » dans une même condition. Le tag `all` et les tags spécifiques sont inclusifs. Les conflits sont symétriques, avec une priorité par défaut.
  - Les conditions ambiguës sont réécrites (R‑ARCH‑004, R‑ARCH‑005).
- **Reporté** : la séparation des tags `models` en dimensions (fournisseur, harnais, capacité) et le langage de prédicats. Ils ne valent la peine que si un sélecteur déterministe devient nécessaire. La validation proposée par la revue (cas annotés, précision et rappel, omissions de règles de sécurité) reste le préalable.

### REVIEW-004 — Codex assimilé à `gpt-5.3-codex` · **accepté, corrigé**
- **Vérification** :
  - La page OpenAI de choix de modèle recommande de commencer par GPT‑6.2 Sol pour la plupart des tâches dans ChatGPT Work ou Codex.
  - Pour `gpt-5.3-codex`, `phase` figure sur les items assistant et doit être conservé lors du replay ; sa perte dégrade fortement les performances.
  - Le guide conseille de retirer les demandes de plan, de préambules et de statut pendant le rollout.
- **Décision** : les consignes « 5.3 » sont conditionnées au modèle exact et à l'intégration. On ne conserve le guide 5.3 que pour les intégrations API qui l'utilisent.
- **Changements** : `04` §6 (produit ≠ modèle, `phase` comme métadonnée, plan d'approbation / outil de plan / récit du plan) ; `06` §8 ; `03` (tableau des obsolètes) ; `01` P2 ; `14` ; règles R‑AUTO‑010 et R‑COMM‑002.

### REVIEW-005 — Garanties surestimées · **accepté, corrigé**
- **Décision** : chaque contrôle porte un type (prévention, détection ou réduction) et une portée. Les invariants critiques échouent fermé.
- **Changements** :
  - `07` §1 : colonne typée.
  - `07` §3.1 : tableau « garantit / ne garantit pas ». Il couvre le worktree, les hooks, `/goal`, la sandbox, les listes d'autorisation et les structured outputs.
  - Règle R‑SEC‑005, anti‑pattern AP‑26, `01` P7, `10` Annexe A et `14` principe 1.
- **Hors périmètre ici** : les tests adverses en environnement jetable que propose la revue. Ils restent à exécuter sur votre configuration réelle.

### REVIEW-006 — Pas d'état terminal de non‑succès · **accepté, corrigé**
- **Décision** : oui, un **noyau d'arrêt non optionnel** est ajouté aux gabarits agentiques. Il distingue quatre états : succès, partiel, bloqué et plafond atteint. Hors succès, l'agent laisse un état reprenable et ne déclare pas la réussite.
- **Changements** :
  - Gabarits T2 et T3 de `11` (blocs « noyau » ; commits conditionnels).
  - `02` §6, contrat de `06` §7, `10` étapes 11 et 13, Annexe A.
  - Règles R‑AUTO‑011 et R‑AUTO‑012, anti‑pattern AP‑25.

### REVIEW-007 — Facteur 15× sans comparateur · **accepté, corrigé**
- **Vérification** : selon le rapport, les agents consomment environ 4× plus de tokens qu'un chat, et les systèmes multi‑agents environ 15× plus qu'un chat. Le gain de 90,2 % compare le système multi‑agents Opus 4 + Sonnet 4 à Opus 4 seul, sur l'évaluation interne de recherche.
- **Décision** : le chiffre reste dans la règle, avec son comparateur, ses modèles et la mention « à mesurer localement ».
- **Changements** : R‑ARCH‑002, `03` T‑20, `08` AP‑09, `13`.

### REVIEW-008 — Ordre des documents longs généralisé · **accepté, corrigé**
- **Décision** : il s'agit d'une recommandation **sémantique** qui s'applique à l'intérieur de la couche variable. Elle est propre à Claude et non transférable sans test. Exception : les documents stables peuvent aller dans la couche cacheable.
- **Changements** : R‑STR‑002 (modèles `claude-api`, preuve OFF seule, `provider_specific`) ; `02` §2.1 ; `13` §6.

### REVIEW-009 — Capacités et versions non suivies · **accepté, corrigé**
- **Décision** :
  - `14` conserve une section de particularités **datée**. Une instruction persistante sans aucune spécificité forcerait des consultations systématiques.
  - Cette section est conditionnée : on vérifie quand la mission en dépend.
  - Une **fiche de capacités** est ajoutée. Elle ne se renseigne que pour ce qui affecte la mission.
  - `14` est mis à jour à **tout** changement qui touche son contenu.
- **Changements** :
  - Champs `volatility` et `last_verified` sur chaque règle.
  - Règle R‑CAP‑001 ; R‑MODEL‑002 (chargement des fichiers persistants à établir) ; R‑MAINT‑001.
  - `13` §7.2 étape 7, `10` étape 7, `04` en‑tête.

### REVIEW-010 — Structured outputs : portée et états d'erreur · **accepté, corrigé**
- **Décision** :
  - Le prompt demande un schéma.
  - Le **consommateur** traite les états non réussis (refus, sortie incomplète, schéma non supporté, `null` métier) et assure le contrôle métier.
  - En l'absence de structured outputs, on valide puis on fait une réparation bornée.
- **Changements** : R‑STR‑007 (conditions de la garantie, sources API) ; nouvelle règle R‑VAL‑005 ; `03` T‑17 ; `02` §4 ; table des états dans le gabarit d'extraction de `11` ; `07` §3.1.
- Les sources S‑O8 et S‑A14 sont marquées **R** : elles ont été vérifiées par la revue, pas relues par l'auteur.

### REVIEW-011 — Pas de baseline sans intermédiaire · **accepté, corrigé**
- **Décision** :
  - Aucun seuil d'amélioration n'est fixé a priori. C'est l'objet du pilote.
  - Une **voie rapide** est ajoutée : pas de reformulation quand elle n'apporte rien.
  - Les étapes de la méthode restent mentales et ne sont pas exposées.
- **Changements** :
  - `12` §5.0 : bras demande directe, prompt minimal, protocole complet, version allégée, mesurés de bout en bout avec le coût du générateur.
  - Règles R‑EVAL‑004 et R‑GEN‑001.
  - Voie rapide dans `10` et branches de livraison dans `14`.
  - `00` et `13` signalent que le gain du générateur n'est pas démontré.

### REVIEW-012 — Statistiques de décision fragiles · **accepté, corrigé**
- **Décision** : la marge de non‑infériorité est définie par classe de tâche et par métrique, **avant** l'essai, par l'utilisateur du protocole. Le référentiel n'impose pas de valeur universelle. Les garde‑fous de sécurité passent avant tout et se vérifient par des tests adverses déterministes.
- **Changements** :
  - `12` §5.1 à §5.4 : le cas comme unité statistique, bootstrap par cas avec répétitions imbriquées, puissance selon les paires discordantes, décision multi‑objectifs (supériorité ou non‑infériorité), simulation du protocole, ablation par non‑infériorité.
  - Règles R‑EVAL‑001 et R‑EVAL‑005 (conflit déclaré avec R‑CTX‑002).

### REVIEW-013 — Modèle économique imprécis · **accepté, corrigé**
- **Vérification** : sur OpenAI (GPT‑5.6 et ultérieurs), l'écriture coûte 1,25× en TTL 30 min et 2,5× en 12 h. Ce sont des tarifs totaux. La lecture coûte 0,1×, ou 0,05× sur GPT‑6.2 Astra et Sol.
- **Décision** : une **convention de comptabilité** suffit, pas un calculateur.
- **Changements** : `05` §1 réécrit (coût réalisé ou coût espéré, compteurs non chevauchants, valorisation explicite du temps, prix versionnés, coût du générateur, exemple conditionnel) ; `05` §9.2 ; `04` §5 ; règle R‑COST‑002.

### REVIEW-014 — Types de preuve et statuts confondus · **accepté en partie**
- **Décision** : des notes ciblées, plutôt qu'un schéma d'affirmations.
- **Changements** :
  - Le champ `evidence` ne contient plus que DOC, OFF, EMP et HYP.
  - La transférabilité passe dans `transfer`, le cycle de vie dans `status` et `notes`.
  - Les chiffres des règles à fort impact sont rattachés à leur comparateur.
  - `00` §3 explique la distinction. EMP précise « test de fournisseur, non indépendant ».
- **Reporté** : l'attribution de la preuve à chaque proposition dans chaque règle. C'est coûteux, et à envisager si un audit inter‑évaluateurs montre des confusions réelles.

### REVIEW-015 — Modes de livraison de `14` · **accepté, corrigé**
- **Décision** : non, le rôle ne produit pas toujours un prompt. Il choisit l'une de cinq branches : voie rapide, clarification, prompt, audit ou comparaison.
- **Changements** :
  - Les hypothèses critiques figurent dans le prompt.
  - Une hypothèse ne remplace jamais une permission (R‑SEC‑007).
  - Les questions découvertes en cours de route se posent quand elles deviennent bloquantes.
  - Répercussions dans `14`, `10` (étapes 6 et 15) et `02` §5.1.

### REVIEW-016 — L'ajout seul ignore les API d'ajout supportées · **accepté, corrigé**
- **Vérification** : chez Anthropic, un message système ajouté en cours de conversation garde l'autorité d'opérateur, le préfixe et les blocs de thinking. Les outils s'ajoutent ou se retirent via `tool_addition` et `tool_removal` (bêta). La disponibilité dépend du modèle et de la plateforme. La documentation interdit d'y placer du contenu non fiable.
- **Décision** : on distingue l'historique immuable, les ajouts autorisés par l'API et la réinitialisation. On renvoie à la documentation pour les modèles et les en‑têtes bêta.
- **Changements** : R‑CTX‑004 ; `02` §2.2 ; `07` §3.3 ; `14`.

### REVIEW-017 — Corroboration non définie · **accepté, corrigé**
- **Décision** : la corroboration dépend du **type d'affirmation**. Une source primaire autoritative et datée suffit pour un fait documentaire. Un fait contesté ou à fort enjeu exige des sources réellement indépendantes. On vérifie que la citation soutient la conclusion, et on rapporte les désaccords.
- **Changements** : R‑SRC‑001 ; `09` §2.2 ; gabarit de recherche de `11` ; `03` T‑11 et T‑12 ; `07` §1.

### REVIEW-018 — Dérives éditoriales · **accepté, corrigé**
- **Décision** : `rules.yaml` fait foi pour les règles, le Markdown pour l'argumentation, et `rules.json` est dérivé.
- **Changements** :
  - L'index liste `rules.json` et le script.
  - Renvoi `04` → `13` §7.
  - Parcours « coût » corrigé : AP‑01, AP‑08, AP‑09, AP‑19, AP‑20.
  - Nombre d'exemples harmonisé à « 2 à 5, indicatif ».

### REVIEW-019 — Mécanismes supposés disponibles · **accepté en partie**
- **Changements** :
  - Retour par fichiers seulement si l'espace est partagé (R‑ARCH‑004, `05` §11).
  - Troncature seulement si le contenu intégral reste accessible (R‑CTX‑007, `05` §6).
  - « Léger » et « local » ne valent pas faible capacité : on se règle sur la capacité observée (R‑MODEL‑003, `04` §9‑10, `10` étape 9).
- **Reporté** : la mesure comparative entre modèle local fort et modèle léger faible. Elle relève de l'expérimentation.

### REVIEW-020 — Autorité et permissions · **accepté, corrigé**
- **Décision** :
  - En mode audit, seule la lecture est compatible avec le mandat. Les tests ou builds qui écrivent ne s'exécutent qu'en sandbox jetable autorisée, et le rapport va dans une zone séparée.
  - Les interdictions délibérées restent absolues.
  - « L'utilisateur prime sur AGENTS.md » concerne les préférences, pas les restrictions.
- **Changements** : R‑SEC‑006 ; R‑TONE‑002 (exception reformulée) ; `07` §3.2 et §3.3 ; gabarit d'audit de `11` ; `09` §2.7 ; `04` §6.

## 4. Nouvelles règles

| ID | Objet | Constats |
|---|---|---|
| R‑AUTO‑011 | États terminaux explicites | 006 |
| R‑AUTO‑012 | Actions conditionnées aux permissions | 006, 020 |
| R‑SEC‑005 | Portée réelle d'une garantie | 005 |
| R‑SEC‑006 | Mandat d'audit en lecture seule | 020 |
| R‑SEC‑007 | Une hypothèse ne remplace jamais une permission | 015, 020 |
| R‑VAL‑005 | Structured outputs : états non réussis et contrôle métier | 010 |
| R‑SRC‑001 | Corroboration selon le type d'affirmation | 017 |
| R‑CAP‑001 | Vérifier les capacités de la cible | 009, 019 |
| R‑CLASS‑001 | Niveau total et modules orthogonaux | 002 |
| R‑GEN‑001 | Branches de livraison et voie rapide | 011, 015 |
| R‑COST‑002 | Comptabilité non chevauchante | 013 |
| R‑EVAL‑004 | Baseline sans intermédiaire | 011 |
| R‑EVAL‑005 | Non‑infériorité pré‑définie | 012 |

## 5. Ce qui reste ouvert

1. **Aucun gain n'est démontré**, ni pour le protocole de génération ni pour les corrections de la v1.1. Le pilote de `12` §5.0 est la prochaine étape utile.
2. **Tests adverses** des contrôles (hooks, sandbox, lecture seule) sur une configuration réelle. Ils n'ont pas été faits dans cet environnement.
3. **Sources non vérifiées indépendamment** : la plupart des références scientifiques (statut M) et plusieurs billets fournisseurs. Les chiffres de Fable 5.2 (−50 % de sessions inachevées, +30 % de tokens, +70‑80 % avec « owner ») ont été lus par l'auteur sur la page officielle, mais la revue ne les a pas tous contrôlés.
4. **Sélecteur déterministe** et schéma d'affirmations : reportés (REVIEW‑003, REVIEW‑014).
