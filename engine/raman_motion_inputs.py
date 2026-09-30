"""Named Raman mean/Sighra assignments on explicit inputs, no ephemeris fill."""
import math
from .motional_strength import NON_LUMINARIES,cheshta_from_supplied_mean_true
from .raman_motion_source_audit import SOURCE_URL


def raman_motion_inputs(mean_sun_unwrapped,superior_means,true_longitudes,inferior_sighra,*,input_profile,coordinate_branch):
    if not isinstance(input_profile,str) or not input_profile.strip() or not isinstance(coordinate_branch,str) or not coordinate_branch.strip():raise ValueError('Named input and coordinate branch required')
    if set(superior_means)-{'Mars','Jupiter','Saturn'} or set(true_longitudes)-set(NON_LUMINARIES) or set(inferior_sighra)-{'Mercury','Venus'}:raise ValueError('Unsupported or misplaced planet input')
    for value in [mean_sun_unwrapped,*superior_means.values(),*true_longitudes.values(),*inferior_sighra.values()]:
        if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value)):raise ValueError('Finite supplied angle or unknown required')
    for value in inferior_sighra.values():
        if value is not None and not 0<=value<360:raise ValueError('Inferior Sighra must be in0..360')
    rows=[]
    for p in NON_LUMINARIES:
        inferior=p in ('Mercury','Venus')
        mean=mean_sun_unwrapped if inferior else superior_means.get(p)
        true=true_longitudes.get(p)
        sighra=inferior_sighra.get(p) if inferior else None if mean_sun_unwrapped is None else mean_sun_unwrapped%360
        missing=[name for name,value in [('mean',mean),('true',true),('sighrochcha',sighra)] if value is None]
        rows.append({'planet':p,'assigned_mean_unwrapped':mean,'supplied_true_unwrapped':true,
            'assigned_sighrochcha_normalized':sighra,'missing_inputs':missing,
            'motion_evidence':None if missing else cheshta_from_supplied_mean_true(p,mean,true,sighra,input_profile=input_profile,coordinate_branch=coordinate_branch),
            'mean_assignment':'supplied mean Sun' if inferior else 'supplied superior planet mean',
            'sighra_assignment':'supplied inferior Sighra' if inferior else 'supplied mean Sun modulo360 (normalization only)'})
    return {'rows':rows,'input_profile':input_profile,'coordinate_branch':coordinate_branch,
        'assignment_source':{'url':SOURCE_URL,'pdf_pages':[80,121,122],'printed_pages':[75,116,117],'verified_against_page_image':True},
        'ephemeris_inputs_computed':False,'ketkar_equivalence_verified':False,'selected_natal_strength':None,
        'notice':'Raman assignment bridge plus separately cited Sripati algebra only. Caller grounds unwrapped mean/true branch; normalizing the Sighra output does not choose their circular average. No heliocentric-as-mean relabel, table typo repair, epoch/time/frame inference, missing-input fallback or selected full strength.'}
