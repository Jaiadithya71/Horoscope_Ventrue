"""Page-verified Ketkar attraction auxiliaries, not planetary longitude."""


def combine_auxiliaries(base, increment):
 if not isinstance(base,(list,tuple)) or not isinstance(increment,(list,tuple)):
  raise ValueError('six integer auxiliaries required')
 if len(base)!=6 or len(increment)!=6 or any(type(x) is not int for x in (*base,*increment)):
  raise ValueError('six integer auxiliaries required')
 if any(x<0 or x>=1000 for x in base) or any(x<0 for x in increment):
  raise ValueError('base must be in 0..999 and increments nonnegative')
 return [(b+i)%1000 for b,i in zip(base,increment)]


def auxiliary_audit():
 base=[661,491,830,830,347,660]
 fifty_year_increment=[338,160,518,821,54,642]
 annual_increment=[60,83,50,16,1,33]
 start=combine_auxiliaries(base,fifty_year_increment)
 end=combine_auxiliaries(start,annual_increment)
 return {'source':{'url':'https://archive.org/details/jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha',
  'pdf_pages':[170,171,191],'printed_pages':[103,104,124],
  'example':'Nyasa2 upper half rows1-5; table5','verified_against_page_image':True},
  'cycle':1000,'saka_base_year':1800,'saka_example_year':1850,
  'base_auxiliaries':base,'supplied_50_year_increment':fifty_year_increment,
  'computed_1850_auxiliaries':start,'printed_1850_auxiliaries':[999,651,348,651,401,302],
  'start_matches':start==[999,651,348,651,401,302],
  'supplied_one_year_increment':annual_increment,'computed_1851_auxiliaries':end,
  'printed_1851_auxiliaries':[59,734,398,667,402,335],
  'end_matches':end==[59,734,398,667,402,335],
  'attraction_days':None,'mean_planet_longitudes':None,'total_strength':None,
  'notice':'Checks printed addition with independent modulo1000 columns only. Increments are supplied printed table values, not a reconstructed motion formula. Source treats nearby Chaitra bright15 and Aries ingress auxiliaries as approximate; not exact ingress timing. Attraction days need table9 lookup/interpolation and its rounding; unresolved, not inferred from auxiliaries.'}
