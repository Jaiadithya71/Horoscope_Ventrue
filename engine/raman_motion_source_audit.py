"""Printed Raman motion-chain consistency, not corrected ephemeris tables."""
from decimal import Decimal as D

SOURCE_URL='https://dn790000.ca.archive.org/0/items/1050-jyotish-books-with-siderial-zodiac/Bhava%20and%20Graha%20Balas_B.V.Raman%201996.pdf'


def raman_motion_source_audit():
    terms=['252.88','201.72','96.13','.92','328.51','-5.01']
    total=sum(map(D,terms))
    triples={'Mars':('181.23','266.34','229.50','293.31'),
        'Mercury':('174.49','181.23','181.52','353.11'),
        'Jupiter':('181.23','66.91','84.01','105.77'),
        'Venus':('158.35','181.23','171.16','342.15'),
        'Saturn':('181.23','111.23','124.39','63.42')}
    rows=[]
    for p,(s,m,t,printed) in triples.items():
        raw=D(s)-(D(m)+D(t))/2;k=(raw%360+360)%360
        rows.append({'planet':p,'printed_worked_inputs':{'sighrochcha':s,'mean':m,'true':t},
            'exact_kendra_from_printed_inputs':str(k),'printed_kendra':printed,
            'exact_difference_from_printed_kendra':str(k-D(printed)),
            'selected_input_correction':None})
    return {'source':{'url':SOURCE_URL,'pdf_pages':[80,81,82,83,84,121,122],
        'printed_pages':[75,76,77,78,79,116,117],'verified_against_page_image':True},
        'named_raman_assignments':{'superior_sighrochcha':'mean Sun for Mars/Jupiter/Saturn',
            'inferior_mean':'mean Sun for Mercury/Venus','ketkar_equivalence_verified':False},
        'saturn':{'rule_and_example_sighrochcha':'181.2275','summary_sighrochcha':'151.23',
            'later_worked_sighrochcha':'181.23','summary_matches_rule_at_two_places':False},
        'venus_example48':{'printed_terms':terms,'exact_sum_printed_terms':str(total),
            'printed_total':'878.35','sum_matches_printed_total':total==D('878.35'),
            'printed_total_mod360':str(D('878.35')%360),'printed_final':'158.35',
            'sum_mod360':str(total%360),'two_day_term_in_example':'.92','two_day_tableIX_value':'3.20',
            'fractional_interval_days':'.578','fractional_day_term_shown':False},
        'mercury':{'correction_coefficient_prose':'.0133','coefficient_worked_and_table':'.00133',
            'printed_total_interval':'6862.578','printed_fractional_row':'.581','fractional_row_matches':False},
        'worked_kendra_rows':rows,'selected_motion_profile':None,'arbitrary_date_ephemeris_complete':False,
        'notice':'Exact arithmetic on printed operands, not a corrected edition. Named Raman assignments provide a separately sourced mean/Sighra interpretation, not a Ketkar/Sripati mapping. Summary Saturn differs from rule and later worked value; Venus displayed terms do not sum to its total and differ from tableIX. Mercury coefficients/fractional rows disagree. Later kendra arithmetic and two-place statement do not certify a global precision policy. No fitted epoch, silent typo repair, reconstructed historical triple or selected strength total.'}
