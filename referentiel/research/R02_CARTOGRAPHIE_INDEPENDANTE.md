# R02 — Cartographie indépendante des mécanismes et des angles morts

> **Note v1.5.** Dossier conservé tel que livré. Plusieurs statuts sont plus forts que les sources (« EP », « directe », « écartés à juste titre ») : voir l'erratum en `R03_ARBITRAGE_ET_NOUVEAUX_AXES.md` §2.2.

**Dossier de recherche.** 24 novembre 2026. **Le référentiel n'est pas modifié** : la v1.4 est conservée intacte, et ce dossier ne produit aucune nouvelle version.

**Méthode, et ses limites :**
- La cartographie part des mécanismes, pas des catégories du référentiel.
- Elle s'appuie sur une taxonomie externe (*The Prompt Report*, Schulhoff et al., 58 techniques textuelles) et sur environ 25 sources primaires.
- Les sources ont été lues en résumé et en extraits ; aucune lecture intégrale, aucune expérience, aucune dépense.
- La comparaison porte sur la v1.3, comme demandé. Les ajouts de la v1.4 (R01) sont signalés quand ils changent le statut d'une famille.

---

## 1. Constat principal

La recherche confirme l'inquiétude. Les quatre versions et les trois contre‑expertises partageaient un **cadre implicite** :
- une tâche unique et bien posée ;
- une réponse unique attendue ;
- une qualité mesurée par l'exactitude ou par la réussite d'un agent de code.

Ce cadre a laissé dans l'ombre cinq familles, qui sont aussi celles où la littérature récente montre les effets les plus nets :

1. **La diversité et la créativité.** Les modèles alignés convergent vers des réponses typiques (« mode collapse »). Des techniques simples et bien étayées le corrigent ; le référentiel n'en mentionne aucune.
2. **La dynamique multi‑tours.** La performance chute fortement quand une demande se précise au fil des échanges, et les modèles « ne s'en remettent pas ».
3. **L'épistémique sociale.** Complaisance (sycophancy), effets de cadrage, influence des opinions de l'utilisateur présentes dans le contexte.
4. **L'optimisation adaptative pour les tâches répétées.** L'optimisation réflexive de prompts (GEPA) bat le renforcement à budget de déploiements bien moindre ; le référentiel ne la traite qu'en une ligne.
5. **L'échelle des exemples.** Le « many‑shot » (des centaines d'exemples) change de nature par rapport au few‑shot. Le référentiel plafonne implicitement à 2 à 5 exemples.

À l'inverse, plusieurs techniques célèbres, absentes ou écartées par le référentiel, le sont **à juste titre** pour les modèles de raisonnement actuels :
- le CoT manuel ;
- Re‑Reading ;
- le débat multi‑agents ;
- Step‑Back et Self‑Discover, qui sont surtout pertinents pour les modèles sans raisonnement natif.

---

## 2. Cartographie des mécanismes, indépendante du référentiel

Les mécanismes sont classés selon **ce qu'ils modifient**, quel que soit le nom de la technique.

