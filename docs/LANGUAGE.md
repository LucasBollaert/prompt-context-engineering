# Language policy — evidence behind it

Researched in November 2026, conditional knowledge: it is bounded to the models and tasks of the studies below and is not a universal figure.

## Language of instructions
- **Frontier models: a small gap.** Anthropic's published multilingual results (Global-MMLU, zero-shot) put French at about 99% of English for Claude Opus 5.5. These benchmarks are fully translated tasks, not just translated instructions.
- **Smaller or older models: English helps more, depending on the task.** In a comparison free of translation artefacts (Enomoto et al., NAACL 2025, short papers; Llama 3, Qwen 2 and Mistral instruct models), English instructions did better for reading comprehension, target-language instructions did better for lexical simplification, and label language mattered for classification. The authors conclude that the advantage of English is not overwhelming.
- **Output language drift.** In the same study, models given English instructions more often answered in another language. Anthropic's documentation recommends stating the output language explicitly, ideally in the system prompt.
- **What this means here.** The evidence does not show a large general gain from English instructions for frontier models, and no gain has been measured for this package. English is the default mainly for consistency with provider documentation and the CLIs, and to maintain one version; a modest gain is plausible on smaller models and some tasks, not guaranteed.
- **Translated prompts are new prompts.** Prompts tuned in one language often degrade when translated or applied to other languages (Zhang et al., *Cross-Lingual Prompt Steerability*, 2025). Behaviour must be re-checked after translation.

## Language of reasoning
- Reasoning models generally reach higher accuracy when they reason in English, and the gap grows with task difficulty (*The Reasoning Lingua Franca*, 2025, MGSM and GPQA Diamond: mathematics and science questions; transfer to other tasks is not established).
- Forcing the thinking language costs accuracy (Qi et al., *When Models Reason in Your Language*, Findings of EMNLP 2025).
- Pivoting through English can also introduce translation errors that native-language reasoning would avoid (*The Reasoning Lingua Franca*).

## Resulting rules (see `SYSTEM_PROMPT.md`, Language)
1. Instructions to models in English by default; the user's or profile's choice prevails.
2. Output language always stated explicitly.
3. Literal clauses and formats, labels and enumerations, quoted examples, human-facing texts and language-dependent tasks stay in their original language.
4. No imposed reasoning language, unless readable traces are needed and their accuracy cost is accepted.

The knowledge base (`referentiel/`) remains in French; models read it without difficulty. An English edition would be a separate version, with its own tests.

## Sources
- Anthropic, *Multilingual support*, Claude Platform documentation (consulted November 2026).
- Enomoto, Kim, Chen, Komachi, *A Fair Comparison without Translationese: English vs. Target-language Instructions for Multilingual LLMs*, NAACL 2025.
- Zhang et al., *Cross-Lingual Prompt Steerability: Towards Accurate and Robust LLM Behavior across Languages*, arXiv:2512.02841.
- *The Reasoning Lingua Franca: A Double-Edged Sword for Multilingual AI*, arXiv:2510.20647.
- Qi, Chen, Xiong, Fernández, Bitterman, Bisazza, *When Models Reason in Your Language: Controlling Thinking Trace Language Comes at the Cost of Accuracy*, Findings of EMNLP 2025.
