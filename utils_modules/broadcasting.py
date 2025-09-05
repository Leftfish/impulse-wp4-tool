"""
Broadcasting organisation rights module.

This module contains logic for calculating broadcasting organisation rights status and related intermediate values.
"""

from defaults import ResultsDict
from utils_modules.text_constants import (
    BroadcastingCondition,
    get_explanation,
    BROADCAST_RIGHTS_TERM,
)

from datetime import datetime
from data.country_codes import is_eea_country


def calculate_intermediate_values_broadcast(data):
    """Calculate intermediate boolean values used in broadcasting organisation rights calculations."""
    current_year = datetime.now().year
    
    # Broadcasting organisation country calculations - accept both field names
    broadcast_orgs = data.get('broadcasters', [])
    broadcast_country_codes = [org.get('country_of_origin') for org in broadcast_orgs]
    country_of_origin_eea_broadcast = any(is_eea_country(code) for code in broadcast_country_codes if code)
    country_of_origin_unknown_broadcast = all(code == 'XX' for code in broadcast_country_codes)
    
    return {
        'CountryOfOriginEEABroadcast': country_of_origin_eea_broadcast,
        'CountryOfOriginUnknownBroadcast': country_of_origin_unknown_broadcast,
        'CURRENT_YEAR': current_year,
    }


def calculate_broadcast_rights_status(data, intermediate):
    """Calculate broadcasting organisation rights status for the original object only."""
    results = ResultsDict()
    
    used_vars = set()

    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Add compound broadcast info message if needed
    if data.get('is_compound_broadcast') in ['compound', 'uncertain']:
        mark_used('is_compound_broadcast')
        _cond = BroadcastingCondition.CompoundBroadcast.value
        results['info'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'info', 'broadcast'),
        })
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_broadcast') == 'not_broadcast':
        mark_used('is_broadcast')
        _cond = BroadcastingCondition.PublicDomainNotABroadcast.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'broadcast'),
        })
        return results, used_vars
    
    if data.get('broadcast_before_1970') == 'broadcast_made_before_1970':
        mark_used('broadcast_before_1970')
        _cond = BroadcastingCondition.PublicDomainRuleOfThumbBroadcasts.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'broadcast'),
        })        
        return results, used_vars

    # Year-based logic when not before 1970
    broadcast_year = data.get('broadcast_year')
    before_1970 = data.get('broadcast_before_1970') == 'broadcast_made_before_1970'
    country_eea_broadcast = intermediate.get('CountryOfOriginEEABroadcast', False)
    used_vars.update(['broadcasters'])
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # 4) Unknown broadcast year (but not before 1970)
    if not before_1970 and not broadcast_year:
        mark_used('broadcast_year')
        _cond = BroadcastingCondition.BroadcastYearUnknown.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'broadcast'),
        })

    # 5) Known broadcast year logic (EEA focus)
    if not before_1970 and broadcast_year and country_eea_broadcast:
        broadcast_protection_lapse = broadcast_year + BROADCAST_RIGHTS_TERM
        mark_used('broadcast_year')
        if current_year_val > broadcast_protection_lapse:
            _cond = BroadcastingCondition.BroadcastProtectionLapsedArticle3.value
            results['green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'green', 'broadcast'),
            })
        else:
            _cond = BroadcastingCondition.BroadcastStillProtectedArticle3.value
            results['red'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'red', 'broadcast'),
            })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1970 and broadcast_year and not country_eea_broadcast:
        broadcast_protection_lapse = broadcast_year + BROADCAST_RIGHTS_TERM
        mark_used('broadcast_year')
        if current_year_val > broadcast_protection_lapse:
            _cond = BroadcastingCondition.BroadcastLapsedEvenIfEEA.value
            results['green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'green', 'broadcast'),
            })
        else:
            _cond = BroadcastingCondition.BroadcastNonEEAUncertain.value
            results['yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'yellow', 'broadcast'),
            })

    # Broadcasting organisation-specific rights overrides (mirror performance logic)
    # 1) Current rightholder override (green if ours and no prior green) - HIGHEST PRIORITY
    mark_used('broadcast_current_rightholder')
    if data.get('broadcast_current_rightholder') == 'rightholder_us':
        _cond = BroadcastingCondition.BroadcastCurrentRightHolderKnown.value
        results['rights_green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'rights_green', 'broadcast'),
        })
        return results, used_vars  # Exit early, no other overrides apply

    # 2) CC license override for broadcast - MEDIUM PRIORITY
    mark_used('broadcast_cc_license')
    cc_choice = data.get('broadcast_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        broadcast_cc_green = ['cc0', 'cc_by']
        broadcast_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in broadcast_cc_green and (results['red'] or results['yellow']):
            _cond = BroadcastingCondition.BroadcastAvailableCCLicense.value
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'broadcast'),
            })
        elif cc_choice in broadcast_cc_yellow and (results['red'] or results['yellow']):
            _cond = BroadcastingCondition.BroadcastAvailableCCLicense.value
            results['rights_yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_yellow', 'broadcast'),
            })

    # 3) Rights acquisition override for broadcast - LOWEST PRIORITY (only if no CC license)
    mark_used('broadcast_rights_acquired_to_make_available')
    ra_choice = data.get('broadcast_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        broadcast_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        broadcast_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in broadcast_ra_green and (results['red'] or results['yellow']):
            _cond = BroadcastingCondition.BroadcastOnlineAvailable.value
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'broadcast'),
            })
        elif ra_choice in broadcast_ra_yellow and (results['red'] or results['yellow']):
            _cond = BroadcastingCondition.BroadcastOnlineAvailable.value
            results['rights_yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_yellow', 'broadcast'),
            })

    return results, used_vars