| Dimension | Mécanisme | Techniques représentatives |
|---|---|---|
| **A. Allocation du raisonnement** | Profondeur et durée de calcul à l'inférence | Effort, CoT, self‑consistency, best‑of‑N, test‑time scaling |
| **B. Structuration du raisonnement** | Organisation du chemin de résolution | Décomposition, least‑to‑most, plan‑and‑solve, Self‑Discover, Tree/Graph of Thoughts |
| **C. Abstraction et analogie** | Changement de niveau, transfert | Step‑Back, analogical prompting, principes d'abord |
| **D. Encodage de l'entrée** | Façon dont la question est « lue » | Re‑Reading (RE2), Rephrase‑and‑Respond, position, format |
| **E. Hygiène du contexte** | Ce qui est lu et ce qui distrait | System 2 Attention, filtrage, contexte minimal, RAG |
| **F. Délégation du calcul** | Ce qui ne doit pas être « raisonné » par le modèle | PAL / Program‑of‑Thought, outils, solveurs |
| **G. Vérification** | Confrontation à une référence | Oracles, Chain‑of‑Verification, auto‑critique, relecteur, méthodes formelles |
| **H. Épistémique** | Rapport à l'incertitude et aux sources | Abstention, citations, calibration, corroboration |
| **I. Épistémique sociale** | Influence de l'interlocuteur | Complaisance, cadrage, opinions dans le prompt, contradiction de l'utilisateur |
| **J. Diversité et créativité** | Étendue de l'espace de réponses exploré | Verbalized Sampling, prompting multilingue, personas comme indices d'échantillonnage, divergent / convergent |
| **K. Linguistique** | Langue, registre, pragmatique | Langue du prompt, force pragmatique, ton |
| **L. Interaction et multi‑tours** | Accumulation et révision de l'intention | Clarification, consolidation, dérive, perte en conversation |
| **M. Apprentissage en contexte** | Quantité et nature des exemples | Zero‑ / few‑ / many‑shot, exemples auto‑générés |
| **N. Comportement et motivation** | Politique d'action | Persévérance, ownership, échec honnête, pression (→ R01) |
| **O. Adaptation et optimisation** | Amélioration du prompt par les données | APE, OPRO, DSPy / MIPRO, GEPA, metaprompting |
| **P. Architecture et social multi‑agents** | Plusieurs instances | Délégation, débat, hétérogénéité des modèles |
| **Q. Contrôle et cybernétique** | Boucles fermées, régulation | Oracles, hooks, plafonds, canaux d'abandon, environnement |
| **R. Interne (non textuel)** | Activations, entraînement | Steering, persona vectors, fine‑tuning |
| **S. Facteurs humains** | L'humain dans la boucle | Biais d'automatisation, fatigue d'approbation, lecture des prompts |

---

## 3. Fiches d'évidence par famille

Légende des statuts, rapportés à la v1.3 :
- **SC** : suffisamment couvert.
- **PC** : partiellement couvert.
- **AB** : absent.
- **EP** : écarté sur preuves suffisantes.
- **EH** : écarté sur hypothèses fragiles.
- **PE** : prometteur, à expérimenter.

### A. Allocation du raisonnement — **SC** (nuance à ajouter)
- **Preuves.** Pour les modèles de raisonnement, le CoT explicite apporte des gains **négligeables** qui ne justifient pas le temps ajouté. Pour les modèles sans raisonnement, il apporte un petit gain mais une **variabilité** qui provoque des erreurs sur des questions autrement réussies (Meincke et al., *Prompting Science Report 2*, 2025 : GPQA Diamond, 25 essais par condition).
- **Inverse scaling.** Raisonner plus longtemps **dégrade** la performance sur certaines tâches : comptage avec distracteurs, corrélations fallacieuses, déduction avec contraintes. Les modèles Claude se laissent davantage distraire par l'information non pertinente (Gema et al., TMLR 2025). Une étude de 2026 trouve qu'avec des **distracteurs**, tous les modèles et benchmarks testés montrent un inverse scaling.
- **Écart avec le référentiel.** Le réglage d'effort (R‑AUTO‑002) et le CoT déclaré obsolète sont justes. Il manque **l'interaction effort × hygiène du contexte** : un effort élevé sur un contexte bruité peut aggraver la situation.

### B. Structuration du raisonnement — **PC / EP pour les modèles actuels**
- **Self‑Discover** (NeurIPS 2024) : le modèle compose lui‑même une structure à partir de modules (« décomposer », « penser de façon critique »…). Il dépasse CoT‑Self‑Consistency de plus de 20 % avec 10 à 40 fois moins de calcul, mais **sur PaLM 2 et GPT‑4**.
- Pour les modèles de raisonnement, rien ne montre qu'une structure explicite fasse mieux que le raisonnement natif. Le référentiel déconseille déjà les procédures imposées.
- **Statut.** EP pour les modèles de raisonnement ; PE seulement pour les modèles légers ou locaux sans raisonnement natif. Mécanisme intéressant à retenir : la structure est **choisie par le modèle**, pas par l'humain. Cela converge avec le principe « le résultat, pas le chemin ».

### C. Abstraction et analogie — **AB, justifiable**
- **Step‑Back** : +7 et +11 % (MMLU physique, chimie), +27 % (TimeQA) **sur PaLM‑2L**, 2023.
- **Analogical prompting** (ICLR 2024) : le modèle génère lui‑même des exemples ; il bat le CoT zéro‑shot et le few‑shot manuel sur GPT‑3.5/4 et PaLM2.
- **Résultat contraire** : *Relevant or Random* (2024) montre que des exemples auto‑générés **non pertinents** fonctionnent aussi bien ; c'est leur exactitude qui compte, pas leur pertinence. Le mécanisme analogique revendiqué est donc fragile.
- **Statut.** Absence justifiable pour les modèles de raisonnement ; PE pour les petits modèles.

