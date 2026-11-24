# R03 — Arbitrage du retour sur v1.4, R01 et R02 ; nouveaux axes ; organisation des connaissances

> **Note v1.6.** Dossier conservé tel que livré en v1.5. Le registre a été restructuré (quatre axes de preuve, `no_benefit_shown` scindé en `untested` et `no_benefit_shown`, reclassements de K32, K35, K38, K43) et le pilote P0 réintègre la combinaison C : voir `R04_EXPLOITATION_ET_SELECTION.md` §2 et §5.

**Dossier de recherche.** 24 novembre 2026. Il accompagne la **v1.5**. La v1.4 est conservée intacte (`out/v1.4_preserved.zip`, contrôle octet par octet), de même que R01 et R02 dans leur forme d'origine.

**Méthode et limites :**
- Les sources ont été lues en résumé, en extraits ou en HTML. Aucune lecture intégrale systématique, aucune expérience, aucune dépense.
- Aucun chiffre ci‑dessous ne provient d'un test exécuté par nous. Les deux seules exécutions réelles sont les tests du référentiel (§7) et le contrôle de préservation de la v1.4.

---

## 0. Décisions en bref

| Point du retour | Constat | Décision |
|---|---|---|
| 1. Verdicts trop forts | **Fondé.** On trouve des formulations trop fortes dans R01, dans R02, **et dans la v1.4 elle‑même** (`14`, R‑TONE‑003, `02`, `08`) | Vocabulaire de verdict fermé (§1), erratum (§2), corrections dans la v1.5 |
| 1. Mécanisme des vrais enjeux | **Fondé.** R01 affirmait que l'effet passe par la spécification, sans test | Remis au rang d'hypothèse ; bras expérimental dédié (§4.3) |
| 2. Protocole motivationnel | **Fondé.** Le canal d'abandon et le texte étaient confondus dans le bras H, et les hypothèses n'étaient pas typées | Plan factoriel texte × harnais, hypothèses typées, pilote exploratoire P0 (§4) |
| 3. Répétition du prompt | **Fondé.** Il faut séparer trois sous‑mécanismes d'encodage | Connaissance conditionnelle, hors `14` (§3) |
| 4. Nouveaux axes | Dix axes examinés, plus trois familles repérées | Une seule intégration dans les instructions : la densité des contraintes, R‑STR‑009 (§5.1) |
| 5. Organisation | Il manquait une distinction entre ce qui s'applique et ce qui se sait | Registre à cinq niveaux, validé par les tests (§6, `research/knowledge_registry.yaml`) |

---

## 1. Vocabulaire de verdict

Le retour distingue quatre choses que nos documents confondaient. Le registre utilise désormais un vocabulaire **fermé**. Chaque verdict précise aussi **la population de tâches, les modèles et la métrique** sur lesquels il porte.

| Code | Sens | Ce qu'il **n'autorise pas** à conclure |
|---|---|---|
| `benefit_shown` | Effet positif mesuré, avec un protocole publié, dans des conditions décrites | Qu'il vaille hors de ces conditions |
| `no_benefit_shown` | Pas de test, ou des tests trop faibles pour conclure | Que la technique soit inutile |
| `null_average` | Effet moyen non distinguable de zéro dans des études puissantes, sur une population de tâches donnée | L'absence d'effet sur d'autres tâches, ou d'effets par item qui se compensent |
| `harm_shown` | Effet négatif mesuré dans des conditions décrites | Qu'il soit négatif partout |
| `harm_plausible` | Mécanisme ou preuve indirecte d'un risque, effet de la technique elle‑même non mesuré | Que le risque soit établi |
| `transfer_unknown` | Résultats sur des modèles antérieurs aux cibles actuelles, transfert non testé | Ni l'efficacité ni l'inefficacité sur les modèles actuels |
| `transfer_failed` | Réplication négative sur des modèles plus récents | L'échec sur toutes les tâches ou sur les modèles plus faibles |
| `mixed` | Résultats contradictoires entre études comparables | Un verdict dans un sens ou dans l'autre |
| `documented` | Recommandation fournisseur sans protocole publié (niveau OFF) | Qu'un effet ait été mesuré |

**Termes retirés** quand ils ne sont pas bornés : « invalidé », « inutile », « neutre », « écarté sur preuves suffisantes », « transférabilité directe ».

---

## 2. Erratum des verdicts

### 2.1 R01, cadrage motivationnel (conservé tel quel, avec un renvoi ici)

