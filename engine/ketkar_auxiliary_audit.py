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


def attraction_component_audit():
 from decimal import Decimal
 vectors={'jupiter_start':['.34','.08','.36','.30','6.63'],
  'jupiter_end':['.42','.24','.43','.26','6.60'],
  'saturn_start':['.95','5.96','11.35','4.56'],
  'saturn_end':['.85','6.23','11.47','5.67']}
 printed={'jupiter_start':'7.71','jupiter_end':'7.95','saturn_start':'22.82','saturn_end':'24.20'}
 rows={}
 for name,values in vectors.items():
  computed=sum(map(Decimal,values),Decimal(0))
  rows[name]={'supplied_printed_components':values,'computed_sum_days':str(computed),
   'printed_sum_days':printed[name],'matches':computed==Decimal(printed[name]),
   'computed_minus_printed_days':str(computed-Decimal(printed[name]))}
 return {'source':{'url':auxiliary_audit()['source']['url'],'pdf_pages':[171],
  'printed_pages':[104],'example':'Nyasa2 lower half rows6-14','verified_against_page_image':True},
  'rows':rows,'printed_annual_difference_days':{'jupiter':'.24','saturn':'1.38'},
  'computed_component_annual_difference_days':{'jupiter':'0.24','saturn':'1.40'},
  'table9_lookup_reconstructed':False,'selected_attraction_days':None,
  'notice':'Saturn end printed component sum24.22 differs from printed24.20 by.02 days; printed annual1.38 follows printed totals, not component sums. No correction selected. Rounding, transcription or lookup discrepancy unresolved; supplied printed components do not certify table9 interpolation.'}
