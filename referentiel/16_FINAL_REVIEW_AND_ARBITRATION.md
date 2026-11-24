# 16 — Arbitrage final et auto‑relecture (v1.1 → v1.2)

**Date :** 24 novembre 2026. **Entrées :** six observations résiduelles de la seconde contre‑expertise (V11‑001 à V11‑006), puis une auto‑relecture de l'ensemble. **Copie intacte de la v1.1 :** archive `referentiel_prompt_engineering_v1.1.zip` (inchangée).

## 1. Ce qui a été réellement exécuté

| Type | Contenu | Résultat |
|---|---|---|
| Test exécuté | Reproduction des tests négatifs de V11‑001 sur une copie de la v1.1 | Clé dupliquée, date `2026-99`, champ inconnu et `notes: 42` **acceptés** ; `conflicts` mal typé et date `2026-13-99` **refusés par plantage Python**, sans message de validation |
| Test exécuté | `scripts/build_rules.py` (v1.2) sur le catalogue réel | OK : 77 règles, 75 actives, 50 avec preuve OFF ; `rules.json` écrit, relu, identique aux données YAML |
| Test exécuté | `scripts/run_tests.py` | **708 vérifications réussies, 0 échec** |
| Test exécuté | 17 mutations négatives du catalogue | Toutes refusées avec un message, sans exception |
| Test exécuté | 4 régressions injectées sur une copie (table de `09`, fonction de niveau, exclusions de la voie rapide, invariant de `14`) | Les 4 sont détectées |
| Vérification documentaire | Zheng et al. (personas) et Sprague et al. (CoT), sur arXiv et dans les actes | Confirmées ; statut M → V (résumé) |
| Simulation théorique | Les 21 cas de `tests/classification_cases.yaml` sont des attendus écrits à la main | Ils testent la cohérence interne, pas un comportement de modèle |
| **Non réalisé** | Essai de prompts sur un modèle, comparaison v1.1 / v1.2 / demande directe, tests adverses de hooks ou de sandbox, mesure de tokens | Aucune dépense engagée |

## 2. Arbitrage des six observations

### V11‑001 — Validation incomplète du catalogue · **accepté, corrigé**
- **Vérification** : le défaut est reproduit, et il est un peu plus large que décrit. En plus des trois cas cités, le validateur acceptait les champs inconnus (une faute de frappe comme `prioirty` passait) et les `notes` de type quelconque. Les deux cas « refusés » l'étaient par un plantage, pas par la validation.
- **Correction** : `build_rules.py` est réécrit, sans dépendance nouvelle (PyYAML seulement). Il apporte :
  - un chargeur strict qui refuse les clés dupliquées et ne convertit ni dates ni booléens implicites ;
  - un schéma explicite (champs obligatoires et autorisés, types, chaînes non vides, doublons dans les listes) ;
  - des dates `YYYY-MM[-DD]` valides et non postérieures à `meta.date` ;
  - des conflits structurés `{with, resolution}`, sans conflit avec soi‑même ;
  - une cohérence entre `status` et `superseded_by`, et un format d'ID ;
  - aucune exception non gérée, et la relecture de `rules.json` comparée aux données.
- **Proportion** : pas de JSON Schema externe ni de moteur de règles. Cela suffit pour un catalogue de 77 règles maintenu à la main.

### V11‑002 — Régressions de classification · **accepté, corrigé**
- **Correction** :
  - `scripts/classification.py` est désormais la référence exécutable (niveau, modules, voie rapide).
  - `tests/classification_cases.yaml` contient 21 cas aux attendus **écrits à la main** : les 9 combinaisons A × D, des modules de risque actifs à bas niveau, et 5 cas d'exclusion de la voie rapide.
  - `run_tests.py` vérifie aussi que la table de `09` §1.1 et la phrase de niveau de `14` concordent avec le code.
  - Il vérifie enfin, sur toutes les combinaisons, que le module de risque élevé ne dépend que de B et que la voie rapide est impossible quand B = 2.
