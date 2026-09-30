"""Fail-closed evidence gate; no undocumented priority between incompatible rules."""


def reconcile_claims(claims):
    """Group outcome claims by topic and interval; abstain on contradiction/gaps.

    Caller-supplied records must have topic, interval, polarity, citation,
    strength_verified, timing_verified. No evidence is manufactured here.
    """
    by_key={}
    for claim in claims:
        key=(claim['topic'],claim['interval'])
        by_key.setdefault(key,[]).append(claim)
    results=[]
    for (topic,interval),items in by_key.items():
        missing=sorted({field for x in items for field in ('citation','strength_verified','timing_verified')
                        if not x.get(field)})
        polarities={x['polarity'] for x in items}
        results.append({'topic':topic,'interval':interval,'status':'abstain',
                        'conflict':len(polarities)>1,'missing_evidence':missing,
                        'source_count':len(items),
                        'notice':'No book-verified rule precedence or outcome calibration; no automatic personal conclusion.'})
    return results
