"""Source-specific nirayana-to-sayana offset, not a modern sidereal default."""
from decimal import Decimal
from .ketkar_solar_example_reconstruction import reconstruct_solar_example


def longitude_frame_audit():
 base=Decimal('22.143');increment=Decimal('.697');offset=base+increment
 solar=reconstruct_solar_example();sun=Decimal(solar['candidate_solar_longitude_degrees'])
 mars=Decimal('305.207')
 return {'source':{'url':solar['source']['url'],'pdf_pages':[177,179,194],
  'printed_pages':[110,112,127],'verified_against_page_image':True,
  'rule':'III24-25 commentary uses sayana longitude for equatorial conversion'},
  'base_ayanamsa_saka1800_degrees':str(base),'supplied50year_increment_degrees':str(increment),
  'computed_ayanamsa_degrees':str(offset),'printed_ayanamsa_degrees':'22.840',
  'source_nirayana_solar_candidate_degrees':str(sun),
  'source_sayana_solar_candidate_degrees':str((sun+offset)%Decimal(360)),
  'printed_nirayana_mars_degrees':str(mars),
  'computed_sayana_mars_degrees':str((mars+offset)%Decimal(360)),
  'printed_sayana_mars_degrees':'328.047',
  'mars_frame_bridge_matches':(mars+offset)==Decimal('328.047'),
  'modern_sidereal_profile_selected':None,'utc_dawn_timestamp':None,
  'independent_ephemeris_agreement':None,
  'notice':'Book-specific supplied year-motion chain and explicit frame bridge. Do not compare352.167nirayana directly with modern tropical longitude or substitute Lahiri. Sayana Sun15.007 is a composed candidate, not a separately printed or independently timed ephemeris result. Historical dawn/UTC reference still unresolved.'}
