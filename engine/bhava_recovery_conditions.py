"""XV.1 translation discrepancy and XV.5 scoped recovery, not outcomes."""
from .debilitation_cancellation_candidates import _and,_or


def _validate(*values):
 if any(x is not None and type(x) is not bool for x in values):
  raise ValueError('Grounded bool or None required')


def _not(value):return None if value is None else not value


def xv1_dignity_qualification(depressed=None,eclipsed=None,inimical_sign=None):
 """Other XV.1 conditions are outside this isolated final qualification."""
 _validate(depressed,eclipsed,inimical_sign)
 safe=_and(_and(_not(depressed),_not(eclipsed)),_not(inimical_sign))
 literal=_and(_and(depressed,eclipsed),inimical_sign)
 return {'qualification_candidates':[
  {'source':'original1937 PDF189 printed152 XV.1','reading':'not depressed, not eclipsed, not inimical','condition':safe},
  {'source':'Kapoor PDF145 XV.1','reading':'literal reproduction omits negation: depressed, combust and inimical','condition':literal}],
  'source_negation_discrepancy':True,'selected_profile':None,'personal_outcome':None,
  'notice':'Final dignity clause only. Literal later reproduction is retained as an error/discrepancy candidate, not a verified alternative classical school or global adverse-dignity override. Other ownership/occupation/aspect and malefic-free requirements are not certified.'}


def xv5_recovery_condition(lord_in_dusthana=None,occupied_by_dusthana_lord=None,
                          benefic_aspect=None):
 _validate(lord_in_dusthana,occupied_by_dusthana_lord,benefic_aspect)
 adverse=_or(lord_in_dusthana,occupied_by_dusthana_lord)
 recovery=_and(adverse,benefic_aspect)
 adverse_without_recovery=_and(adverse,_not(benefic_aspect))
 return {'adverse_base_condition':adverse,'benefic_aspect_exception':recovery,
  'adverse_condition_without_checked_exception':adverse_without_recovery,
  'selected_personal_effect':None,'global_precedence':None,
  'source':{'slug':'phaladeepika-1937','chapter':'XV','sloka':5,'pdf_page':191,
     'printed_page':154,'verified_against_page_image':True},
  'comparison_source':{'title':'Kapoor Phaladeepika','pdf_page':147,'verified_against_page_image':True},
  'notice':'Scoped XV.5 exception only. No universal recovery over XV.3/6 or other rules, no strength or timing decision. Lord/dusthana frame and aspect convention must be grounded externally. Missing aspect is unknown, not no recovery; no adverse base does not itself imply favorable result.'}
