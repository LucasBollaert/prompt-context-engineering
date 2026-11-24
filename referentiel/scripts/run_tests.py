#!/usr/bin/env python3
"""Tests locaux du référentiel (aucun appel réseau, aucun appel de modèle).

Portée : ces tests détectent des régressions de structure, de concordance et de présence
lexicale. Ils NE démontrent NI la cohérence sémantique des textes NI la qualité des prompts
produits. Une contradiction ajoutée à côté d'un invariant peut passer : voir la revue
sémantique manuelle (tests/semantic_review_cases.md).

Usage : python3 scripts/run_tests.py
  1. Catalogue réel valide ; rules.json équivalent aux données YAML.
  2. Tests négatifs : chaque mutation connue doit être refusée proprement (sans exception).
  3. Classification : cas de référence écrits à la main (tests/classification_cases.yaml),
     exhaustivité/exclusivité sur 729 combinaisons, indépendance des modules vis-à-vis du niveau.
  4. Concordance documentaire : table de 09 §1.1, phrase de niveau de 14, exclusions de la
     voie rapide dans 10 et 14.
  5. Références croisées : IDs de règles, anti-patterns, techniques, fichiers et sections.
"""
import glob, json, os, re, sys
from itertools import product
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from build_rules import validate_text          # noqa: E402
from classification import level, modules, fast_path, delivery   # noqa: E402
import copy                                            # noqa: E402
from build_rules import StrictLoader                   # noqa: E402

failures, passed = [], 0
def check(cond, msg):
    global passed
    if cond: passed += 1
    else: failures.append(msg)

read = lambda f: open(os.path.join(ROOT, f), encoding='utf-8').read()

# 1. Catalogue réel
text = read('rules.yaml')
data, errs = validate_text(text)
check(not errs, f"catalogue réel invalide : {errs[:5]}")
if os.path.exists(os.path.join(ROOT, 'rules.json')):
    check(json.loads(read('rules.json')) == data, "rules.json diffère de rules.yaml (relancer build_rules.py)")
else:
    failures.append("rules.json absent")

# 2. Tests négatifs
first_rule = text.index('- id: ')
def mutate(old, new, count=1, after=first_rule):
    return text[:after] + text[after:].replace(old, new, count)
mutations = {
    'clé dupliquée': mutate("  priority: high\n", "  priority: high\n  priority: low\n"),
    'date mois 99': mutate("last_verified: 2026-11", "last_verified: 2026-99"),
    'date invalide jour': mutate("last_verified: 2026-11", "last_verified: 2026-13-99"),
    'date future': mutate("last_verified: 2026-11", "last_verified: 2027-01"),
    'conflicts chaîne': re.sub(r"  conflicts: \[\]\n", "  conflicts: R-AUTO-001\n", text, count=1),
    'conflicts liste de chaînes': re.sub(r"  conflicts: \[\]\n", "  conflicts:\n  - R-AUTO-001\n", text, count=1),
    'conflit sans résolution': mutate("    resolution:", "    resolutio:"),
    'champ inconnu': mutate("  priority: high\n", "  priority: high\n  prioirty: low\n"),
    'notes non-liste': mutate("  priority: high\n", "  priority: high\n  notes: 42\n"),
    'OFF non cité': mutate("  - 'OFF'\n", "  - OFF\n"),
    'priorité hors énumération': mutate("  priority: high\n", "  priority: urgent\n"),
    'source inconnue': mutate("  - S-A1\n", "  - S-ZZ9\n"),
    'évidence vide': re.sub(r"  evidence:\n(  - '?[A-Z]+'?\n)+", "  evidence: []\n", text, count=1),
    'champ manquant': mutate("  volatility: low\n", ""),
    'dépréciée sans remplaçant': text.replace("  superseded_by:\n  - R-STR-007\n  - R-CLAR-003\n", ""),
    'ID dupliqué': mutate("- id: R-ARCH-001", "- id: R-COST-001"),
    'YAML cassé': text + "\n  - : : [\n",
}
# Mutations structurées (V12-001), appliquées en mémoire sur les données chargées
base = yaml.load(text, Loader=StrictLoader)
dep_i = next(i for i, r in enumerate(base['rules']) if r['status'] == 'deprecated')
def via(fn):
    d = copy.deepcopy(base); fn(d); return yaml.safe_dump(d, allow_unicode=True, sort_keys=False)