- **Limite** : les cas de référence et le code ont le même auteur. L'indépendance tient à ce que les attendus sont des valeurs écrites, et non calculées.

### V11‑003 — Déclenchement de la voie rapide · **accepté, corrigé (prioritaire)**
- **Constat confirmé** : en v1.1, la formule « bien posée **ou** simple et sans risque » autorisait la voie rapide pour une demande bien rédigée mais dangereuse. Le principe 1 corrigeait le problème en théorie, mais pas la condition elle‑même.
- **Correction** : la voie rapide exige désormais deux conditions cumulées. Il ne doit y avoir aucun module bloquant (irréversible, destructif, données de production, financier, données sensibles ou communication externe, outil d'écriture, permission non établie, ambiguïté qui change le livrable). Et la demande doit être bien posée ou de niveau T0. Une demande bien formulée mais risquée **garde sa formulation**, mais reçoit les éléments de sécurité.
- **Fichiers concernés** :
  - `14` (branches de livraison, principe 1, modules) et `10` (section voie rapide, étape 15) ;
  - `09` §1.2, ainsi que les règles R‑GEN‑001 (avec un conflit déclaré avec R‑SEC‑003) et R‑CLASS‑001 ;
  - les 5 situations de l'observation sont des cas de test.

### V11‑004 — Incertitude statistique des gains de coût · **accepté, corrigé**
- **Correction** (`12` §5.1, règle R‑EVAL‑005) :
  - Un gain de coût n'est **établi** que si la borne supérieure de l'IC de Δ coût par succès est sous zéro, ou sous un seuil de gain pratique déclaré à l'avance. L'IC est calculé par bootstrap par cas, en recalculant le ratio à chaque rééchantillonnage.
  - Si l'estimation est favorable mais que l'IC contient zéro, ou s'il s'agit d'un pilote, la décision est **provisoire**. Elle est acceptable si le changement est réversible et peu coûteux. Elle est étiquetée, suivie en production et réévaluée après un nombre de cas fixé d'avance.
  - La fiche de résultat distingue désormais une adoption étayée d'une adoption provisoire.
- **Proportion** : aucune exigence nouvelle pour les explorations, qui restent permises mais ne concluent pas.

### V11‑005 — Volume des instructions persistantes · **accepté, `14` condensé ; efficacité non démontrée**
- **Auto‑relecture de `14`** :
  - Trois sections disaient la même chose sous trois formes : branches de livraison, modes et format de sortie. Elles sont fusionnées.
  - La méthode en 14 étapes était présentée comme une procédure. Elle devient une **liste de contrôle à appliquer selon les besoins** ; pour une demande simple, l'intention, les manques et les risques suffisent.
  - Deux lignes du tableau des techniques répétaient des modules (« agent qui écrit », « multi‑sessions ») : elles sont supprimées.
  - Les particularités de modèles sont réduites à celles qui changent le prompt. Le reste renvoie à `04`.
  - Le contenu des niveaux (T2) recoupait le module environnement : le chevauchement est retiré.
- **Ajouts justifiés** : la borne de la voie rapide, la délégation ponctuelle, la mention qu'un prompt court suffit pour une tâche difficile quand la cible est capable, et le gain de coût provisoire.
- **Résultat** : 2 096 mots, contre 2 433 en v1.1 (−14 %) et 1 537 en v1.0. Les 17 invariants critiques sont vérifiés par `run_tests.py`, ce qui évite qu'une condensation future en retire un sans le signaler.
- **Non démontré** : que la version condensée fasse mieux, ou aussi bien. La comparaison v1.2 / v1.1 / demande directe reste à mener (`12` §5.0).

### V11‑006 — Simplicité architecturale et délégation · **accepté, explicité**
- **Décision** : on distingue trois cas, résolution déclarée entre R‑ARCH‑001 et R‑ARCH‑002 :
  - **Architecture permanente ou répétée** : elle demande une preuve par mesure (R‑ARCH‑001).
  - **Délégation ponctuelle pendant une mission** : c'est le jugement de l'agent, selon les critères de R‑ARCH‑002, sans démonstration préalable. Cela préserve sa liberté méthodologique.
  - **Rendre la délégation systématique** (harnais, fichier persistant) : on la teste d'abord sur quelques missions.
- **Fichiers concernés** : `01` P9, `03` T‑20, `14` (tableau des techniques).

## 3. Nouvelles constatations de l'auto‑relecture

| ID | Constat | Gravité | Correction |
|---|---|---|---|
| SR‑01 | `07` §3 listait encore le **worktree comme une sandbox** : une régression de REVIEW‑005 restée hors du périmètre corrigé en v1.1 | Modérée | Corrigé : un worktree n'est pas une sandbox. Hook `PreToolUse` limité à l'outil visé, classifieur marqué probabiliste |
| SR‑02 | 7 lignes de `07` §1 n'avaient pas le type de contrôle (prévention, détection, réduction) annoncé par la légende | Mineure | Typées |
| SR‑03 | R‑AUTO‑005 (« Finishing work ») lu en disjonction : il s'appliquait à **toute** tâche longue, alors que la source et `11` le réservent au comportement observé ; coût d'environ +30 % de tokens | Modérée | Condition conjonctive : tâches longues ET arrêts observés ou documentés pour le modèle |
| SR‑04 | R‑EX‑001 déclenchait les exemples sur l'étiquette « modèle léger », en contradiction avec R‑MODEL‑003 (capacité observée) | Mineure | Corrigé |
| SR‑05 | L'interaction R‑ARCH‑001 / R‑VAL‑003 (relecteur systématique d'un travail long, même parfaitement testé) était signalée par la première revue (`03` §3) mais non traitée en v1.1 | Modérée | Relecteur seulement si un risque résiduel n'est pas couvert par les vérifications mécaniques (règle, `10`, `14`) |
| SR‑06 | R‑VAL‑002 (preuves) et R‑CTX‑001 (contexte minimal), toutes deux de priorité haute, sans résolution déclarée | Mineure | Résolution : preuves succinctes (extraits, références, commande et code retour) |
| SR‑07 | Le contenu des niveaux dans `10` §9 et `14` dupliquait le module environnement : risque de double comptage et de prompts gonflés | Mineure | Le niveau T2 ne porte plus le périmètre ni l'autonomie |
| SR‑08 | Terminologie mêlée « Tier » / « Niveau » dans `09` | Mineure | Unifiée |
| SR‑09 | Les références S‑R17 (titre obsolète) et S‑R7 étaient citées de mémoire | Mineure | Vérifiées ; `03` T‑05, `08` et R‑STR‑008 mis à jour |