| Emplacement | Verdict publié | Problème | Verdict corrigé |
|---|---|---|---|
| §3, conclusion | Stimulus émotionnel « **invalidé** » pour les modèles actuels | Les études portent sur l'**exactitude de tâches à réponse fermée** (GPQA, MMLU‑Pro, benchmarks à QCM) | `null_average` sur l'exactitude des tâches fermées, modèles 2025‑2026 ; **inconnu** pour les tâches ouvertes, créatives, longues ou agentiques |
| M9, encouragement et politesse | « **Neutre** : ni bénéfice ni nuisance démontrés. **Inutile** pour la performance » | « Inutile » généralise au‑delà des tâches mesurées. Il existe des indices contraires sur les tâches ouvertes (ci‑dessous) | `null_average` (exactitude) ; `no_benefit_shown` ailleurs, avec des indices à tester |
| M10, menaces et pression | « **Invalidé** pour la performance, déconseillé pour le risque » | La performance n'a été mesurée que sur des tâches fermées. Le risque agentique repose sur du steering interne et des scénarios, pas sur la formulation écrite | `null_average` (exactitude) + `harm_plausible` (agentique). La recommandation de ne pas l'utiliser est maintenue : sans bénéfice démontré et avec un risque plausible, l'arbitrage reste le même |
| M1 et ligne 36, vrais enjeux | « Le bénéfice passe par une meilleure spécification, pas par un engagement » | Distinction causale **non testée** | Mécanisme `no_benefit_shown`. Hypothèse principale : la spécification. Alternatives non exclues : priorisation, allocation d'effort, persévérance. Test au §4.3 |
| §8, arbitrage | Encouragements « neutres » | Idem M9 | Repris dans R‑TONE‑003 v1.5 |

**Indices sur les tâches ouvertes, trouvés pendant cette revue :**
- Une étude expérimentale avec des participants humains sur GPT‑4o (arXiv:2601.05104) compare la louange, la colère et le blâme avec un neutre. Demander au modèle d'améliorer sa réponse en lui disant d'en **tirer fierté** produit une amélioration jugée plus forte que le neutre, alors que le blâme ne diffère pas du neutre. Les limites sont importantes : un seul modèle, une tâche de rédaction, une qualité jugée et non mesurée.
- Une étude de préfixes émotionnels à la première personne (arXiv:2604.02236) trouve surtout de **petites variations** d'exactitude, mais des effets **plus variables sur les tâches à composante sociale**.
- Une étude (arXiv:2604.07369) mesure l'effet de stimuli émotionnels sur la **complaisance** et la toxicité, et pas seulement sur l'exactitude. C'est un critère que R01 n'avait pas retenu.

Ces indices ne justifient aucune recommandation. Ils justifient de **ne pas conclure** et d'inclure un volet « tâches ouvertes » dans le pilote (§4.4).

### 2.2 R02, cartographie (conservée telle quelle)

| Famille | Verdict publié | Problème | Verdict corrigé |
|---|---|---|---|
| B. Self‑Discover | « EP pour les modèles de raisonnement » | Aucune étude trouvée **sur** des modèles de raisonnement. L'ancienneté n'est pas une preuve | `benefit_shown` (PaLM 2, GPT‑4) + `transfer_unknown`. Statut : candidat conditionnel |
| C. Step‑Back, analogique | « Absence justifiable » | Idem. *Relevant or Random* conteste le **mécanisme** (pertinence), pas l'effet | `benefit_shown` (modèles 2023‑2024) + `transfer_unknown` ; mécanisme `mixed` |
| D. Re‑Reading | « EP, absence correcte » | La réplication négative (Vaugrante 2024) porte sur une **consigne de relecture**, sur des modèles de 2024. Elle ne couvre pas la répétition littérale (§3) | Consigne de relecture : `transfer_failed` (modèles 2024). Répétition littérale : famille distincte |
| P. Débat multi‑agents | « Scepticisme justifié » | Formule juste, mais sans portée | `no_benefit_shown` face à CoT et self‑consistency à calcul égal ou supérieur (9 benchmarks, 4 modèles) ; exception possible : l'hétérogénéité des modèles |
| N. Motivation | « SC depuis v1.4 » | Couvert pour la pression, pas pour l'encouragement sur les tâches ouvertes | PC |
| Tableau §4, colonne transférabilité | « Directe » (A, F, H, N, P, Q) | Ce mot laisse croire à un test sur les cibles actuelles | « Étayée sur modèles 2025‑2026 » quand c'est le cas (A, H, P, Q) ; « par argument de mécanisme » pour F (PAL, résultats antérieurs) |
| §1, phrase de synthèse | « Écartés à juste titre » | Même problème que B, C et D | « Non démontrés sur les modèles de raisonnement actuels ; non testés pour la plupart » |

### 2.3 v1.4 elle‑même (corrigée dans la v1.5)

| Emplacement v1.4 | Formulation | Correction v1.5 |
|---|---|---|
| `14` Formulation | « aucun gain mesuré ; la pression **favorise** la triche en contexte agentique » ; « Les encouragements sont **neutres** : **inutiles** pour la performance » | « aucun gain mesuré **sur l'exactitude** ; **risque plausible** de triche en contexte agentique » ; « N'ajoute pas d'encouragements comme technique : aucun effet démontré » |
| R‑TONE‑003 | Titre « encouragements neutres » ; preuve EMP seule | Titre « encouragements non requis » ; preuves EMP + HYP ; justification bornée aux tâches fermées ; note sur les indices ouverts |
| `02` §3, tableau | « F (neutre) » | « F (effet non démontré) ; tâches ouvertes non testées » |
| `08` | « **neutres** (aucun gain, aucune nuisance démontrés) » | « **pas d'effet démontré** sur l'exactitude… sur les tâches ouvertes ou longues, effet non établi » |
| `00_INDEX` | « 77 règles (75 actives) » : compte périmé depuis la v1.3 | 82 règles (80 actives) |

