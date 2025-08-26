"""
Broadcasting organisation rights module.

This module contains logic for calculating broadcasting organisation rights status and related intermediate values.
"""

from datetime import datetime
from data.country_codes import is_eea_country


def calculate_intermediate_values_broadcast(data):
    """Calculate intermediate boolean values used in broadcasting organisation rights calculations."""
    current_year = datetime.now().year
    
    # Broadcasting organisation country calculations - accept both field names
    broadcast_orgs = data.get('broadcasters', data.get('broadcasting_organisations', []))
    broadcast_country_codes = [org.get('country_of_origin') for org in broadcast_orgs]
    country_of_origin_eea_broadcast = any(is_eea_country(code) for code in broadcast_country_codes if code)
    country_of_origin_unknown_broadcast = all(code == 'XX' for code in broadcast_country_codes)
    
    return {
        'CountryOfOriginEEABroadcast': country_of_origin_eea_broadcast,
        'CountryOfOriginUnknownBroadcast': country_of_origin_unknown_broadcast,
        'CURRENT_YEAR': current_year
    }


def calculate_broadcast_rights_status(data, intermediate):
    """Calculate broadcasting organisation rights status for the original object only."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_broadcast') == 'not_broadcast':
        mark_used('is_broadcast')
        results['green'].append({
            'condition': 'PublicDomainNotABroadcast',
            'explanation': 'It is not protected as a broadcast.'
        })
        return results, used_vars
    
    if data.get('broadcast_before_1970') == 'broadcast_made_before_1970':
        mark_used('broadcast_before_1970')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumbBroadcasts',
            'explanation': 'Given the time the broadcast was made, it has passed to the public domain.'
        })
        return results, used_vars
    
    # Add compound broadcast info message if needed
    if data.get('is_compound_broadcast') in ['compound', 'uncertain']:
        mark_used('is_compound_broadcast')
        results['info'].append({
            'condition': 'CompoundBroadcast',
            'explanation': 'This broadcast is, in fact, a collection of multiple broadcasts or it is made from various broadcasts. The analysis must be performed for each separately.'
        })
    
    # Year-based logic when not before 1970
    broadcast_year = data.get('broadcast_year')
    before_1970 = data.get('broadcast_before_1970') == 'broadcast_made_before_1970'
    country_eea_broadcast = intermediate.get('CountryOfOriginEEABroadcast', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # 4) Unknown broadcast year (but not before 1970)
    if not before_1970 and not broadcast_year:
        results['yellow'].append({
            'condition': 'BroadcastYearUnknown',
            'explanation': 'It is impossible to determine if a broadcast is still protected.'
        })
        return results, used_vars

    # 5) Known broadcast year logic (EEA focus)
    if not before_1970 and broadcast_year and country_eea_broadcast:
        broadcast_protection_lapse = broadcast_year + 50

        if current_year_val > broadcast_protection_lapse:
            results['green'].append({
                'condition': 'BroadcastProtectionLapsedArticle3',
                'explanation': 'The broadcast was protected but the protection has lapsed.'
            })
        else:
            results['red'].append({
                'condition': 'BroadcastStillProtectedArticle3',
                'explanation': 'The broadcast is still under protection.'
            })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1970 and broadcast_year and not country_eea_broadcast:
        broadcast_protection_lapse = broadcast_year + 50

        if current_year_val > broadcast_protection_lapse:
            results['green'].append({
                'condition': 'BroadcastLapsedEvenIfEEA',
                'explanation': 'Country of origin appears to be outside the EEA, but the broadcast would have lost protection even if the country of origin were in the EEA.'
            })
        else:
            results['yellow'].append({
                'condition': 'BroadcastNonEEAUncertain',
                'explanation': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the broadcast would not have lapsed even under EEA rules, the status is uncertain.'
            })

    # Broadcasting organisation-specific rights overrides (mirror performance logic)
    # 1) Current rightholder override (green if ours and no prior green) - HIGHEST PRIORITY
    mark_used('broadcast_current_rightholder')
    if data.get('broadcast_current_rightholder') == 'rightholder_us':
        results['red'] = []
        results['yellow'] = []
        results['green'].append({
            'condition': 'BroadcastCurrentRightHolderKnown',
            'explanation': 'The broadcast is protected by broadcasting organisation rights, but you are the rightholder.'
        })
        return results, used_vars  # Exit early, no other overrides apply

    # 2) CC license override for broadcast - MEDIUM PRIORITY
    mark_used('broadcast_cc_license')
    cc_choice = data.get('broadcast_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        broadcast_cc_green = ['cc0', 'cc_by']
        broadcast_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in broadcast_cc_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'BroadcastAvailableCCLicense',
                'explanation': 'While the broadcast is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in broadcast_cc_yellow and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['yellow'].append({
                'condition': 'BroadcastAvailableCCLicense',
                'explanation': 'While the broadcast is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
            })

    # 3) Rights acquisition override for broadcast - LOWEST PRIORITY (only if no CC license)
    mark_used('broadcast_rights_acquired_to_make_available')
    ra_choice = data.get('broadcast_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        broadcast_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        broadcast_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in broadcast_ra_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'BroadcastOnlineAvailable',
                'explanation': 'While the broadcast is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in broadcast_ra_yellow and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['yellow'].append({
                'condition': 'BroadcastOnlineAvailable',
                'explanation': 'While the broadcast is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
            })
    
    return results, used_vars
