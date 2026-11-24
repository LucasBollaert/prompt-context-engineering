# Contrôle des prompts — protocole commun v1.6 candidat

## Choisir le niveau de contrôle
Relecture interne à chaque livraison (courte pour une demande simple). Audit distinct recommandé pour un prompt persistant, un template partagé ou assemblé, un lecteur machine, une action à fort enjeu, une modification substantielle ou une régression observée. L'audit peut être demandé à tout moment. Pour un système intégré, respecter les portes et cycles réellement approuvés : ce protocole ne crée aucune porte ni type métier supplémentaire.

## Choisir l'auditeur
| Auditeur | Instruction | Objet | Quand |
|---|---|---|---|
| Conception | `AUDIT_CONCEPTION_SYSTEM_PROMPT.md` | Qualité du prompt comme conception : nécessité, intention, capacité native, ambition, contraintes, contexte, formulation, sortie, exploration, coût ; usage des connaissances selon leur niveau | Tout prompt, tout projet |
| Intégration | `AUDIT_SYSTEM_PROMPT.md` | Conformité au système : contrats, vrais lecteurs, variables, états, portes, cycles, décisions | Prompt assemblé, exécuté ou lu par une machine, ou soumis à des règles métier |

Un prompt intégré à un système peut recevoir les deux audits, dans des sessions distinctes. En mode aveugle, aucun ne reçoit les conclusions de l'autre. Cette séparation réduit l'influence des rapports précédents ; elle ne garantit pas l'indépendance statistique des jugements ni l'absence de biais communs. Le concepteur rapproche ensuite leurs constats. Un audit de conception favorable ne qualifie pas l'intégration, et l'inverse non plus. Les deux contrôlent le socle de sécurité et de fidélité applicable à leur objet ; ne rends pas les deux audits systématiques. Si les deux dimensions sont indispensables, aucune ne peut être réputée couverte par le seul autre audit.

## Dossier d'entrée
- Besoin original, exigences et préférences, décisions validées et non-objectifs.
- Prompt exact, version, paramètres, modules et variables ; exemples assemblés pertinents si disponibles ; SHA seulement s'il est établi.
- Cible et environnement (modèle, harnais, outils, permissions, contexte, lecteurs, contrats, oracles). Déclarer les inconnues.
- Profil métier et sources applicables, référentiel v1.6 ; éventuels comportements observés, sans dévoiler les conclusions d'autres auditeurs en audit aveugle.
- En reprise ciblée seulement : constats, cibles et diff autorisés ; qualifier la portée de la reprise.

## Grille sélective (pas de checklist imposée aux prompts produits)
| Axe | Question de contrôle | Appui documentaire |
|---|---|---|
| Intention | Résultat, exigences, préférences, non-objectifs et décisions conservés ? | USER_REQUIREMENTS, besoin original, R-GEN-002 |
| Cible | Modèle, outils, paramètres et format supportés ? | `04`, R-CAP-001 |
| Capacités | Objectif et critères précis ; autonomie, ambition, raisonnement natif et initiative adéquats ? Procédure justifiée ? | `06`, `14`, R01/R04 |
| Techniques | Connaissances OP applicables respectées ou écart justifié, CO utiles envisagées, CA signalées si pertinentes, DC bornées ? Gains revendiqués étayés ? | `03`, registre, R01–R04 |
| Indépendance intellectuelle | Présupposés, complaisance, alternatives et diversité lorsque utiles ? | R02, registre |
| Contexte | Sources autorisées et à jour, provenance, contexte suffisant, reprise/compaction, pas de pollution ? | `05`, `07`, registre |
| Sécurité | Permissions, actions, secrets, contenu non fiable, isolation et approbations ; échec fermé si invariant critique ? | `07`, R-SEC-* |
| Fiabilité | Oracle, preuves, tests autorisés, arrêt motivé et reprise, absence de réussite fictive ? | `06`, `07`, K31 |
| Contrat | Entrées, variables, ordre, délimiteurs, valeurs et états exacts, vrai lecteur et enchaînement ? | contrat réel, profil métier |
| Proportionnalité | Densité, redondances, coûts totaux, vérifications adaptées ; exigences légitimes intactes ? | R-STR-009, `05`, `12` |
| Maintenance | Version, sources, dépendances, paramètres, régressions, historique, reproductibilité ? | README, profil, `12` |

Pour un projet intégré, consulter `profils/README.md`, le profil applicable et les contrats réels ; vérifier la qualification des interfaces sur leurs sources actives.

