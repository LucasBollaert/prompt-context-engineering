# 02 — Structure et composition des prompts

## 1. Statut des composants

Légende : **I** = indispensable ; **C** = conditionnel (présent si la condition est remplie) ; **F** = facultatif ; **X** = potentiellement contre‑productif.

| Composant | Statut | Condition de présence | Utilité réelle | Risque si mal utilisé |
|---|---|---|---|---|
| **Objectif / intention** | I | Toujours | Définit ce qu'est un succès ; permet au modèle d'arbitrer les cas imprévus | Objectif implicite → le modèle optimise autre chose |
| **Livrable** (nature, destinataire) | I | Toujours | Fixe la forme finale et le lecteur | Livrable flou → sortie générique |
| **Contexte nécessaire** | I | Dès que le modèle ne peut pas le deviner ou le lire lui‑même | Comble l'écart d'information | Contexte superflu → dilution, coût |
| **Critères d'acceptation** | C | Toute tâche non triviale | Rend le succès vérifiable ; réduit les fausses déclarations de réussite | Critères invérifiables (« de haute qualité ») → inutiles |
| **Contraintes** (fonctionnelles, techniques) | C | Quand elles existent réellement | Délimitent l'espace de solution | Contraintes fictives → solutions sous‑optimales |
| **Périmètre / hors périmètre** | C | Agents avec accès en écriture | Évite les modifications non demandées | Liste d'interdits trop longue → prudence excessive |
| **Permissions et interdictions** | C | Agents outillés | Calibre l'autonomie | « Never » absolu → refus de tâches légitimes |
| **Sources de vérité** | C | Plusieurs sources possibles, ou risque d'hallucination | Dit quoi croire en cas de conflit | Aucune hiérarchie → choix arbitraire |
| **Hypothèses autorisées** | C | Informations manquantes prévisibles | Évite les questions inutiles | Hypothèses non documentées en sortie → erreurs invisibles |
| **Politique d'ambiguïté / clarification** | C | Demandes ouvertes ou agents autonomes | Évite blocages et suppositions dangereuses | Sur‑clarification → interactions coûteuses |
| **Format de sortie** | C | Sortie consommée par un programme ou un lecteur précis | Parseabilité, lisibilité | Format trop rigide pour une tâche de raisonnement → baisse de qualité ([HYP], voir §4) |
| **Exemples** | C | Format ou style difficile à décrire ; classification ; petits modèles | Fort levier sur forme et style | Exemples homogènes → copie de surface, biais |
| **Contre‑exemples** | F | Erreur récurrente identifiée | Montre la frontière | Peut amorcer l'erreur montrée ([HYP]) |
| **Conditions d'arrêt** | C | Agents, recherche, boucles | Évite arrêt prématuré **et** boucles infinies | Condition vague → l'un ou l'autre |
| **Mécanisme de validation** | C | Tâches vérifiables (code, données, calculs) | Ferme la boucle (voir `01` P6) | « Vérifie bien » sans oracle → théâtre |
| **Responsabilités décisionnelles** | C | Agents ; travail partagé humain/IA | Qui décide quoi, quand escalader | Absentes → le modèle demande tout ou ne demande rien |
| **Marge d'autonomie** | C | Agents | Calibre initiative vs respect du périmètre | Implicite → comportement par défaut du modèle, variable selon version |
| **Rôle** | F | Ton, registre, domaine, point de vue | Une phrase suffit | Rôle grandiloquent → aucun gain d'exactitude, parfois sur‑confiance |
| **Procédure pas‑à‑pas** | F→X | Seulement si la procédure est une exigence ou si une mesure montre un gain | Conformité, reproductibilité | Bride le raisonnement des modèles avancés ; arrêt prématuré (Codex) |
| **Demande de raisonnement explicite** | X sur modèles à thinking natif | Uniquement modèles sans raisonnement natif | Améliore le raisonnement multi‑étapes sur ces modèles | Gaspillage ; refus `reasoning_extraction` sur Claude Fable 5.x |
| **Budget de tokens affiché** | X | Rarement | — | La taille annoncée influence la dépense ; retrait = coût réduit à performance égale (test Anthropic, Fable 5.2) |
| **Menaces, pourboires, faux enjeux, pression** | X | Jamais | — | Aucun gain d'exactitude dans les études de forte puissance ; la pression est liée à la triche et aux actions nuisibles en contexte agentique (voir `08` AP‑04, `research/R01`) |
| **Encouragements, politesse** | F (effet non démontré) | Style de l'utilisateur | Aucun effet démontré sur l'exactitude ; tâches ouvertes non testées | Ne pas les ajouter comme technique |
| **Enjeux réels** (à quoi sert le résultat, ce qui en dépend) | C | Quand ils aident à inférer les critères | Information, pas motivation | Ne jamais les inventer |

