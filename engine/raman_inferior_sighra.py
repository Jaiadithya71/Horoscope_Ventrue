"""Raw RamanVIII/IX lookup candidates with unresolved printed cells preserved."""
from decimal import Decimal as D
from .raman_motion_source_audit import SOURCE_URL

MERCURY=[['4.09','40.92','49.23','133.32',None],['8.18','81.84','98.46','264.64','126.36'],['12.28','122.77','147.69','36.95','9.54'],['16.37','163.69','196.93','169.27','252.72'],['20.46','204.62','246.16','301.59','135.90'],['24.55','245.54','295.39','73.91','19.08'],['28.65','266.46','344.62','206.34','262.26'],['32.74','327.38','33.85','338.50','145.44'],['36.83','8.31','83.09','110.86','28.63']]
VENUS=[['1.60','16.02','160.21','162.15','181.46'],['3.20','32.04','320.43','324.29','2.93'],['4.81','48.06','120.64','246.44','184.39'],['6.41','64.09','280.86','288.52','5.86'],['8.01','80.11','81.07','90.73','187.32'],['9.61','96.13','241.29','252.88','8.87'],['11.21','116.15','41.50','55.02','190.25'],['12.82','128.17','201.72','217.17','11.71'],['14.42','144.19','1.93','19.32','193.18']]


def raman_inferior_sighra(planet,elapsed_days,birth_year_offset,*,epoch_clock_profile):
    if planet not in ('Mercury','Venus'):raise ValueError('Inferior planet required')
    if type(birth_year_offset) is not int:raise ValueError('Explicit integer birth-year minus1900 required')
    if not isinstance(epoch_clock_profile,str) or not epoch_clock_profile.strip():raise ValueError('Named epoch/clock profile required')
    if isinstance(elapsed_days,bool):raise ValueError('Finite elapsed days required')
    days=D(str(elapsed_days))
    if not days.is_finite() or abs(days)>=100000:raise ValueError('Finite absolute interval below100000 required')
    table=MERCURY if planet=='Mercury' else VENUS;n=int(abs(days));fraction=abs(days)-n;pieces=[]
    for i,place in enumerate((1,10,100,1000,10000)):
        digit=n//place%10
        if digit:pieces.append({'place':place,'digit':digit,'printed_entry':table[digit-1][i]})
    missing=[r for r in pieces if r['printed_entry'] is None]
    motion=None if missing else sum((D(r['printed_entry']) for r in pieces),D(0))+fraction*D(table[0][0])
    if motion is not None and days<0:motion=-motion
    t=D(birth_year_offset);rows=[]
    variants=[('table_and_worked_coefficient',D('6.67')-D('.00133')*t),('main_prose_coefficient',D('6.67')-D('.0133')*t)] if planet=='Mercury' else [('tableIX_coefficient',-(D(5)+D('.0001')*t)),('main_prose_and_worked_coefficient',-(D(5)+D('.001')*t))]
    epoch=D(164) if planet=='Mercury' else D('328.51')
    for name,c in variants:
        total=None if motion is None else epoch+motion+c
        rows.append({'correction_profile':name,'correction_degrees':str(c),'sighrochcha_degrees':None if total is None else str((total%360+360)%360)})
    return {'planet':planet,'supplied_elapsed_days':str(days),'supplied_birth_year_offset':birth_year_offset,'epoch_clock_profile':epoch_clock_profile,
        'printed_pieces':pieces,'unreadable_cells':missing,'fractional_motion_degrees':str(fraction*D(table[0][0])),
        'candidates':rows,'selected_sighrochcha':None,
        'source':{'url':SOURCE_URL,'pdf_pages':[81,82,121,122],'printed_pages':[76,77,116,117],'verified_against_page_image':True},
        'historical_ephemeris_verified':False,
        'notice':'Raw independent digit columns, no uniform-rate repair or worked-result fitting. Mercury ten-thousands row1 malformed243.AS stays unknown; row7 tens visually266.46, not OCR206.46. Coefficient discrepancies stay separate. Birth-year offset and elapsed clock are external, not inferred fractional years. Fraction uses printed one-day rate as a named candidate, not proven precision policy. Venus table civil-time wording and general76E epoch mapping are not independently arbitrated. No selected motion input or complete strength.'}