r0 = lambda d: d['rules'][0]
mutations.update({
    'date calendaire impossible (30 février)': via(lambda d: r0(d).update(last_verified='2026-02-30')),
    'meta.date impossible (31 novembre)': via(lambda d: d['meta'].update(date='2026-11-31')),
    'priority liste': via(lambda d: r0(d).update(priority=[])),
    'evidence contenant un objet': via(lambda d: r0(d).update(evidence=[{}])),
    'sources contenant une liste': via(lambda d: r0(d).update(sources=[[]])),
    'clé YAML complexe': text + "\n? [a, b]\n: x\n",
    'énumération status étendue': via(lambda d: (d['meta']['status_values'].append('banana'), r0(d).update(status='banana'))),
    'meta.canonical false': via(lambda d: d['meta'].update(canonical=False)),
    'remplacement vers soi-même': via(lambda d: d['rules'][dep_i].update(superseded_by=[d['rules'][dep_i]['id']])),
    'sources dupliquées': via(lambda d: r0(d).update(sources=r0(d)['sources'] * 2)),
    # v1.4
    'niveau de preuve fictif dans meta': via(lambda d: d['meta']['evidence_levels'].update(FAKE='x')),
    'niveau de preuve fictif utilisé': via(lambda d: (d['meta']['evidence_levels'].update(FAKE='x'), r0(d)['evidence'].append('FAKE'))),
    'transfer fictif': via(lambda d: d['meta']['transfer_levels'].update(zzz='x')),
    'volatilité fictive': via(lambda d: d['meta']['volatility_levels'].update(extreme='x')),
    'description de niveau vide': via(lambda d: d['meta']['evidence_levels'].update(DOC='')),
    'sémantique de sélection vidée': via(lambda d: d['meta'].update(selection_semantics={})),
    'version non numérique': via(lambda d: d['meta'].update(version='abc')),
    'conflits en double vers la même règle': via(lambda d: r0(d)['conflicts'].extend([{'with': 'R-ARCH-001', 'resolution': 'a'}, {'with': 'R-ARCH-001', 'resolution': 'b'}])),
})
# Cas explicitement AUTORISÉS (convention documentée dans meta.selection_semantics)
allowed = {'conditions vides (= toujours applicable)': via(lambda d: r0(d).update(conditions=[])),
           'nouveau tag modèle documenté (extensible)': via(lambda d: (d['meta']['model_tags'].append('gpt-7'), r0(d)['models'].append('gpt-7')))}
for name, mtext in allowed.items():
    _, e = validate_text(mtext)
    check(not e, f"cas autorisé refusé : {name} ({e[:2]})")

for name, mtext in mutations.items():
    check(mtext != text, f"mutation sans effet (test mal construit) : {name}")
    try:
        _, e = validate_text(mtext)
        check(bool(e), f"mutation acceptée : {name}")
    except Exception as ex:          # le validateur ne doit jamais planter
        failures.append(f"mutation « {name} » : exception {type(ex).__name__}: {ex}")

# 3. Classification
cases = yaml.safe_load(read('tests/classification_cases.yaml'))['cases']
for c in cases:
    A, B, C, D, E, F = c['axes']
    check(level(A, D) == c['level'], f"niveau {c['name']} : {level(A, D)} ≠ {c['level']}")
    perm, info = c.get('permissions', 'na'), c.get('info_stakes', 0)
    m = modules(B, C, E, F, perm, info)
    for x in c.get('modules_include', []):
        check(x in m, f"module {x} absent pour {c['name']}")
    for x in c.get('modules_exclude', []):
        check(x not in m, f"module {x} présent à tort pour {c['name']}")
    kw = dict(well_formed=c.get('well_formed', False), permissions=perm, info_stakes=info,
              missing_useful_lines=c.get('missing_useful_lines', False))
    if 'fast_path' in c:
        fp = fast_path(A, B, C, D, E, F, **kw)
        check(fp == c['fast_path'], f"voie rapide {c['name']} : {fp} ≠ {c['fast_path']}")
    if 'delivery' in c:
        dv = delivery(A, B, C, D, E, F, **kw)
        check(dv == c['delivery'], f"livraison {c['name']} : {dv} ≠ {c['delivery']}")
for c in yaml.safe_load(read('tests/classification_cases.yaml')).get('invalid_inputs', []):
    try:
        A, B, C, D, E, F = c['axes']
        delivery(A, B, C, D, E, F, permissions=c.get('permissions', 'na'),
                 well_formed=c.get('well_formed', False), info_stakes=c.get('info_stakes', 0),
                 missing_useful_lines=c.get('missing_useful_lines', False))
        failures.append(f"entrée hors domaine acceptée : {c['name']}")
    except ValueError:
        passed += 1
