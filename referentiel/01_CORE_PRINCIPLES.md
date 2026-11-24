# 01 — Principes fondamentaux

Ces principes valent pour tous les modèles étudiés. Chacun indique son niveau de preuve et ses limites. Les règles opérationnelles qui en découlent sont dans `rules.yaml` (IDs entre crochets).

## Résumé en 13 lignes

1. Optimiser le **coût total** du résultat, pas la taille du prompt.
2. Spécifier le **résultat** (objectif, critères, contraintes) plutôt que la **procédure**.
3. Le contexte est une **ressource finie** qui se dégrade quand elle grossit.
4. Expliquer le **pourquoi** d'une contrainte ; le modèle généralise mieux.
5. Les modèles récents sont **littéraux** : ce qui n'est pas demandé n'est pas fait, ce qui est crié est sur‑appliqué.
6. Fournir un **oracle** : une vérification exécutable vaut mieux qu'une consigne « vérifie bien ».
7. Un prompt **n'est pas un contrôle** : ce qui doit être garanti l'est par un mécanisme externe.
8. Régler l'**autonomie** sur la **réversibilité** et le **risque**, pas sur la difficulté.
9. Commencer **simple** ; chaque ajout de complexité doit être justifié par une mesure.
10. Un prompt doit être **cohérent** : les contradictions coûtent du raisonnement et produisent de l'arbitraire.
11. Les recommandations sont **spécifiques** à un modèle et à un environnement, et **datées**.
12. **Mesurer** plutôt que croire : l'amélioration perçue n'est pas l'amélioration réelle.
13. Écrire pour un **lecteur à faible contexte** : sous‑agent, relecteur, ou humain qui revient.

---

## P1 — Le coût total, pas la longueur du prompt [R-COST-001]

**Énoncé.** Le coût d'un résultat est : tokens d'entrée (dont contexte répété à chaque tour) + tokens de raisonnement + tokens de sortie + appels d'outils + tours de correction + temps humain de vérification et de reprise. Un prompt initial plus long qui évite deux tours de correction est généralement moins cher.

**Preuve.** [DOC] pour la structure de facturation (entrée, sortie, cache). [OFF] Claude Code : « A clean session with a better prompt almost always outperforms a long session with accumulated corrections » (docs Claude Code, *Best practices*). [EMP] Anthropic mesure, pour son système de recherche multi‑agents, que la quantité de tokens explique à elle seule 80 % de la variance de performance sur BrowseComp — dépenser plus peut être rentable si la tâche le justifie.

**Limites.** Le temps humain est rarement mesuré ; il domine pourtant souvent le coût réel.

## P2 — Spécifier le résultat, pas le chemin [R-AUTO-001]

**Énoncé.** Décrire l'objectif, les critères d'acceptation, les invariants et les limites. Ne prescrire une méthode que si elle est elle‑même une exigence (conformité, reproductibilité, sécurité) ou si le modèle échoue mesurablement sans elle.

**Preuve.** [OFF] Anthropic : préférer des instructions générales (« réfléchis en profondeur ») à des plans pas‑à‑pas prescriptifs avec le thinking. [OFF] Anthropic, *Demystifying evals for AI agents* (janv. 2026) : ne pas sur‑spécifier le chemin de l'agent. [OFF] OpenAI, guide `gpt-5.3-codex` : retirer les demandes de plan préalable et de préambules quand l'intégration ne conserve pas le champ `phase`, car elles peuvent provoquer un arrêt prématuré.

**Limites.** Les modèles légers et les modèles locaux bénéficient plus souvent d'une procédure explicite ([HYP], cohérent avec l'expérience courante, peu de mesures publiques comparatives).

## P3 — Le contexte est fini et se dégrade [R-CTX-001]

**Énoncé.** Au‑delà d'une certaine longueur, ajouter du contenu tend à rendre l'exploitation du contexte moins fiable, surtout avec des distracteurs proches. Inclure ce qui change la réponse ; retirer le reste ; charger le reste à la demande. *(Heuristique étayée sur les modèles et tâches étudiés, pas une loi universelle ni une dégradation monotone garantie.)*

**Preuve.** [EMP] Chroma, *Context Rot* (juillet 2025) : sur 18 modèles, la performance devient moins fiable quand la longueur de l'entrée augmente, même à tâche constante. [EMP] Liu et al., *Lost in the Middle* (2023) : information au milieu d'un long contexte moins bien exploitée. [OFF] Anthropic, *Effective context engineering* (sept. 2025) : traiter le contexte comme une ressource finie à rendements décroissants. [OFF] Docs Claude Code : la fenêtre de contexte est la ressource la plus importante à gérer.

