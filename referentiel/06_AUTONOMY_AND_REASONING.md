# 06 — Exploiter l'intelligence et l'autonomie

## 1. Thèse

Un modèle avancé dispose de plus de connaissances procédurales qu'un prompt ne peut en contenir. Le rôle du prompt est de lui transmettre ce qu'il **ne peut pas savoir** (intention, contexte, contraintes, critères, limites de pouvoir) et de lui laisser ce qu'il **sait mieux faire** (méthode, ordre des étapes, choix techniques), sous réserve de vérification.

Preuves convergentes : [OFF] Anthropic (instructions générales > plans prescriptifs avec thinking ; ne pas sur‑spécifier le chemin dans les évaluations d'agents) ; [OFF] OpenAI Codex (retirer plans et préambules imposés qui provoquent des arrêts prématurés ; le modèle produit du code de haute qualité « sans longues instructions ») ; [OFF] Anthropic, context engineering (« bonne altitude » : ni logique if‑else fragile, ni consignes vagues).

## 2. Les huit équilibres

| Tension | Pencher vers la liberté quand… | Pencher vers le contrôle quand… | Formulation type |
|---|---|---|---|
| Instructions précises ↔ liberté | Le modèle a accès aux informations et la tâche est réversible | Contraintes métier invisibles, conformité | « Objectif + invariants ; méthode libre » |
| Objectifs ↔ méthode imposée | Plusieurs méthodes valides | La méthode est une exigence (audit, réglementation) | « Utilise la méthode X **car** l'auditeur l'exige » |
| Contrôle ↔ autonomie | Sandbox, tests, branches | Effets externes, irréversibles | Permissions techniques + liste d'actions sans approbation |
| Plan explicite ↔ plan natif | Diff simple ou exploratoire | Multi‑fichiers, incertain, humain veut valider | Plan mode / outil de plan natif, pas un plan dicté |
| Exécution directe ↔ validation préalable | Coût d'erreur faible | Coût d'erreur élevé | « Agis, puis demande l'acceptation des changements » (cas Cursor) |
| Initiative ↔ périmètre | Le propriétaire veut un code sain (« owner ») | Changements minimaux souhaités | Déclarer qui possède le code (Fable 5.2) |
| Exploration ↔ dérive | Problème ouvert | Budget serré | Critère d'arrêt de recherche + budget d'outils |
| Créativité ↔ déterminisme | Idéation, design | Sorties machine, conformité | Variantes demandées vs schéma strict |

## 3. Quand une méthode détaillée **réduit** la qualité

1. **Le modèle sait mieux.** Prescrire « lis d'abord A puis B puis C » empêche une découverte qui rendrait C inutile.
2. **La procédure contient une erreur.** Un modèle littéral la suit. Le défaut devient systématique.
3. **Arrêts prématurés.** Sur gpt‑5.3‑codex, plans et préambules imposés en prompt peuvent stopper l'exécution [OFF].
4. **Sur‑vérification et sur‑déclenchement.** Consignes « vérifie toujours », « utilise toujours l'outil X » → boucles et coût (Opus 4.6, Opus 5, cas Cursor) [OFF].
5. **Raisonnement contraint.** Formats de sortie stricts imposés avant la réflexion [CTR].
6. **Contradiction avec le harnais.** Une méthode écrite qui diverge des outils natifs (format ReAct textuel, plan textuel vs outil de plan).

**Quand la méthode reste utile** : conformité imposée ; connaissance métier non publique (« dans ce service, vérifier d'abord le cache Redis car… ») ; modèles légers ou locaux ; reproductibilité d'audit ; erreur récurrente mesurée.

## 4. Formuler objectifs, invariants et critères

### 4.1 Le triplet de base
```
Objectif : [résultat observable, pour qui, pourquoi]
Invariants : [ce qui doit rester vrai — vérifiable]
Critères de réussite : [conditions de fin, avec la vérification qui les prouve]
```

### 4.2 Transformer une procédure en critères

| Prescription (à éviter) | Critère (préférable) |
|---|---|
| « Ajoute un try/except autour de chaque appel réseau » | « Une panne réseau ne fait pas planter le processus ; test : couper le réseau, le service répond 503 » |
| « Lis tous les fichiers du dossier avant de commencer » | « Ne modifie pas de code que tu n'as pas lu » |
| « Fais une recherche sur 10 sites » | « Deux sources primaires indépendantes concordent, datées de moins de 6 mois » |
| « Écris d'abord le test, puis le code, puis refactorise » | « Un test reproduit le bug et échoue avant la correction ; il passe après » (le TDD reste utile comme **preuve**, pas comme rituel) |

### 4.3 Critères vérifiables : propriétés
- **Observables** (sortie, état, fichier), pas intentionnels (« de qualité »).
- **Associés à une vérification** (commande, comparaison, citation).
- **Hiérarchisés** (indispensables vs souhaitables).
- **Bornés** (que faire si un critère est inatteignable : signaler, pas tricher).

## 5. Permettre au modèle de remettre en question

Les modèles littéraux exécutent même une demande fondée sur une hypothèse fausse. Pour mobiliser leur jugement :

```
Si tu constates que la demande repose sur une hypothèse incorrecte, ou qu'une approche nettement
meilleure existe, dis-le avant de poursuivre, en une ou deux phrases, avec la preuve. Si l'écart est
mineur, poursuis selon la demande et signale-le dans le rapport.
```

Et pour les tests : « Si un test semble incorrect, signale‑le plutôt que de le contourner » ([OFF] Anthropic).

Limite : sur‑utilisé, ce droit produit des débats inutiles. Le réserver aux écarts qui changent le résultat.

## 6. Calibrer la proactivité (eagerness)

| Symptôme | Levier 1 (paramètre) | Levier 2 (prompt) | Levier 3 (environnement) |
|---|---|---|---|
| S'arrête trop tôt, propose de continuer | Monter l'effort | Consigne « Finishing work » (Fable 5.2) ; « persévère jusqu'à résolution » (OpenAI) | `/goal`, hook `Stop` |
| Demande trop de confirmations | — | Nommer les actions sans approbation ; donner le contexte produit (annulation possible — cas Cursor) | Auto mode, listes d'autorisation, sandbox |
| Agit trop (hors périmètre, irréversible) | Baisser l'effort | Seuils d'incertitude par outil ; « demande avant X » | Permissions, sandbox, approbation |
| Explore sans fin | Baisser l'effort | Critère d'arrêt (« dès que les résultats convergent ») ; budget d'appels avec échappatoire | Plafond de tours |
| Sur‑délègue | — | Bloc officiel de cadrage des sous‑agents | Description d'outil de délégation explicitant le coût |
| Sur‑ingénierie | — | « Ne fais que les changements demandés ; pas d'abstraction pour un usage unique » | Revue du diff |

Principe : essayer d'abord le **paramètre**, puis l'**environnement**, enfin le **texte** — le texte est le levier le moins fiable et le plus difficile à maintenir. [HYP fondée sur `01` P7]

## 7. Contrat d'autonomie (gabarit)

```
## Autonomie
Tu peux sans demander : lire tout fichier du dépôt, lancer les tests et le linter, créer et
modifier des fichiers dans src/ et tests/, créer des commits locaux sur la branche courante.
Demande avant : modifier une dépendance, changer une interface publique, supprimer un fichier
que tu n'as pas créé.
Ne fais pas (bloqué techniquement de toute façon) : push, accès réseau hors registres de paquets.
En cas d'obstacle ordinaire (erreur, timeout, test instable) : diagnostique et contourne avec les
moyens dont tu disposes. Ne t'arrête que pour une décision qui m'appartient ou une action listée
ci-dessus ; dans ce cas, continue le travail qui n'en dépend pas.
Hypothèses : fais des hypothèses raisonnables, liste-les dans le rapport final. Une hypothèse ne
vaut jamais permission pour une action listée « Demande avant ».
Fin : termine dans un état explicite — succès (avec preuves), partiel, bloqué ou plafond atteint —
en laissant un état reprenable ; hors succès, ne déclare pas la tâche réussie.
```

Ce gabarit applique : actions nommées plutôt que « agis librement » (Fable 5.2) ; exceptions explicites ; cohérence avec les permissions techniques ; continuation du travail indépendant ; états terminaux [R-AUTO-011] ; actions conditionnées aux permissions [R-AUTO-012].

## 8. Planification : explicite ou native ?

| Situation | Choix |
|---|---|
| Diff descriptible en une phrase | Pas de plan |
| Humain veut valider l'approche | Plan mode / outil de plan natif, plan édité par l'humain |
| Tâche longue non supervisée | Spec écrite (SPEC.md / PLANS.md) + état persistant ; le modèle planifie le détail |
| Modèle à effort `minimal`/`low` | Planification explicite courte utile ([OFF] GPT‑5 minimal reasoning) |
| `gpt-5.3-codex` via une intégration API qui ne conserve pas `phase` | Pas de plan ni de préambule demandés en prompt ; outil `update_plan` |
| Codex (client officiel) ou autre modèle (GPT‑6.2) | Suivre le guide du modèle utilisé ; ne pas hériter des consignes 5.3 |

## 9. Raisonnement : quoi demander, quoi ne pas demander

- **Demander** : de considérer des hypothèses concurrentes (recherche, débogage) ; de vérifier par un moyen externe ; de signaler son niveau de certitude **qualitativement** avec la raison (« non vérifié : la doc ne couvre pas la version 3 »).
- **Ne pas demander** : « réfléchis étape par étape » (natif) ; d'afficher le raisonnement (refus possible, non fidèle) ; une confiance chiffrée non calibrée (« confiance : 87 % ») — les probabilités verbalisées sont mal calibrées et les modèles tendent à la sur‑confiance (Xiong et al. 2023 [EMP]).
- **Contre les allers‑retours** : « Choisis une approche et tiens‑t'en ; ne reconsidère une décision que si une information nouvelle la contredit directement » ([OFF] Anthropic).

## 10. Créativité vs déterminisme

- Pour la créativité : demander explicitement l'ambition et les éléments voulus (les modèles récents ne font pas « plus » sans demande [OFF]) ; demander plusieurs variantes **différentes** sur un axe nommé ; éviter les exemples uniques qui ancrent.
- Pour le déterminisme : schéma, exemples couvrant les cas limites, effort bas, contrôles déterministes. Les paramètres d'échantillonnage (`temperature`) ne sont plus disponibles sur certains modèles récents [DOC] : le déterminisme vient du format et de la validation, pas de l'échantillonnage.