ad = {(c['axes'][0], c['axes'][3]) for c in cases}
check(len(ad) == 9, f"les cas de référence ne couvrent que {len(ad)}/9 combinaisons A×D")
levels = [level(a, d) for a, b, cc, d, e, f in product(range(3), repeat=6)]
check(len(levels) == 729 and all(l in {'T0', 'T1', 'T2', 'T3'} for l in levels), "fonction de niveau non totale")
for b, cc, e, f in product(range(3), repeat=4):
    ms = {frozenset(modules(b, cc, e, f)) for _ in range(1)}
    check(('risk_strict' in modules(b, cc, e, f)) == (b == 2), "module de risque mal déclenché")
    for a, d in product(range(3), repeat=2):
        if b == 2:
            check(delivery(a, b, cc, d, e, f, True) == 'prompt', "voie rapide ou prompt minimal possible avec risque élevé")

# 4. Concordance documentaire
t09 = read('09_TASK_CLASSIFICATION.md')
rows = re.findall(r'^\| \*\*A = (\d)\*\* \| (T\d) \| (T\d) \| (T\d) \|$', t09, re.M)
check(len(rows) == 3, "table A×D introuvable dans 09 §1.1")
for a, *ts in rows:
    for d, t in enumerate(ts):
        check(level(int(a), d) == t, f"09 §1.1 : A={a} D={d} indique {t}, code {level(int(a), d)}")
sentence = "**T3** si D = 2. Sinon **T2** si A = 2, ou si A = 1 et D = 1. Sinon **T1** si A = 1 ou D = 1. Sinon **T0**."
check(sentence in read('14_AI_PROMPT_ENGINEER_INSTRUCTIONS.md'), "14 : règle de niveau absente ou divergente")
for f in ['10_PROMPT_GENERATION_PROTOCOL.md', '14_AI_PROMPT_ENGINEER_INSTRUCTIONS.md']:
    t = read(f)
    check("jamais" in t and "voie rapide" in t.lower(), f"{f} : voie rapide non bornée")
    for kw in ['irréversible', 'permission']:
        seg = t[t.lower().index('voie rapide'):][:1500].lower()
        check(kw in seg, f"{f} : la condition de voie rapide ne mentionne pas « {kw} »")

# 4b. Présence lexicale des invariants de 14 (détecte une suppression, pas une contradiction ajoutée)
INVARIANTS_14 = {
    'priorité sécurité indépendante du niveau': "quels que soient le niveau et la branche",
    'prompt non garant': "Un prompt ne garantit rien",
    'type et portée des contrôles': "**prévient**, **détecte** ou **réduit**",
    'échec fermé': "échoue fermé",
    'hypothèse ≠ permission': "Une hypothèse ne remplace jamais une permission",
    'voie rapide bornée': "Elle ne s'applique **jamais**",
    'risque bien formulé': "**bien formulée mais risquée**",
    'modules non retirables': "ni le niveau ni la voie rapide ne les retirent",
    'états terminaux': "**états terminaux**",
    'actions conditionnées': "prescrites **seulement** si elles sont autorisées",
    'audit lecture seule': "Lecture seule",
    'contenu non fiable': "Données balisées comme non fiables",
    'états structured outputs': "refus, sortie incomplète, schéma non supporté",
    'preuves': "exige des preuves",
    'capacités non supposées': "Ne suppose pas qu'un AGENTS.md ou un CLAUDE.md est chargé",
    'gain de coût provisoire': "**provisoire**",
    'honnêteté': "Ne prétends pas avoir testé",
    'sortie exécutée en aval': "Ce que tu produis sera exécuté",
    'pas de promotion de contenu importé': "au rang d'instruction système sans mandat explicite",
    'pas de contournement de politiques': "contourner les politiques de sécurité de la cible",
    'confidentialité': "placeholders",
    'portée jamais changée en silence': "Ne change jamais la portée en silence",
    'enjeu informationnel': "**Enjeu informationnel**",
    'prompt minimal': "**prompt minimal**",
    'pas de faux enjeux ni pression': "Pas de menaces, de pourboires, de faux enjeux ni de pression",
    'échec honnête valable': "présente l'arrêt motivé comme une issue valable",
    'densité des exigences': "Le respect conjoint des « doit » baisse avec leur nombre",
    'exigences utilisateur conservées': "garde ceux de l'utilisateur",
    "registre : OP seul d'office": "n'applique d'office que l'OP",
}
t14 = read('14_AI_PROMPT_ENGINEER_INSTRUCTIONS.md')
for name, needle in INVARIANTS_14.items():
    check(needle in t14, f"14 : invariant manquant « {name} »")