Non modifié, par choix : `15_REVIEW_ARBITRATION.md` décrit l'état de la v1.1. Il indique notamment que le validateur testait la taxonomie, alors que ce test est déplacé dans `run_tests.py` en v1.2. C'est un document historique ; la correction est consignée ici et dans `CHANGELOG.md`.

## 4. Observations rejetées ou reportées

Aucune observation V11 n'est rejetée. Restent reportés :
1. **Sélecteur déterministe et schéma de preuves par proposition** : reportés depuis la v1.1. Les deux contre‑expertises jugent ce report proportionné.
2. **Normalisation des tags `models`** (fournisseur, harnais, capacité) : liée au point 1.
3. **Contrôle des références de section** : il ne couvre que les formes `` `NN` §X ``. Les renvois en prose (« voir le gabarit Relecteur ») ne sont pas vérifiés.

## 5. Le référentiel appliqué à lui‑même

| Principe | Évaluation | Verdict |
|---|---|---|
| Proportionnalité | La voie rapide et la liste de contrôle permettent de ne rien produire de superflu. Mais l'ensemble reste volumineux : 15 documents et environ 4 000 lignes. | Acceptable : seul `14` est chargé en permanence ; le reste se consulte à la demande |
| Contexte minimal suffisant | `14` est autosuffisant pour les invariants ; ses particularités datées renvoient à `04` | Respecté |
| Liberté méthodologique | La méthode n'est plus une procédure, la délégation ponctuelle est autorisée, la cible garde le droit de contester | Respecté |
| Coût total par succès | Le référentiel admet que son propre bénéfice n'est pas démontré et prévoit de le mesurer (`12` §5.0) | Cohérent, **non vérifié** |
| Capacités natives | L'effort plutôt que le texte, les outils de plan natifs, les hooks ; pas de CoT manuel | Respecté |
| Vérifiabilité | Le catalogue, la classification et les invariants sont testés automatiquement ; le comportement des modèles ne l'est pas | Partiel, par nature |
| Complexité injustifiée | Trois scripts Python sans dépendance nouvelle ; pas de moteur de règles | Respecté |

