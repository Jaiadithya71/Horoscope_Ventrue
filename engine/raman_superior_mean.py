"""Raw superior-planet mean tables, not a repaired historical ephemeris."""
from decimal import Decimal as D
from .raman_motion_source_audit import SOURCE_URL

MARS=[['.524','52.40','164.02','200.19'],['1.048','104.80','328.04','40.39'],['1.572','157.21','132.06','240.58'],['2.096','209.61','296.08','80.78'],['2.620','262.01','100.10','280.97'],['3.144','314.41','264.12','121.16'],['3.668','6.81','68.14','321.36'],['4.192','59.22','232.55','161.55'],['4.716','111.62','36.17','1.74']]
JUPITER=[['.08','.83','8.31','83.1','110.96'],['.17','1.66','16.62','166.19','221.96'],['.25','2.49','24.93','249.29','332.89'],['.33','3.32','33.24','332.39','83.85'],['.41','4.15','41.55','55.48','194.82'],['.50','4.99','42.86','138.58','305.78'],['.58','5.82','58.17','221.67','56.74'],['.66','6.65','66.58','304.77','167.71'],['.75','7.48','74.79','78.87','278.67']]
SATURN=[['.03','.33','3.34','33.44','334.39'],['.07','.67','6.69','66.88','308.79'],['.10','1.00','10.03','100.32','283.18'],['.13','1.34','13.38','133.76','257.57'],['.17','1.67','16.72','167.20','231.97'],['.20','2.01','20.06','200.64','206.36'],['.23','2.34','23.41','234.08','180.75'],['.27','2.68','26.75','267.51','152.14'],['.30','3.01','30.10','300.95','122.54']]


def raman_superior_mean(planet,elapsed_days,birth_year_offset,*,epoch_clock_profile):
    if planet not in ('Mars','Jupiter','Saturn'):raise ValueError('Superior planet required')
    if type(birth_year_offset) is not int:raise ValueError('Integer birth-year minus1900 required')
    if not isinstance(epoch_clock_profile,str) or not epoch_clock_profile.strip():raise ValueError('Named epoch-clock profile required')
    if isinstance(elapsed_days,bool):raise ValueError('Finite elapsed days required')
    days=D(str(elapsed_days))
    if not days.is_finite() or abs(days)>=100000:raise ValueError('Finite absolute interval below100000 required')
    table={'Mars':MARS,'Jupiter':JUPITER,'Saturn':SATURN}[planet]
    n=int(abs(days));fraction=abs(days)-n;pieces=[]
    for i,place in enumerate((1,10,100,1000,10000)):
        digit=n//place%10
        if not digit:continue
        index={1:0,10:0,100:1,1000:2,10000:3}[place] if planet=='Mars' else i
        entry=table[digit-1][index];value=D(entry)*(10 if planet=='Mars' and place==10 else 1)
        pieces.append({'place':place,'digit':digit,'printed_entry':entry,'motion_degrees':str(value)})
    fractional=fraction*D(table[0][0]);motion=sum((D(r['motion_degrees']) for r in pieces),D(0))+fractional
    if days<0:motion=-motion
    t=D(birth_year_offset);constant={'Mars':D('270.22'),'Jupiter':D('220.04'),'Saturn':D('236.74')}[planet]
    correction={'Mars':D(0),'Jupiter':-(D('3.33')+D('.0067')*t),'Saturn':D(5)+D('.001')*t}[planet]
    total=constant+motion+correction
    return {'planet':planet,'supplied_elapsed_days':str(days),'supplied_birth_year_offset':birth_year_offset,
        'epoch_clock_profile':epoch_clock_profile,'printed_pieces':pieces,'fractional_motion_degrees':str(fractional),
        'epoch_constant':str(constant),'correction_degrees':str(correction),'sum_before_normalization':str(total),
        'raw_mean_degrees':str((total%360+360)%360),'selected_unwrapped_mean':None,
        'historical_ephemeris_verified':False,
        'source':{'url':SOURCE_URL,'pdf_pages':[78,79,118,119,120,121],'printed_pages':[73,74,113,114,115,116],'verified_against_page_image':True},
        'notice':'Raw independent digit columns and exact printed coefficient arithmetic, not worked-output fitting. Fraction uses rounded one-day entry without reconstructing hidden precision. Jupiter600-day42.86 stays raw despite worked49.86; worked2-day1.66 disagrees with table. Saturn epoch visually236.74, not OCR236.14. No inferred revolution branch or complete strength.'}


def raman_superior_example_audit():
    rows=[]
    for planet,printed in [('Mars','162.020'),('Jupiter','240.48'),('Saturn','35.65')]:
        x=raman_superior_mean(planet,'4602.5',12,epoch_clock_profile='Printed1912 supplied interval')
        rows.append({'lookup':x,'printed_worked_mean':printed,'exact_raw_lookup_matches':D(x['raw_mean_degrees'])==D(printed)})
    return {'rows':rows,'jupiter_600_day_raw':'42.86','jupiter_600_day_worked':'49.86',
        'jupiter_2_day_raw':'.17','jupiter_2_day_worked':'1.66',
        'jupiter_4000_day_raw':'332.39','jupiter_4000_day_worked':'332.29',
        'notice':'Matches certify only a particular raw arithmetic route. Differences include printed errors and rounding; no repair or preferred ephemeris asserted.'}