# 5. Références croisées
ids = {r['id'] for r in data['rules']} if data else set()
mds = {os.path.basename(p): open(p, encoding='utf-8').read().replace('‑', '-') for p in glob.glob(os.path.join(ROOT, '*.md'))}
aps = set(re.findall(r'^### (AP-\d+)', mds['08_ANTI_PATTERNS.md'], re.M))
techs = set(re.findall(r'^### (T-\d+b?)', mds['03_ADVANCED_TECHNIQUES.md'], re.M))
prefix = {f[:2]: f for f in mds if re.match(r'^\d\d_', f)}
history = {'15_REVIEW_ARBITRATION.md', '16_FINAL_REVIEW_AND_ARBITRATION.md', 'CHANGELOG.md'}
for f, t in mds.items():
    for ref in set(re.findall(r'R-[A-Z]+-\d{3}', t)):
        check(ref in ids, f"{f} : règle inconnue {ref}")
    if f in history: continue
    for ref in set(re.findall(r'\bAP-\d+\b', t)):
        check(ref in aps, f"{f} : anti-pattern inconnu {ref}")
    for ref in set(re.findall(r'(?<![A-Za-z-])T-\d+b?\b', t)):
        check(ref in techs, f"{f} : technique inconnue {ref}")
    for num, sec in re.findall(r'`(\d\d)`\s*§(\d+(?:\.\d+)?)', t):
        target = prefix.get(num)
        check(target is not None, f"{f} : fichier `{num}` inexistant")
        if target:
            heads = re.findall(r'^#{2,4} (\d+(?:\.\d+)?)[.\s]', mds[target], re.M)
            check(sec in heads, f"{f} : section `{num}` §{sec} introuvable")

# 6. v1.5 — verdicts non bornés absents des textes opérationnels
for f, banned in [('14_AI_PROMPT_ENGINEER_INSTRUCTIONS.md', ["encouragements sont neutres", "inutiles pour la performance", "la pression favorise la triche"]),
                  ('08_ANTI_PATTERNS.md', ["sont **neutres**"]), ('02_PROMPT_STRUCTURE.md', ["F (neutre)"])]:
    txt = read(f)
    for b in banned:
        check(b not in txt, f"{f} : verdict non borné réintroduit « {b} »")
if data:
    tone = next(r for r in data['rules'] if r['id'] == 'R-TONE-003')
    check('neutre' not in tone['title'].lower(), "R-TONE-003 : titre encore « neutre »")
    check('HYP' in tone['evidence'], "R-TONE-003 : le risque agentique doit être marqué HYP")

# 7. Registre des connaissances (validateur strict scripts/registry.py, R04 §2)
from registry import validate_registry_text, VOCAB as REG_VOCAB   # noqa: E402
REG_PATH = os.path.join(ROOT, 'research', 'knowledge_registry.yaml')
reg_text = open(REG_PATH, encoding='utf-8').read()
rules_by_id = {r['id']: r for r in data['rules']} if data else {}
reg, reg_errs = validate_registry_text(reg_text, rules_by_id)
check(reg is not None and not reg_errs, f"registre invalide : {reg_errs[:3]}")


def reg_mut(old, new, count=1, base=None):
    src = reg_text if base is None else base
    assert old in src, f"motif de mutation introuvable : {old!r}"
    return src.replace(old, new, count)


