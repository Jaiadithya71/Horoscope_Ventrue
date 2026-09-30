"""BPHS XXVII.18 identity on separately supplied, provenance-labeled input."""
import math

SOURCE={'url':'https://ia903205.us.archive.org/30/items/brihatparasarahorashastrabyr.santhanam/Brihat%20Par%C4%81%C5%9Bara%20Hor%C4%81%20%C5%9Ah%C4%81stra%20By%20R.%20Santhanam.pdf',
    'chapter':'27','sloka':18,'pdf_page':235,'printed_page':225,'verified_against_page_image':True,
    'edition_notice':'Retrieved digital Santhanam-attributed VolumeI text; visual verification does not certify original print or critical-edition fidelity'}


def supplied_luminary_motion_identity(planet,component_rupa,*,component_profile):
    if planet not in ('Sun','Moon'):raise ValueError('Luminary required')
    if isinstance(component_rupa,bool) or not isinstance(component_rupa,(float,int)) or not math.isfinite(component_rupa) or component_rupa<0:raise ValueError('Finite nonnegative component required')
    if not isinstance(component_profile,str) or not component_profile.strip():raise ValueError('Named input component profile required')
    return {'planet':planet,'input_component':'ayana' if planet=='Sun' else 'paksha',
        'supplied_component_rupa':component_rupa,'component_profile':component_profile,
        'motion_rupa':component_rupa,'identity_profile':'BPHS27.18_Santhanam_digital',
        'source':dict(SOURCE),'selected_sripati_motion':None,'total_strength':None,
        'notice':'Identity only: no extra multiplication or cap. Caller must separately ground upstream Ayana/Paksha and multiplier profile. Named BPHS evidence corroborates Sripati printed equalities, not selection of Sripati multipliers, epoch, declination or inclusive motion layout. No reconstructed complete total or personal effect.'}


def supplied_bphs_doubled_component_chain(planet,undoubled_component_rupa,*,base_component_profile):
    """Explicit commentary multiplier then XVIII identity, not base calculation."""
    x=supplied_luminary_motion_identity(planet,undoubled_component_rupa,component_profile=base_component_profile)
    if undoubled_component_rupa>1:raise ValueError('Undoubled normalized base must be in zero..one')
    value=2*undoubled_component_rupa
    return {'planet':planet,'supplied_undoubled_component_rupa':undoubled_component_rupa,
        'base_component_profile':base_component_profile,'commentary_multiplier':2,
        'doubled_upstream_component_rupa':value,
        'motion_identity':supplied_luminary_motion_identity(planet,value,component_profile='BPHS Santhanam commentary double of supplied base: '+base_component_profile),
        'multiplier_source':dict(SOURCE,pdf_page=228 if planet=='Sun' else 222,printed_page=218 if planet=='Sun' else 212,sloka='15-17 commentary' if planet=='Sun' else '10-11 commentary'),
        'engine_computed_base_component':None,'selected_sripati_motion':None,'total_strength':None,
        'notice':'One explicit upstream doubling followed by identity, not doubling motion again. BPHS commentary uses a23deg27min declination shortcut and conditional Moon/Mercury Paksha classifications unlike the implemented Sripati24deg/fixed-benefic candidates. Supplied base provenance is not certified BPHS computation. No cross-book complete total or automatic layout sum.'}