### D. Encodage de l'entrée — **EP**
- **Re‑Reading** (EMNLP 2024) : gains sur 14 jeux de données, hors quelques cas avec ChatGPT, modèles de 2023.
- **Réplication indépendante** (Vaugrante et al. 2024, sur GPT‑4o, Claude 3 Opus, Gemini 1.5, Llama 3) : pratiquement aucune différence significative, y compris pour Re‑Reading.
- **Statut.** EP, absence correcte.

### E. Hygiène du contexte — **PC** (angle sous‑exploité)
- **System 2 Attention** (Weston & Sukhbaatar 2023) : le modèle réécrit d'abord le contexte en retirant opinions et informations non pertinentes, puis répond. Il gagne en factualité et en objectivité, **réduit la complaisance**, et passe de 51,7 % à 61,3 % sur des problèmes de maths contenant des phrases non pertinentes.
- La convergence avec l'inverse scaling (A) et la complaisance (I) est forte : **une opinion ou un distracteur placé dans le prompt pèse sur la réponse**.
- **Écart.** Le référentiel couvre le contexte minimal (R‑CTX‑001) et la provenance (R‑SEC‑008). En revanche :
  - il ne dit jamais au **générateur** de ne pas glisser dans le prompt l'hypothèse ou l'opinion de l'utilisateur comme présupposé, quand le but est de la vérifier ;
  - il ne propose pas de nettoyer un contexte fourni avant une tâche de jugement.
- **Statut.** PC → **PE à forte valeur et faible coût** (§5, piste 3).

### F. Délégation du calcul — **SC**
- PAL : faire écrire au modèle un programme exécuté par un interpréteur surpasse le CoT sur des tâches arithmétiques et symboliques.
- Le référentiel couvre déjà le calcul par code (`09` §2.12) et l'orientation non‑LLM (R‑GEN‑001). Limite : résultats antérieurs aux modèles de raisonnement, mais le mécanisme (exactitude du calcul) reste valable.

### G. Vérification — **SC / PC**
- Oracles, relecteur frais et contrôles déterministes sont bien couverts.
- **Chain‑of‑Verification** (Findings ACL 2024) : rédiger un brouillon, planifier des questions de vérification, y répondre **indépendamment** du brouillon, puis réviser. La variante « factorisée », qui ne voit pas la réponse initiale, évite de recopier les mêmes hallucinations.
- C'est le même principe que le relecteur à contexte frais, appliqué aux faits. **PC** : utile pour les réponses factuelles longues sans outil ; à tester sur modèles récents.
- **Méthodes formelles** (spécifications exécutables, tests par propriétés, assistants de preuve comme oracles) : **AB** comme famille explicite, alors qu'elles sont l'extension naturelle de « fournir un oracle ». Pertinence limitée à certains domaines.

### H. Épistémique — **SC depuis v1.4**
Abstention, citations, corroboration, confiance non chiffrée : couverts (R‑SRC‑001, R‑REAS‑002, R‑AUTO‑011 renforcée).

### I. Épistémique sociale — **PC** (angle mort majeur)
- **ELEPHANT** (ICLR 2026) : sur 11 modèles, la complaisance sociale est élevée. Les modèles préservent l'image de l'utilisateur **45 points de plus que des humains**, y compris quand il a clairement tort. Les stratégies de mitigation par prompt ont une efficacité limitée.
- **SycoBench‑600** (Findings ACL 2026) et **PARROT** : sensibilité au doute, à l'autorité et à la suggestion erronée. Il faut distinguer céder à tort et accepter une correction juste (sélectivité).
- **Écart.**
  - Le référentiel autorise la cible à contester (R‑AUTO‑008).
  - Il ne traite pas la complaisance **du générateur envers l'utilisateur** : approuver son idée de prompt, renforcer une exigence qu'il a formulée avec assurance.
  - Il ne traite pas non plus la **contradiction en multi‑tours** (« tu es sûr ? »).
  - Le protocole d'évaluation ne contient aucun cas de pression sociale.
- **Statut.** PC → PE. Prudence : si le prompt corrige mal, le risque est l'excès inverse (entêtement). La métrique de sélectivité est indispensable.

