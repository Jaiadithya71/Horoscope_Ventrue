"""One verified competing-school period rule, no invented general arbiter."""
from .natal import PERIODS


def period_school_conflict(main_lord,sub_lord):
 known=dict(PERIODS)
 if main_lord not in known or sub_lord not in known:raise ValueError('Known main and subperiod lords required')
 applies=main_lord=='Jupiter' and sub_lord=='Mercury'
 source={'slug':'phaladeepika-1937','chapter':'XXI','sloka':41,'pdf_page':269,'printed_page':232,
         'url':'https://archive.org/details/in.ernet.dli.2015.92117','verified_against_page_image':True}
 return {'main_lord':main_lord,'sub_lord':sub_lord,'scope_match':applies,
   'competing_school_evidence':[
      {'school':'some_opinion_in_original_verse','polarity':'adverse','paraphrase':'Adverse personal conduct and distress themes are stated by one school.'},
      {'school':'others_opinion_in_original_verse','polarity':'beneficial','paraphrase':'Religious activity, family, wealth and happiness themes are stated by the other school.'}
    ] if applies else [],
   'source':source,'cross_checked_translation':{'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':203,'chapter':'XXI','sloka':41,'verified_against_page_image':True},
   'unresolved_school_conflict':applies,'selected_school':None,'personal_outcome':None,
   'notice':'Exact lord-pair scope only. A nonmatching pair means this checked conflict does not apply, not agreement or a favorable/adverse result. Neither supplied strength nor timing selects a school in this verse; no general rank, health prediction, probabilities or automatic conclusion.'}
