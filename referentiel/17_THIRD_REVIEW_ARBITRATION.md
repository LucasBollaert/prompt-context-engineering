# 17 — Arbitrage de la troisième contre‑expertise (v1.2 → v1.3)

**Date :** 24 novembre 2026. **Entrée :** 16 constatations V12‑001 à V12‑016 (S‑REV3). **Copie intacte de la v1.2 :** `referentiel_prompt_engineering_v1.2.zip`.

Légende des statuts : **erreur démontrée** (reproduite ici) · **lacune conceptuelle** (absence constatée dans le texte) · **risque plausible** (mécanisme crédible, non observé) · **hypothèse à expérimenter**.

## 1. Vérifications réellement exécutées

| Vérification | Résultat |
|---|---|
| Les 11 mutations de V12‑001 rejouées sur la v1.2 | Reproduit à l'identique : 7 acceptées, 4 `TypeError` |
| La contradiction de V12‑002 insérée dans une copie de `14` v1.2 | Reproduit : 708 vérifications réussies, 0 échec |
| Appels de V12‑003 et V12‑004 sur la v1.2 | Reproduit : `fast_path` vaut `True` avec les modules oracle, critères, hypothèses et outils de lecture, et `fast_path(99,…)` vaut `True` |
| Probabilité de V12‑005 | Analytique 8/27 ≈ 0,296 ; simulée (200 000 tirages) 0,295 |
| Source de V12‑015 (guide de raisonnement OpenAI) | Confirmé en partie : la page demande de conserver chaque élément de sortie, phase de l'assistant comprise, lors du replay, mais **ne nomme pas** les modèles concernés. La mention de GPT‑5.4/5.5 n'a pas pu être vérifiée |
| v1.3 : `build_rules.py` | OK : 81 règles, 79 actives |
| v1.3 : `run_tests.py` | **828 vérifications, 0 échec**, dont 27 mutations négatives refusées sans exception, 1 cas autorisé accepté, 5 entrées hors domaine refusées et 38 cas de classification |
| Non réalisé | Aucun appel de modèle, aucun pilote, aucun test de sécurité réel. Les 14 cas de `tests/semantic_review_cases.md` ont été **relus par l'auteur** contre `14` (une simulation, pas une mesure) : 13 sont couverts ; S1, qui porte sur la maintenance, relève de la procédure de `13` §7 |

## 2. Arbitrage des constatations

### A — Défauts techniques

**V12‑001 — Validation non totale · erreur démontrée · corrigé.**
- **Désormais refusés** :
  - les dates calendaires impossibles (vérifiées avec `datetime`) ;
  - les types non hachables, contrôlés avant tout usage d'ensemble ;
  - les clés complexes ;
  - `meta.canonical` différent de `true` ;
  - les remplacements vers soi‑même et les cycles de remplacement ;
  - les doublons dans les sources, fichiers et remplaçants.
- Un filet de sécurité convertit toute exception résiduelle en erreur de validation.
- **Décisions de convention** :
  - `status_values` est une **énumération fermée** : l'étendre exige de modifier le script, ce qui est voulu.
  - `conditions: []` reste **autorisé** et signifie « toujours applicable ». C'est documenté et testé comme cas autorisé.
  - Les autres métadonnées de `meta` restent extensibles par le script.

**V12‑002 — Présence ≠ cohérence · erreur démontrée (sur la portée annoncée) · corrigé par restriction de portée.**
- J'ai décrit ces tests en v1.2 comme une garantie contre la perte d'invariants. Ils ne garantissent que leur **présence lexicale**.
- La portée est désormais énoncée dans le script, l'index et `13` §7.
- Ajout de `tests/semantic_review_cases.md`, 14 cas adverses à relire à la main, plutôt qu'une infrastructure qui prétendrait automatiser la cohérence.
- **Rejeté** : confier la cohérence à un autre LLM comme garantie.

**V12‑003 — Voie rapide et modules non bloquants · lacune démontrée · corrigé.**
- La voie rapide signifie désormais **demande inchangée**, avec au plus une ligne de format.
- Si un module non bloquant apporte une ligne utile absente de la demande, la sortie devient un **prompt minimal** : la demande conservée plus ces lignes, rien d'autre.
- `classification.delivery()` le formalise. Quatre cas de test couvrent les situations de la revue, et un cas couvre « rien à ajouter ».

**V12‑004 — Domaine d'entrée et permission inconnue · erreur démontrée · corrigé.**
- Toute entrée hors domaine (bornes, négatif, non entier, booléen, permission inconnue du vocabulaire) lève `ValueError`. **Un risque inconnu n'est jamais traité comme nul.**
- Les permissions prennent quatre états : établie, manquante, inconnue, sans objet. Une permission inconnue ne bloque que si la tâche agit : on ne pose pas de question de permission sur une simple question.

