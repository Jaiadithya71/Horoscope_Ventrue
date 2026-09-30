"""Convention matrix, never a vote or selected personal forecast."""
import datetime as dt
from .solar_dates import dated_hierarchy
from .period_evidence import lunar_traversal_evidence

CALENDARS=('elapsed_utc_return_interpolation','sidereal_solar_angular_progress','fixed_365_25_day_software_comparison')
BALANCES=('equal_sector_longitude_fraction','normalized_actual_traversal_fraction','printed_XIX_3_fixed_60_divisor')


def compare_conventions(birth,instant):
    """Report valid and invalid choices equally; no overfull balance clipping."""
    if not isinstance(instant,dt.datetime) or instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError('Query instant must be timezone-aware')
    evidence=lunar_traversal_evidence(birth)
    rows=[]
    for calendar in CALENDARS:
        for balance in BALANCES:
            try:
                h=dated_hierarchy(birth,evidence['birth_moon_longitude'],instant,
                                  balance_method=balance,calendar_profile=calendar)
                rows.append({'calendar_profile':calendar,'balance_method':balance,
                             'status':'computed_convention_estimate',
                             'lord_path':[x['lord'] for x in h['hierarchy']],
                             'hierarchy':h['hierarchy'],'calendar_source':h['calendar_source'],
                             'calendar_convention':h['calendar_convention']})
            except ValueError as exc:
                rows.append({'calendar_profile':calendar,'balance_method':balance,
                             'status':'invalid_or_out_of_horizon','reason':str(exc),
                             'lord_path':None,'hierarchy':None})
    paths={tuple(r['lord_path']) for r in rows if r['lord_path'] is not None}
    return {'query_utc':instant.astimezone(dt.timezone.utc).isoformat(),
            'birth_balance_evidence':evidence,'comparison_rows':rows,
            'distinct_computed_lord_paths':[list(p) for p in sorted(paths)],
            'lord_path_agreement':len(paths)==1 if paths else None,
            'invalid_combinations':sum(r['status']!='computed_convention_estimate' for r in rows),
            'selected_profile':None,'status':'unresolved_source_convention',
            'notice':'Agreement is model/convention agreement only, not independently verified timing, majority voting, calendar selection, Balaji setting or personal outcome. Invalid overfull balances remain invalid; no clipping or silent fallback. Query must be after birth and within each profile horizon.'}


def main():
    import argparse,json
    from .natal import birth_utc
    p=argparse.ArgumentParser(description='Compare calendar and birth-balance conventions without choosing a winner')
    p.add_argument('--birth-date',required=True);p.add_argument('--birth-time',required=True)
    p.add_argument('--birth-tz',required=True);p.add_argument('--at',required=True)
    a=p.parse_args()
    try:result=compare_conventions(birth_utc(a.birth_date,a.birth_time,a.birth_tz),dt.datetime.fromisoformat(a.at))
    except ValueError as exc:p.error(str(exc))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
