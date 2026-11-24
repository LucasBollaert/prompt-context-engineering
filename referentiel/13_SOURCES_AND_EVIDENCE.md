# 13 — Sources, niveaux de preuve et maintenance

## 1. Statut de vérification

- **V** = consultée pendant la rédaction (23‑24 nov. 2026), contenu vérifié.
- **E** = consultée partiellement (extraits, résumés de recherche).
- **M** = référence connue citée de mémoire, **non re‑vérifiée** pendant la rédaction ; à contrôler avant de s'y appuyer pour une décision importante.
- **R** = consultée par la contre‑expertise indépendante du 24 nov. 2026 (S‑REV), qui en a confirmé le passage cité ; non relue intégralement par l'auteur.

Ces statuts sont des déclarations de consultation, pas des preuves d'exactitude. La contre‑expertise a vérifié de façon ciblée S‑A1, S‑A2, S‑A3, S‑A6, S‑A8, S‑A9, S‑O2, S‑O3, S‑O4, S‑R1, S‑R2 (résumé) et S‑R25 (résumé) ; les autres n'ont pas été vérifiées indépendamment.

## 2. Sources fournisseurs — Anthropic

| ID | Source | Date | Statut | Utilisée pour |
|---|---|---|---|---|
| S-A1 | *Prompting best practices* — platform.claude.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct | maintenue, consultée nov. 2026 | V | Clarté, raisons, exemples (3‑5), XML, long contexte (documents en haut, question à la fin, jusqu'à 30 %), thinking adaptatif, `budget_tokens` déprécié, prefill non supporté 4.6+, ton/majuscules, parallélisme, agentique, sous‑agents, sur‑ingénierie, tests, sécurité |
| S-A2 | *Prompting Claude Fable 5.2* — …/prompting-claude-fable-5-2 | consultée nov. 2026 | V | Effort, « Finishing work » (−50 % sessions inachevées, +30 % tokens), propriété du code (75 % vs <10 %, +70‑80 % tokens), progression, sous‑agents, prudence cumulée, prompts hérités, rapports, refus |
| S-A3 | *Best practices for Claude Code* — code.claude.com/docs/en/best-practices | maintenue, consultée nov. 2026 | V | Contexte, vérification, plan mode, CLAUDE.md, permissions/auto mode, hooks, skills, sous‑agents, sessions, fan‑out, revue adversariale, échecs fréquents |
| S-A4 | *Claude Code: Best practices for agentic coding* (blog) — anthropic.com/engineering/claude-code-best-practices | 18 avr. 2025, non maintenu | E | Historique (emphase « IMPORTANT/YOU MUST ») |
| S-A5 | *Effective context engineering for AI agents* — anthropic.com/engineering/effective-context-engineering-for-ai-agents | sept./oct. 2025 | E | Contexte fini, *context rot*, altitude, outils minimaux, exemples diversifiés, juste‑à‑temps, compaction, notes, sous‑agents (retours condensés) |
| S-A6 | *How we built our multi-agent research system* — anthropic.com/engineering/multi-agent-research-system | 13 juin 2025 | V (passages chiffrés, nov. 2026) | +90,2 % vs Opus 4 seul (évaluation interne de recherche, Opus 4 + Sonnet 4), tokens ~4× (agents) et ~15× (multi‑agents) **par rapport au chat**, 80 % de variance expliquée par les tokens (BrowseComp), limites (dépendances, code) |
| S-A7 | *Building multi-agent systems: when and how to use them* — claude.com/resources/articles/… | 23 janv. 2026 | E | Meilleur prompt mono‑agent souvent équivalent |
| S-A8 | *Demystifying evals for AI agents* — anthropic.com/engineering/demystifying-evals-for-ai-agents | 9 janv. 2026 | E | Tâches/essais/correcteurs, transcript vs résultat, pass@k / pass^k, ne pas sur‑spécifier le chemin, juge avec « inconnu » |
| S-A9 | *Pricing* / *Prompt caching* — platform.claude.com/docs/en/about-claude/pricing | consultée nov. 2026 | V | 1,25× / 2× / 0,1×, rentabilité, préfixe outils→system→messages, cumul Batch |
| S-A10 | *Building effective agents* — anthropic.com/engineering/building-effective-agents | déc. 2024 | M | Workflows vs agents ; commencer simple |
| S-A11 | *Writing effective tools for agents* — anthropic.com/engineering/writing-tools-for-agents | 2025 | M | Conception d'outils |
| S-A12 | *Effective harnesses for long-running agents* — anthropic.com/engineering/effective-harnesses-for-long-running-agents | nov. 2025 | M | Initialisation, liste de fonctionnalités, fichier de progression |
| S-A13 | *Equipping agents for the real world with Agent Skills* — anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | oct. 2025 | M | Chargement progressif |
| S-A17 | Anthropic — *Emotion concepts in a large language model* (2 avr. 2026) | V (résumé) | Vecteurs d'émotion de Claude Sonnet 4.5 ; « desperate » amplifié → triche et chantage accrus (steering, pas prompt) | [EMP] mécanistique |
| S-A18 | Anthropic — *Agentic misalignment* (20 juin 2025) | V (extraits) | Menace de remplacement ou conflit d'objectifs → actions nuisibles sur 16 modèles, dans des scénarios sans autre issue | [EMP] scénarios |
| S-A14 | *Structured outputs* — platform.claude.com/docs/en/build-with-claude/structured-outputs | consultée nov. 2026 | R | Schéma compilé en grammaire ; refus possibles ; pas de garantie d'exactitude métier |
| S-A15 | *Mid-conversation system messages and tool changes* — platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages | consultée nov. 2026 | V | Messages système ajoutés en cours de conversation (autorité d'opérateur, préfixe et thinking préservés), ajout/retrait d'outils inline (bêta), modèles supportés, interdiction d'y placer du contenu non fiable |
| S-A16 | *Per-message effort* — platform.claude.com/docs/en/build-with-claude/effort-per-message | consultée nov. 2026 | R | Changement d'effort par message selon plateforme |

## 3. Sources fournisseurs — OpenAI

| ID | Source | Date | Statut | Utilisée pour |
|---|---|---|---|---|
| S-O1 | *GPT-5 prompting guide* — developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | 7 août 2025 | V | Eagerness, préambules, effort, Responses API (73,9 → 78,2 %), contradictions, verbosité, minimal reasoning, Markdown (rappel 3‑5 messages), metaprompting, cas Cursor |
| S-O2 | *Prompt guidance* (GPT‑6.2) — developers.openai.com/api/docs/guides/prompt-guidance | consultée nov. 2026 (non datée) | V | Astra/Sol, clarification, autonomie, effort, paramètres retirés, ordre `instructions`, cache |
| S-O3 | *Prompt guidance — gpt-5.3-codex* | consultée nov. 2026 | V | Hypothèses raisonnables, bout en bout, outils, troncature 10k, migration (retirer plans/préambules), `phase`, compaction |
| S-O4 | *Codex best practices* — developers.openai.com/codex/learn/best-practices | consultée nov. 2026 | E | AGENTS.md (hiérarchie, court, mise à jour après erreur répétée), PLANS.md, skills, config, erreurs fréquentes |
| S-O5 | *GPT-5.1 prompting guide* | 13 nov. 2025 | E | Contexte historique |
| S-O6 | *GPT-5-Codex prompting guide* | 23 sept. 2025 | E | « Moins d'instructions », non interchangeable avec GPT‑5 |
| S-O7 | Wallace et al., *The Instruction Hierarchy* — arXiv:2404.13208 | 2024 | M | Hiérarchie system > user > outils |
| S-O8 | *Structured model outputs* — developers.openai.com/api/docs/guides/structured-outputs | consultée nov. 2026 | R | Conformité garantie pour sorties complètes non refusées et schémas supportés ; refus et `incomplete` à gérer |
| S-O9 | *Model selection* — developers.openai.com/api/docs/guides/model-selection | consultée nov. 2026 | V | « Pour la plupart des tâches dans ChatGPT Work ou Codex, commencer par GPT‑6.2 Sol » ; Astra pour projets complexes ; disponibilité variable selon produit |
| S-O10 | *Prompt caching* — developers.openai.com/api/docs/guides/prompt-caching | consultée nov. 2026 | V | GPT‑5.6+ : écriture 1,25× (TTL 30 min) ou 2,5× (12 h, Responses), tarifs totaux ; lecture 0,1× (0,05× sur GPT‑6.2 Astra/Sol, GPT‑6.1 Sol/Terra) ; seuil 1 024 tokens ; modèles antérieurs sans frais d'écriture |
| S-O11 | *Using GPT-5.3-Codex* — developers.openai.com/api/docs/guides/latest-model?model=gpt-5.3-codex | consultée nov. 2026 | V | Champ `phase` (`commentary` / `final_answer`) sur les items assistant, à conserver au replay ; requis quand le prompt demande des préambules ; sinon retirer plans/préambules du prompt |
| S-O13 | *Reasoning models* — developers.openai.com/api/docs/guides/reasoning | consultée nov. 2026 | V (partielle) | Replay sans réponses stockées : conserver chaque élément de sortie, raisonnement chiffré et phase de l'assistant compris, dans l'ordre d'origine ; la page ne liste pas les modèles concernés |
| S-O12 | *Custom instructions with AGENTS.md* — learn.chatgpt.com/docs/agent-configuration/agents-md | consultée nov. 2026 | R | Découverte global → racine → cwd, un fichier par niveau, overrides, limite par défaut 32 KiB |

## 4. Littérature scientifique et rapports techniques

| ID | Référence | Statut | Apport | Niveau |
|---|---|---|---|---|
| S-R1 | Hong, Troynikov, Huber — *Context Rot*, Chroma, juil. 2025 — research.trychroma.com/context-rot | V | Dégradation avec la longueur sur 18 modèles, distracteurs | [EMP] |
| S-R2 | Liu et al. — *Lost in the Middle*, arXiv:2307.03172 (TACL 2024) | M | Courbe en U de position | [EMP] |
| S-R3 | Hsieh et al. — *RULER*, arXiv:2404.06654 | M | Longueur effective < annoncée | [EMP] |
| S-R4 | Modarressi et al. — *NoLiMa*, 2025 | E (via presse) | Chute sans correspondance littérale | [EMP] |
| S-R5 | Wei et al. — *Chain-of-Thought Prompting*, arXiv:2201.11903 | M | CoT | [EMP] |
| S-R6 | Kojima et al. — *Zero-shot reasoners*, arXiv:2205.11916 | M | « Let's think step by step » | [EMP] |
| S-R7 | Sprague et al. — *To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning*, arXiv:2409.12183 (ICLR 2025) | V (résumé, nov. 2026) | Méta‑analyse de plus de 100 articles et 14 modèles : bénéfice concentré sur maths et logique | [EMP] |
| S-R8 | Liu et al. — *Mind Your Step (by Step)*, arXiv:2410.21333 | M | CoT nuisible sur certaines tâches | [EMP] |
| S-R9 | Turpin et al. — *Language Models Don't Always Say What They Think*, arXiv:2305.04388 | M | Infidélité du CoT | [EMP] |
| S-R10 | Wang et al. — *Self-Consistency*, arXiv:2203.11171 | M | Vote | [EMP] |
| S-R11 | Huang et al. — *LLMs Cannot Self-Correct Reasoning Yet*, arXiv:2310.01798 | M | Limites de l'auto‑correction | [EMP] |
| S-R12 | Madaan et al. — *Self-Refine*, arXiv:2303.17651 | M | Raffinement itératif | [EMP] |
| S-R13 | Yao et al. — *ReAct*, arXiv:2210.03629 | M | Raisonnement + action | [EMP] |
| S-R14 | Zhou et al. — *Least-to-Most*, arXiv:2205.10625 | M | Décomposition | [EMP] |
| S-R15 | Brown et al. — *GPT-3 / few-shot*, arXiv:2005.14165 | M | In‑context learning | [EMP] |
| S-R16 | Zhao et al. — *Calibrate Before Use*, arXiv:2102.09690 | M | Biais d'exemples | [EMP] |
| S-R17 | Zheng et al. — *When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of LLMs*, arXiv:2311.10054 (Findings EMNLP 2024 ; titre de la v1 : *Is "A Helpful Assistant" the Best Role…*) | V (résumé, nov. 2026) | 162 rôles, 2 410 questions factuelles : pas d'amélioration, effets nuls ou légèrement négatifs | [EMP] |
| S-R18 | Li et al. — *EmotionPrompt*, arXiv:2307.11760 (v1 à LLM@IJCAI'23) | V (résumé) | Gains relatifs +8 % / +115 % sur modèles de 2023 ; non répliqués (S-R29, S-R30) | [EMP] historique, non répliqué |
| S-R19 | Sclar et al. — *Quantifying LMs' Sensitivity to Spurious Features in Prompt Design*, arXiv:2310.11324 | M | Sensibilité au formatage | [EMP] |
| S-R20 | Tam et al. — *Let Me Speak Freely?*, arXiv:2408.02442 | M | Contraintes de format vs raisonnement | [EMP]/[CTR] |
| S-R21 | Xiong et al. — *Can LLMs Express Their Uncertainty?*, arXiv:2306.13063 | M | Sur‑confiance verbalisée | [EMP] |
| S-R22 | Zheng et al. — *Judging LLM-as-a-Judge*, arXiv:2306.05685 | M | Juges LLM et biais | [EMP] |
| S-R23 | Lewis et al. — *RAG*, arXiv:2005.11401 | M | RAG | [EMP] |
| S-R24 | Khattab et al. — *DSPy*, arXiv:2310.03714 ; Yang et al. — *OPRO*, arXiv:2309.03409 | M | Optimisation automatique | [EMP] |
| S-R25 | Beurer‑Kellner et al. — *Design Patterns for Securing LLM Agents against Prompt Injections*, arXiv:2506.08837 | V | Patterns, limites des défenses heuristiques | [EMP] |
| S-R26 | Debenedetti et al. — *CaMeL*, arXiv:2503.18813 | M | Défense par flux de données | [EMP] |
| S-R28 | Meincke et al. — *Prompting Science Report 3: I'll pay you or I'll kill you — but will you care?*, arXiv:2508.00614 (2025) | V (résumé) | Pourboires et menaces : pas d'effet significatif en général sur GPQA/MMLU-Pro ; effets par question imprévisibles | [EMP] |
| S-R29 | Vaugrante et al. — *A Looming Replication Crisis in Evaluating Behavior in Language Models?*, arXiv:2409.20303 | V (résumé) | Réplication de CoT, EmotionPrompting, ExpertPrompting, sandbagging, Re-Reading sur 6 modèles : pratiquement aucune différence significative | [EMP] |
| S-R30 | Joshi et al. — *Sticks and Stones: Positive vs. Negative Emotional Prompt Framings*, atelier Hypothesis Testing ICML 2026 | V (résumé) | Préenregistré, 28 000 essais, 5 modèles de 2026 : aucune asymétrie, légère baisse vs neutre (distraction) | [EMP] |
| S-R31 | Zhong, Raghunathan, Carlini — *ImpossibleBench*, arXiv:2510.20270 (ICLR 2026) | V (section 5) | Prompt strict, canal d'abandon, tests en lecture seule : fortes baisses de la triche, dépendantes du modèle | [EMP] |
| S-R32 | Geng et al. — *Measuring Pragmatic Influence in LLM Instructions*, arXiv:2602.21223 (2026) | V (résumé) | Urgence et autorité déplacent systématiquement la priorisation des consignes (5 modèles ouverts) | [EMP] |
| S-R33 | Jaroslawicz et al. — *How Many Instructions Can LLMs Follow at Once?* (IFScale), arXiv:2507.11538 (NeurIPS 2025) | E (résumé) | 500 consignes d'inclusion de mots, 20 modèles : 68 % au mieux à densité maximale ; biais vers les premières consignes | [EMP] |
| S-R34 | *LLMs Can Follow Instructions, But Not Many at Once* (Constraint Saturation Evaluation), arXiv:2608.12426 (préprint, août 2026) | E (résumé) | 1 à 12 contraintes vérifiées sans juge, 15 modèles : réussite conjointe effondrée au‑delà de quelques contraintes ; échecs quasi indépendants | [EMP] |
| S-R35 | Agarwal et al. — *Many-Shot In-Context Learning*, NeurIPS 2024 | E (résumé) | Des centaines d'exemples : gains importants vs few‑shot, surmonte des biais de pré‑entraînement | [EMP] |
| S-R36 | Leviathan, Kalman, Matias — *Prompt Repetition Improves Non-Reasoning LLMs*, arXiv:2512.14982 (déc. 2025) | V (HTML) | `<Q><Q>` : 47 victoires / 70, 0 défaite sans raisonnement (p < 0,1) ; neutre avec raisonnement ; modèles de 2024‑2025 | [EMP] |
| S-R27 | Schulhoff et al. — *The Prompt Report*, arXiv:2406.06608 | M | Taxonomie de techniques | [EMP] (revue) |

## 5. Sources industrielles et communautaires

| ID | Source | Statut | Apport | Niveau |
|---|---|---|---|---|
| S-I1 | Willison — *The lethal trifecta for AI agents*, simonwillison.net, juin 2025 | E (via Sophos) | Modèle de menace | [OFF] industriel |
| S-I2 | Meta — *Agents Rule of Two*, 2025 | E (via Sophos) | Règle de deux | [OFF] industriel |
| S-I3 | Sophos — *Operating inside the lethal trifecta*, 2026 | E | Contournement des défenses par attaques adaptatives | [EMP] secondaire |
| S-I4 | Cognition — *Don't Build Multi-Agents*, 2025 | E (via LangChain) | Limites multi‑agents qui écrivent | [OFF] industriel |
| S-I5 | OpenAI — *Model Spec* (version 2025-09-12), model-spec.openai.com/2025-09-12.html | R | Chaîne de commandement, statut des contenus non fiables | [OFF] industriel |
| S-I6 | OWASP GenAI — *LLM01 Prompt Injection* et *Improper Output Handling* (genai.owasp.org) | R | Modèle de risque : injection, sortie de modèle consommée en aval sans contrôle | [OFF] industriel |
| S-I7 | OWASP GenAI — *LLM07:2025 System Prompt Leakage* | R | Pas de secrets dans les prompts système | [OFF] industriel |
| S-I8 | OWASP — *LLM Prompt Injection Prevention Cheat Sheet* | R | Mesures de prévention | [OFF] industriel |
| S-I9 | NIST — *AI 600-1, Generative AI Profile* (doi:10.6028/NIST.AI.600-1) | R (notice) | Cadrage des risques informationnels (confabulation, contenus à fort enjeu) | [OFF] institutionnel |
| S-REV2 | Seconde contre‑expertise (observations V11‑001 à 006), 24 nov. 2026 | V | Voir `16` | [HYP] analytique |
| S-REV3 | Troisième contre‑expertise (V12‑001 à 016), 24 nov. 2026 | V | Voir `17` | [HYP] analytique |
| S-REV | Contre‑expertise indépendante du référentiel v1.0 (`independent_review/`, 24 nov. 2026) — 20 constatations | V | Défauts de contrat, de taxonomie, de garanties, d'arrêt, de statistiques ; voir `15_REVIEW_ARBITRATION.md` | [HYP] analytique (aucun essai de modèle) |

Les articles de blog communautaires consultés (Medium, DEV, DataCamp…) n'ont **pas** été retenus comme sources de preuve ; certains contiennent des chiffres non sourcés (ex. « ~80 % d'adhérence de CLAUDE.md »), volontairement exclus.

## 6. Carte des affirmations clés → preuve

| Affirmation | Fichier | Sources | Niveau | Robustesse |
|---|---|---|---|---|
| Le contexte long dégrade la performance | 01, 05 | S-R1, S-R2, S-R3, S-A3, S-A5 | [EMP] | Forte, multi‑sources |
| Documents en haut / question à la fin | 02, 05 | S-A1 | [OFF] | Moyenne pour Claude (test interne non publié) ; non transférable aux autres fournisseurs sans test |
| Les majuscules / « CRITICAL » sur‑déclenchent | 01, 08 | S-A1, S-A2, S-O1 (Cursor) | [OFF] | Moyenne, cohérente entre fournisseurs |
| Donner un oracle exécutable est le levier majeur en code | 01, 03 | S-A3, S-O4 | [OFF] | Forte (consensus fournisseurs) |
| Multi‑agents rentable seulement pour tâches parallèles | 03, 08 | S-A6, S-A7, S-I4 | [EMP]/[OFF] | Moyenne : le 15× compare au **chat**, pas à un agent unique à qualité égale ; +90,2 % = évaluation interne (Opus 4/Sonnet 4) |
| Personas n'améliorent pas l'exactitude | 03, 08 | S-R17 | [EMP] | Moyenne (questions factuelles, modèles 2023‑2024) |
| CoT manuel obsolète sur modèles à raisonnement | 03 | S-A1, S-A2, S-R7 | [OFF]/[EMP] | Forte |
| Auto‑correction sans signal externe peu efficace | 03 | S-R11 | [EMP] | Moyenne (modèles 2023 ; modèles récents meilleurs — S-A1 note qu'Opus 5 vérifie bien seul) |
| Confiance verbalisée mal calibrée | 06, 08 | S-R21 | [EMP] | Moyenne |
| Défenses textuelles contre injection insuffisantes | 07 | S-R25, S-R26, S-I3 | [EMP] | Forte |
| Prompt caching Anthropic : 1,25× / 2× / 0,1× | 05 | S-A9 | [DOC] | Forte (vérifiée), exceptions par modèle |
| Prompt caching OpenAI GPT‑5.6+ : écriture 1,25×/2,5×, lecture 0,1×/0,05× | 05 | S-O10 | [DOC] | Forte (vérifiée), varie par modèle |
| Structured outputs garantissent le schéma | 02, 03 | S-O8, S-A14 | [DOC] | Forte **sous conditions** (sortie complète, non refusée, schéma supporté) ; aucune garantie métier |
| Prompts plus longs pour tâches répétées / non supervisées | 05 | Raisonnement économique | [HYP] | À mesurer |
| Plus de structure aide quand la capacité observée est faible | 04, 10 | Pratique courante | [HYP] | À mesurer ; « léger » ou « local » ne signifie pas faible capacité |
| Le générateur de prompts réduit le coût total | 10, 14 | — | [HYP] | **Non démontré** ; protocole `12` §5.0 |

## 7. Méthode de mise à jour du référentiel

### 7.1 Déclencheurs
1. Sortie d'un nouveau modèle ou d'une nouvelle version chez un fournisseur couvert.
2. Modification d'une page de bonnes pratiques officielle (S-A1, S-A2, S-A3, S-O2, S-O3, S-O4).
3. Publication majeure (benchmark, attaque, technique).
4. Échec répété observé en production contredisant une règle.
5. Revue périodique : trimestrielle.

### 7.2 Procédure
1. **Collecter** les changements (page « differences from earlier models », notes de version, guides de migration).
2. **Classer** chaque changement : nouveau comportement, paramètre retiré/ajouté, recommandation modifiée, technique devenue obsolète.
3. **Mettre à jour `rules.yaml` d'abord** (source canonique ; mettre à jour `last_verified`) : modifier `models`, `evidence`, `status` (`active` → `deprecated`), ajouter `superseded_by`. Ne jamais réutiliser un ID ; une règle retirée garde son ID avec `status: deprecated`.
4. **Exécuter `python3 scripts/build_rules.py` puis `python3 scripts/run_tests.py`** : le premier valide le catalogue et régénère `rules.json` ; le second exécute les tests négatifs, les cas de référence de classification, la concordance 09/10/14, la présence lexicale des invariants de 14 et les références croisées. Ces tests ne prouvent pas la cohérence sémantique : après toute modification de `10` ou `14`, relire aussi `tests/semantic_review_cases.md`. Ne jamais éditer `rules.json` à la main. Toute modification de la classification passe par `scripts/classification.py`, `tests/classification_cases.yaml` (attendus écrits à la main), `09` et `14` ensemble.
5. **Répercuter** dans les fichiers Markdown concernés (chaque règle liste ses fichiers via `files`) ; en cas de divergence, `rules.yaml` fait foi pour les règles, le Markdown pour l'argumentation.
6. **Re‑valider** sur le jeu de régression (`12` §7) les prompts de production touchés : balayage d'effort, ablation des consignes héritées.
7. **Mettre à jour `14` dès qu'un changement affecte son contenu**, quelle que soit la priorité de la règle (une spécificité de modèle de priorité moyenne peut invalider une instruction persistante).
8. **Journaliser** dans §8 (date, changement, source).

### 7.3 Budget de `14`
`14` est passé de 1 537 mots (v1.0) à 2 302 (v1.3), chaque revue ayant ajouté des précautions. Pour éviter un effet de cliquet contraire au principe de proportionnalité, toute **addition** à `14` doit soit être compensée par une suppression équivalente, soit être justifiée par un échec observé (pilote, production) ou par une contrainte de sécurité nouvelle et documentée. Les relectures sans données ne suffisent plus à justifier un ajout.

### 7.4 Règles de péremption
- Recommandation spécifique à un modèle : à revoir à chaque version de ce modèle.
- [HYP] non testée depuis 12 mois : signaler comme « à vérifier ».
- Source **M** : à vérifier avant usage critique ; passer en **V** lors de la prochaine revue.

## 8. Journal des versions

| Version | Date | Changement |
|---|---|---|
| 1.0 | 2026‑11‑23/24 | Création. Modèles couverts : Claude Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5 ; GPT‑6.2 Astra/Sol ; gpt‑5.3‑codex. |
| 1.1 | 2026‑11‑24 | Intégration de la contre‑expertise (S‑REV) : codes de preuve en chaînes et validateur, sémantique de sélection, niveaux de prompt totaux + modules, portée des garanties, états terminaux, Codex conditionné au modèle, structured outputs, coût non chevauchant, baseline et non‑infériorité, 13 nouvelles règles. Détail : `15_REVIEW_ARBITRATION.md`. |
| 1.2 | 2026‑11‑24 | Observations résiduelles V11‑001 à 006 et auto‑relecture : validateur strict + 17 tests négatifs, cas de référence de classification, voie rapide bornée par la sécurité, incertitude du coût et décisions provisoires, architecture vs délégation ponctuelle, `14` condensé (−14 %) avec tests d'invariants, 9 corrections issues de l'auto‑relecture. Détail : `16_FINAL_REVIEW_AND_ARBITRATION.md`. |
| 1.3 | 2026‑11‑24 | Troisième contre‑expertise : validateur total (dates calendaires, types, énumération fermée, cycles), domaine d'entrée de la classification, voie rapide / prompt minimal, sécurité du générateur (provenance et autorité), confidentialité des prompts produits, fidélité à l'intention, module de prudence épistémique, protocole (effet du workflow vs de la reformulation, zéro succès, cas insolubles, paraphrases), portée des tests clarifiée. Détail : `17_THIRD_REVIEW_ARBITRATION.md`. |
| 1.4 | 2026‑11‑24 | Recherche sur le cadrage motivationnel (`research/R01`) : R‑TONE‑003 réécrite et requalifiée (EMP), vrais enjeux comme information (R‑CLAR‑002), droit à l'échec honnête et canal d'abandon (R‑AUTO‑011, R‑VAL‑004), force pragmatique (R‑STR‑004) ; corrections techniques (types stricts, vocabulaire méthodologique fermé) ; `14` à budget constant. |
