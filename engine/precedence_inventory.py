"""Source-scoped precedence coverage, not a global rank or readiness percentage."""


def precedence_inventory():
    rows=[
        ('relationship_evidence','friendship','IV.10',[74],'natural preferred to temporal relationship','does not arbitrate house/yoga/period outcomes'),
        ('dignity_motion_rays','strength_precedence','IV.4/7',[72,73],'retrograde and overpowering rays qualify dignity','simultaneous conditions and full strength remain unresolved'),
        ('lord_protection','bhava_recovery_conditions','XV.3',[190],'absence of benefic lord influence qualifies adverse lord condition','house aspect is not lord aspect'),
        ('house_recovery','bhava_recovery_conditions','XV.5',[191],'benefic house aspect qualifies this verse adverse base','does not overrule XV.3/6 or unrelated clauses'),
        ('dusthana_severity','dusthana_strength_qualification','XV.9',[193],'strong reduces severity; not favorable','requires supplied strength status and house frame'),
        ('lagna_ownership','lordship_precedence','XV.10-11',[193,194],'Lagna/dusthana exception retained beside Moolatrikona emphasis','half-dasha translation and global effect weights unresolved'),
        ('sandhi_period_effect','period_sandhi_gate','XV.13-14',[194],'exact Sandhi qualifies favorable dignity and sixfold strength','degree geometry required; zero effect not harm'),
        ('dusthana_growth','house_growth_scope','XV.18-19',[196],'house growth distinguished from benefit to person','shared dusthana direction consistent, not a school conflict'),
        ('three_strength_alternative','bhava_condition_gate','XV.25-26',[198],'all-three condition retained beside explicit others-say placement','no school winner from supplied strength'),
        ('lagna_strength_connective','lagna_house_strength_connective','XV.27',[199],'OR and AND English connective candidates retained','adverse weakness quantifier and Sanskrit resolution unselected'),
        ('own_other_house','dual_owner_occupation_exception','XV.29',[199,200],'other-own-house occupation excludes dusthana ownership in this clause','does not cancel all adverse chart conditions'),
        ('lord_period_disposition','period_disposition_gate','XX.14',[241],'favorable and adverse alternatives can both apply','friendship/rays/geometry and later favorable connective remain unselected'),
        ('vargottama_qualification','vargottama_period_qualification','XX.22',[245],'fall/rays qualify favorable Vargottama reading to mixed','no universal override'),
        ('period_manifestation','period_manifestation_gate','XX.43-44',[252],'no automatic own-subperiod owned-house output; relationship candidates kept','relation profile and similarly-circumstanced classification unselected'),
        ('angular_trinal_related_pair','angular_trinal_pair_conditions','XX.45-46',[252],'extra adverse ownership does not disqualify this related pair condition','fifth/ninth candidate scope; relation profile and independent strong-Kendra flag unresolved'),
        ('angular_trinal_period_wording','angular_trinal_period_readings','XX.49',[253],'unrelated no-harm and positive-good English readings retained separately','Trikona enumeration, relation hypothesis and translation selection unresolved'),
        ('period_school_conflict','period_school_conflict','XXI.41',[269],'Jupiter main/Mercury subperiod opposite schools retained','no school selected by strength or timing')]
    return {'scope_records':[{'id':i,'implementation':m,'checked_scope':s,'remaining_boundary':b,
        'source':{'url':'https://archive.org/details/in.ernet.dli.2015.92117','chapter_sloka':v,'pdf_pages':p},
        'input_dependent_applicability':None} for i,m,v,p,s,b in rows],
        'unresolved_global_arbitration':[
            'No book-verified global priority across distinct house/yoga/period/transit rules',
            'Translation discrepancies are not automatically authentic competing Sanskrit schools',
            'A coherent complete natal strength and calendar profile are still unselected',
            'No independent personalized outcome benchmark establishes prediction accuracy'],
        'global_rank':None,'selected_school':None,'personal_outcome':None,
        'notice':'Inventory of implemented scoped evidence, not executed natal applicability, proof all classical rules are covered, completion percentage or predictor readiness. A local exception can qualify its own condition without supplying a global reconciliation policy.'}