REG_MUTATIONS = {
    # Les quatre cas acceptés par le validateur v1.5 (retour indépendant, §2)
    'verdict officiel fictif (meta + entrées)': reg_mut('benefit_shown', 'efficace', -1),
    'sources null': reg_mut("  sources: Meincke et al., Prompting Science Report 2\n", "  sources: null\n"),
    'clé tier dupliquée': reg_mut("  tier: OP\n", "  tier: OP\n  tier: CA\n"),
    'OP measured sans bénéfice mesuré': reg_mut(
        "    intervention:\n    - benefit_shown\n    transfer: current_models\n  population: tâches impossibles",
        "    intervention:\n    - untested\n    transfer: not_applicable\n  population: tâches impossibles"),
    # Défauts voisins
    'OP measured à transfert inconnu': reg_mut(
        "    transfer: current_models\n  population: tâches impossibles",
        "    transfer: transfer_unknown\n  population: tâches impossibles"),
    'OP sans base': reg_mut("  basis: measured\n", ""),
    'base sur une entrée non OP': reg_mut("  tier: CA\n", "  tier: CA\n  basis: measured\n"),
    "OP reposant sur une absence d'effet": reg_mut(
        "    - documented\n    transfer: current_models\n  population: QCM",
        "    - null_average\n    transfer: current_models\n  population: QCM"),
    "CO sans preuve d'intervention": reg_mut(
        "    intervention:\n    - benefit_shown\n    - mixed\n    transfer: current_models\n",
        "    intervention:\n    - untested\n    transfer: not_applicable\n"),
    'DC sans conditions': reg_mut("  conditions: modèles de 2024 et plus récents, tâches de raisonnement\n", ""),
    'CA avec nuisance démontrée': reg_mut(
        "    - benefit_shown\n    transfer: transfer_unknown\n  population: BBH",
        "    - harm_shown\n    transfer: transfer_unknown\n  population: BBH"),
    'untested combiné': reg_mut("    - untested\n    transfer: not_applicable\n",
                                "    - untested\n    - mixed\n    transfer: not_applicable\n"),
    'non testé mais transfert affirmé': reg_mut("    - untested\n    transfer: not_applicable\n",
                                                "    - untested\n    transfer: current_models\n"),
    'déclencheur inconnu': reg_mut("  - reasoning_model\n  next:", "  - toujours\n  next:"),
    'all combiné': reg_mut("  - all\n  next:", "  - all\n  - multi_turn\n  next:"),
    'champ inconnu': reg_mut("  family: A Allocation du raisonnement\n",
                             "  family: A Allocation du raisonnement\n  score: 9\n"),
    'texte vide': reg_mut("  next: revalider à chaque génération de modèles\n", "  next: ''\n"),
    "liste à la place d'un texte": reg_mut("  models: modèles de raisonnement 2025\n", "  models: [a, b]\n"),
    'axe de preuve manquant': reg_mut("    mechanism: not_applicable\n    intervention:\n    - documented\n    transfer: current_models\n  population: QCM",
                                      "    intervention:\n    - documented\n    transfer: current_models\n  population: QCM"),
    'règle liée inexistante': reg_mut("  rule: R-STR-009\n", "  rule: R-STR-999\n"),
    'vocabulaire meta réduit': reg_mut("  - harm_plausible\n", ""),
    'identifiant dupliqué': reg_mut("- id: K02\n", "- id: K01\n"),
    'racine supplémentaire': reg_text + "\nextra: 1\n",
}
for name, mtext in REG_MUTATIONS.items():
    try:
        _d2, e2 = validate_registry_text(mtext, rules_by_id)
        check(bool(e2), f"registre : mutation acceptée « {name} »")
    except Exception as ex:   # le validateur ne doit jamais lever
        check(False, f"registre : exception sur « {name} » : {type(ex).__name__}")
# Base « reasoned » liée à une règle qui se présente comme seulement empirique : doit échouer
rb2 = {k: dict(v) for k, v in rules_by_id.items()}
if 'R-STR-009' in rb2:
    rb2['R-STR-009']['evidence'] = ['EMP']
    check(bool(validate_registry_text(reg_text, rb2)[1]),
          "registre : base « reasoned » acceptée pour une règle seulement EMP")

if reg and not reg_errs:
    n = len(reg['entries'])
    r04 = open(os.path.join(ROOT, 'research', 'R04_EXPLOITATION_ET_SELECTION.md'), encoding='utf-8').read()
    check(f"**{n} entrées**" in r04, "R04 : nombre d'entrées du registre divergent")
    idx = read('00_INDEX.md')
    check(f"{n} entrées classées" in idx, "00_INDEX : nombre d'entrées du registre divergent")
    nact = sum(1 for r in data['rules'] if r['status'] == 'active')
    check(f"{len(data['rules'])} règles atomiques ({nact} actives" in idx, "00_INDEX : nombre de règles divergent")
    # Table de consultation de 10 : identique à celle que produit le registre
    t10 = read('10_PROMPT_GENERATION_PROTOCOL.md')
    m = re.search(r'<!-- registre:début -->\n(.*?)\n<!-- registre:fin -->', t10, re.S)
    check(m is not None, "10 : table de consultation du registre absente")
    if m:
        got = {}
        for line in m.group(1).splitlines()[2:]:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            got[cells[0].strip('`')] = [set() if c == '—' else set(c.split(', ')) for c in cells[2:]]
        check(set(got) == set(REG_VOCAB['triggers']), "10 : déclencheurs de la table ≠ vocabulaire du registre")
        for trig in REG_VOCAB['triggers']:
            exp = [{e['id'] for e in reg['entries'] if trig in e['triggers'] and e['tier'] == tier}
                   for tier in REG_VOCAB['tiers']]
            check(got.get(trig) == exp, f"10 : ligne « {trig} » désynchronisée du registre")

print(f"{passed} vérifications réussies, {len(failures)} échec(s).")
for x in failures: print(" -", x)
sys.exit(1 if failures else 0)