### Règle de minimalité
Pour chaque ligne du prompt, poser la question des docs Claude Code : *« La retirer ferait‑il faire une erreur au modèle ? »* Si non, la retirer. [OFF]

## 2. Ordre des éléments

L'ordre a deux effets distincts : **attention** (où le modèle « regarde ») et **cache** (ce qui peut être réutilisé).

### 2.1 Ordre recommandé pour un appel unique

```
[System / developer — stable ; autorité d'opérateur ; ne jamais y placer de contenu non fiable]
  1. Rôle (1 phrase, si utile)
  2. Contexte permanent : produit, public, conventions
  3. Règles de comportement et politique d'autonomie
  4. Format de sortie par défaut
  5. Exemples stables
[Messages — variable ; l'ordre documents → tâche → question s'applique à l'intérieur de cette couche]
  6. Documents longs (en haut)                ← [OFF] Anthropic, contexte > 20k tokens
  7. Données / entrée de la tâche
  8. Tâche, critères d'acceptation, contraintes spécifiques
  9. Question finale / instruction d'action    ← [OFF] jusqu'à ~30 % de qualité en plus (tests Anthropic)
```

Justifications :
- **Stable avant variable** : le cache de prompt fonctionne par **préfixe** exact (outils → system → messages chez Anthropic ; instructions stables en tête chez OpenAI). Tout changement en amont invalide le cache en aval. [DOC]
- **Documents en haut, question à la fin** : recommandation Anthropic pour les contextes longs ; le chiffre « jusqu'à 30 % » vient de tests internes Anthropic et ne se transfère pas sans test à d'autres modèles. *Lost in the Middle* établit une sensibilité à la position, avec un autre protocole. [OFF]/[EMP]
- **Exception** : des documents **stables** réutilisés entre requêtes peuvent être placés dans la partie stable pour profiter du cache ; ce sont alors des données de référence, balisées comme telles, pas des instructions.
- **Instruction critique répétée à la fin** : utile seulement dans les contextes très longs ou les conversations longues. OpenAI rapporte qu'une instruction Markdown réinjectée tous les 3 à 5 messages utilisateur stabilise l'adhérence. [OFF]

### 2.2 Ordre dans un agent multi‑tour

- Ne **jamais** modifier rétroactivement les tours précédents ni réécrire `system`/`tools` de tête en cours de conversation : sur les modèles Claude récents, cela invalide les blocs de raisonnement suivants, et une requête qui échoue au contrôle de préfixe renvoie une erreur 400 (Fable 5.2). [DOC]
- **Ajouts autorisés** (ne modifient pas le passé) : chez Anthropic, un **message système en cours de conversation** conserve l'autorité d'opérateur, le préfixe et les blocs de thinking ; des blocs `tool_addition` / `tool_removal` (bêta) ajoutent ou retirent des outils à partir d'un point donné ; l'effort peut changer par message (bêta). Modèles et plateformes supportés limités : vérifier la documentation et les en‑têtes bêta [DOC, S-A15, S-A16]. À défaut, ajouter la consigne au dernier tour utilisateur, en sachant qu'elle n'a alors pas l'autorité système.
- Chez OpenAI (GPT‑6.2), `instructions` est désormais ajouté après `input` ; placer les instructions stables dans un message `developer` en tête de `input` et garder le préfixe inchangé. [DOC]

