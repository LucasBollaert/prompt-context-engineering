"""Valide research/knowledge_registry.yaml (registre des connaissances, R04 §2).

Réutilise le chargeur strict de build_rules (clés dupliquées refusées, pas de conversion
de dates). Les vocabulaires de référence sont définis ICI ; ceux du fichier doivent leur
être identiques, ce qui empêche d'« officialiser » une valeur en modifiant le fichier seul.

Usage : python3 scripts/registry.py  →  code retour 0 si valide.
Bibliothèque : validate_registry_text(text, active_rules) → (données ou None, erreurs).
"""
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_rules import StrictLoader  # noqa: E402

VOCAB = {
    'tiers': ['OP', 'CO', 'CA', 'DC', 'QO'],
    'basis': ['measured', 'documented', 'reasoned'],
    'phenomenon': ['shown', 'mixed', 'not_shown', 'untested', 'not_applicable'],
    'mechanism': ['shown', 'proposed', 'contested', 'untested', 'not_applicable'],
    'intervention': ['benefit_shown', 'null_average', 'no_benefit_shown', 'harm_shown',
                     'harm_plausible', 'mixed', 'documented', 'untested'],
    'transfer': ['current_models', 'transfer_unknown', 'transfer_failed', 'not_applicable'],
    'triggers': ['all', 'reasoning_model', 'non_reasoning_model', 'light_local_model', 'long_context',
                 'multimodal', 'creative_diversity', 'multi_turn', 'agentic_code', 'repeated_pipeline',
                 'many_constraints', 'time_sensitive', 'judgment_eval', 'factual_longform',
                 'motivation_framing', 'evaluation_design', 'cost_compression', 'personalization',
                 'structured_output'],
}
META_KEYS = {'version', 'date'} | set(VOCAB)
REQUIRED = {'id', 'family', 'technique', 'tier', 'evidence', 'population', 'models', 'sources',
            'triggers', 'next'}
OPTIONAL = {'rule', 'basis', 'conditions'}
TEXT_FIELDS = ['family', 'technique', 'population', 'models', 'sources', 'next']
EVIDENCE_KEYS = {'phenomenon', 'mechanism', 'intervention', 'transfer'}
NEGATIVE = {'harm_shown', 'harm_plausible', 'no_benefit_shown', 'null_average', 'mixed'}


def _str(x):
    return isinstance(x, str) and x.strip() != ''


def _str_list(x):
    return isinstance(x, list) and len(x) > 0 and all(_str(v) for v in x) and len(set(x)) == len(x)


