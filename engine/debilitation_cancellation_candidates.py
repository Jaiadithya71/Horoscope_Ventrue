"""VII.26 scoped conditional candidates, not strength or outcome arbitration."""


def _or(a,b):
 return True if a is True or b is True else False if a is False and b is False else None


def _and(a,b):
 return False if a is False or b is False else True if a is True and b is True else None


def cancellation_candidates(debilitated=None,depression_lord_kendra=None,
                            exaltation_sign_lord_kendra=None,
                            planet_exalted_in_depression_sign_kendra=None):
 """Inputs must be explicitly source-grounded; unknown is never false.

 Each Kendra flag means from either Lagna or Moon. Sign mapping, aspects,
 alternative VII.27-30 recipes, complete strength and outcome remain outside
 this isolated VII.26 helper. No candidate is selected.
 """
 flags=(debilitated,depression_lord_kendra,exaltation_sign_lord_kendra,
        planet_exalted_in_depression_sign_kendra)
 if any(x is not None and not isinstance(x,bool) for x in flags):
  raise ValueError('Grounded bool or None required')
 candidates=[]
 for meaning,value in [('own_exaltation_sign_lord',exaltation_sign_lord_kendra),
                       ('planet_exalted_in_occupied_depression_sign',planet_exalted_in_depression_sign_kendra)]:
  for connective,op in [('either',_or),('both',_and)]:
   candidates.append({'uchchanatha_reading':meaning,'connective_reading':connective,
     'qualifying_condition':_and(debilitated,op(depression_lord_kendra,value)),
     'scope':'VII.26 condition only; not complete cancellation assessment',
     'source_references':['phaladeepika-1937 PDF117 printed80 VII.26 and note',
                          'phaladeepika-kapoor PDF89 VII.26 commentary']})
 return {'candidates':candidates,'selected_profile':None,'total_strength':None,
   'personal_outcome':None,'global_precedence':None,
   'notice':'Kapoor explicitly reports either-versus-both and alternate Uchchanatha readings. This helper preserves the axes, not an assertion that every school uses all four combinations. A false VII.26 condition does not deny VII.27-30. A true flag does not undo all adverse factors or assert status, wealth or an event.'}