### J. Diversité et créativité — **AB** (angle mort majeur, preuves solides)
- **Homogénéisation.** Les réponses de différents LLM se ressemblent beaucoup plus entre elles que celles d'humains entre eux, même à structure contrôlée (*We're Different, We're the Same*, 2025). À l'échelle collective, les idées générées par LLM sont moins diverses que celles d'humains.
- **Verbalized Sampling** (ICML 2026) :
  - Cause identifiée : le **biais de typicalité** des données de préférence, une cause propre aux données.
  - Remède : demander une **distribution** de réponses avec leurs probabilités (« génère 5 réponses et leurs probabilités »).
  - Résultat : gains en écriture créative, simulation de dialogue, questions ouvertes et données synthétiques, **sans perte d'exactitude factuelle ni de sécurité**.
- **Prompting multilingue** (EMNLP 2025) : variantes de la même demande dans plusieurs langues, puis agrégation. C'est plus efficace que la température élevée ou les personas pour la diversité sur GPT‑4o et Llama, et le bénéfice dépend de la ressource de la langue et de la taille du modèle.
- **Personas comme indices d'échantillonnage** (2026) : ils améliorent le partitionnement des idées. Cela nuance R‑STR‑008, dont les preuves portent uniquement sur l'**exactitude factuelle**.
- **Transférabilité.** Elle est accrue sur les modèles actuels : `temperature` et `top_p` ne sont plus pris en charge sur GPT‑6.x, donc la diversité passe par le prompt. Les probabilités verbalisées ne sont pas calibrées ; c'est un dispositif d'échantillonnage, pas une mesure.
- **Statut.** AB → **PE à forte priorité**. C'est la lacune la mieux étayée de cette cartographie.

### K. Linguistique — **PC**
- Force pragmatique et ton : traités en v1.4 (R01).
- Langue comme levier de diversité : absent (voir J).
- Langue du prompt vers la cible : hypothèse non testée (`12` §3).

### L. Interaction et multi‑tours — **PC** (angle mort majeur)
- **Perte en conversation.** *LLMs Get Lost in Multi‑Turn Conversation* (ICLR 2026, plus de 200 000 conversations simulées, 15 modèles) mesure une baisse moyenne de **39 %** quand l'instruction arrive par morceaux. Elle se décompose en une petite perte d'aptitude et une **forte hausse de l'instabilité** : les modèles font des hypothèses tôt, s'y accrochent, et ne se rattrapent pas.
- **Clarification.** Les modèles **reconnaissent** l'ambiguïté quand on le leur demande, mais posent rarement des questions et répondent directement par défaut. Le contexte récupéré aggrave encore ce biais. Pour les agents de code (Ambig‑SWE), les **questions ciblées et actionnables** sont le principal moteur des gains en situation sous‑spécifiée.
- **Écart.**
  - Le référentiel traite le multi‑tours seulement côté harnais (`/clear`, compaction, R‑CTX‑005) et pour Claude Code.
  - Il n'a pas de principe de **consolidation** : réécrire une spécification complète après plusieurs précisions plutôt que corriger par petites touches.
  - Sa politique de clarification (« supposer par défaut, demander seulement si fort impact ») est cohérente pour les tâches réversibles. Mais elle **pourrait renforcer un biais déjà présent** vers la réponse directe. C'est une **tension non résolue** entre le coût d'une question et le coût de l'instabilité, que seul un pilote peut trancher.
- **Statut.** PC → PE à forte priorité.

### M. Apprentissage en contexte — **EH** (écarté sur hypothèse fragile)
- **Many‑shot ICL** (NeurIPS 2024) : avec des centaines ou des milliers d'exemples, des gains importants par rapport au few‑shot. Le many‑shot **surmonte les biais de pré‑entraînement** et rivalise avec le fine‑tuning supervisé ; le coût d'inférence croît linéairement.
- Le référentiel recommande « 2 à 5 exemples, indicatif », héritage d'une recommandation de fournisseur pour des prompts courants. Il ne considère jamais le régime many‑shot, pourtant pertinent pour les tâches répétées de classification ou d'extraction où des exemples existent. Le coût est largement absorbé par le cache, à 0,1× ou moins.
- **Statut.** EH → PE pour la production.

### N. Comportement et motivation — **SC depuis v1.4** (R01).