Risque principal : le coût de **maintenance**. Chaque nouvelle version de modèle touche `04`, `14` et les règles à volatilité haute. La procédure de `13` §7 et les tests réduisent ce risque sans l'éliminer.

## 6. Réponses aux questions sur `14`

| Question | Réponse |
|---|---|
| Utilisable sans consulter les autres documents ? | Oui pour les invariants. Consulter `04` ou la documentation du fournisseur si une particularité de modèle conditionne la mission. |
| Liberté suffisante pour l'imprévu ? | Oui : liste de contrôle indicative, principes ordonnés pour arbitrer, droit de contester l'approche. |
| Reconnaître qu'aucune optimisation n'est utile ? | Oui : voie rapide, bornée par la sécurité. |
| Choisir les techniques sans tout appliquer ? | Oui : le tableau est conditionnel, et la consigne dit explicitement que l'intention, les manques et les risques suffisent pour une demande simple. |
| Prompt court pour une mission complexe ? | Oui : c'est explicite au principe 3, et la voie rapide est permise pour une demande complexe mais sûre et bien posée (cas de test). |
| Sécurité indépendante de la complexité ? | Oui : principe 1 (« quels que soient le niveau et la branche »), modules non retirables ; c'est testé. |
| Recommandations conditionnelles aux capacités ? | Oui : capacités à établir, formulation conditionnelle, particularités datées. |
| Comportements déjà assurés imposés inutilement ? | Réduits. Restent quelques rappels (pas de MAJUSCULES, pas de CoT manuel) que les modèles cibles n'appliquent pas spontanément quand ils **écrivent** des prompts. Leur utilité n'est pas mesurée. |
| Branches complètes ? | Oui : voie rapide, clarification, prompt, optimisation, audit, comparaison. |

## 7. Incertitudes restantes

1. **Le bénéfice du protocole et de `14` n'est démontré par aucune mesure**, ni contre une demande directe, ni entre les versions 1.0, 1.1 et 1.2.
2. **Les contrôles techniques** (hooks, sandbox, lecture seule) n'ont pas été testés en conditions adverses sur une configuration réelle.
3. **Les sources** : environ 25 références scientifiques restent citées de mémoire (M). Les chiffres des fournisseurs (Fable 5.2, recherche multi‑agents) sont des tests internes non répliqués.
4. **La volatilité** : les particularités de modèles datent du 24 novembre 2026 et changeront à la prochaine version.
5. **Les cas de classification** sont cohérents en interne. Leur pertinence sur des demandes réelles reste à vérifier sur un échantillon annoté.

## 8. Appréciation finale de maturité

| Usage | Maturité |
|---|---|
| Documentation de référence pour humains | **Stable** |
| `14` comme instruction persistante d'une IA en assistance, avec revue humaine des prompts produits | **Prêt pour un pilote** |
| Usage agentique à fort enjeu | Pilote possible, **à condition** de mettre en place et de tester les contrôles externes recommandés ; le référentiel ne les remplace pas |
| Sélection automatique et déterministe de règles | **Non prêt**, et volontairement non visé |
| Affirmation d'un gain de qualité ou de coût | **Non étayée** tant que le pilote de `12` §5.0 n'a pas été mené |

Recommandation : stabiliser la v1.2 et ne plus la modifier avant d'avoir des données. La prochaine version doit être motivée par les résultats du pilote ou par une nouvelle version de modèle, pas par une nouvelle relecture.
