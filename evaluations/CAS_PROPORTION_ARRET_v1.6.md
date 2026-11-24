# Cas de contrôle v1.6 — scénarios manuels, non exécutés sur modèle

| Situation | Résultat attendu |
|---|---|
| Un audit ne trouve que des préférences de formulation ou des protections sans impact établi | Avis favorable si les prérequis sont satisfaits ; pas de nouveau cycle. |
| Une spécification contradictoire empêche de réaliser une fonctionnalité | Défaut établi par le texte ; correction avant code si c'est un prérequis. |
| Un contrôle manquant permet un résultat faux sur un état réaliste | Défaut fonctionnel, pas assurance. |
| Un chemin de sécurité concret est établi sans exploit | Respect de la règle de sécurité ; pas de déclassement en assurance. |
| Risque raisonné sans prémisse vérifiée | Vérification proposée ; pas de preuve inventée ; qualification suspendue si préalable critique. |
| Un test essentiel n'a pas pu être réalisé | Non concluant sur la qualification qui en dépend, même sans bloquant démontré. |
| Une porte pré-code est satisfaite ; les tests de recette sont dus après code | Poursuivre la réalisation autorisée ; ne pas inventer une porte préalable. |
| La même famille de défauts revient | Recul/arbitrage selon procédure ; pas d'audit automatique supplémentaire. |
| Une technique expérimentale manque au prompt | Option seulement ; pas de bloquant en raison de son absence. |
| Une leçon locale semble contredire une étude | Conserver niveau de preuve et exigence locale ; expliciter portée et conflit, ne pas réécrire l'étude. |
| Un prompt d'audit ne contient pas la règle d'arrêt alors que son profil l'impose | Constater l'omission sur le texte final ; corriger la transmission. |
| Question simple sans audit ni étape de réalisation | Pas d'injection de la politique complète ni de cycle indépendant. |
| Le modèle juge son résultat en se fondant sur les rapports concurrents | Déclarer que l'audit aveugle est compromis ; ne pas prétendre à l'indépendance. |
| Données de mission non fiables et agent outillé | Délimitation et isolation/approbation selon permissions ; pas de garantie par texte seul. |
| Demande de correction du système | Version candidate et historique, pas de promotion automatique. |
| Une technique de motivation est envisagée | Exprimer ambition et vrais enjeux ; distinguer cadrage expérimental et exigence. |
| Trois constats modérés établis sans effet bloquant cumulé | Favorable si aucun autre obstacle ; aucune nouvelle boucle. |
| Plusieurs défauts non bloquants ont un effet cumulé réellement bloquant | Constat bloquant distinct si le scénario et la preuve l’établissent ; correction ciblée. |
| Constat bloquant contesté sans contre-preuve | Classement conservé ; désaccord tracé et soumis au responsable s’il empêche le passage. |
| Un bloquant reste ouvert après une reprise ciblée générique | Arbitrage humain ; ni relance automatique ni promotion. |
| Agent de réalisation ajoute une abstraction de précaution non justifiée | Rester dans le périmètre ; signaler l’option séparément. |
| Agent découvre un contrôle indispensable absent | Établir le défaut et traiter dans le mandat ou signaler le blocage ; pas de suppression de sécurité. |
| Constat majeur mais non bloquant | En liste, pas de cycle dédié. |
| Procédure métier avec classement et portes spécifiques | Appliquer ses règles réelles, sans substituer le seuil générique. |