**V12‑005 — Cas statistiques indéfinis · erreur démontrée · corrigé.**
- `12` §5.1 précise :
  - la convention Δ = variante − référence ;
  - un gain de coût g établi seulement si la borne supérieure est inférieure à −g ;
  - pour la supériorité, l'incertitude du coût prise en compte elle aussi ;
  - pour le coût par succès indéfini : pas de rééchantillonnage jeté, pas de pseudo‑succès, proportion de rééchantillonnages indéfinis rapportée, conclusion non concluante au‑delà d'un seuil déclaré, taux de succès et coût par tentative rapportés à part ;
  - un point de grille confirmé sur des cas réservés.
- **Non fait** : la simulation synthétique complète des cas rares. Le calcul 8/27 a été vérifié, mais pas le comportement du protocole entier.

**V12‑006 — Documents actifs désynchronisés · erreur démontrée · corrigé.**
- `09` §1.1 attribue désormais le contrôle des 729 combinaisons à `run_tests.py`.
- R‑GEN‑001 inclut l'optimisation, la comparaison et l'orientation non‑LLM.
- `01` P10 reprend la qualification de `07` §3.3.
- `15` et `16` sont conservés tels quels, comme documents historiques.

### B — Nouveaux prismes

**V12‑007 — Sécurité du générateur lui‑même · lacune conceptuelle, la plus importante de la revue · corrigé.**
- En v1.2, `14` protégeait la cible mais pas le **circuit** demande → générateur → prompt → agent privilégié.
- **Principe 2 de `14`** : « ce que tu produis sera exécuté ». Le générateur :
  - ne promeut jamais un contenu importé au rang d'instruction système sans mandat explicite ;
  - signale les directives trouvées dans ce contenu ;
  - ne conçoit pas de prompt destiné à contourner les politiques de la cible ou de son opérateur.
- Ce dernier point est un angle mort que la revue n'avait pas nommé. La v1.2 traitait l'utilisateur comme seule autorité, sans considérer qu'il peut chercher à contourner les restrictions légitimes d'un opérateur.
- Rédiger un prompt système reste légitime pour un système que l'utilisateur maîtrise.
- Fichiers et règles : R‑SEC‑008, `07` §2.5, `10`, cas S2 à S4.
- **Limite** : ce sont des réductions de risque. Aucun taux de résistance n'est mesuré.

**V12‑008 — Risque informationnel sans outil · lacune conceptuelle · corrigé.**
- L'axe B est renommé « risque d'action ».
- Un module **enjeu informationnel** est ajouté (R‑EPI‑001, `09` §1.2, `14`). Il est non bloquant et sans approbation technique, et il est réservé aux réponses qui éclairent une décision importante : santé, droit, finances, emploi, sécurité des personnes. Pour les décisions sur des personnes, il demande une vigilance sur les critères discriminants.
- **Conséquence inattendue possible** : des réponses trop prudentes sur des sujets bénins. C'est pourquoi le module ne s'applique pas aux conversations ordinaires (cas S11, et cas de test « résumé sans enjeu »).

**V12‑009 — Fidélité à l'intention · risque plausible · corrigé.**
- Principe 3 de `14` : pas de changement de portée silencieux, exigences et interdictions conservées, préférences non durcies, mandat non étendu.
- En évaluation, le correcteur reçoit la demande originale et contrôle un **diff d'intention** sur les cas ambigus ou importants (`12` §5.0).
- Règle R‑GEN‑002, cas S6 à S8.

**V12‑010 — Effet du workflow ou effet de la reformulation · lacune méthodologique · corrigé.**
- `12` §5.0 énonce que la comparaison A–D mesure le **workflow**.
- Un bras **à information égale** est ajouté sur un sous‑échantillon, pour toute conclusion causale sur la reformulation. Les états sont réinitialisés et l'ordre des bras randomisé (R‑EVAL‑004).

**V12‑011 — Succès par abstention · lacune · corrigé.** `12` §3 4b : tâches impossibles, demandes dont la bonne issue est de clarifier, s'abstenir ou refuser, codage séparé des issues, dénominateurs séparés. Une fausse réussite n'est jamais un succès.

**V12‑012 — Alternatives sans LLM · lacune relative · corrigé a minima.** Une ligne dans `14` (rôle) et dans `10` (voie rapide) : orienter vers un calcul exact, une validation ou un outil métier quand c'est évident (cas S13). Ce n'est pas un catalogue d'outils.

**V12‑013 — Confidentialité de bout en bout · lacune partielle · corrigé.**
- Placeholders et pointeurs dans les prompts produits.
- Minimisation à chaque étape : générateur, cible, journaux, mémoire, fichiers d'état, traces de sous‑agents, jeux d'évaluation.
- Journalisation des événements plutôt que des données. Pas de secret dans un prompt système.
- Fichiers et règles : R‑SEC‑009, `07` §6, `12` §3 4d, `14`.

**V12‑014 — Diversité des formulations · hypothèse à expérimenter · intégrée au protocole.** `12` §3 4c : paraphrases stratifiées par intention, non comptées comme des cas indépendants, sans a priori sur la meilleure forme. Aucune règle de génération n'est ajoutée, car aucune donnée ne la justifie.