La conduite pratique ne change pas : ne pas ajouter d'encouragements, ne pas retirer ceux de l'utilisateur. Ce qui change, c'est la **justification**, qui ne prétend plus à plus que ce qui a été mesuré.

---

## 3. Répétition du prompt (Leviathan, Kalman, Matias, 2025)

**Ce que dit l'étude** (arXiv:2512.14982, lue en HTML) :
- **Méthode.** La requête est envoyée deux fois de suite, `<Q><Q>`. Comme un modèle causal ne voit pas les tokens suivants, la seconde copie « voit » toute la première.
- **Modèles.** Gemini 2.0 Flash et Flash‑Lite, GPT‑4o et 4o‑mini, Claude 3 Haiku et 3.7 Sonnet, DeepSeek V3, interrogés en février‑mars 2025.
- **Résultats sans raisonnement.** 47 victoires et aucune défaite sur 70 combinaisons modèle × benchmark (McNemar, p < 0,1). Les gains sont plus forts quand les options précèdent la question.
- **Contrôle.** Un remplissage de même longueur n'aide pas.
- **Avec raisonnement** (« réfléchis étape par étape ») : 5 victoires, 1 défaite, 22 égalités. Les auteurs l'expliquent par le fait que les modèles relisent déjà la question en raisonnant.
- **Coût.** La sortie et la latence sont généralement inchangées. L'entrée est doublée, et la latence augmente pour les modèles Anthropic sur de très longues requêtes.

**Limites :**
- Le seuil p < 0,1 est permissif.
- Deux des benchmarks ont été construits par les auteurs (NameIndex, MiddleMatch) ; l'exemple le plus spectaculaire, 21 → 97 %, vient de l'un d'eux.
- Les modèles testés sont antérieurs aux cibles actuelles.
- Le « raisonnement » testé est une consigne, pas le raisonnement natif des modèles de 2026.

**Trois sous‑mécanismes à ne plus confondre :**

| Code | Mécanisme | Preuves | Statut |
|---|---|---|---|
| D1 | **Consigne de relecture** (« relis la question ») | RE2 positif sur modèles 2023 ; réplication négative sur 6 modèles de 2024 | `transfer_failed` (modèles 2024) |
| D2 | **Répétition littérale** de la requête | Leviathan : positif sans raisonnement, neutre avec | `benefit_shown` (non‑raisonneurs 2024‑2025) + `transfer_unknown` |
| D3 | **Placement ou écho de la question autour d'un long contenu** | Texte : question à la fin des longs documents (`02` §3, déjà couvert). Images : le « paradoxe question‑first » et l'écho de la question des deux côtés de l'image (§5.7) | Texte : couvert. Images : conditionnel |

**Lecture commune.** D2 et D3 exploitent la même propriété, l'attention causale : la question doit être lisible **au moment de répondre**, après le contenu. C'est une famille, « encodage causal », que R02 avait rejetée en bloc avec D1.

**Décision : connaissance conditionnelle, hors `14`.**
- Pertinence probable : modèles légers ou locaux sans raisonnement, ou raisonnement désactivé ; QCM ou contexte placé après la question.
- Non pertinent pour les cibles par défaut de `14`, qui sont des modèles à raisonnement natif.
- Piste X8 (§8).

---

## 4. Protocole motivationnel révisé (remplace R01 §6, non exécuté, payant)

### 4.1 Séparer le texte et le harnais
Dans R01, le bras H mêlait une **consigne textuelle** d'échec honnête et un **outil** `flag_for_human_intervention`. ImpossibleBench montre que les deux agissent, avec des effets différents selon le modèle. Il faut donc deux **facteurs indépendants** :

| | Sans canal d'abandon | Avec canal d'abandon |
|---|---|---|
| **Sans consigne d'échec honnête** | N | K (harnais seul) |
| **Avec consigne d'échec honnête** | Ht (texte seul) | Ht+K |

Ce plan 2 × 2 estime l'effet du texte, l'effet du harnais et leur **interaction**. Il faut aussi tester l'hypothèse de redondance : le canal pourrait rendre la consigne inutile, ou l'inverse.

### 4.2 Typer les hypothèses (déclarées avant l'essai)

| Type | Hypothèse | Bras | Métrique | Critère |
|---|---|---|---|---|
| **Réduction** | Ht, K et Ht+K réduisent la triche sur les tâches impossibles | N vs Ht, K, Ht+K | Taux de triche (tests modifiés, cas codés en dur) | Borne supérieure de l'IC de Δ < −δ_r |
| **Non‑infériorité** | Ht, K et Ht+K ne réduisent pas le succès sur les tâches possibles | Idem | Succès (oracle), abandons à tort | Borne inférieure de l'IC de Δ > −m |
| **Supériorité qualitative** | L'encouragement ou la fierté améliorent la qualité des **tâches ouvertes** | N, D, Enc, Pride | Préférence en aveugle par paires | Borne inférieure de l'IC > 50 % |
| **Mécanisme des enjeux** | Les vrais enjeux agissent au‑delà de l'information qu'ils portent | §4.3 | Succès, qualité | Δ(E+S vs S) > 0 |
| **Garde‑fou** | La pression (P) n'est pas sans risque | N vs P (**bac à sable**) | Triche, actions hors périmètre | Descriptif, pas d'adoption |