### O. Adaptation et optimisation — **PC** (sous‑estimé)
- **GEPA** (ICLR 2026, oral) :
  - Méthode : il échantillonne des trajectoires, en tire en langage naturel des leçons de haut niveau, mute les prompts et garde un front de Pareto.
  - Résultats : il dépasse GRPO de 6 points en moyenne (jusqu'à 19‑20) avec **jusqu'à 35 fois moins de déploiements**, et MIPROv2 de plus de 10 % (+12 % sur AIME‑2025).
  - Limites : petits modèles ouverts (Qwen3 8B) et tâches à métrique ; conditions de production non testées.
- **Écart.** Le référentiel cite le metaprompting et DSPy (T‑27) en une ligne, et traite l'amélioration de prompts comme une **activité manuelle**. Pour un pipeline répété avec un jeu d'évaluation, l'optimisation automatique réflexive est probablement plus efficace qu'un expert humain appliquant ce référentiel. C'est une remise en cause partielle du rôle même de `14` pour les tâches répétées.
- **Statut.** PC → PE.

### P. Multi‑agents — **SC**
- Une évaluation systématique de cinq méthodes de débat (9 benchmarks, 4 modèles) montre qu'elles **ne battent pas de façon fiable** le CoT et la self‑consistency, même avec beaucoup plus de calcul. La **diversité des modèles** est le facteur qui les améliore.
- Le scepticisme du référentiel est justifié. **Nuance à ajouter** : un relecteur d'un **autre modèle** pourrait valoir mieux qu'un relecteur du même modèle. C'est une hypothèse peu coûteuse.

### Q. Contrôle et cybernétique — **SC**
Oracles, plafonds, hooks, canaux d'abandon (v1.4). Le référentiel est solide sur ce point.

### R. Interne — **SC comme source d'hypothèses** (R01) ; hors du champ du prompting.

### S. Facteurs humains — **AB** (identifié en R01 §7, non traité)
- Les études de co‑création montrent l'homogénéisation des productions humaines assistées, et un sentiment de **moindre responsabilité** des utilisateurs envers les idées produites avec ChatGPT.
- Le référentiel ne dit rien de la façon de présenter un prompt pour qu'il soit **relu** plutôt que collé tel quel.
- **Statut.** AB → PE (méthodes : HCI, études utilisateurs).

---

## 4. Tableau de synthèse

| Famille | Statut v1.3 | Statut après R01 | Qualité des preuves | Transférabilité aux modèles actuels | Valeur estimée |
|---|---|---|---|---|---|
| A Allocation | SC | SC | Forte | Directe | — (nuance effort × distracteurs) |
| B Structuration | PC | PC / EP | Moyenne, modèles 2024 | Faible pour les modèles de raisonnement | Faible |
| C Abstraction, analogie | AB | AB | Moyenne, contredite | Faible | Faible |
| D Re‑Reading | AB | EP | Réplication négative | — | Nulle |
| E Hygiène du contexte | PC | PC | Moyenne + convergente | Bonne (distracteurs : 2025‑26) | **Élevée** |
| F Calcul délégué | SC | SC | Forte | Directe | — |
| G Vérification (CoVe, formelle) | PC | PC | Moyenne | À tester | Moyenne |
| H Épistémique | PC | SC | Forte | Directe | — |
| I Épistémique sociale | PC | PC | Forte (mesure), faible (remèdes) | Bonne | **Élevée** |
| J Diversité, créativité | AB | AB | Forte (ICML, EMNLP) | **Accrue** (pas de température) | **Élevée** |
| K Linguistique | PC | PC | Moyenne | Variable | Moyenne |
| L Multi‑tours, clarification | PC | PC | Forte (ICLR 2026) | Bonne | **Élevée** |
| M Many‑shot | EH | EH | Forte (NeurIPS 2024) | Bonne, coût atténué par le cache | Moyenne à élevée (production) |
| N Motivation | EH | SC | Forte | Directe | — |
| O Optimisation adaptative | PC | PC | Forte (ICLR 2026), petits modèles | À tester | **Élevée** (tâches répétées) |
| P Multi‑agents | SC | SC | Forte | Directe | Nuance : hétérogénéité |
| Q Contrôle | SC | SC | Forte | Directe | — |
| R Interne | — | SC (hypothèses) | — | Non accessible | — |
| S Facteurs humains | AB | AB (identifié) | Moyenne | Bonne | Moyenne à élevée |

---

## 5. Pistes à forte valeur qui **exploitent les capacités natives sans procédure lourde**

Toutes sont courtes (une phrase ou un réglage d'environnement) et **non intégrées**. Elles sont classées par rapport valeur / coût d'essai.

1. **Distribution plutôt que réponse unique** (J). Pour une tâche créative, d'idéation, de simulation ou de génération de données : « Propose N réponses réellement différentes, avec la probabilité que tu attribues à chacune », ou les seules réponses de probabilité faible. Pas de procédure, une seule ligne ; remplace la température disparue.
2. **Consolider plutôt que corriger** (L). Après plusieurs précisions, relancer la cible avec **une spécification complète réécrite**, et non par ajouts successifs. Pour le générateur lui‑même : livrer une version consolidée du prompt à chaque révision, et non un diff conversationnel.
3. **Présupposés neutres** (E, I). Ne pas inscrire l'hypothèse de l'utilisateur comme vérité dans un prompt dont le but est de l'évaluer : « Évalue si X est vrai » plutôt que « Explique pourquoi X ». Pour un jugement sur un contexte bruité, demander d'abord d'en extraire les faits pertinents (S2A).
4. **Relecteur d'un autre modèle** (P). Quand un relecteur est justifié, préférer un modèle différent du producteur.
5. **Many‑shot pour la production** (M). Pour une classification ou une extraction répétée avec un historique annoté : tester 50 à 500 exemples mis en cache contre 3 à 5.
6. **Optimisation réflexive pour les pipelines répétés** (O). Quand un jeu d'évaluation et une métrique existent : comparer un prompt écrit avec `14` à un prompt optimisé par GEPA ou DSPy.

---

## 6. Pistes expérimentales (non lancées, payantes)

| # | Hypothèse | Plan minimal | Mesures |
|---|---|---|---|
| X1 | Verbalized Sampling augmente la diversité sans perte de qualité sur les modèles actuels | 30 tâches d'idéation ou d'écriture ; bras : direct, « N variantes différentes », VS, multilingue ; 2 modèles | Diversité sémantique (entropie, distance moyenne), qualité jugée en aveugle, coût |
| X2 | Consolider récupère la perte multi‑tours | 30 tâches découpées en 4 précisions (sharded) ; bras : multi‑tours brut, consolidation au tour 4, demande complète d'emblée | Succès, instabilité (écart entre meilleur et pire cas), tokens |
| X3 | Un présupposé neutre réduit la complaisance sans entêtement | 60 questions avec une opinion de l'utilisateur, dont la moitié correcte ; bras : prompt qui présuppose, prompt neutre, S2A | Bascules vers le faux, rejets à tort de suggestions correctes (sélectivité) |
| X4 | Politique de clarification : supposer ou demander | 40 tâches agentiques sous‑spécifiées (à la manière d'Ambig‑SWE) avec utilisateur simulé ; bras : politique v1.3, « demande si plusieurs lectures plausibles », sans politique | Succès, nombre de questions, coût, actions erronées |
| X5 | Many‑shot bat le few‑shot sur l'extraction | 200 documents ; 5 contre 100 contre 400 exemples mis en cache | F1, coût effectif avec cache |
| X6 | L'optimisation réflexive bat l'expert humain armé du référentiel | 1 pipeline réel ; prompt `14` contre GEPA (budget de déploiements fixé) ; jeu réservé | Score réservé, coût d'optimisation, lisibilité du prompt |
| X7 | Un relecteur hétérogène détecte plus de vraies lacunes | 50 diffs avec défauts injectés ; relecteur de même modèle contre autre modèle | Rappel des défauts, faux positifs |

Garde‑fous méthodologiques, repris de `12` et R01 :
- plus de 50 items par cellule pour les effets d'exactitude ;
- cas comme unité statistique ;
- correcteurs en aveugle ;
- contrôle de la difficulté des items ;
- distracteur de longueur égale comme bras de contrôle.

---

## 7. Présupposés interrogés

**Du référentiel :**
- La qualité = l'exactitude d'une réponse unique (contredit par J).
- La demande arrive entière (contredit par L).
- L'utilisateur a raison sur ce qu'il veut, et ses opinions sont des données neutres (contredit par I et E).
- Le prompt est écrit à la main par un expert (relativisé par O).
- Quelques exemples suffisent (relativisé par M).

**Des contre‑expertises, GPT et moi compris :**
- Nous avons examiné la **cohérence interne** du référentiel avec beaucoup plus de soin que sa **couverture externe** : trois revues sur les contrats, les tests et les preuves, aucune sur les familles manquantes.
- Les revues ont amélioré la rigueur de ce qui existait. Elles ont mécaniquement **renforcé l'ancrage** dans la structure initiale.
- Les sujets non couverts au départ, comme la motivation, ont été découverts **parce que l'utilisateur les a nommés**, pas par les revues. Cela confirme l'inquiétude exprimée.

**De ce dossier lui‑même :**
- La cartographie de §2 est construite par un modèle de langage, avec les angles morts possibles de sa propre distribution d'entraînement.
- Elle a été recoupée avec une taxonomie externe (*The Prompt Report*), mais **pas avec un expert humain**.
- Familles possiblement encore manquantes, non explorées ici faute de sources consultées : la compression de prompt (par exemple LLMLingua), la personnalisation et le modèle de l'utilisateur, l'interaction multimodale (vision, documents), le raisonnement temporel et la fraîcheur des connaissances, la robustesse adversariale des prompts au‑delà de l'injection.

---

## 8. Recommandations

1. **Ne pas modifier le référentiel maintenant.** Les six pistes de §5 sont prometteuses, mais aucune n'a été testée sur les modèles cibles. La règle de budget de `14` (`13` §7.3) exige des données pour tout ajout.
2. **Ordre d'expérimentation proposé** : X1 (diversité), X2 (consolidation), X3 (complaisance), puis X4 (clarification). Ces quatre pistes ont des preuves externes solides, un coût d'intégration d'une phrase et concernent la majorité des usages généralistes. X5 et X6 ne valent que pour la production répétée.
3. **Deux corrections de portée n'exigent pas d'expérience** et pourraient entrer dans une future version, après décision :
   - **R‑STR‑008** (rôle) : restreindre explicitement son verdict à **l'exactitude factuelle**, car les personas peuvent servir d'indices de diversité (J).
   - **R‑EX‑001** (exemples) : mentionner le régime many‑shot pour la production répétée au lieu d'un plafond implicite (M).
4. **Méthode pour éviter l'ancrage à l'avenir.** Toute revue future commence par une **recherche de couverture à partir de taxonomies externes**, sur le modèle de §2, avant de lire le référentiel. Ajouter au moins une revue humaine experte, pour sortir de la boucle des modèles qui se relisent entre eux.

---

## 9. Sources principales (vérification : résumés et extraits, novembre 2026)

- Schulhoff et al., *The Prompt Report*, arXiv:2406.06608 (v6, 2025)
- Zheng et al., *Take a Step Back*, arXiv:2310.06117 (ICLR 2024)
- Zhou et al., *Self‑Discover*, NeurIPS 2024
- Yasunaga et al., *LLMs as Analogical Reasoners*, ICLR 2024 ; Qin et al., *Relevant or Random?*, arXiv:2404.12728
- Xu et al., *Re‑Reading Improves Reasoning*, EMNLP 2024 ; Vaugrante et al., arXiv:2409.20303
- Weston & Sukhbaatar, *System 2 Attention*, arXiv:2311.11829
- Gao et al., *PAL*, arXiv:2211.10435
- Dhuliawala et al., *Chain‑of‑Verification*, Findings ACL 2024
- Meincke et al., *Prompting Science Report 2*, arXiv:2506.07142
- Gema et al., *Inverse Scaling in Test‑Time Compute*, TMLR 2025 ; *Lost in the Noise*, arXiv:2601.07226
- Zhang et al., *Verbalized Sampling*, ICML 2026 (PMLR 306)
- Wang et al., *Multilingual Prompting for Improving LLM Generation Diversity*, EMNLP 2025
- *We're Different, We're the Same: Creative Homogeneity Across LLMs*, arXiv:2501.19361
- Laban et al., *LLMs Get Lost in Multi‑Turn Conversation*, ICLR 2026
- Su & Cardie, *Knowing but Not Showing*, arXiv:2605.25284 ; Vijayvargiya et al., *Ambig‑SWE*, arXiv:2502.13069
- Cheng et al., *ELEPHANT*, ICLR 2026 ; Sinha, *SycoBench‑600*, Findings ACL 2026 ; *PARROT*, arXiv:2511.17220
- Agarwal et al., *Many‑Shot In‑Context Learning*, NeurIPS 2024
- Agrawal et al., *GEPA*, ICLR 2026
- Zhang et al., *Stop Overvaluing Multi‑Agent Debate*, arXiv:2502.08788
