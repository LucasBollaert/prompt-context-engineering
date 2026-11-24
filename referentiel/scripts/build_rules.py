#!/usr/bin/env python3
"""Valide rules.yaml (source canonique) et génère rules.json.

Usage : python3 scripts/build_rules.py      (depuis n'importe quel répertoire)
Code retour 1 si une vérification échoue ; rules.json n'est alors pas écrit.

Vérifications :
  1. Syntaxe YAML, clés dupliquées (refusées), scalaires conservés en chaînes (pas de
     conversion implicite en booléen ou en date).
  2. Schéma : champs obligatoires et autorisés, types, énumérations, dates YYYY-MM[-DD].
  3. Références : IDs uniques, conflits (structure, cible, pas d'auto-conflit),
     superseded_by, sources présentes dans 13, fichiers existants.
  4. Équivalence : rules.json relu == données validées.
Le module expose validate_text() pour les tests (scripts/run_tests.py).
"""
import datetime, json, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_RE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?$')
RULE_REQ = {
    'id': str, 'title': str, 'description': str, 'rationale': str, 'scope': str,
    'conditions': list, 'exceptions': list, 'priority': str, 'evidence': list, 'models': list,
    'sources': list, 'conflicts': list, 'files': list, 'status': str, 'transfer': str,
    'volatility': str, 'last_verified': str}
RULE_OPT = {'notes': list, 'superseded_by': list}
META_REQ = {'version': str, 'date': str, 'canonical': bool, 'derived_artifacts': list,
            'evidence_levels': dict, 'transfer_levels': dict, 'volatility_levels': dict,
            'status_values': list, 'model_tags': list, 'selection_semantics': dict}
PRIORITIES = {'high', 'medium', 'low'}
# Énumérations fermées : les étendre exige de modifier ce script (décision v1.3).
STATUS_VALUES = {'active', 'deprecated'}
# Vocabulaire méthodologique (00 §3) : fermé. Ajouter un niveau de preuve est une décision de
# méthode, pas une donnée : elle passe par ce script et par 00 §3. model_tags reste extensible
# (un nouveau modèle est une opération de maintenance courante).
CLOSED_VOCAB = {'evidence_levels': {'DOC', 'OFF', 'EMP', 'HYP'},
                'transfer_levels': {'general', 'provider_specific', 'contested'},
                'volatility_levels': {'low', 'medium', 'high'}}
SEMANTICS_KEYS = {'intended_use', 'conditions', 'exceptions', 'models', 'conflicts', 'priority', 'files', 'enumerations'}
VERSION_RE = re.compile(r'^\d+\.\d+$')
ID_RE = re.compile(r'^R-[A-Z]+-\d{3}$')


class StrictLoader(yaml.SafeLoader):
    """SafeLoader qui refuse les clés dupliquées et ne convertit pas les dates."""


StrictLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != 'tag:yaml.org,2002:timestamp']
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def _mapping(loader, node, deep=False):
    keys = set()
    for knode, _ in node.value:
        key = loader.construct_object(knode, deep=deep)
        if key in keys:
            raise yaml.constructor.ConstructorError(
                None, None, f"clé dupliquée « {key} »", knode.start_mark)
        keys.add(key)
    return loader.construct_mapping(node, deep=deep)


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def valid_date(s):
    """YYYY-MM ou YYYY-MM-DD, date calendaire réelle."""
    if not isinstance(s, str) or not DATE_RE.match(s):
        return False
    try:
        datetime.date.fromisoformat(s if len(s) == 10 else s + '-01')
        return True
    except ValueError:
        return False


def hashable_str(x):
    return isinstance(x, str)


def validate_text(text, root=ROOT):
    """Retourne (données, erreurs). Ne lève jamais d'exception."""
    try:
        return _validate(text, root)
    except Exception as e:  # filet de sécurité : toute anomalie non prévue devient une erreur
        return None, [f"erreur de validation inattendue : {type(e).__name__}: {e}"]