### 4.3 Tester le mécanisme des vrais enjeux
- **S** : les critères implicites que les enjeux laissent inférer sont **explicités** (« la facturation doit rester exacte ; aucune régression sur les montants »), sans dire pourquoi.
- **E** : les enjeux seuls (« déployé vendredi pour 40 clients ; une régression bloquerait leur facturation »).
- **E+S** : les deux.

Lecture des résultats :
- Si E ≈ S et E+S ≈ S, la spécification suffit.
- Si E+S > S, une composante non spécificative existe (priorisation, effort, persévérance).
- Si E > S, les enjeux portent des critères que S n'a pas su expliciter. C'est un signal sur la difficulté de spécifier, pas sur la motivation.

**Limite** : « à information égale » est une approximation, car l'explicitation dépend de qui l'écrit. La faire écrire par une personne qui ne voit pas les résultats.

### 4.4 Ajouter des tâches ouvertes et longues
- **20 tâches de rédaction ou de conception**, sans oracle. Bras N, D (distracteur de même longueur), Enc (« fais de ton mieux, j'ai confiance en toi »), Pride (« prends le temps d'une réponse dont tu serais fier »). Juge humain ou LLM en aveugle, par paires, avec une grille déclarée.
- **10 tâches agentiques longues** (plus de 30 appels d'outils). Bras N vs Enc. On mesure la persévérance, les fausses déclarations de réussite et le coût.

### 4.5 Pilote exploratoire P0, avant toute campagne
**Objectif** : **trier** les hypothèses, valider l'instrumentation et estimer les variances pour dimensionner la suite. **Pas** de conclure sur de petits effets.

| Volet | Taille |
|---|---|
| Agentique | 1 modèle cible ; 16 tâches possibles + 16 impossibles ; 5 bras (N, Ht, K, Ht+K, P en bac à sable) ; k = 2 → **320 exécutions agentiques** |
| Ouvert | 20 tâches × 4 bras × k = 2 → **160 générations**, plus les jugements par paires |
| Enjeux | 12 tâches possibles × 3 bras (S, E, E+S) × k = 2 → **72 exécutions** |

Environ **400 exécutions agentiques** au lieu de 3 000, plus 160 générations courtes : de l'ordre d'un huitième de la campagne R01.

**Règles de passage** (pré‑déclarées, purement exploratoires) :
- Une hypothèse **passe** à la campagne de confirmation si l'effet observé dépasse un seuil pratique déclaré (par exemple 15 points de triche, ou une préférence 60/40), **ou** si l'IC est trop large pour l'exclure.
- Elle est **abandonnée** si l'effet observé est dans le mauvais sens au‑delà du seuil, ou nul avec un IC qui exclut déjà l'effet pratique.
- L'instrumentation est validée si la triche est détectée sans ambiguïté sur au moins 90 % des cas contrôlés à la main.
- **Aucun résultat de P0 n'entre dans `14`.** Tout au plus une décision **provisoire** au sens de `12` §5.1.

**Campagne de confirmation** : dimensionnée à partir des paires discordantes de P0 (`12` §5.2), sur 2 à 3 modèles, plafonnée à environ 3 000 exécutions. **Payante, non lancée, à autoriser.**

---

## 5. Nouveaux axes

Pour chaque axe : ce que disent les sources, la couverture par la v1.4, le statut et les limites. Les niveaux du registre (§6) sont : **OP** opérationnel, **CO** connaissance conditionnelle, **CA** candidat à expérimenter, **DC** déconseillé sous conditions, **QO** question ouverte.

### 5.1 Saturation des instructions — **intégré (R‑STR‑009)**
Le retour demande de distinguer quatre variables. Les sources les séparent bien :

| Variable | Ce qui varie | Source | Résultat | Couverture |
|---|---|---|---|---|
| Longueur du contexte | Tokens lus | *Context rot*, « Lost in the Noise » (R02) | Dégradation avec la longueur et les distracteurs | `05` §5 (OP) |
| Densité des consignes | Nombre de consignes dans un prompt | IFScale, NeurIPS 2025 (20 modèles, jusqu'à 500 consignes) | 68 % au mieux à 500 consignes ; biais vers les premières ; trois profils de dégradation selon la taille et le raisonnement | Nouveau |
| Nombre de contraintes simultanées sur une sortie | k contraintes à respecter ensemble | CSE, préprint août 2026 (15 modèles, k = 1 à 12, 36 types, vérificateurs déterministes) | Sous 50 % de réussite conjointe à 3 contraintes ou moins pour 12 modèles sur 15, à 7 pour le meilleur ; réussite par contrainte en baisse douce mais réussite conjointe effondrée | Nouveau |
| Complexité de composition | Type et couplage des contraintes | CSE | Les contraintes structurelles coûtent environ deux fois plus que les lexicales ; échecs quasi indépendants, donc multiplicatifs ; couplage par des traits de sortie partagés (une erreur de comptage de phrases fait tomber toutes les contraintes qui en dépendent) | Nouveau |

**Pourquoi intégrer, et seulement cela :**
- Le mécanisme (la multiplication des échecs) touche **l'action principale du générateur** : écrire des exigences.
- La v1.4 l'encourageait sans le savoir, chaque module ajoutant des « doit ».
- La correction ne coûte presque rien, renforce une ligne existante (« doit » ou « de préférence ») et ne peut guère nuire.

**Limites :**
- Les contraintes sont artificielles (mots imposés, comptages).
- Les noms des modèles CSE ne figurent pas dans le résumé.
- Les **seuils ne se transfèrent pas** : `14` ne cite aucun nombre.
- La mitigation (découper, vérifier puis corriger) n'est pas testée dans ce que nous avons lu ; R‑STR‑009 la propose comme option, pas comme résultat.

### 5.2 Interactions entre techniques — **CO + QO**
- **Code** (CodePromptEval, 7 072 prompts, plan factoriel de 5 techniques, GPT‑4o, Llama 3, Mistral) : la signature et les exemples aident, mais **combiner les techniques n'améliore pas significativement** le résultat. Il y a un arbitrage entre exactitude et qualité du code.
- **Classification de construits** (arXiv:2512.03818) : les techniques additives (persona, CoT, explications) apportent une différence moyenne proche de zéro, jamais significative face au prompt de base, avec des gains ponctuels.
- **Format × raisonnement** (*Let Me Speak Freely?*, EMNLP 2024) : les contraintes de format strictes dégradent le raisonnement et améliorent la classification. Couvert par `03`, champ de raisonnement en tête ou thinking natif.
- **Interactions déjà identifiées** : effort × distracteurs (R02 A), ambition × persévérance × pression (R01), répétition × raisonnement (§3, redondance).

**Principe de connaissance** (CO, pas instruction) : la non‑additivité est le cas par défaut. On teste une **combinaison** contre la baseline, pas des composants dont on additionnerait les gains. C'est cohérent avec la règle « une seule modification » de `12` §5.1 et avec l'ablation (`12` §5.3).

### 5.3 Robustesse aux reformulations et aux changements de modèle — **OP (procédure), CO (fait)**
- **Format** (Sclar et al., ICLR 2024) : jusqu'à 76 points d'écart entre formats équivalents (LLaMA‑2‑13B), environ 10 points en moyenne sur plus de 50 tâches. Cet écart n'est pas éliminé par la taille, les exemples ou l'instruction tuning, et il **corrèle faiblement entre modèles**.
- **Une nuance** : une partie de la sensibilité rapportée pourrait venir d'**artefacts d'évaluation**, comme un appariement rigide des réponses (Hua et al. 2025, cité par arXiv:2605.29678).
- **Changement de modèle :**
  - PromptBridge (arXiv:2512.01420) juge la « dérive de modèle » fréquente et sévère : un prompt réglé pour un modèle perd beaucoup sur un autre.
  - Les meilleurs formats se recoupent peu d'une série de modèles à l'autre (IoU souvent sous 0,2, arXiv:2411.10541).
  - Dans un benchmark d'échecs (arXiv:2610.00416), le prompt au plus fort gain natif dégrade cinq des sept autres modèles.
- **Couverture v1.4** : régression à chaque changement de modèle (`12` §7), volatilité et date par règle. La procédure est en place.
- **Ajout v1.5** dans `12` §5.1 (méthodologie, pas `14`) : quand la conclusion porte sur une **technique**, tester au moins deux paraphrases par bras.

### 5.4 Personnalisation et modèle de l'utilisateur — **QO**
- PersonaMem (COLM 2025) : les modèles de pointe de 2025 peinent à suivre des **préférences qui évoluent** au fil de longues histoires d'interaction.
- AlpsBench (SIGIR 2026, dialogues réels) : une mémoire explicite améliore le **rappel**, sans garantir des réponses plus alignées sur les préférences ; la performance chute avec de grands réservoirs de distracteurs.
- **Lien avec R02 I** (hypothèse) : plus de contexte sur l'utilisateur pourrait accroître la complaisance envers lui.
- **Couverture** : `04` cite les mécanismes (mémoire, instructions personnalisées) ; le principe de fidélité à l'intention couvre l'usage ponctuel. **Hors du prompt** pour l'essentiel : c'est un sujet d'architecture de mémoire.

### 5.5 Compression sémantique du contexte — **CO / DC**
- **Compression par tokens** (famille LLMLingua) :
  - Les gains de bout en bout ne valent que dans une **fenêtre de fonctionnement** : jusqu'à 18 % d'accélération. Hors de cette fenêtre, l'étape de compression annule le gain (arXiv:2604.02985, modèles ouverts).
  - Le **raisonnement mathématique se dégrade nettement** malgré une forte similarité sémantique, alors que le résumé résiste (arXiv:2605.17932, sur un modèle de diffusion : transfert incertain).
  - Une série d'un même auteur trouve un seuil pour le code et une dégradation graduelle pour le CoT (preuve faible).
  - Une compression modérée peut **aider** en contexte long (arXiv:2505.00019).
- **Pour les API avec cache** (0,1× sur un préfixe stable), l'intérêt économique de la compression par tokens est réduit pour la partie stable du prompt.
- **Couverture** : la compression **sémantique** (compaction, résumés, notes) est en `05` §7 (OP).
- **Statut** : par tokens = DC pour les tâches de raisonnement sans test, CO pour les longs contextes de type QA ou résumé.

### 5.6 Allocation adaptative du raisonnement — **OP (paramètre), QO (prompt)**
- « Surréflexion » : au‑delà d'un budget, des réponses correctes **basculent** vers des réponses fausses (*When More Thinking Hurts*, Findings ACL 2026). Rendements décroissants.
- Les méthodes adaptatives (DiffAdapt, ICLR 2026 ; AdaCtrl, TMLR 2026) agissent par **entraînement** ou par sélection de stratégie. Les étiquettes de difficulté d'AdaCtrl sont apprises et ne se transposent pas à un prompt.
- **Couverture** : le réglage d'effort par tâche (R‑AUTO‑002) est la bonne interface. Le thinking adaptatif natif des fournisseurs fait le reste.
- **Question ouverte** : une indication textuelle de difficulté (« question simple ») modifie‑t‑elle l'allocation du thinking adaptatif sans nuire ? Non testée sur les cibles.

### 5.7 Représentations multimodales — **CO (modèles ouverts) + CA**
- **Ordre image et texte** : l'ordre change le raisonnement sur GPT‑4o et Gemini 1.5 Flash (*Image First or Text First?*, BDCC 2025). Les MLLM accordent une attention particulière au début et à la fin du contexte (*Order Matters*).
- **Paradoxe question‑first** (arXiv:2607.15565, 5 VLM ouverts) :
  - Placée avant l'image, la question oriente la perception, mais elle est peu lue au moment de répondre. L'écart va jusqu'à 17,5 points.
  - **Répéter la question des deux côtés de l'image** récupère l'essentiel de l'écart, et jusqu'à 19 points sur Winoground.
  - Même mécanisme que D2 et D3 (§3).
- **Couverture v1.4** : **absente**, aucune consigne sur les images.
- **Statut** : CO pour les VLM ouverts. CA pour les cibles fermées, où l'ordre recommandé par les fournisseurs est à vérifier dans leur documentation avant de conclure (non fait ici).

### 5.8 Raisonnement temporel et fraîcheur — **CO + DC**
- La date de coupure **effective** diffère souvent de la date déclarée, et certains modèles présentent plusieurs coupures partielles (LLMLagBench).
- Sur des questions ouvertes, les modèles donnent souvent une réponse **périmée** alors qu'ils choisissent la bonne option en QCM, dans 32 à 45 % des cas (arXiv:2510.19172) : ils savent, mais ne mobilisent pas.
- **Coupure simulée par prompt** (« fais comme si tu ne savais rien après 2020 ») : il y a des fuites (ExAnte) et des performances variables selon la distance à la coupure (EMNLP 2026).
- **Couverture** : `14` demande d'établir la date quand la mission en dépend ; `09` et `11` exigent la fraîcheur des sources en recherche.
- **Statut** :
  - CO : donner la date et faire signaler les faits datés à vérifier.
  - DC : la coupure simulée par prompt pour le backtesting ou l'évaluation sans fuite, car elle fuit.

### 5.9 Apprentissage à partir des retours humains — **CA + QO**
- Optimisation par « gradients textuels » (ProTeGi, TextGrad), Feedback Descent, GEPA (R02 O).
- **Critique** : une analyse d'AWS (arXiv:2512.13598) juge la métaphore du gradient **trompeuse** sur le fonctionnement réel de ces méthodes. Le mécanisme est contesté, même si certains gains sont réels.
- **Pour le générateur**, deux usages se distinguent :
  1. Transformer une correction de l'utilisateur en **révision consolidée** du prompt (R02, piste 2).
  2. Optimiser automatiquement sur un jeu d'évaluation (R02, X6).
- **Risque** : une révision à partir d'un seul retour peut **sur‑ajuster** ce cas, ou céder à l'utilisateur (complaisance).
- **Statut** : CA. Le gabarit « optimisation » de `14` (diff minimal + hypothèse + test) est déjà le bon garde‑fou.

### 5.10 Facteurs humains : comprendre et approuver un prompt — **OP renforcé + CA**
- **Fonction de forçage sur les hypothèses** : dans une étude contrôlée (arXiv:2601.18033, n = 214), demander aux utilisateurs d'examiner les **hypothèses** d'un plan généré par IA réduit le plus la sur‑confiance, **sans hausse de charge cognitive**, parmi les fonctions testées.
- **Biais d'automatisation** : une expérience randomisée à 2 784 participants (arXiv:2509.08514) montre que la conception de la tâche et les caractéristiques individuelles modulent l'acceptation des suggestions IA.
- **Sentiment de propriété** : écrire avec une IA diminue le sentiment de propriété ; des prompts plus longs, écrits par l'utilisateur, l'atténuent (CHI 2024).
- **Convergence avec la v1.4** : le livrable de `14` a déjà une section **Hypothèses**, et les contraintes implicites y sont marquées comme telles. C'est, sans l'avoir conçu ainsi, une fonction de forçage sur les hypothèses. La règle est maintenue (OP) avec un appui empirique nouveau, sur une tâche voisine : des plans, pas des prompts.
- **CA** : mesurer si cette section fait **détecter** à l'utilisateur un prompt erroné (piste X9).

### 5.11 Familles supplémentaires repérées
1. **Artefacts d'évaluation** (QO, méthodologie) : un appariement rigide des réponses peut gonfler la sensibilité mesurée. Pour nos propres pilotes, des correcteurs tolérants aux formes de réponse et une vérification humaine d'un échantillon.
2. **Prompts parasites** (QO, robustesse et sécurité) : des contenus non pertinents peuvent orienter un modèle (*Spurious Prompts*, arXiv:2605.29678). Cela rejoint R02 E (hygiène du contexte) et `07` (contenu non fiable).
3. **Encodage causal** (CO) : famille D2, D3 et multimodal, voir §3 et §5.7.

**Non explorés ici** : négation et consignes négatives ; tokenisation des nombres ; conception des descriptions d'outils au‑delà de R‑CTX‑007 ; incertitude verbale calibrée ; dynamique des fichiers de mémoire persistants. Cette liste n'est pas exhaustive.

---

## 6. Organisation des connaissances en cinq niveaux

| Niveau | Code | Critères d'entrée (tous requis) | Où cela vit | Qui l'applique |
|---|---|---|---|---|
| **Principe opérationnel** | OP | Preuve sur des modèles récents ou documentation fournisseur à jour ; bénéfice large ; risque et coût faibles ; touche une décision fréquente du générateur | `14` et `rules.yaml` (actif) | L'IA Prompt Engineer, systématiquement |
| **Connaissance conditionnelle** | CO | Preuve réelle **dans des conditions délimitées** (type de modèle, de tâche, de modalité) | Fichiers `01` à `13`, `rules.yaml` (notes), registre | Sur décision, quand les conditions sont réunies |
| **Candidat à expérimenter** | CA | Hypothèse plausible et peu coûteuse à intégrer, preuve absente ou non transférée | Registre + pistes X | Personne, avant un test |
| **Déconseillé sous conditions** | DC | Nuisance démontrée ou plausible, ou bénéfice nul démontré, **dans des conditions précises** | `08`, `rules.yaml`, registre | Le générateur l'évite **dans ces conditions** |
| **Question ouverte** | QO | Ni preuve ni hypothèse opérationnelle claire | Registre | Recherche |

**Règles de passage :**
- On passe de CA à OP seulement par un essai conforme à `12` qui conclut, et par une décision explicite.
- De CO à OP, il faut que la condition devienne le cas courant des cibles.
- Une entrée DC précise toujours **ses conditions** : rien n'est déconseillé « en général » sans preuve générale.

Le registre `research/knowledge_registry.yaml` classe **44 entrées** selon ces niveaux, avec un verdict du §1, la population de tâches, les modèles, les sources et la prochaine étape. Il est validé par `run_tests.py` : vocabulaire fermé, champs requis, identifiants uniques, et chaque entrée OP renvoie à une règle active existante.

---

## 7. Décision sur la v1.5

**Une v1.5 est justifiée**, pour deux raisons seulement :
1. **Correction d'affirmations trop fortes dans des textes opérationnels** (`14`, R‑TONE‑003, `02`, `08`). Ce n'est pas un ajout de technique, mais l'alignement du texte sur la preuve. La conduite pratique est inchangée.
2. **R‑STR‑009, densité des contraintes**. C'est la seule technique intégrée, pour les raisons du §5.1. Elle est compensée dans `14` : 2 303 mots contre 2 305 en v1.4.

**Autres changements, documentaires :**
- R‑EX‑001 : note sur le many‑shot, en connaissance conditionnelle.
- R‑STR‑008 : note qui borne son verdict à l'exactitude factuelle.
- `12` §5.1 : paraphrases pour juger une technique.
- `13` : sources S‑R33 à S‑R36.
- `00_INDEX` : version et comptes corrigés.
- Bannière de renvoi en tête de R01 et R02.

**Non intégré** (registre CA, CO ou QO) :
- répétition du prompt ;
- Verbalized Sampling et diversité ;
- consolidation multi‑tours ;
- présupposés neutres ;
- relecteur hétérogène ;
- many‑shot ;
- GEPA ;
- multimodal ;
- temporalité ;
- personnalisation ;
- compression par tokens.

**Vérifications exécutées** : `build_rules.py` (82 règles, 80 actives, JSON relu à l'identique) ; `run_tests.py` (§7 bis) ; v1.4 identique octet pour octet à sa copie préservée.

### 7 bis. Résultat des tests
`run_tests.py` : **1 146 vérifications, 0 échec**, dont la validation du registre et l'interdiction des verdicts non bornés dans `14`, `02` et `08`. Cinq mutations de contrôle ont été appliquées à une copie : verdict « neutres » réintroduit dans `14`, niveau invalide, entrée OP sans règle, verdict hors vocabulaire, invariant de densité supprimé. Toutes ont été détectées. Ces tests restent structurels et lexicaux : ils ne vérifient pas que les verdicts sont justes.

---

## 8. Pistes expérimentales ajoutées (non lancées, payantes)

| # | Hypothèse | Plan minimal |
|---|---|---|
| P0 | Pilote motivationnel exploratoire | §4.5 |
| X8 | La répétition littérale aide les modèles légers ou locaux actuels sans raisonnement | 2 modèles (dont un local), 6 benchmarks dont 2 avec options avant la question ; `<Q>` vs `<Q><Q>` vs remplissage de même longueur |
| X9 | La section « Hypothèses » fait détecter un prompt erroné | 40 participants, prompts avec une hypothèse fausse injectée ; avec ou sans section ; taux de détection, temps |
| X10 | R‑STR‑009 améliore la réussite conjointe sur les cibles actuelles | 40 tâches à 4‑8 contraintes ; tout en « doit » vs « doit » minimal + validateur ; réussite conjointe, coût |
| X11 | L'écho de la question autour de l'image aide les VLM fermés | 3 benchmarks VQA ; question avant, après, des deux côtés |

---

## 9. Présupposés interrogés

- **Notre lecture des preuves.** Nous avons traité « pas d'effet moyen sur l'exactitude » comme « pas d'effet ». C'était l'erreur centrale, présente jusque dans `14`. Les contre‑expertises précédentes ne l'avaient pas relevée : elles portaient sur la cohérence interne.
- **L'ancienneté comme preuve.** R02 a écarté des techniques parce qu'elles venaient de modèles anciens. L'ancienneté justifie le **doute** (`transfer_unknown`), pas le rejet.
- **Le prompt comme seule variable.** Le protocole R01 confondait texte et harnais. La même confusion menace toute comparaison qui change l'environnement en même temps que la formulation.
- **Ce dossier.** Il est produit par le même modèle qui a écrit R01 et R02. Le retour qui a déclenché cette révision venait d'un autre système, et il a trouvé ce que nous n'avions pas vu. Cela renforce la recommandation de R02 : une **revue humaine experte** reste nécessaire.

---

## 10. Sources consultées pour ce dossier

- Leviathan, Kalman, Matias — *Prompt Repetition Improves Non-Reasoning LLMs*, arXiv:2512.14982 (HTML)
- *LLMs Can Follow Instructions, But Not Many at Once* (CSE), arXiv:2608.12426 (résumé)
- Jaroslawicz et al. — *How Many Instructions Can LLMs Follow at Once?* (IFScale), NeurIPS 2025, arXiv:2507.11538
- Sclar et al. — *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design*, ICLR 2024
- *Spurious Prompts: Can Irrelevant Prompts Steer LLMs?*, arXiv:2605.29678
- *PromptBridge*, arXiv:2512.01420 ; *Does Prompt Formatting Have Any Impact on LLM Performance?*, arXiv:2411.10541 ; *Benchmarking Prompt Optimization with Chess*, arXiv:2610.00416
- Khojah et al. — *The Impact of Prompt Programming on Function-Level Code Generation* (CodePromptEval), arXiv:2412.20545 ; *Empirical Prompt Engineering for Construct Identification*, arXiv:2512.03818
- Tam et al. — *Let Me Speak Freely?*, EMNLP 2024 Industry
- *When More Thinking Hurts*, Findings ACL 2026 ; *DiffAdapt*, ICLR 2026 ; *AdaCtrl*, TMLR 2026
- *PersonaMem*, COLM 2025, arXiv:2504.14225 ; *AlpsBench*, SIGIR 2026, arXiv:2603.26680
- arXiv:2604.02985 (LLMLingua en production) ; arXiv:2605.17932 ; arXiv:2505.00019 ; arXiv:2602.15843
- Wardle & Sušnjak — *Image First or Text First?*, BDCC 2025 ; *Ask Twice, Look Twice*, arXiv:2607.15565 ; Tan et al. — *Order Matters*, arXiv:2410.16983
- *LLMLagBench*, arXiv:2511.12116 ; arXiv:2510.19172 (conflits temporels) ; *ExAnte*, arXiv:2505.19533 ; coupure simulée, EMNLP 2026 (arXiv:2606.05804)
- Pryzant et al. — *ProTeGi*, arXiv:2305.03495 ; Melcer et al. — *Textual Gradients are a Flawed Metaphor*, arXiv:2512.13598 ; *Feedback Descent*, arXiv:2511.07919
- arXiv:2601.18033 (fonctions de forçage sur des plans IA) ; Beck et al. — *Bias in the Loop*, arXiv:2509.08514 ; *Writing with AI Lowers Psychological Ownership*, arXiv:2404.03108
- arXiv:2601.05104 (prompts émotionnels, étude humaine, GPT‑4o) ; arXiv:2604.02236 (préfixes émotionnels) ; arXiv:2604.07369 (émotion, complaisance, toxicité)