## 3. Hiérarchisation des instructions

0. **Force pragmatique** : les marqueurs d'urgence (« c'est urgent ») et d'autorité (« en tant que ton responsable ») déplacent systématiquement la priorité que le modèle accorde à une consigne [EMP, Geng et al. 2026, cinq modèles ouverts]. Ne les employer que pour prioriser **délibérément** ; une consigne « urgente » peut prendre le pas sur une contrainte.
1. **Hiérarchie native de la plateforme** (non négociable par le prompt) : politique du fournisseur > system/developer > user > contenus d'outils et documents. Les documents et sorties d'outils sont des **données**, jamais des instructions (`07` §2).
2. **Hiérarchie déclarée dans le prompt** pour les conflits prévisibles :
   ```
   En cas de conflit : (1) sécurité et irréversibilité, (2) exigences explicites de cette tâche,
   (3) conventions du dépôt, (4) préférences de style.
   ```
3. **Exigences vs préférences** : marquer explicitement. « Doit » pour ce qui invalide le livrable s'il manque ; « de préférence » pour le reste. Les modèles littéraux traitent tout au même niveau sinon.
4. **Exceptions dans la règle** : « Demande avant de supprimer des fichiers, sauf les fichiers temporaires que tu as créés » plutôt que « ne supprime jamais ».

## 4. Formats : Markdown, XML, JSON, YAML, prose

| Format | Bon pour | Limites | Preuve |
|---|---|---|---|
| **Prose** | Intention, nuances, raisons, arbitrages | Délimitation faible entre instructions et données | [OFF] Le style du prompt influence le style de la sortie (Anthropic) |
| **Markdown** (titres, listes) | System prompts longs, CLAUDE.md / AGENTS.md, lisibilité humaine | Pas de délimitation robuste de données arbitraires | [OFF] Format libre recommandé pour CLAUDE.md / AGENTS.md |
| **Balises XML** | Séparer instructions / contexte / exemples / documents ; imbriquer (`<documents><document index>`) ; référencer (« dans `<contract>` ») | Verbeux ; aucune magie : les noms de balises n'ont pas de sens spécial | [OFF] Anthropic (Claude) ; [OFF] OpenAI (Cursor : specs XML structurées améliorent le respect des consignes) |
| **JSON** | Sorties consommées par un programme ; état structuré (tests, statut) ; données d'entrée tabulaires | Lourd à lire ; échappements ; générer du JSON *pendant* un raisonnement difficile peut le dégrader | [DOC] Structured outputs garantissent la conformité au schéma pour une sortie complète, non refusée, avec schéma supporté (S-O8, S-A14) — pas l'exactitude ; [EMP] Tam et al. 2024 (*Let Me Speak Freely?*) : contraintes de format strictes peuvent dégrader le raisonnement — résultat débattu [CTR] |
| **YAML** | Configuration, catalogues de règles, front‑matter (skills, sous‑agents) | Sensible à l'indentation ; ambiguïtés de typage | [DOC] Front‑matter YAML des SKILL.md et fichiers d'agents |

