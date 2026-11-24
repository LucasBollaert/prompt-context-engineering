# Historique des modifications

## v1.6 — 24 novembre 2026
Arbitrage du retour indépendant sur v1.5 et R03. Détail : `research/R04_EXPLOITATION_ET_SELECTION.md`.
- **Défaut démontré, validateur** : les quatre mutations signalées (verdict fictif, `sources: null`, `tier` dupliqué, OP sans preuve d'efficacité) étaient acceptées. Nouveau `scripts/registry.py` qui réutilise `StrictLoader`, vocabulaires de référence dans le code, types stricts, cohérence niveau × preuve ; 24 mutations négatives, toutes refusées.
- **Défaut démontré, preuve du problème ≠ preuve de la solution** : registre restructuré en quatre axes (phénomène, mécanisme, intervention, transfert) ; base déclarée pour les entrées OP (measured, documented, reasoned). K32 et K35 en base `reasoned`, K38 de CO à CA, K43 avec transfert inconnu. R‑STR‑009 passe de EMP à EMP + HYP.
- **R‑STR‑009 réécrite** : contraintes redondantes, indépendantes, interdépendantes et facilitatrices ; exigences de l'utilisateur conservées (conflit déclaré avec R‑GEN‑002) ; le contrôle complète l'énoncé sans le remplacer.
- **Consultation sélective** : champ `triggers` (19 situations), une ligne dans `14` (OP d'office, CA proposé, DC évité), table générée dans `10` étape 8 et contrôlée par les tests.
- **Registre** : 49 entrées (K45 sélection apprise par requête, dont EmotionRL ; K46 sélection par le modèle ; K47 retours au fil des tours ; K48 combinaison motivationnelle C ; K49 contraintes facilitatrices).
- **Pilote P0** : bras C et C+K réintroduits, volets agentique long et créatif explicites, décomposition de C prévue en confirmation. Non lancé.
- **Tests** : 930 vérifications, 0 échec (contre 1 146 : contrôles par entrée remplacés par un validateur et des mutations ciblées).
- `14` : 2 305 mots, ajouts compensés.

## v1.5 — 24 novembre 2026
Arbitrage du retour indépendant sur v1.4, R01 et R02, et recherche sur dix nouveaux axes. Détail : `research/R03_ARBITRAGE_ET_NOUVEAUX_AXES.md`.
- **Verdicts bornés** : vocabulaire de verdict fermé (R03 §1) ; erratum de R01, R02 et de la v1.4 (R03 §2). « Neutre », « inutile », « invalidé », « favorise » retirés des textes opérationnels quand les sources ne portaient que sur l'exactitude des tâches fermées.
- **R‑TONE‑003** : encouragements « sans effet démontré sur l'exactitude », effet sur les tâches ouvertes non établi ; risque agentique marqué HYP. Conduite inchangée. `14`, `02` §3 et `08` alignés.
- **R‑STR‑009 (nouvelle)** : peu d'exigences dures simultanées ; vérifiables confiées à un contrôle (IFScale, CSE). Seule technique intégrée à `14`.
- **Notes** : R‑EX‑001 (régime many‑shot, conditionnel) ; R‑STR‑008 (verdict limité à l'exactitude factuelle).
- `12` §5.1 : au moins deux paraphrases par bras pour conclure sur une technique.
- `13` : sources S‑R33 à S‑R36. `00_INDEX` : version et comptes de règles corrigés (le compte « 77 » était périmé depuis la v1.3).
- **Registre des connaissances** `research/knowledge_registry.yaml` : 44 entrées en cinq niveaux (OP, CO, CA, DC, QO), validées par les tests.
- **Protocole motivationnel révisé** (R03 §4) : plan texte × harnais, hypothèses typées, test du mécanisme des enjeux, volet tâches ouvertes, pilote exploratoire P0 d'environ 400 exécutions agentiques avant toute campagne. Non lancé.
- **Tests** : invariant de densité dans `14`, verdicts non bornés interdits dans `14`, `02` et `08`, validation du registre ; 1 146 vérifications, 0 échec ; 5 mutations de contrôle toutes détectées.
- `14` : 2 303 mots (2 305 en v1.4), ajouts compensés.
- Non intégré : répétition du prompt, diversité (Verbalized Sampling, multilingue), consolidation multi‑tours, présupposés neutres, relecteur hétérogène, many‑shot, GEPA, multimodal, temporalité, personnalisation, compression par tokens (registre CA, CO, DC ou QO).

## v1.4 — 24 novembre 2026
Recherche sur le cadrage motivationnel et corrections techniques résiduelles. Détail : `research/R01_CADRAGE_MOTIVATIONNEL.md` (§8 arbitrage, §9 corrections).
- **R‑TONE‑003 réécrite** : menaces, pourboires, faux enjeux et pression proscrits sur preuve EMP (absence d'effet sur l'exactitude dans les études de forte puissance ; lien mécanistique entre pression et triche en contexte agentique) ; encouragements et politesse requalifiés **neutres**.
- **R‑CLAR‑002** : vrais enjeux du résultat comme information, jamais inventés.
- **R‑AUTO‑011, R‑VAL‑004** : droit à l'échec honnête présenté comme issue valable, canal d'abandon côté harnais, consigne stricte « arrête‑toi et explique » (preuves ImpossibleBench, effet dépendant du modèle).
- **R‑STR‑004, `02` §3, `07` §2.4** : l'urgence et l'autorité déplacent la priorité des consignes ; à employer délibérément, à surveiller dans les contenus non fiables.
- `08` AP‑04, `11` T3, `12` §6 (conscience d'être évalué, grille qui récompense la supposition, variantes impossibles).
- **Technique** : options de classification booléennes et permissions typées strictement ; vocabulaire méthodologique (preuve, transfert, volatilité) fermé ; version, sémantique de sélection, descriptions et conflits en double validés. 35 mutations négatives, 11 entrées hors domaine ; 868 vérifications.
- `14` : 2 305 mots (budget constant, ajouts compensés).
- Non intégré, car expérimental : ambition au‑delà de R‑CLAR‑001, défi, compétition, coopération, hypothèse combinée (bras C du pilote).

## v1.3 — 24 novembre 2026
Troisième contre‑expertise (V12‑001 à 016) et auto‑relecture des présupposés. Détail : `17_THIRD_REVIEW_ARBITRATION.md`.

**Défauts démontrés corrigés**
- Validateur : dates calendaires réelles, contrôle des types avant usage d'ensembles, clés complexes refusées, `canonical: true` exigé, `status_values` fermé, remplacements vers soi‑même et cycles refusés, doublons refusés, aucune exception non gérée ; `conditions: []` autorisé et documenté.
- Classification : entrées hors domaine refusées ; permissions à quatre états ; `delivery()` distingue voie rapide (demande inchangée), prompt minimal et prompt complet.
- Tests : 828 vérifications ; leur portée est désormais énoncée comme structure, concordance et **présence lexicale**, pas cohérence sémantique ; 14 cas de revue sémantique manuelle (`tests/semantic_review_cases.md`).
- `12` : convention Δ, seuil de gain −g, coût par succès indéfini, incertitude du coût en supériorité, confirmation de la grille sur cas réservés.
- `09`, `01` P10, R‑GEN‑001 : documents actifs resynchronisés.

**Lacunes comblées**
- Sécurité du générateur : le prompt produit est traité comme une sortie exécutée en aval, sans promotion de contenu importé ni contournement des politiques de la cible (R‑SEC‑008, `07` §2.5).
- Confidentialité des prompts et de leurs traces (R‑SEC‑009, `07` §6).
- Fidélité à l'intention : aucun changement de portée silencieux, diff d'intention en évaluation (R‑GEN‑002).
- Module de prudence épistémique pour les réponses à fort enjeu, non bloquant (R‑EPI‑001) ; l'axe B devient « risque d'action ».
- Protocole : effet du workflow ou de la reformulation (bras à information égale), cas d'abstention et de refus, paraphrases, données anonymisées, note de déploiement.
- Orientation non‑LLM quand elle est évidente ; `phase` et raisonnement conservés au replay pour toute intégration OpenAI ; `01` P3 et P5 bornés.

**Garde‑fou contre l'inflation** : règle de budget de `14` (`13` §7.3). `14` : 2 302 mots (+10 % par rapport à la v1.2, ajouts en partie compensés par des coupes).

## v1.2 — 24 novembre 2026
Observations résiduelles V11‑001 à V11‑006 et auto‑relecture. Détail : `16_FINAL_REVIEW_AND_ARBITRATION.md`.

**Catalogue et outillage**
- `scripts/build_rules.py` réécrit. Il refuse les clés dupliquées, les champs inconnus, les types incorrects, les dates invalides ou futures et les conflits mal formés, sans jamais planter. Il vérifie que `rules.json` relu est identique au YAML.
- Nouveau `scripts/classification.py` : la référence exécutable du niveau, des modules et de la voie rapide.
- Nouveaux `tests/classification_cases.yaml` (21 cas écrits à la main) et `scripts/run_tests.py`. Ce dernier couvre 17 tests négatifs, la classification, la concordance entre `09`, `10` et `14`, 17 invariants de `14` et les références croisées : 708 vérifications.
- Règles modifiées :
  - R‑GEN‑001 (voie rapide bornée) et R‑CLASS‑001 ;
  - R‑EVAL‑005 (incertitude du coût, décisions provisoires) ;
  - R‑ARCH‑001 et R‑ARCH‑002 (architecture permanente ou délégation ponctuelle) ;
  - R‑AUTO‑005 et R‑VAL‑003 (conditions conjonctives), R‑EX‑001 (capacité observée) ;
  - R‑VAL‑002 (résolution avec R‑CTX‑001) et R‑STR‑008 (source vérifiée).

**Documents**
- `14` : condensé de 2 433 à 2 096 mots. Branches, modes et format fusionnés ; méthode présentée comme liste de contrôle ; voie rapide bornée ; aucun invariant retiré, ce que vérifient les tests.
- `10` : section voie rapide réécrite ; contenu des niveaux sans chevauchement avec les modules.
- `12` §5.1 : critère d'établissement d'un gain de coût, décisions provisoires, fiche de résultat.
- `07` : le worktree n'est plus présenté comme une sandbox ; tous les contrôles sont typés.
- `01` P9 et `03` T‑20 : distinction entre architecture et délégation ponctuelle.
- `09` : terminologie « Niveau » ; la voie rapide ne retire aucun module.
- `13` : S‑R7 et S‑R17 vérifiées, procédure de maintenance avec `run_tests.py`, journal.
- `00` : index des nouveaux fichiers.

## v1.1 — 24 novembre 2026
Intégration de la première contre‑expertise (20 constatations). Détail : `15_REVIEW_ARBITRATION.md`.
- Codes de preuve en chaînes (`OFF` était lu comme booléen) et premier validateur.
- Niveaux T0‑T3 rendus totaux (A × D) et modules orthogonaux.
- Portée des garanties, états terminaux, mandat d'audit en lecture seule.
- Codex conditionné au modèle (`phase`), structured outputs avec états non réussis.
- Comptabilité de coût non chevauchante, baseline sans intermédiaire, non‑infériorité.
- 13 nouvelles règles.

## v1.0 — 23 novembre 2026
Création : 15 documents, 64 règles, sources vérifiées ou citées de mémoire.