def _validate(text, root):
    errors = []
    err = errors.append
    try:
        data = yaml.load(text, Loader=StrictLoader)
        raw = yaml.load(text, Loader=yaml.BaseLoader)
    except yaml.YAMLError as e:
        return None, [f"YAML invalide : {e}"]
    if not isinstance(data, dict) or set(data) != {'meta', 'rules'}:
        return data, ["racine : exactement les clés meta et rules attendues"]
    meta, rules = data['meta'], data['rules']
    if not isinstance(meta, dict) or not isinstance(rules, list):
        return data, ["meta doit être un objet et rules une liste"]

    # --- meta
    for k, t in META_REQ.items():
        if not isinstance(meta.get(k), t):
            err(f"meta.{k} : absent ou de type {type(meta.get(k)).__name__}, attendu {t.__name__}")
    for k in set(meta) - set(META_REQ):
        err(f"meta : champ inconnu {k!r}")
    if not valid_date(meta.get('date')):
        err(f"meta.date invalide : {meta.get('date')!r}")
    if meta.get('canonical') is not True:
        err("meta.canonical doit valoir true : rules.yaml est la source canonique")
    if isinstance(meta.get('status_values'), list) and set(map(str, meta['status_values'])) != STATUS_VALUES:
        err(f"meta.status_values doit être exactement {sorted(STATUS_VALUES)} (énumération fermée)")
    if isinstance(meta.get('version'), str) and not VERSION_RE.match(meta['version']):
        err(f"meta.version invalide : {meta['version']!r} (attendu MAJEUR.MINEUR)")
    ss = meta.get('selection_semantics')
    if isinstance(ss, dict):
        if set(ss) != SEMANTICS_KEYS:
            err(f"meta.selection_semantics : clés attendues {sorted(SEMANTICS_KEYS)}, reçues {sorted(map(str, ss))}")
        for k, v in ss.items():
            if not isinstance(v, str) or not v.strip(): err(f"meta.selection_semantics.{k} vide ou non textuel")
    enums = {}
    for k in ['evidence_levels', 'transfer_levels', 'volatility_levels']:
        v = meta.get(k) if isinstance(meta.get(k), dict) else {}
        if not all(isinstance(x, str) for x in v):
            err(f"meta.{k} : clés non textuelles {list(v)!r}")
        elif set(v) != CLOSED_VOCAB[k]:
            err(f"meta.{k} : vocabulaire fermé {sorted(CLOSED_VOCAB[k])}, reçu {sorted(v)}")
        for x, desc in v.items():
            if not isinstance(desc, str) or not desc.strip(): err(f"meta.{k}.{x} : description vide")
        enums[k] = set(v)
    for k in ['status_values', 'model_tags']:
        v = meta.get(k) if isinstance(meta.get(k), list) else []
        if not all(isinstance(x, str) for x in v):
            err(f"meta.{k} : valeurs non textuelles")
        enums[k] = set(v)

    # --- références externes
    try:
        src_text = open(os.path.join(root, '13_SOURCES_AND_EVIDENCE.md'), encoding='utf-8').read()
    except OSError:
        src_text = ''
        err("13_SOURCES_AND_EVIDENCE.md introuvable")
    sources = set(re.findall(r'\| (S-[A-Z]+\d*) \|', src_text))
    md_prefixes = {f[:2] for f in os.listdir(root) if re.match(r'^\d\d_.*\.md$', f)}

    # --- règles
    ids = []
    for i, r in enumerate(rules):
        where = r.get('id', f'#{i}') if isinstance(r, dict) else f'#{i}'
        if not isinstance(r, dict):
            err(f"{where} : une règle doit être un objet"); continue
        for k, t in RULE_REQ.items():
            if k not in r: err(f"{where} : champ manquant {k}")
            elif not isinstance(r[k], t): err(f"{where} : {k} de type {type(r[k]).__name__}, attendu {t.__name__}")
        for k, t in RULE_OPT.items():
            if k in r and not isinstance(r[k], t): err(f"{where} : {k} de type {type(r[k]).__name__}, attendu {t.__name__}")
        for k in set(r) - set(RULE_REQ) - set(RULE_OPT):
            err(f"{where} : champ inconnu {k!r}")
        for k in ['id', 'title', 'description', 'rationale', 'scope']:
            if isinstance(r.get(k), str) and not r[k].strip(): err(f"{where} : {k} vide")
        for k in ['conditions', 'exceptions', 'evidence', 'models', 'sources', 'files', 'notes', 'superseded_by']:
            v = r.get(k)
            if isinstance(v, list) and not all(isinstance(x, str) and x.strip() for x in v):
                err(f"{where} : {k} doit contenir des chaînes non vides ({v!r})")
        rid = r.get('id')
        if rid is not None and not isinstance(rid, str):
            err(f"{where} : id doit être une chaîne")
        if isinstance(rid, str):
            if not ID_RE.match(rid): err(f"{where} : format d'ID invalide")
            ids.append(rid)
        if isinstance(r.get('last_verified'), str) and not valid_date(r['last_verified']):
            err(f"{where} : last_verified invalide {r['last_verified']!r} (date réelle YYYY-MM ou YYYY-MM-DD)")
        elif isinstance(r.get('last_verified'), str) and valid_date(meta.get('date')) and r['last_verified'] > meta['date']:
            err(f"{where} : last_verified postérieur à meta.date")
        if not hashable_str(r.get('priority')) or r.get('priority') not in PRIORITIES:
            err(f"{where} : priorité invalide {r.get('priority')!r}")
        for field, enum in [('status', 'status_values'), ('transfer', 'transfer_levels'), ('volatility', 'volatility_levels')]:
            if not hashable_str(r.get(field)) or r.get(field) not in enums[enum]: err(f"{where} : {field} invalide {r.get(field)!r}")
        for f, enum in [('evidence', 'evidence_levels'), ('models', 'model_tags')]:
            v = r.get(f) if isinstance(r.get(f), list) else []
            if not v: err(f"{where} : {f} vide")
            for x in v:
                if not hashable_str(x) or x not in enums[enum]: err(f"{where} : {f} inconnu {x!r}")
        for f in ['evidence', 'models', 'sources', 'files', 'superseded_by']:
            v = r.get(f)
            if isinstance(v, list) and all(hashable_str(x) for x in v) and len(set(v)) != len(v):
                err(f"{where} : doublon dans {f}")
        for s in r.get('sources', []) if isinstance(r.get('sources'), list) else []:
            if not hashable_str(s) or s not in sources: err(f"{where} : source absente de 13 : {s!r}")
        for f in r.get('files', []) if isinstance(r.get('files'), list) else []:
            if not hashable_str(f) or f not in md_prefixes: err(f"{where} : fichier inexistant {f!r}")
        if r.get('status') == 'deprecated' and not r.get('superseded_by'):
            err(f"{where} : règle dépréciée sans superseded_by")
        if r.get('status') == 'active' and 'superseded_by' in r:
            err(f"{where} : règle active avec superseded_by")
    idset = set(ids)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes: err(f"IDs dupliqués : {sorted(dupes)}")
    for r in rules:
        if not isinstance(r, dict): continue
        rid = r.get('id')
        targets = [c.get('with') for c in r.get('conflicts', []) if isinstance(c, dict)] if isinstance(r.get('conflicts'), list) else []
        if all(isinstance(x, str) for x in targets) and len(set(targets)) != len(targets):
            err(f"{rid} : plusieurs conflits déclarés vers la même règle")
        for c in r.get('conflicts', []) if isinstance(r.get('conflicts'), list) else []:
            if not isinstance(c, dict) or set(c) != {'with', 'resolution'}:
                err(f"{rid} : conflit mal formé {c!r} (attendu {{with, resolution}})"); continue
            if not hashable_str(c['with']) or c['with'] not in idset: err(f"{rid} : conflit vers ID inconnu {c['with']!r}")
            if c['with'] == rid: err(f"{rid} : conflit avec soi-même")
            if not isinstance(c['resolution'], str) or not c['resolution'].strip():
                err(f"{rid} : résolution de conflit vide")
        for s in r.get('superseded_by', []) if isinstance(r.get('superseded_by'), list) else []:
            if not hashable_str(s) or s not in idset: err(f"{rid} : superseded_by inconnu {s!r}")
            elif s == rid: err(f"{rid} : superseded_by vers elle-même")
    # chaînes de remplacement : sans cycle et aboutissant à une règle active
    by_id = {r.get('id'): r for r in rules if isinstance(r, dict) and isinstance(r.get('id'), str)}
    for rid, r in by_id.items():
        if r.get('status') != 'deprecated' or not isinstance(r.get('superseded_by'), list): continue
        stack, seen = [(rid, (rid,))], set()
        while stack:
            cur, path = stack.pop()
            for s in by_id.get(cur, {}).get('superseded_by', []) or []:
                if not isinstance(s, str) or s not in by_id: continue
                if s in path: err(f"{rid} : cycle de remplacement {' -> '.join(path + (s,))}"); continue
                if by_id[s].get('status') == 'deprecated' and s not in seen:
                    seen.add(s); stack.append((s, path + (s,)))

    # --- aucune conversion implicite : comparaison avec le chargeur « tout chaîne »
    if not errors:
        for r, rr in zip(rules, raw['rules']):
            for f in ['evidence', 'models', 'sources', 'files', 'conditions', 'exceptions', 'last_verified', 'priority']:
                if r.get(f) != rr.get(f): err(f"{r['id']} : {f} interprété différemment selon le parseur")
    return data, errors


def main():
    text = open(os.path.join(ROOT, 'rules.yaml'), encoding='utf-8').read()
    data, errors = validate_text(text)
    if errors:
        print("ÉCHEC :")
        for e in errors: print(" -", e)
        return 1
    out = os.path.join(ROOT, 'rules.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    if json.load(open(out, encoding='utf-8')) != data:
        print("ÉCHEC : rules.json relu diffère des données validées"); return 1
    rules = data['rules']
    print(f"OK : {len(rules)} règles ({sum(r['status'] == 'active' for r in rules)} actives), "
          f"{sum('OFF' in r['evidence'] for r in rules)} avec preuve OFF ; rules.json écrit et relu à l'identique.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