## P4 — Expliquer le pourquoi [R-CLAR-002]

**Énoncé.** « Pas de points de suspension, car la sortie est lue par un moteur de synthèse vocale » produit une meilleure généralisation que « NE JAMAIS utiliser de points de suspension ».

**Preuve.** [OFF] Anthropic, *Prompting best practices* (exemple cité ci‑dessus).

**Bénéfice secondaire.** La raison permet au modèle de traiter correctement les cas non prévus et de détecter quand la règle ne s'applique pas.

## P5 — Littéralité des modèles récents [R-CLAR-001, R-TONE-001]

**Énoncé.** Les modèles de pointe de 2025‑2026 documentés par Anthropic et OpenAI suivent les instructions de façon plus littérale que leurs prédécesseurs (à vérifier pour tout autre modèle). Deux conséquences :
- Ce qui n'est pas demandé n'est pas fait : demander explicitement l'ambition (« inclus autant de fonctionnalités pertinentes que possible ») ou l'action (« modifie » plutôt que « peux‑tu suggérer »).
- Ce qui est martelé est sur‑appliqué : « CRITICAL », « YOU MUST », « NEVER » provoquent du sur‑déclenchement ; « never » est traité comme absolu.

**Preuve.** [OFF] Anthropic : les formulations agressives héritées causent un sur‑déclenchement ; remplacer « CRITICAL: You MUST use this tool when… » par « Use this tool when… ». [OFF] Anthropic, Fable 5.2 : le modèle traite « never » comme absolu, préférer « Ask for approval before deleting files ». [OFF] OpenAI, GPT‑5 : un prompt contradictoire force le modèle à dépenser du raisonnement pour concilier les règles ; Cursor a constaté qu'une consigne « sois THOROUGH » provoquait un usage excessif d'outils.

## P6 — Un oracle plutôt qu'une injonction [R-VAL-001]