def validate_registry_text(text, rules):
    """rules : dict id → règle (rules.yaml chargé). Retourne (données, erreurs)."""
    errors = []
    err = errors.append
    try:
        data = yaml.load(text, Loader=StrictLoader)
    except yaml.YAMLError as e:
        return None, [f"YAML invalide : {e}"]
    if not isinstance(data, dict) or set(data) != {'meta', 'entries'}:
        return None, ["racine : exactement « meta » et « entries » attendus"]
    meta, entries = data['meta'], data['entries']
    if not isinstance(meta, dict) or set(meta) != META_KEYS:
        err(f"meta : clés attendues {sorted(META_KEYS)}")
    else:
        for k, v in VOCAB.items():
            if meta.get(k) != v:
                err(f"meta.{k} diffère du vocabulaire de référence du validateur")
        if not (_str(meta.get('version')) and re.fullmatch(r'\d+\.\d+', meta['version'])):
            err("meta.version invalide")
    if not isinstance(entries, list) or not entries:
        return None, errors + ["entries : liste non vide attendue"]
    active = {i for i, r in rules.items() if r.get('status') == 'active'}
    seen = set()
    for n, e in enumerate(entries):
        if not isinstance(e, dict):
            err(f"entrée {n} : objet attendu")
            continue
        eid = e.get('id') if _str(e.get('id')) else f"#{n}"
        w = f"registre {eid}"
        if not (_str(e.get('id')) and re.fullmatch(r'K\d{2}', e['id'])):
            err(f"{w} : identifiant invalide")
        if eid in seen:
            err(f"{w} : identifiant dupliqué")
        seen.add(eid)
        keys = set(e)
        if not REQUIRED <= keys:
            err(f"{w} : champs manquants {sorted(REQUIRED - keys)}")
        if not keys <= REQUIRED | OPTIONAL:
            err(f"{w} : champs inconnus {sorted(keys - REQUIRED - OPTIONAL)}")
        for f in TEXT_FIELDS:
            if f in e and not _str(e[f]):
                err(f"{w} : « {f} » doit être un texte non vide")
        tier = e.get('tier')
        if tier not in VOCAB['tiers']:
            err(f"{w} : niveau invalide {tier!r}")
        trig = e.get('triggers')
        if not (_str_list(trig) and all(t in VOCAB['triggers'] for t in trig)):
            err(f"{w} : déclencheurs invalides {trig!r}")
        elif 'all' in trig and len(trig) > 1:
            err(f"{w} : « all » ne se combine pas")
        if 'conditions' in e and not _str(e['conditions']):
            err(f"{w} : « conditions » doit être un texte non vide")
        ev = e.get('evidence')
        if not (isinstance(ev, dict) and set(ev) == EVIDENCE_KEYS):
            err(f"{w} : evidence doit contenir exactement {sorted(EVIDENCE_KEYS)}")
            continue
        for ax in ('phenomenon', 'mechanism', 'transfer'):
            if ev[ax] not in VOCAB[ax]:
                err(f"{w} : evidence.{ax} hors vocabulaire {ev[ax]!r}")
        iv = ev['intervention']
        if not (_str_list(iv) and all(x in VOCAB['intervention'] for x in iv)):
            err(f"{w} : evidence.intervention hors vocabulaire {iv!r}")
            continue
        # Cohérence des axes
        if 'untested' in iv and len(iv) > 1:
            err(f"{w} : « untested » ne se combine pas avec une autre valeur")
        if (iv == ['untested']) != (ev['transfer'] == 'not_applicable'):
            err(f"{w} : transfert « not_applicable » si et seulement si l'intervention n'est pas testée")
        # Règle liée
        rule = e.get('rule')
        if rule is not None and rule not in active:
            err(f"{w} : règle inconnue ou inactive {rule!r}")
        # Base (OP seulement)
        basis = e.get('basis')
        if tier != 'OP' and 'basis' in e:
            err(f"{w} : « basis » réservé aux entrées OP")
        if tier == 'OP':
            if rule not in active:
                err(f"{w} : entrée OP sans règle active")
            if basis not in VOCAB['basis']:
                err(f"{w} : entrée OP sans base valide (measured, documented, reasoned)")
            if set(iv) & {'harm_shown', 'null_average', 'no_benefit_shown'} or ev['transfer'] == 'transfer_failed':
                err(f"{w} : une entrée OP ne peut reposer sur une absence d'effet, une nuisance ou un échec de transfert")
            if basis == 'measured' and not ('benefit_shown' in iv and ev['transfer'] == 'current_models'):
                err(f"{w} : base « measured » exige un bénéfice mesuré sur des modèles actuels")
            if basis == 'documented' and 'documented' not in iv:
                err(f"{w} : base « documented » exige une intervention documentée")
            if basis == 'reasoned' and rule in rules:
                evid = rules[rule].get('evidence') or []
                if not ({'HYP', 'OFF'} & set(evid)):
                    err(f"{w} : base « reasoned » mais la règle {rule} se présente comme seulement empirique {evid!r}")
        if tier == 'CO' and not ({'benefit_shown', 'documented', 'mixed'} & set(iv)):
            err(f"{w} : une entrée CO exige une preuve d'intervention, même conditionnelle")
        if tier == 'DC':
            if not _str(e.get('conditions')):
                err(f"{w} : entrée DC sans conditions")
            if not (NEGATIVE & set(iv) or ev['transfer'] == 'transfer_failed'):
                err(f"{w} : entrée DC sans preuve négative, nulle, mitigée ou d'échec de transfert")
        if tier == 'CA' and 'harm_shown' in iv:
            err(f"{w} : nuisance démontrée : relève de DC, pas de CA")
    return data, errors


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rules = {r['id']: r for r in yaml.load(open(os.path.join(root, 'rules.yaml'), encoding='utf-8'),
                                            Loader=StrictLoader)['rules']}
    text = open(os.path.join(root, 'research', 'knowledge_registry.yaml'), encoding='utf-8').read()
    data, errors = validate_registry_text(text, rules)
    for x in errors:
        print(" -", x)
    if data and not errors:
        print(f"OK : {len(data['entries'])} entrées valides.")
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
