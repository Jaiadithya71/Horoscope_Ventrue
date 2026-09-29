"""Compare atomic Balaji transcript claims with generated rule findings.

This is transcript agreement, NOT outcome accuracy. Unsupported claims count as gaps.
"""
import argparse
import json
from pathlib import Path
from .forecast import forecast

DATA = Path(__file__).resolve().parents[1]/'benchmarks'/'balaji_2026_claims.json'


def score(claims):
    rows=[]
    for c in claims:
        generated=forecast(c['date'],c['moon_sign'])
        if c['kind']=='chart_position':
            p=generated['placements'][c['planet']]
            matched=p['house_from_moon']==c['asserted_house_from_moon']
            rows.append({**c,'status':'chart_match' if matched else 'chart_mismatch',
                         'actual_house':p['house_from_moon'],'actual_sign':p['sign'],
                         'computation':generated['model']})
        elif c['kind']=='outcome':
            exact=[f for f in generated['findings'] if f['topic']==c['topic']]
            rows.append({**c,'status':'supported_topic_only' if exact else 'unsupported',
                         'rule_ids':[f['id'] for f in exact],
                         'caution':'Topic-only matching is not an exact prediction match.'})
        else:raise ValueError('Unknown claim kind')
    counts={s:sum(r['status']==s for r in rows) for s in sorted(set(r['status'] for r in rows))}
    return {'metric':'Agreement with transcripted mechanics, not empirical predictive accuracy',
            'n':len(rows),'counts':counts,'claims':rows}


def main():
    a=argparse.ArgumentParser();a.add_argument('--data',default=str(DATA));opt=a.parse_args()
    print(json.dumps(score(json.loads(Path(opt.data).read_text())),indent=2))

if __name__=='__main__':main()