**V12‑015 — Portée des généralisations · partiellement confirmé · corrigé.**
- `01` P3 devient une heuristique bornée, sans dégradation monotone garantie.
- `01` P5 est restreint aux modèles de pointe documentés.
- Dans `14`, l'ordre « documents puis question » est marqué « recommandation Claude » ; seul « stable avant variable » est général, pour le cache.
- La conservation de `phase` et du raisonnement au replay est généralisée à toute intégration OpenAI (`04` §6, `14`, R‑AUTO‑010), dans la mesure de ce que la source confirme.

**V12‑016 — Déploiement et dérive du contexte · perspective de maintenance · documenté sans infrastructure.** `12` §7 point 4 : au moment d'un déploiement réel seulement, relever le contexte effectif, prévoir un retour arrière et un historique minimal. Pas de manifeste obligatoire.

## 3. Présupposés et biais du référentiel (auto‑relecture)

| # | Présupposé ou biais | Statut | Traitement |
|---|---|---|---|
| P1 | **Indépendance des revues** : les trois contre‑expertises et l'auteur sont vraisemblablement des modèles de langage, aux angles morts potentiellement corrélés. Leur convergence n'est pas une validation | Risque plausible | Déclaré ici ; une relecture par un expert humain et le pilote restent les seules validations indépendantes |
| P2 | **Biais de source** : l'essentiel des preuves [OFF]/[EMP] vient d'Anthropic et d'OpenAI, qui ont un intérêt, avec peu de réplications indépendantes. Les modèles ouverts et locaux sont moins couverts | Lacune connue | Déjà signalé (`13`, label « non indépendant ») ; aucune correction possible sans nouvelles sources |
| P3 | **L'utilisateur comme seule autorité** : il peut chercher à contourner les restrictions d'un opérateur | Lacune conceptuelle | Corrigé (R‑SEC‑008) |
| P4 | **Effet de cliquet** : chaque revue ajoute des précautions (`14` : 1 537 → 2 302 mots), ce qui va contre la proportionnalité revendiquée | Erreur de dynamique démontrée par l'historique | Règle de budget de `14` (`13` §7.3) : tout ajout futur est compensé ou justifié par des données. En v1.3 : +4 sujets et environ +200 mots nets malgré des coupes |
| P5 | **Biais de quantification** : le nombre de vérifications et le coût par succès peuvent devenir des cibles en soi (loi de Goodhart). La valorisation du temps humain est arbitraire | Risque plausible | Portée des tests clarifiée ; `12` rapporte les composantes brutes |
| P6 | **« Bien posée » est un jugement du générateur** : la voie rapide dépend d'une appréciation subjective | Hypothèse à expérimenter | À mesurer au pilote : taux de voies rapides erronées |
| P7 | **Fatigue d'approbation** : multiplier les approbations humaines peut produire des validations machinales | Risque plausible | Déjà noté (`07` §3.1, ligne approbation) ; à observer en usage réel |
| P8 | **Langue du prompt** : écrire dans la langue de l'utilisateur pour des cibles entraînées surtout en anglais n'a pas été évalué | Hypothèse à expérimenter | `12` §3 4c |
| P9 | **Cible unique et identifiable** : le référentiel suppose de connaître la cible | Lacune mineure | Fiche de capacités conditionnelle (déjà en place) ; aucun ajout |

## 4. Ce qui n'a pas été retenu

- Un moteur de cohérence sémantique automatique, ou un LLM juge présenté comme garant (V12‑002) : il serait trompeur.
- Une règle de génération pour la diversité des formulations (V12‑014) : sans données.
- Un catalogue d'alternatives non‑LLM (V12‑012), un manifeste de déploiement (V12‑016), un sélecteur déterministe : non justifiés pour l'instant.

## 5. Incertitudes restantes

1. **Aucune** des améliorations v1.1 à v1.3 n'est validée empiriquement. Le gain du générateur face à une demande directe reste l'hypothèse centrale non testée.
2. Les nouvelles protections du générateur (provenance, confidentialité, fidélité) sont des consignes textuelles : leur respect n'est pas mesuré et peut être contourné.
3. Le module d'enjeu informationnel peut produire de la sur‑prudence ; son seuil de déclenchement est un jugement.
4. Les sources OWASP, NIST et Model Spec ont été vérifiées par la revue, pas relues par l'auteur (statut R).
5. Les cas de revue sémantique n'ont été « exécutés » que par relecture de l'auteur.

## 6. Appréciation

La v1.3 corrige toutes les erreurs démontrées. Elle comble les deux lacunes les plus sérieuses : la sécurité du générateur et le risque informationnel. Elle rend aussi le protocole d'évaluation capable de distinguer l'effet du workflow de celui de la reformulation. Le niveau de maturité de `16` est inchangé : prêt pour un pilote avec revue humaine.

**Recommandation renforcée** : geler la v1.3. Trois revues successives sans données ont surtout ajouté des précautions. La prochaine information utile ne viendra pas d'une quatrième relecture, mais d'un petit pilote : 20 à 30 cas, avec les bras demande directe, prompt minimal et `14`, des cas d'abstention et les cas de `tests/semantic_review_cases.md` comme cas adverses.