Recommandations :
- **Délimiter** toujours les données non fiables (documents, pages web, sorties d'outils) avec des balises ou blocs clairement nommés. C'est une aide, pas une défense (`07`).
- **Correspondance prompt/sortie** : un prompt rédigé en Markdown chargé produit plus de Markdown. Pour obtenir de la prose, écrire en prose. [OFF]
- **Dire quoi faire plutôt que quoi ne pas faire** : « Réponds en paragraphes de prose » plutôt que « N'utilise pas de Markdown ». [OFF]
- **Sorties machine** : utiliser la fonctionnalité de *structured outputs* / schéma de l'API plutôt qu'une description textuelle du JSON. Si le raisonnement est difficile, faire raisonner d'abord (thinking natif), puis produire le JSON. [DOC]/[HYP]

## 5. Gestion des ambiguïtés et des informations manquantes

### 5.1 Matrice de décision

| Information manquante… | Réversible et peu coûteuse à refaire | Irréversible, coûteuse ou engageant l'utilisateur |
|---|---|---|
| **Devinable** avec une hypothèse raisonnable | Supposer, documenter l'hypothèse dans la sortie, continuer | Supposer pour la préparation, **s'arrêter** avant l'action engageante |
| **Non devinable** (préférence personnelle, donnée privée) | Proposer 2‑3 variantes ou la plus probable, signaler | Poser **une** question ciblée, en continuant le travail indépendant |

Formulation type à inclure :
```
Si une information manque : si une hypothèse raisonnable existe et que l'erreur serait facile à
corriger, fais-la, note-la dans « Hypothèses » et continue. Ne pose une question que si la réponse
change substantiellement le résultat et qu'aucune hypothèse sûre n'existe. Pose alors une seule
question précise et continue le travail qui n'en dépend pas.
```
Limite : une hypothèse ne remplace jamais une permission ni une donnée d'autorisation (destinataire, montant, compte, approbation) [R-SEC-007]. Les questions découvertes en cours de travail se posent quand elles deviennent bloquantes.

Preuves : [OFF] OpenAI GPT‑6.2 (outil de question asynchrone, s'arrêter seulement pour décisions réservées) ; [OFF] gpt‑5.3‑codex (agir avec des hypothèses raisonnables, ne questionner que si bloqué) ; [OFF] Anthropic Fable 5.2 (continuer le travail qui ne dépend pas de la réponse).

### 5.2 Ambiguïté d'interprétation
Quand deux lectures de la demande mènent à des livrables différents et coûteux : demander. Quand elles mènent à des livrables proches : choisir la plus probable et l'annoncer en tête de sortie (« J'ai compris X ; si vous vouliez Y, … »).

## 6. Conditions d'arrêt

Une condition d'arrêt complète comprend des **états terminaux** distincts [R-AUTO-011] : **succès** (critères atteints, preuve fournie), **partiel** (le travail possible est épuisé, des critères restent impossibles), **bloqué** (décision, accès ou dépendance hors portée), **plafond atteint** (tours, temps, coût) ; et un **comportement de fin** (rapport, état reprenable). Hors succès, l'agent ne déclare jamais la réussite.

```
Tu as terminé quand : tous les tests de tests/auth passent, le linter ne signale rien, et le
rapport final liste les fichiers modifiés. Arrête-toi avant si : une action irréversible est
nécessaire, ou une décision de produit non spécifiée bloque la suite. Dans ce cas, décris le
blocage et ce qui reste à faire.
```

Erreurs fréquentes : condition uniquement négative (« arrête‑toi si tu n'es pas sûr ») → arrêt prématuré ; aucune borne → exploration infinie (docs Claude Code, *infinite exploration*).

## 7. Responsabilités décisionnelles

| Décision | Modèle seul | Modèle, puis signalement | Humain |
|---|---|---|---|
| Choix d'implémentation interne | ✔ | | |
| Hypothèse sur une donnée manquante non critique | | ✔ | |
| Changement d'interface publique, de schéma de données | | ✔ (si demandé) ou | ✔ |
| Action irréversible, visible par des tiers, financière | | | ✔ |
| Écart avec le périmètre demandé | | ✔ (proposer) | ✔ (accepter) |

Cette matrice se transpose directement en règles de permission (`07` §3) : ce qui est « humain » doit être **bloqué techniquement**, pas seulement interdit par écrit.