**Énoncé.** Le modèle s'arrête quand le travail « a l'air fini ». Lui donner un signal binaire lisible (tests, build, linter, diff contre une référence, capture d'écran comparée) ferme la boucle.

**Preuve.** [OFF] Docs Claude Code : « Give Claude a check it can run… It's the difference between a session you watch and one you walk away from. » Demander des **preuves** (sortie de test, commande et code retour) plutôt qu'une affirmation de succès.

## P7 — Un prompt n'est pas une garantie [R-SEC-001]

**Énoncé.** Une instruction textuelle est probabiliste. Tout ce qui doit arriver à chaque fois, ou ne jamais arriver, relève d'un mécanisme externe : hook, permission, sandbox, schéma, test, approbation humaine. Ce mécanisme ne garantit que la propriété qu'il contrôle, sur les canaux qu'il couvre ; certains contrôles (relecteur LLM, `/goal`, classifieurs) sont eux‑mêmes probabilistes (`07` §3.1).

**Preuve.** [OFF] Docs Claude Code : les instructions de CLAUDE.md sont consultatives, les hooks sont déterministes. [OFF] Anthropic (bloc paiements) : « C'est une consigne, pas une garantie : faites approuver par une personne chaque appel d'outil capable de mouvoir de l'argent. » [EMP] Beurer‑Kellner et al. (2025) : il est peu probable que des agents généralistes offrent des garanties fiables contre l'injection de prompt tant que défenses et agents reposent sur la même classe de modèles.

## P8 — Autonomie proportionnée au risque, pas à la difficulté [R-AUTO-003]

**Énoncé.** Une tâche difficile mais réversible (refactorisation sur une branche avec tests) mérite beaucoup d'autonomie. Une tâche facile mais irréversible (supprimer une base, envoyer un e‑mail) mérite un point d'arrêt.

**Preuve.** [OFF] OpenAI GPT‑5 : seuils d'incertitude différents par outil (très bas pour un paiement ou une suppression, très haut pour une recherche). [OFF] OpenAI GPT‑6.2 : s'arrêter uniquement pour changement de périmètre, blocage réel, décision réservée à l'utilisateur, ou avant une action irréversible. [OFF] Anthropic : confirmer avant les actions destructives, visibles par d'autres ou difficiles à annuler.

## P9 — Simplicité d'abord [R-ARCH-001]

**Énoncé.** Pour une architecture **permanente ou répétée**, commencer par un appel unique, bien spécifié, avec le meilleur modèle abordable. N'ajouter chaîne, multi‑agents, auto‑critique ou vote que si une mesure montre un gain qui couvre le coût.

**Preuve.** [OFF] Anthropic, *Building multi-agent systems* (janv. 2026) : des équipes ont passé des mois sur des architectures multi‑agents pour découvrir qu'un meilleur prompt sur un agent unique donnait des résultats équivalents. [EMP] Le système de recherche multi‑agents d'Anthropic consomme environ 15× les tokens d'une conversation.

**Portée.** Ce principe vise la conception d'architectures. Il n'interdit pas à un agent de déléguer **ponctuellement** pendant une mission quand les critères de R-ARCH-002 sont réunis ; rendre cette délégation systématique (harnais, fichier persistant) suppose de la tester d'abord.

## P10 — Cohérence interne et hiérarchie explicite [R-STR-004]

**Énoncé.** Deux règles qui se contredisent produisent un arbitrage imprévisible et coûteux. Résoudre les conflits dans le prompt, ou déclarer explicitement l'ordre de priorité.

**Preuve.** [OFF] OpenAI, GPT‑5 (exemple de l'assistant de triage médical aux règles contradictoires). [DOC] Hiérarchies natives : system/developer > user > contenus d'outils (OpenAI, *Instruction hierarchy*, Wallace et al., 2024 [EMP]) ; dans Codex, les instructions de l'utilisateur priment sur AGENTS.md pour les préférences et conventions, sans lever les restrictions système/développeur ni les permissions techniques (`07` §3.3).

## P11 — Spécificité et péremption [R-MAINT-001]

**Énoncé.** Une technique utile pour un modèle peut être neutre ou nuisible pour son successeur. Chaque recommandation doit porter un périmètre (modèle, version, environnement) et une date.

**Preuve.** [OFF] Anthropic publie une page de différences par version (Fable 5.2, Opus 5.5, Sonnet 5.5…), et recommande de refaire le balayage d'effort à chaque version plutôt que de reprendre celui du modèle précédent. [DOC] Le prefill de réponse, technique standard jusqu'en 2025, renvoie une erreur 400 sur Claude 4.6+.

## P12 — Mesurer, pas croire [R-EVAL-001]

**Énoncé.** La variance d'échantillonnage, l'effet de nouveauté et le biais de confirmation suffisent à faire paraître meilleure une formulation équivalente. Toute modification non triviale d'un prompt de production se valide sur un jeu d'évaluation, avec répétitions.

**Preuve.** [EMP] Sclar et al. (2023) : des variations de formatage sans changement de sens font varier fortement la performance de certains modèles. [OFF] Anthropic (Fable 5.2) : ajouter les consignes **une à la fois** et mesurer effet et coût. Voir `12`.

## P13 — Écrire pour un lecteur à faible contexte [R-COMM-001]

**Énoncé.** Un sous‑agent ne voit que son brief. Un relecteur ne voit que le diff. Un humain qui revient n'a pas vu les appels d'outils. Tout message transmis doit se suffire à lui‑même : objectif, contexte nécessaire, critères, format de retour.

**Preuve.** [OFF] Anthropic, Fable 5.2 : consigne « Write for an intelligent but low-context reader ». [OFF] Anthropic, *multi-agent research system* : des briefs de sous‑agents trop vagues provoquaient duplication du travail et lacunes.

---

## Ce qui n'est PAS un principe (idées reçues)

| Idée reçue | Statut | Pourquoi |
|---|---|---|
| « Plus le prompt est long et détaillé, mieux c'est » | Faux en général | Dilution, sur‑spécification, coût (P2, P3) |
| « Il faut toujours un rôle d'expert » | [CTR] | Utile pour le ton et le domaine ; effet sur l'exactitude faible ou nul dans les études (voir `03` T‑05) |
| « Il faut toujours demander de raisonner étape par étape » | [OBS] sur modèles à raisonnement natif | Le thinking natif le fait ; la demande peut gaspiller ou déclencher un refus (`reasoning_extraction`) |
| « Les majuscules augmentent l'adhérence » | [OBS]/[CTR] | Sur‑déclenchement sur modèles récents ; tolérable sur **une seule** ligne qui est réellement ignorée (docs Claude Code) |
| « Un prompt bien écrit garantit la sécurité » | Faux | P7 |