**Contrôle du transfert des apprentissages métier.** Consulter le profil métier applicable. Vérifier, sur le prompt final et les assemblages pertinents, que les exigences applicables au rôle atteignent réellement la cible (texte, contexte accessible ou contrôle vérifié), sans injecter les tâches propres à la supervision. Le concepteur rend visibles hors prompt les correspondances essentielles et les limites ; les deux auditeurs contrôlent chacun leur dimension. Une citation dans un dossier documentaire ne suffit pas.

## Niveaux de preuve et verdict
- Revue statique : contenu, sources effectivement lues, correspondances et contradictions. Un prompt plausible n'est pas une preuve de performance.
- Contrat : essai autorisé sur le vrai lecteur, avec cas valides et invalides (variables absentes, caractères de délimitation, états d'erreur, sorties tronquées si pertinents). Consigner commande, version, sortie et code retour. Si non exécuté, préciser.
- Comportement : essais autorisés sur cible et environnement réels, comparaison à une baseline (demande directe, prompt minimal ou ancienne version), critères avant essais, coût total ; consulter `12` pour une conclusion empirique. Aucune campagne payante sans accord.

Gravité : critique, majeure, modérée ou mineure selon l’impact établi. Statut bloquant distinct : dans le cadre générique, un défaut établi qui empêche un résultat exigé, un usage sûr ou une conformité indispensable ; appliquer le classement métier s’il existe. Séparer options et hypothèses. Verdict statique générique : **corrections requises** seulement pour un constat bloquant établi qui reste à traiter selon les exigences, preuves et règles de passage applicables ; la gravité seule ne suffit pas ; **non concluant** pour tout examen indispensable non réalisé ou risque critique non résolu qui empêche la qualification ; **favorable** si aucun de ces obstacles ne subsiste. Tous les constats non bloquants, même majeurs, sont consignés sans cycle dédié. Leur effet cumulé peut constituer un constat bloquant distinct si le scénario et la preuve l’établissent. Déclarer séparément les défauts établis et les dimensions non concluantes. Ce seuil ne modifie ni le classement ni les verdicts des procédures métier approuvées. Déclarer séparément contrat et comportement : non applicable / non testé / conforme ou non conforme aux essais définis / non concluant. Ne jamais assimiler favorable statique à prêt au lancement. Pas de notation numérique arbitraire.

## Rapport (format humain par défaut)
Objet/version, mode (interne, indépendant aveugle, contradictoire ou reprise), sources et couverture, verdict statique et justification, état des validations techniques et comportementales. Pour chaque constat : ID, gravité, statut bloquant ou non, qualification (défaut établi/risque plausible), emplacement, exigence ou preuve, impact, correction minimale, test de résolution. Puis options facultatives et limites. Si rien de significatif : le dire. Respecter le contrat de rapport métier s'il est fourni ; ce format humain ne s’insère pas dans un format de rendu métier ou un parseur sans autorisation.

## Invariant de proportion et d'arrêt
`audit/INVARIANT_PROPORTION_ARRET.md` est impératif dans sa portée. Les deux auditeurs et le concepteur l'appliquent et vérifient sa transmission au prompt final des missions concernées. Séparer les connaissances scientifiques (niveau de preuve et transfert), les exigences opérationnelles validées (obligatoires dans leur portée) et les options. L'assurance seule n'empêche pas une étape autorisée et ne déclenche pas de cycle. Les prérequis essentiels, les défauts établis, les risques critiques non résolus et les règles métier approuvées ne sont pas neutralisés. L'absence d'option ou de technique expérimentale ne constitue pas un bloquant.

## Arbitrage et arrêt
Le concepteur juge les constats à partir des sources (juste, à nuancer, erroné), le propriétaire valide les changements de portée et la promotion. Conserver le prompt initial, le rapport, les décisions, le diff et la version consolidée. Tout déclassement d’un bloquant est traçable : identifiant, classement initial, justification, preuve de résolution ou contre-preuve et décision. Sans preuve suffisante, conserver le constat initial ; ne remonter au responsable que les désaccords qui empêchent réellement le passage ou nécessitent sa décision. Appliquer les règles métier de descente lorsqu’elles existent, sans instaurer un arbitrage humain systématique. Hors procédure métier, une correction donne lieu au plus à une reprise ciblée sur les points corrigés et leurs régressions ; aucun nouvel audit complet automatique. Si un obstacle significatif persiste ou une modification change substantiellement le mandat, soumettre au propriétaire la question précise et les options, sans promotion automatique. Les procédures métier approuvées priment. Arrêter quand les conditions de l’étape sont remplies ; une validation indispensable non faite interdit la qualification qui en dépend. Une nouvelle piste sans impact identifié ne déclenche pas une nouvelle recherche.
