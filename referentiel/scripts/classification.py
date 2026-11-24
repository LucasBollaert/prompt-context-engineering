"""Référence exécutable de la classification de 09 §1 (niveau, modules, voie rapide).

Ce module traduit la documentation. tests/classification_cases.yaml contient des attendus écrits
à la main, indépendamment de ce code. scripts/run_tests.py vérifie que le code, les cas de
référence, la table de 09 et la phrase de 14 restent concordants.

Axes, chacun de 0 à 2 (voir 09 §1) :
  A complexité · B risque d'action · C vérifiabilité · D horizon · E ambiguïté · F environnement.
Attributs supplémentaires :
  info_stakes : 0 = réponse sans enjeu particulier ; 1 = la réponse éclaire une décision humaine
                importante (santé, droit, finances, emploi, sécurité des personnes).
  permissions : 'established' | 'missing' | 'unknown' | 'na' (sans objet : aucune action).
Toute entrée hors domaine lève ValueError : un risque inconnu n'est jamais traité comme nul.
"""

PERMISSIONS = {'established', 'missing', 'unknown', 'na'}


def _check(**axes):
    for name, v in axes.items():
        if type(v) is not int or not 0 <= v <= 2:
            raise ValueError(f"axe {name} hors domaine : {v!r} (entier 0, 1 ou 2 attendu)")


def level(A, D):
    """Niveau T0-T3 : fonction de A et D uniquement."""
    _check(A=A, D=D)
    if D == 2:
        return 'T3'
    if A == 2 or (A == 1 and D == 1):
        return 'T2'
    if A == 1 or D == 1:
        return 'T1'
    return 'T0'


def _flag(name, v):
    if type(v) is not bool:
        raise ValueError(f"{name} doit être un booléen True/False, reçu {v!r}")


def modules(B, C, E, F, permissions='na', info_stakes=0):
    """Modules actifs ; ne dépendent jamais du niveau."""
    _check(B=B, C=C, E=E, F=F)
    if not isinstance(permissions, str) or permissions not in PERMISSIONS:
        raise ValueError(f"permissions hors domaine : {permissions!r}")
    if info_stakes not in (0, 1) or type(info_stakes) is not int:
        raise ValueError(f"info_stakes hors domaine : {info_stakes!r}")
    m = set()
    if B == 1: m.add('risk_scope')
    if B == 2: m.add('risk_strict')            # approbation technique + contrôles externes
    acts = B >= 1 or F == 2
    if permissions == 'missing' or (permissions == 'unknown' and acts):
        m.add('permissions')                   # établir avant toute action
    if C == 0: m.add('oracle')
    if C == 1: m.add('criteria_review')
    if C == 2: m.add('criteria_human')
    if E == 1: m.add('assumptions')
    if E == 2: m.add('clarify_or_announce')
    if F == 1: m.add('read_tools')
    if F == 2: m.add('write_tools')            # périmètre, autonomie, états terminaux
    if info_stakes == 1: m.add('epistemic')    # incertitude, sources, limites, validation compétente
    return m


BLOCKING = {'risk_scope', 'risk_strict', 'permissions', 'clarify_or_announce', 'write_tools'}


def delivery(A, B, C, D, E, F, well_formed=False, permissions='na', info_stakes=0,
             missing_useful_lines=False):
    """Branche de livraison pour une demande de génération :
    'fast_path'      demande inchangée (au plus une ligne de format) ;
    'minimal_prompt' demande conservée + les quelques lignes utiles des modules non bloquants
                     qui manquent (critère d'arrêt, hypothèse, vérification, prudence) ;
    'prompt'         construction complète proportionnée au niveau et aux modules.
    Un module bloquant exclut toujours la voie rapide et le prompt minimal."""
    _flag('well_formed', well_formed)
    _flag('missing_useful_lines', missing_useful_lines)
    lvl = level(A, D)
    m = modules(B, C, E, F, permissions, info_stakes)
    if m & BLOCKING:
        return 'prompt'
    if not (well_formed or lvl == 'T0'):
        return 'prompt'
    return 'minimal_prompt' if missing_useful_lines else 'fast_path'


def fast_path(A, B, C, D, E, F, well_formed=False, permissions='na', info_stakes=0,
              missing_useful_lines=False):
    return delivery(A, B, C, D, E, F, well_formed, permissions, info_stakes,
                    missing_useful_lines) == 'fast_path'
