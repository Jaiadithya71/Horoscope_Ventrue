"""Worked own-Shadvarga statement constrains guesses, not a new definition."""
from .sripati_worked_navamsa_audit import WORKED_DMS
from .vargas import six_vargas
from .continuous_strength import drekkanabala


def own_shadvarga_refinement_audit():
    rows=[]
    for p,(sign,degree,minute,second) in WORKED_DMS.items():
        longitude=sign*30+degree+minute/60+second/3600
        vargas=six_vargas(longitude)['vargas']
        own=[r['varga'] for r in vargas if r['owner']==p]
        base=drekkanabala(p,longitude)
        rows.append({'planet':p,'six_varga_owner_flags':{r['varga']:r['owner']==p for r in vargas},
            'own_varga_names':own,'any_own_varga':bool(own),'all_six_owned':len(own)==6,
            'base_decan_rupa':base['rupa'],
            'quoted_refinement_rupa':.5 if p=='Jupiter' else None,
            'selected_refined_component':None})
    j=next(r for r in rows if r['planet']=='Jupiter')
    return {'rows':rows,'source':{'url':'https://archive.org/details/dli.ernet.203510',
        'pdf_page':52,'printed_page':38,'chapter':'III','sloka':'5 commentary','verified_against_page_image':True},
        'earlier_edition_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
            'pdf_pages':[97,98],'printed_pages':[81,82],'verified_against_page_image':True},
        'quoted_component_replacement':{'base_virupa':15,'refined_virupa':30,
            'earlier_edition_leading_digit_clear':True,'added_full_rupa':False,
            'explicit_any_or_all_quantifier_verified':False,
            'sanskrit_scope_notice':'Quoted svavarga compound observed, not an independently settled any-one/all-six interpretation.'},
        'all_six_required_guess_fits_explicit_jupiter_example':j['all_six_owned'],
        'any_own_quantifier_verified':False,'selected_refinement_definition':None,
        'selected_positional_total':None,
        'notice':'Commentary explicitly changes Jupiter .25 to .5 under quoted own-Shadvarga adjustment. Checked worked Jupiter owns Rasi/Drekkana/Dwadasamsa, not all six: an all-six definition contradicts this example. This does not establish any-one, own-Rasi, own-Drekkana or another quantifier. Other rows have no individually quoted refined values; absence is not zero. Base sex-class/decan condition and cited cross-source geometry stay separate. No fitted adjustment or full total.'}
