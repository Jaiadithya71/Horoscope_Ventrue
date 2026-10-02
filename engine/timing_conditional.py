"""Dated Vimshottari timelines under every source-stated convention, never a selected one.

Sources (scan-checked, timing research file): Brihat Jataka translator's notes
(printed pp. 95-97, 61): birth balance from the time the Moon takes to cross its
nakshatra, dasa years as 360-day Savana years or 365.242264-day Soura years,
antardasa = main years x sub years / 120. Planet years and nakshatra groups agree
with Jatakachundrika, the Astrological Self-Instructor and Phaladeepika XXI.2.
Four timelines are produced (two balance readings x two year lengths) and a
marriage-period overlay is reported per timeline plus the dates all four share.
No timeline is chosen. The Brihat Jataka printed Soura conversions are not
reproduced by its own constant, so only the constant is used, not the printed figures.
"""
import datetime as dt
from .forecast import swe, julian_day, FLAGS
from .natal import PERIODS, STAR_ARC

YEAR_LENGTHS={'savana_360':360.0,'soura_365_242264':365.242264}
BRIHAT_JATAKA_URL='https://archive.org/details/brihatjataka00varaiala'
SOURCE={'book':'brihat-jataka-1905','pdf_pages':[105,139,140,141],'printed_pages':[61,95,96,97],
        'verified_against_page_image':True,'url':BRIHAT_JATAKA_URL,
        'also':['phaladeepika-1937 XXI.2 PDF 258 (antardasa x/120)']}
HORIZON_YEARS=120


def _moon_lon(jd):
    return swe.calc_ut(jd,swe.MOON,FLAGS)[0][0]%360


def moon_crossing_fraction(birth_jd):
    """Fraction of the Moon's nakshatra crossing elapsed at birth, by actual elapsed time (BJ method)."""
    lon=_moon_lon(birth_jd);star=int(lon/STAR_ARC)
    start=star*STAR_ARC;end=(star+1)*STAR_ARC
    def root(target,lo,hi):
        # bisection on signed angular offset (monotone over a few days)
        f=lambda jd:((_moon_lon(jd)-target+180)%360)-180
        for _ in range(60):
            mid=(lo+hi)/2
            if f(mid)>=0:hi=mid
            else:lo=mid
        return (lo+hi)/2
    entry=root(start%360,birth_jd-2,birth_jd+.0001)
    exit_=root(end%360,birth_jd-.0001,birth_jd+2)
    return {'fraction_elapsed':(birth_jd-entry)/(exit_-entry),'crossing_days':exit_-entry,
            'entry_jd':entry,'exit_jd':exit_}


def _lord_index(star):return (star+7)%9


def _timeline(birth,fraction_elapsed,star,year_days):
    idx=_lord_index(star)
    lord,years=PERIODS[idx]
    remaining=years*(1-fraction_elapsed)
    maha=[];cursor=birth;cur_year_offset=0.0
    for i in range(12):
        name,y=PERIODS[(idx+i)%9]
        length=remaining if i==0 else float(y)
        start_off=cur_year_offset;end_off=cur_year_offset+length
        if start_off>=HORIZON_YEARS:break
        # antardasa inside this mahadasa; first one starts mid-way if birth falls inside it
        anta=[];full_start=start_off if i else start_off-(y-remaining) if False else None
        total=float(y)
        offset_in=0.0 if i else (years-remaining)  # years of the first maha already elapsed at birth
        a_cursor=0.0
        for k in range(9):
            an,ay=PERIODS[(((idx+i)%9)+k)%9]
            alen=total*ay/120
            a_start=a_cursor;a_end=a_cursor+alen;a_cursor=a_end
            if a_end<=offset_in:continue
            s=max(a_start,offset_in)-offset_in+start_off;e=a_end-offset_in+start_off
            if s>=HORIZON_YEARS:break
            anta.append({'lord':an,'start':(birth+dt.timedelta(days=s*year_days)).isoformat(),
                         'end':(birth+dt.timedelta(days=e*year_days)).isoformat(),'_s':s,'_e':e})
        maha.append({'lord':name,'start':(birth+dt.timedelta(days=start_off*year_days)).isoformat(),
                     'end':(birth+dt.timedelta(days=end_off*year_days)).isoformat(),'antardasas':anta,'_s':start_off,'_e':end_off})
        cur_year_offset=end_off
    return maha


def _windows(timeline,lords):
    out=[]
    for m in timeline:
        if m['lord'] not in lords:continue
        for a in m['antardasas']:
            if a['lord'] in lords:out.append((a['_s'],a['_e'],m['lord'],a['lord']))
    return out


def timing_conditional(chart,*,marriage_rows=None):
    utc=dt.datetime.fromisoformat(chart['birth_utc']);jd=julian_day(utc)
    moon=chart['placements']['Moon']['longitude'];star=int(moon/STAR_ARC)
    cross=moon_crossing_fraction(jd)
    uniform=(moon/STAR_ARC)-star
    candidate_lords=[]
    if marriage_rows:
        row=next((r for r in marriage_rows if r['rule_id']=='phaladeepika-x-13-period-candidate-lords'),None)
        if row:
            txt=row['detail'].split('[')[-1].rstrip(']')
            candidate_lords=[x.strip(" '") for x in txt.split(',') if x.strip(" '")]
    timelines={};
    for bname,frac in (('moon_time_in_nakshatra_bj',cross['fraction_elapsed']),('moon_longitude_uniform',uniform)):
        for yname,yd in YEAR_LENGTHS.items():
            tl=_timeline(utc,frac,star,yd)
            key=f'{bname}|{yname}'
            marriage=[{'maha_lord':a,'antar_lord':b,
                       'start':(utc+dt.timedelta(days=s*yd)).isoformat(),'end':(utc+dt.timedelta(days=e*yd)).isoformat()}
                      for s,e,a,b in _windows(tl,candidate_lords)] if candidate_lords else []
            clean=[{k:v for k,v in m.items() if k not in('_s','_e')}|{'antardasas':[{k:v for k,v in a.items() if not k.startswith('_')} for a in m['antardasas']]} for m in tl]
            timelines[key]={'balance_reading':bname,'year_length_profile':yname,'year_length_days':yd,
                            'first_period_balance_years':PERIODS[_lord_index(star)][1]*(1-frac),
                            'mahadasas':clean,'marriage_candidate_antardasa_windows':marriage}
    return {'status':'four_conditional_timelines_none_selected','birth_utc':chart['birth_utc'],
        'moon_nakshatra_index_1_based':star+1,'birth_balance_alternatives':{
            'moon_time_in_nakshatra_bj':cross['fraction_elapsed'],'moon_longitude_uniform':uniform,
            'difference_fraction':abs(cross['fraction_elapsed']-uniform)},
        'timelines':timelines,'selected_timeline':None,'marriage_candidate_lords':candidate_lords,
        'source':SOURCE,
        'unresolved':['which birth-balance reading','which year length (Savana 360 vs Soura 365.242264); the book prints both','whether Phaladeepika X.13 means Mahadasa, Antardasa or either: windows shown need both levels, mahadasa-only reading is the mahadasa list',
                      'Brihat Jataka printed Soura conversions do not recompute from its constant','Ashtottari and Kalachakra are other systems the sources name'],
        'notice':'Dated windows are source arithmetic under named conventions, not predictions. Marriage windows apply only if the marriage period-candidate rule is accepted; no event is claimed.'}
